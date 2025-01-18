# openai_utils.py
# This module handles all OpenAI API interactions.

import openai
import logging

def translate_to_chinese(text, api_key):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate the following text to Chinese: {text}",
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error during translation to Chinese: {e}")
        return None

def generate_response(text, api_key):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Respond to the following text: {text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error during response generation: {e}")
        return None

def translate_response_to_chinese(response, api_key):
    return translate_to_chinese(response, api_key)
