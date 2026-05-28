import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Using the voice ID from your snippet
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

def generate_audio_stream(text):
    """
    Calls ElevenLabs API to generate speech from text.
    Returns the audio content (bytes) to be sent to the frontend.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.content
    except Exception as e:
        error_details = ""
        if hasattr(e, 'response') and e.response is not None:
            error_details = e.response.text
        print(f"Error calling ElevenLabs API: {e}. Details: {error_details}")
        return None
