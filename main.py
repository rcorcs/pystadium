import io
from time import sleep
import threading
import signal
import logging
from PIL import Image
import signal
from typing import List
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles

from stadium import StadiumScreen

import pong

app = FastAPI()

stadium = StadiumScreen()

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

app.mount("/client", StaticFiles(directory="public", html=True), name="public")

imgByteArr = None
killed = False

@app.get("/health-check")
def read_root():
    return {"Hello": "World"}

@app.get("/image")
def stream_image():
    global stadium
    return StreamingResponse(io.BytesIO(stadium.getByteArray()), media_type="image/png")

class Data(BaseModel):
    event_input: List[str] = []

@app.post("/input")
def read_input(data: Data):
    return {'message': 'ok'}

def on_exit(signum, frame):
    logger.info('Killing remaining threads...')
    logger.info('Bye!')
    killed = True

signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)


x = threading.Thread(target=pong.game,args=(stadium,))
x.start()

