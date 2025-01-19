import os
from pathlib import Path
from openai_utils import translate_to_language, generate_response, translate_response_to_language, create_text_to_speech, get_language
from prompting import prompt_output_language
from pitch import increase_pitch
from transcribe import transcribe_speech

def main():
    language = prompt_output_language()
    emotion = 'Neutral'     # Change with input from camera
    
    while True:
        chime_filepath = Path(__file__).parent / "mp3/chime.mp3"
        os.system(f"afplay {chime_filepath}")

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
            pitched_input_translation_filepath = Path(__file__).parent / "mp3/pitched_input_translation.mp3"
            create_text_to_speech(language_translation, input_translation_filepath)
            # os.system(f"afplay {input_translation_filepath}")
            increase_pitch(input_translation_filepath, "mp3/pitched_input_translation.mp3")

            english_response_filepath = Path(__file__).parent / "mp3/english_response.mp3"
            pitched_english_response_filepath = Path(__file__).parent / "mp3/pitched_english_response.mp3"
            create_text_to_speech(english_response, english_response_filepath)
            # os.system(f"afplay {english_response_filepath}")
            increase_pitch(english_response_filepath, "mp3/pitched_english_response.mp3")
            
            language_response_filepath = Path(__file__).parent / "mp3/language_response.mp3"
            pitched_language_response_filepath = Path(__file__).parent / "mp3/pitched_language_response.mp3"
            create_text_to_speech(language_response, language_response_filepath)
            # os.system(f"afplay {language_response_filepath}")
            increase_pitch(language_response_filepath, "mp3/pitched_language_response.mp3")

            # Speak files (MacOS only)
            os.system(f"afplay {pitched_input_translation_filepath}")
            os.system(f"afplay {pitched_language_response_filepath}")
            os.system(f"afplay {pitched_english_response_filepath}")


if __name__ == "__main__":
    main()
