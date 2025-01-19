import os
from pathlib import Path
from speechgen.speechgen_work import lang_dict
from transcribe import transcribe_speech
from openai_utils import get_language
from speechgen.speechgen_work import make_speech

def prompt_output_language():
    # Prompt the user to choose a language
    prompt_filepath = Path(__file__).parent / "mp3/language_prompt.mp3"
    make_speech("What language should I speak back in?", 'English', prompt_filepath)
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
            if language.title() in lang_dict:
                confirmation_filepath = Path(__file__).parent / "mp3/language_confirmation.mp3"
                make_speech(f"Okay, I'll speak in {language}", 'English', confirmation_filepath)
                os.system(f"afplay {confirmation_filepath}")
                return language
            else:
                failure_filepath = Path(__file__).parent / "mp3/language_failure.mp3"
                make_speech(f"Sorry, I don't know that one. Can you try another language?", 'English', failure_filepath)
                os.system(f"afplay {failure_filepath}")
                return prompt_output_language()
            