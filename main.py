import socket
import os
import numpy as np
from PIL import ImageGrab

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8090))

print("[*] Connected to server")



def start_screenshare():
    try:
        print("Trying to send image")
        # Get the image
        img = get_screenshot()

        # Send the image to the server
        print("[*] Sending image " + str(len(img)) + " bytes")
        s.sendall(img)
    except Exception as e:
        print(f"Error sending image: {str(e)}")


def get_screenshot():
    # Get the screenshot of the current screen and return it as bytes
    img = ImageGrab.grab()
    img = np.array(img)

    # Convert the image to bytes
    img_bytes = img.tobytes()

    return img_bytes


def stop_screenshare():
    s.close()


if __name__ == "__main__":
    start_screenshare()
