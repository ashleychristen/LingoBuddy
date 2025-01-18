import logging
import queue
import re
import sys
import time
from assemblyai import transcribe_audio
from openai_utils import translate_to_language, generate_response, translate_response_to_language
from speechgen import speak_language_translation, speak_language_response, speak_english_response
from config import get_api_key, get_email
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
    start_time = time.time()  # Record the start time

    for response in responses:
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        if elapsed_time >= 3:
            print("Exiting after 3 seconds.")
            break

        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()
            num_chars_printed = len(transcript)
        else:
            print(transcript + overwrite_chars)
            num_chars_printed = 0

    print(time.time())
    return transcript


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

        
    transcribed_text = transcript
    return transcript

def main():
    # Load Speeghgen API information
    # speechgen_key = get_api_key('SPEECHGEN_API_KEY')
    #speechgen_email = get_email('SPEECHGEN_EMAIL')
    
    language = 'French'  # Change as needed
    
    while True:
        transcribed_text = transcribe_speech()
        print(transcribed_text)
        #transcribed_text = "hello how are you!"

        if transcribed_text:
            print(f"Transcribed: {transcribed_text}")
            print(time.time())


            # OpenAI operations
            language_translation = translate_to_language(language, transcribed_text)
            print(time.time())
            english_response = generate_response(transcribed_text)
            print(time.time())
            language_response = translate_response_to_language(language, english_response)
            print(time.time())

            print(f"Translated ({language}):", language_translation)
            print("English Response:", english_response)
            print(f"Translated Response ({language}):", language_response)

            # SpeechGen synthesis (if needed)
            #speak_language_translation(language_translation, speechgen_key)
            #speak_language_response(language_response, speechgen_key)
            #speak_english_response(english_response, speechgen_key)


if __name__ == "__main__":
    main()
