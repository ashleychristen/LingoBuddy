import requests
import logging

# Function to interact with the SpeechGen API
def text_to_speech(text, language, api_key, voice=None, speed=1.0):
    """
    Convert text to speech using the SpeechGen API.

    Args:
        text (str): The text to synthesize.
        language (str): The language code for the output speech.
        api_key (str): The API key for authentication.
        voice (str, optional): The specific voice to use (default is None).
        speed (float, optional): The speed of the speech (default is 1.0).

    Returns:
        bytes or None: The audio content in binary format, or None on failure.
    """
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',  # Update if API uses different auth format
            'Content-Type': 'application/json'
        }
        data = {
            'text': text,
            'language': language,
            'voice': voice or 'default',  # Default voice if none specified
            'speed': speed  # Speech speed (default is normal)
        }
        response = requests.post(
            ' https://speechgen.io/index.php?r=api/text',  # Replace with actual endpoint
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.content  # Binary audio data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during text-to-speech synthesis: {e}")
        return None

# Define specific language translation functions
def speak_language_translation(input_text, api_key):
    """Synthesize speech for a French translation."""
    print(123)
    return text_to_speech(input_text, 'fr', api_key)

def speak_language_response(response_text, api_key):
    """Synthesize speech for a French response."""
    return text_to_speech(response_text, 'fr', api_key)

def speak_english_response(response_text, api_key):
    """Synthesize speech for an English response."""
    return text_to_speech(response_text, 'en-US', api_key)
