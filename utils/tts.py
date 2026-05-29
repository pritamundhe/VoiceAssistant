import asyncio
import edge_tts

def generate_audio_stream(text):
    """
    Calls Edge TTS API to generate speech from text.
    Returns the audio content (bytes) to be sent to the frontend.
    """
    async def _generate():
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data

    try:
        return asyncio.run(_generate())
    except Exception as e:
        print(f"Error calling Edge TTS: {e}")
        return None
