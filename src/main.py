# main.py
# This script orchestrates the entire flow of the application.

import os
from pathlib import Path
from openai_utils import translate_to_language, generate_response, translate_response_to_language, create_text_to_speech
from prompting import prompt_output_language
from transcribe import transcribe_speech
from facial.emotion import end_video, get_curr_emotion
from speechgen.speechgen_work import make_speech

def main():
    # start_video()
    print("Prompting user to select language...")
    language = prompt_output_language()
    
    emotion = 'Neutral'     # Change with input from camera
    
    while True:
        print("Indicating user to begin speaking...")
        chime_filepath = Path(__file__).parent / "mp3/chime.mp3"
        os.system(f"afplay {chime_filepath}")

        emotion = get_curr_emotion()
        print(f"Emotion: {emotion}")
        transcribed_text = transcribe_speech()

        if transcribed_text:
            print(f"Transcribed: {transcribed_text}")

            # OpenAI operations
            language_translation = translate_to_language(transcribed_text, language)
            english_response = generate_response(transcribed_text, emotion)
            language_response = translate_response_to_language(english_response, language)

            print(f"Translated ({language}):", language_translation)
            print("English Response:", english_response)
            print(f"Translated Response ({language}):", language_response)

            # Create text to speech mp3s
            input_translation_filepath = Path(__file__).parent / "mp3/input_translation.mp3"
            print(language)
            make_speech(language_translation, language, input_translation_filepath)

            english_response_filepath = Path(__file__).parent / "mp3/english_response.mp3"
            make_speech(english_response, 'English', english_response_filepath)
            
            language_response_filepath = Path(__file__).parent / "mp3/language_response.mp3"
            make_speech(language_response, language, language_response_filepath)

            # Speak files (MacOS only)
            os.system(f"afplay {input_translation_filepath}")
            os.system(f"afplay {language_response_filepath}")
            os.system(f"afplay {english_response_filepath}")

    end_video()


if __name__ == "__main__":
    main()
