# speechgen.py
# This module handles text-to-speech synthesis using the SpeechGen API.

import requests
import logging

def text_to_speech(text, language, api_key):
    try:
        headers = {
            'authorization': api_key,
            'content-type': 'application/json'
        }
        response = requests.post(
            'https://api.speechgen.com/v1/synthesize',
            headers=headers,
            json={'text': text, 'language': language}
        )
        response.raise_for_status()
        return response.content  # Assuming the API returns audio content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during text-to-speech synthesis: {e}")
        return None

def speak_language_translation(input_text, api_key):
    return text_to_speech(input_text, 'zh', api_key)

def speak_language_response(response_text, api_key):
    return text_to_speech(response_text, 'zh', api_key)

def speak_english_response(response_text, api_key):
    return text_to_speech(response_text, 'en', api_key)
