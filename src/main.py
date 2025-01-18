# main.py
# This script orchestrates the entire flow of the application.

import os
from pathlib import Path
from assemblyai import transcribe_audio
from openai_utils import translate_to_language, generate_response, translate_response_to_language, create_text_to_speech
from speechgen import speak_language_translation, speak_language_response, speak_english_response
from config import get_api_key
from pitch import increase_pitch

def main():
    transcribed_text = "Hello! I'm coding for UofTHacks 12."
    language = 'Spanish'
    emotion = 'Neutral'
    
    # OpenAI operations
    language_translation = translate_to_language(transcribed_text, language)
    english_response = generate_response(transcribed_text, emotion)
    language_response = translate_response_to_language(english_response, language)

    # Print to console for debugging
    print(transcribed_text)
    print(language_translation)
    print(english_response)
    print(language_response)
    
    # Create and speak (on mac) the files
    speech_filepath = Path(__file__).parent / "speech.mp3"
    pitched_filepath = Path(__file__).parent / "pitched_speech.mp3"

    create_text_to_speech(language_translation, speech_filepath)
    # os.system(f"afplay {speech_filepath}")
    increase_pitch(speech_filepath)
    os.system(f"afplay {pitched_filepath}")

    create_text_to_speech(language_response, speech_filepath)
    # os.system(f"afplay {speech_filepath}")
    increase_pitch(speech_filepath)
    os.system(f"afplay {pitched_filepath}")

    create_text_to_speech(english_response, speech_filepath)
    # os.system(f"afplay {speech_filepath}")
    increase_pitch(speech_filepath)
    os.system(f"afplay {pitched_filepath}")
    

if __name__ == "__main__":
    main()
