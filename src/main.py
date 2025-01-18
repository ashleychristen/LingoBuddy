# main.py
# This script orchestrates the entire flow of the application.

import logging
from assemblyai import transcribe_audio
from openai_utils import translate_to_language, generate_response, translate_response_to_language
from speechgen import speak_language_translation, speak_language_response, speak_english_response
from config import get_api_key

def main():
    # logging.basicConfig(filename='logs/app.log', level=logging.INFO)
    
    # Load API keys
    assemblyai_key = get_api_key('ASSEMBLYAI_API_KEY')
    speechgen_key = get_api_key('SPEECHGEN_API_KEY')
    
    # Transcribe audio
    # audio_file_path = 'path/to/audio/file'  # TODO: Update with actual path
    # transcribed_text = transcribe_audio(audio_file_path, assemblyai_key)
    # if not transcribed_text:
    #     logging.error("Failed to transcribe audio.")
    #     return

    transcribed_text = "Hello. My friend has not messaged me back."
    language = "German"
    emotion = "Sad"
    
    # OpenAI operations
    language_translation = translate_to_language(transcribed_text, language)
    english_response = generate_response(transcribed_text, emotion)
    language_response = translate_response_to_language(english_response, language)

    print(transcribed_text)
    print(language_translation)
    print(english_response)
    print(language_response)
    
    # SpeechGen synthesis
    # speak_language_translation(language_translation, speechgen_key)
    # speak_language_response(language_response, speechgen_key)
    # speak_english_response(english_response, speechgen_key)

if __name__ == "__main__":
    main()
