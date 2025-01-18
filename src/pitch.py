from pydub import AudioSegment

def increase_pitch(filepath):
    audio = AudioSegment.from_mp3(filepath)

    # Change the pitch by shifting it
    # A positive value shifts the pitch up; -500 is 1 semitone, -1000 is 2 semitones, etc.
    pitch_shift = 500  # Example: Pitch up by 1 semitone

    # Shift the pitch without altering the length significantly
    pitched_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * (2 ** (pitch_shift / 1200.0)))
    })

    # Export the pitched audio
    pitched_audio.export("pitched_speech.mp3", format="mp3")
