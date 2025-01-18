# main.py
# This script orchestrates the entire flow of the application.

import logging
from assemblyai import transcribe_audio
from openai_utils import translate_to_chinese, generate_response, translate_response_to_chinese
from speechgen import speak_chinese_translation, speak_chinese_response, speak_english_response
from config import get_api_key

def main():
    logging.basicConfig(filename='logs/app.log', level=logging.INFO)
    
    # Load API keys
    assemblyai_key = get_api_key('ASSEMBLYAI_API_KEY')
    openai_key = get_api_key('OPENAI_API_KEY')
    speechgen_key = get_api_key('SPEECHGEN_API_KEY')
    
    # Transcribe audio
    # audio_file_path = 'path/to/audio/file'  # TODO: Update with actual path
    # transcribed_text = transcribe_audio(audio_file_path, assemblyai_key)
    # if not transcribed_text:
    #     logging.error("Failed to transcribe audio.")
    #     return

    transcribed_text = 'Hello. How are you?'
    
    # OpenAI operations
    chinese_translation = translate_to_chinese(transcribed_text, openai_key)
    english_response = generate_response(transcribed_text, openai_key)
    chinese_response = translate_response_to_chinese(english_response, openai_key)

    print(transcribed_text)
    print(chinese_translation)
    print(english_response)
    print(chinese_response)
    
    # SpeechGen synthesis
    # speak_chinese_translation(chinese_translation, speechgen_key)
    # speak_chinese_response(chinese_response, speechgen_key)
    # speak_english_response(english_response, speechgen_key)

if __name__ == "__main__":
    main()
