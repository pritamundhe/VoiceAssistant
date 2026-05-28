import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Using the voice ID from your snippet
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)

def generate_audio_stream(text):
    """
    Calls ElevenLabs API to generate speech from text using the official SDK.
    Returns the audio content (bytes) to be sent to the frontend.
    """
    try:
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # The SDK returns a generator of bytes. We combine it into a single bytes object for Flask.
        audio_bytes = b"".join(list(audio_generator))
        return audio_bytes
    except Exception as e:
        print(f"Error calling ElevenLabs API: {e}")
        return None
