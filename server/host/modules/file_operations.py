from host.handler.command_handler import command


@command("pwd")
def pwd(self, client_socket):
    client_socket.send("pwd".encode())


@command("mkdir")
def mkdir(self, client_socket):
    client_socket.send("mkdir".encode())
