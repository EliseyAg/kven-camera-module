from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

from camera import Camera


Payload.max_decode_packets = 1024

app = Flask(__name__, static_folder="templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    cam = Camera()
    socketio.on_event('connect', cam.test_connect)
    socketio.on_event('frame', cam.receive_image)
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
