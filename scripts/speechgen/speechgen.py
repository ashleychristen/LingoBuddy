# From https://speechgen.io/en/node/python-tts/

import requests
import json
import time
import os
from datetime import datetime

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to read settings from the settings.txt file
def read_settings(file_path):
    settings = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=>')
            settings[key.strip("'")] = eval(value.strip(", "))
    return settings

# Function to get the list of voices
def get_voices():
    url = "https://speechgen.io/index.php?r=api/voices"
    response = requests.get(url)
    log_message(f"Voices API response status code: {response.status_code}")
    if response.status_code == 200:
        try:
            voices_data = response.json()
            if isinstance(voices_data, dict):
                voices = []
                for language, voices_list in voices_data.items():
                    voices.extend(voice for voice in voices_list)
                log_message(f"Extracted voices count: {len(voices)}")
                return voices
            else:
                log_message("Error: Unexpected JSON structure")
                return []
        except json.JSONDecodeError:
            log_message("Error decoding JSON response from voices API.")
            return []
    else:
        log_message("Failed to fetch voices from API.")
        return []

# Function to send a request via API
def send_request(url, data):
    response = requests.post(url, data=data)
    return response.json()

# Function for logging
def log_message(message, to_console=True):
    log_file = r'c:\scripts\speechgen\log.txt'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {message}"
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(log_entry + "\n")
    if to_console:
        print(log_entry)

# Function for process animation
def animate_process(message, duration=30):
    animation = "|/-\\"
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        print(f"\r{message} {animation[idx % len(animation)]}", end="")
        time.sleep(0.5)
        idx += 1
    print()


# Main function
def main():
    # File paths
    text_file = r'c:/scripts/speechgen/text.txt'
    api_file = r'c:/scripts/speechgen/api.txt'
    settings_file = r'c:/scripts/speechgen/settings.txt'
    output_folder = r'c:/scripts/speechgen/mp3'
    
    # Checking if the settings file exists
    if not os.path.exists(settings_file):
        log_message(f"Settings file not found: {settings_file}", to_console=True)
        return
    
    # Reading the text for speech synthesis
    text = read_file(text_file)
    
    # Reading API settings
    api_info = json.loads(read_file(api_file))
    email = api_info.get("email", "").strip()
    token = api_info.get("token", "").strip()
    
    # Reading settings from the settings.txt file
    settings = read_settings(settings_file)
    
    # Getting the list of voices
    voices = get_voices()
    log_message(f"Number of available voices: {len(voices)}")
    
    # Checking the validity of the voice
    voice = settings.get('voice', 'John')
    matched_voice = next((v for v in voices if v['voice'] == voice), None)
    if matched_voice is None:
        available_voices = ', '.join([v['voice'] for v in voices])
        log_message(f"Error: Voice '{voice}' is not available. Available voices are: {available_voices}")
        voice = 'John'  # Setting the default voice
        log_message(f"Using default voice: {voice}")
    else:
        log_message(f"Using voice: {matched_voice}")
    
    # Forming the data for the request
    data = {
        'token': token,
        'email': email,
        'voice': voice,
        'text': text,
    }
    optional_params = ['format', 'speed', 'pitch', 'emotion', 'pause_sentence', 'pause_paragraph', 'bitrate']
    for param in optional_params:
        if param in settings:
            data[param] = settings[param]
    
    # Shortening the content of the text for logging
    short_text = text if len(text) <= 100 else text[:97] + '...'
    
    url = "https://speechgen.io/index.php?r=api/text"
    
    # Logging the request
    log_message(f"Submitting voiceover request to {url}", to_console=True)
    log_message(f"Request: {json.dumps({**data, 'text': short_text})}", to_console=False)
    
    # Sending the request and getting the response
    response = send_request(url, data)
    log_message(f"Response: {json.dumps(response)}", to_console=False)

    # Handling the response
    if response['status'] == 1:
        if 'file' in response and 'format' in response:
            file_url = response['file']
            file_format = response['format']
            file_id = response['id']
            file_path = os.path.join(output_folder, f'{file_id}_{voice}.{file_format}')
            file_content = requests.get(file_url).content
            with open(file_path, 'wb') as file:
                file.write(file_content)
            log_message("Voiceover completed", to_console=True)
            log_message(f"Voiceover completed: {file_path}", to_console=False)
        else:
            log_message(f"Error: Missing 'file' or 'format' in response. Status: {response['status']}, Error: {response.get('error', 'No error message')}", to_console=True)
    else:
        log_message(f"Error: {response.get('error', 'Unknown error')}", to_console=True)


if __name__ == "__main__":
    main()