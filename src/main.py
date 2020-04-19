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

from stadium import Stadium

import pong

app = FastAPI()

stadium = Stadium()

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

app.mount("/client", StaticFiles(directory="../public", html=True), name="public")

imgByteArr = None
killed = False

@app.get("/health-check")
def read_root():
    return {"Hello": "World"}

@app.get("/image")
def stream_image():
    return StreamingResponse(io.BytesIO(stadium.screen().getByteArray()), media_type="image/png")

class Data(BaseModel):
    event_input: List[str] = []

@app.post("/input")
def read_input(data: Data):
    stadium.keyEvents().set(data.event_input)
    return {'message': 'ok'}

@app.on_event("shutdown")
def shutdown_event():
  stadium.shutdown()

x = threading.Thread(target=pong.game,args=(stadium,))
x.start()

