import queue
import sys
import time
from pathlib import Path
from openai_utils import translate_to_language, generate_response, translate_response_to_language, create_text_to_speech, get_language
from pitch import increase_pitch
from google.cloud import speech
import pyaudio

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
        """The audio -- and generator -- is guaranteed to be on the main thread."""
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self: object) -> object:
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(
            self: object,
            type: object,
            value: object,
            traceback: object,
    ) -> None:
        """Closes the stream, regardless of whether the connection was lost or not."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
            self: object,
            in_data: object,
            frame_count: int,
            time_info: object,
            status_flags: object,
    ) -> object:
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Generates audio chunks from the stream of audio data in chunks."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses):
    num_chars_printed = 0
    start_time = time.time()
    end_time = start_time + 3  # Set the duration to 3 seconds
    transcript = ""
    interim_buffer = ""  # Buffer for interim results

    while time.time() < end_time:
        try:
            response = next(responses)

            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            current_transcript = result.alternatives[0].transcript

            if result.is_final:
                # Add final result to transcript and clear interim buffer
                transcript += f"{current_transcript} "
                interim_buffer = ""
                print(current_transcript)  # Show the final result
                num_chars_printed = 0
            else:
                # Buffer interim results for smoother display
                interim_buffer = current_transcript
                overwrite_chars = " " * (num_chars_printed - len(interim_buffer))
                sys.stdout.write(interim_buffer + overwrite_chars + "\r")
                sys.stdout.flush()
                num_chars_printed = len(interim_buffer)
        except StopIteration:
            break

    return transcript.strip()


def transcribe_speech() -> str:
    """Transcribes speech using Google Speech-to-Text."""
    language_code = "en-US"
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        transcript = listen_print_loop(responses)

    return transcript