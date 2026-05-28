import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

SYSTEM_PROMPT = "You are the user's personal voice assistant. You must remember all the details, preferences, and information they share with you in the conversation history, and use it to give highly personalized and contextual answers. Keep your answers concise, natural, and conversational as they will be spoken out loud. Avoid using complex markdown, code blocks, or symbols."

def generate_response(messages_history):
    """
    Generate a response from DeepSeek API given the conversation history.
    messages_history format: [{'role': 'user'/'assistant', 'content': '...'}]
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(messages_history)
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        return "I'm sorry, I couldn't connect to my brain right now."
