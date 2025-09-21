from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

import cv2

import eventlet
import numpy as np

import base64
import os


Payload.max_decode_packets = 1024

app = Flask(__name__, static_folder="templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})


@socketio.on("frame")
def receive_image(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
