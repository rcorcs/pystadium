import io
from time import sleep
import threading
import signal
import logging
from PIL import Image
import signal
from starlette.responses import StreamingResponse
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles

from stadium import StadiumScreen

import game

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

@app.get("/image/{image_name}")
def read_image(image_name: str):
    global stadium
    return StreamingResponse(io.BytesIO(stadium.getByteArray()), media_type="image/png")

def on_exit(signum, frame):
    logger.info('Killing remaining threads...')
    logger.info('Bye!')
    killed = True

signal.signal(signal.SIGINT, on_exit)
signal.signal(signal.SIGTERM, on_exit)


x = threading.Thread(target=game.game,args=(stadium,))
x.start()

