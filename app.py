import os
# Fix for the PostgreSQL TLS CA certificate issue affecting `requests`
if 'REQUESTS_CA_BUNDLE' in os.environ:
    del os.environ['REQUESTS_CA_BUNDLE']
if 'CURL_CA_BUNDLE' in os.environ:
    del os.environ['CURL_CA_BUNDLE']

from flask import Flask, render_template, request, jsonify, send_file
import io
from utils.db import save_message, get_recent_history
from utils.llm import generate_response
from utils.tts import generate_audio_stream

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
        
    # Save user message to DB
    save_message('user', user_message)
    
    # Get a larger chunk of conversation history from MongoDB so it remembers past details
    history = get_recent_history(limit=50) 
    
    # Generate AI response
    ai_response = generate_response(history)
    
    # Save AI response to DB
    save_message('assistant', ai_response)
    
    return jsonify({
        "response": ai_response
    })

@app.route('/api/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
        
    # Generate audio
    audio_data = generate_audio_stream(text)
    
    if audio_data:
        # Return audio file
        return send_file(
            io.BytesIO(audio_data),
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="response.mp3"
        )
    else:
        return jsonify({"error": "Failed to generate audio"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
