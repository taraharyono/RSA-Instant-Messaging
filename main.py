from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import RSA

app = Flask(__name__)
app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_orginis="*")

@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User connected!":
        emit('message', message, broadcast=True)

@socketio.on('bangkitAlice')
def generate_key_Alice():
    print("kunci dibangkitkan")

@socketio.on('bangkitBob')
def generate_key_Alice():
    print("kunci dibangkitkan")
    
@socketio.on('decryptAlice')
def decrypt_Alice():
    print("Decrypt message Alice")

@socketio.on('decryptBob')
def decrypt_Bob():
    print("Decrypt message Bob")


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000, allow_unsafe_werkzeug=True)
        