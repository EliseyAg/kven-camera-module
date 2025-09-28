from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import cv2

import numpy as np
import base64


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


class Camera:
    def __init__(self):
        pass

    def test_connect(self, data):
        print("Connected")
        emit("my response", {"data": "Connected"})

    def receive_image(self, b_image):
        # Decode the base64-encoded image data
        image = base64_to_image(b_image)
