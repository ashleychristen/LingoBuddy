# assemblyai.py
# This module handles the transcription logic using AssemblyAI.

import requests
import logging

def transcribe_audio(audio_file_path, api_key):
    try:
        headers = {
            'authorization': api_key,
            'content-type': 'application/json'
        }
        response = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers=headers,
            json={'audio_url': audio_file_path}
        )
        response.raise_for_status()
        return response.json()['text']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during transcription: {e}")
        return None
