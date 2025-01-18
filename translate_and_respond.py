
# OLD but keeping it just in case

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Define the OpenAI API endpoint
api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Function to send a request to the OpenAI API
def translate_and_respond(text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"Translate the following text to Chinese and generate a response: {text}",
        "max_tokens": 100
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        chinese_translation = result['choices'][0]['text']
        
        # TODO: Integrate live transcription with AssemblyAI
        # TODO: Integrate speech synthesis with SpeechGen

        return chinese_translation
    except requests.exceptions.RequestException as e:
        with open("error.log", "a") as log_file:
            log_file.write(f"Error: {e}\n")
        return None

# Example usage
if __name__ == "__main__":
    english_text = "Hello, how are you?"
    translated_text = translate_and_respond(english_text)
    if translated_text:
        print("Translated and responded text:", translated_text)
    else:
        print("An error occurred. Check error.log for details.")
