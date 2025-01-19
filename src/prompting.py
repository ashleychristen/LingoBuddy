import os
from pathlib import Path
from transcribe import transcribe_speech
from openai_utils import get_language, create_text_to_speech

def prompt_output_language():
    # Prompt the user to choose a language
    prompt_filepath = Path(__file__).parent / "mp3/language_prompt.mp3"
    os.system(f"afplay {prompt_filepath}")

    while True:
        # Indicate to start speaking
        chime_filepath = Path(__file__).parent / "mp3/chime.mp3"
        os.system(f"afplay {chime_filepath}")

        # Listen for a response
        transcribed_text = transcribe_speech()
        print(transcribed_text)
        
        if transcribed_text:
            # Confirm language and return
            print(f"Transcribed: {transcribed_text}")
            language = get_language(transcribed_text)
            confirmation_filepath = Path(__file__).parent / "mp3/language_confirmation.mp3"
            create_text_to_speech(f"Got it. I'll speak in {language}", confirmation_filepath)
            os.system(f"afplay {confirmation_filepath}")
            return language