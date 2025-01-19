import requests
import json
import os
from main import *
from datetime import datetime

# Constants
API_URL = "https://speechgen.io/index.php?r=api/text"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is
MP3_DIR = os.path.join(BASE_DIR, "mp3")
LOG_FILE = os.path.join(BASE_DIR, "speechgen.log")

def make_speech(text, language, path):
    voice = grab_language(language)
    settings = load_settings(voice)
    convert_text_to_speech(settings, text, path)

def load_api_credentials():
    with open(os.path.join(BASE_DIR, "api.txt")) as f:
        return json.load(f)

def grab_language(language):
    lang_dict = {}
    lang_dict['English'] = 'Anny'
    lang_dict['Welsh'] = 'Nia'
    lang_dict['Basque'] = 'Ainhoa'
    lang_dict['Maltese'] = 'Ganni'
    lang_dict['Galician'] = 'Sabela'
    lang_dict['Zulu'] = 'Thando'
    lang_dict['Amharic'] = 'Mekdes'
    lang_dict['Azerbaijani'] = 'Banu'
    lang_dict['Catalan'] = 'Joana'
    lang_dict['Khmer'] = 'Sreymom'
    lang_dict['Cantonese'] = 'XiaoMin'
    lang_dict['Shanghainese'] = 'Xiaotong'
    lang_dict['Mandarin'] = 'Xiaobei'
    lang_dict['Spanish'] = 'Irene'

    if language.title() in lang_dict:
        return lang_dict[language]
    else:
        return 'Anny'

def load_settings(voice):
    # with open(os.path.join(BASE_DIR, "settings.txt")) as f:
        # settings_text = f.read()
        # Convert the settings format to a dictionary
    settings_dict = {}
    settings_dict['format'] = 'mp3'
    settings_dict['voice'] = voice
    settings_dict['speed'] = 1.0
    settings_dict['pitch'] = 1.6
    settings_dict['emotion'] = 'good'
    settings_dict['pause_sentence'] = 300
    settings_dict['pause_paragraph'] = 400
    settings_dict['bitrate'] = 48000

        # for line in settings_text.split(','):
        #     if '=>' in line:
        #         key, value = line.split('=>')
        #         key = key.strip().strip("'")
        #         value = value.strip().strip("'")
        #         settings_dict[key] = value
    return settings_dict

def load_text():
    with open(os.path.join(BASE_DIR, "text.txt"), encoding='utf-8') as f:
        return f.read().strip()

def log_message(message, to_console=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    if to_console:
        print(log_entry)
        
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + "\n")

def convert_text_to_speech(settings, text, path):
    try:
        # Load credentials, settings, and text
        credentials = load_api_credentials()
        #settings = load_settings()
        #text = load_text()

        # Check text length
        if len(text) > 2000:
            raise ValueError("Text length exceeds 2000 characters. Please use Method 2 for longer texts.")

        # Prepare request data
        data = {
            "token": credentials["token"],
            "email": credentials["email"],
            "text": text,
            **settings
        }

        # Log request
        log_message("Sending request to SpeechGen API...")
        
        # Send request
        response = requests.post(API_URL, data=data).json()
        
        # Handle response
        if response.get('status') == 1 and 'file' in response:
            # Download the file
            file_url = response['file']
            file_format = response.get('format', 'mp3')
            file_id = response.get('id', 'output')
            voice = settings.get('voice', 'default')
            
            output_path = os.path.join(MP3_DIR, f'{path}')
            
            # Download and save the audio file
            audio_content = requests.get(file_url).content
            with open(output_path, 'wb') as f:
                f.write(audio_content)
                
            log_message(f"Successfully created audio file: {output_path}")
            log_message(f"Remaining balance: {response.get('balans', 'unknown')}")
        else:
            error_msg = response.get('error', 'Unknown error occurred')
            log_message(f"Error: {error_msg}")
            
    except Exception as e:
        log_message(f"Error: {str(e)}")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs(MP3_DIR, exist_ok=True)
    
    # Run the conversion
    convert_text_to_speech()