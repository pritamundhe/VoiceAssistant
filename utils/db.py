import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("voice_assistant_db")
history_collection = db.get_collection("chat_history")

def save_message(role, content):
    """
    Save a message to the database.
    role: 'user' or 'assistant'
    content: the text content
    """
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    }
    history_collection.insert_one(message)

def get_recent_history(limit=10):
    """
    Get the most recent messages from the database.
    Returns a list of dicts: [{'role': '...', 'content': '...'}]
    """
    cursor = history_collection.find({}, {"_id": 0, "role": 1, "content": 1}).sort("timestamp", -1).limit(limit)
    messages = list(cursor)
    # Reverse to return chronological order
    messages.reverse()
    return messages
