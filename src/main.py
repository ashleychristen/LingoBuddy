# main.py
# This script orchestrates the entire flow of the application.

import os
from pathlib import Path
from openai_utils import translate_to_language, generate_response, translate_response_to_language, create_text_to_speech
from prompting import prompt_output_language
from pitch import increase_pitch
from transcribe import transcribe_speech
from facial.emotion import start_video, end_video, get_curr_emotion
from speechgen.speechgen import make_speech

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
            input_translation_filepath = Path(__file__).parent / "src/mp3/input_translation.mp3"
            #pitched_input_translation_filepath = Path(__file__).parent / "mp3/pitched_input_translation.mp3"
            make_speech(language_translation, input_translation_filepath)
            # os.system(f"afplay {input_translation_filepath}")
            #increase_pitch(input_translation_filepath, "mp3/pitched_input_translation.mp3")

            english_response_filepath = Path(__file__).parent / "src/mp3/english_response.mp3"
            #pitched_english_response_filepath = Path(__file__).parent / "mp3/pitched_english_response.mp3"
            make_speech(english_response, english_response_filepath)
            # os.system(f"afplay {english_response_filepath}")
            # increase_pitch(english_response_filepath, "mp3/pitched_english_response.mp3")
            
            language_response_filepath = Path(__file__).parent / "src/mp3/language_response.mp3"
            #pitched_language_response_filepath = Path(__file__).parent / "mp3/pitched_language_response.mp3"
            make_speech(language_response, language_response_filepath)
            # os.system(f"afplay {language_response_filepath}")
            # increase_pitch(language_response_filepath, "mp3/pitched_language_response.mp3")

            # Speak files (MacOS only)
            os.system(f"afplay {input_translation_filepath}")
            os.system(f"afplay {language_response_filepath}")
            os.system(f"afplay {english_response_filepath}")

    end_video()


if __name__ == "__main__":
    main()
