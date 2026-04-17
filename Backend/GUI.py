from flask import Flask
from flask_socketio import SocketIO
import os
 
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
 
ORB_HTML = os.path.join(os.path.dirname(__file__), "..", "Frontend", "orb.html")
 
def set_state(state):
    socketio.emit("state", {"state": state})
 
@app.route("/")
def index():
    with open(ORB_HTML, encoding="utf-8") as f:
        return f.read()
 
def run():
    socketio.run(app, port=5000, debug=False, use_reloader=False)
 