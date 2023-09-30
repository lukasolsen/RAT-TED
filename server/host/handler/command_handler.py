# command_handlers.py
# A dictionary to map commands to their associated functions
command_handlers = {}

# Decorator to register a function as a command handler


def command(name):
    def decorator(func):
        command_handlers[name] = func
        return func
    return decorator

# Function to execute a command


def execute_command(self, command, client_socket):
    command_parts = command.split()
    command_name = command_parts[0]
    args = command_parts[1:]

    if command_name in command_handlers:
        try:
            command_handlers[command_name](self, client_socket, *args)
        except TypeError:
            print("Invalid number of arguments")
    else:
        # You can handle unsupported commands here or send them to the client
        client_socket.send(command.encode())
