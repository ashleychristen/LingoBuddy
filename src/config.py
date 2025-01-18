# config.py
# This module centralizes configuration such as API keys or reusable constants.

import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key(key_name):
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"API key for {key_name} not found. Please set it in the .env file.")
    return api_key
