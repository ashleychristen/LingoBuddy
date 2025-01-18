# openai_utils.py
# This module handles all OpenAI API interactions.

from config import get_api_key
from openai import OpenAI
import logging

# Initialize client
openai_key = get_api_key('OPENAI_API_KEY')
client = OpenAI(api_key=openai_key)

def translate_to_chinese(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator. Your job is to directly translate as accurately as " +
                 "possible and say nothing else"},
                {
                    "role": "user",
                    "content": f"Translate the following text into Chinese: {text}"
                }
            ],
            max_tokens=100)
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error during translation to Chinese: {e}")
        return None

def generate_response(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a toy, and a child is speaking to you."},
                {
                    "role": "user",
                    "content": f"Generate an appropriate response to this comment: {text}"
                }
            ],
            max_tokens=100)
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error during response generation: {e}")
        return None

def translate_response_to_chinese(response):
    return translate_to_chinese(response)
