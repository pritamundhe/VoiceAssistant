import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app import app
except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    from flask import Flask
    app = Flask(__name__)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<h1>Server Crashed on Startup</h1><pre>{error_trace}</pre>", 500
