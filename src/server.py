import io
from time import sleep

import logging
from PIL import Image
import signal

from typing import List
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles


from stadium import Stadium


app = FastAPI()

library = {}
library['pong'] = {'path':'/home/rodrigo/dev/pystadium/games/pong.py','stadium':None}

@app.get("/health-check")
def read_root():
  return {"Hello": "World"}

@app.get("/launch/{game}")
def launch_game(game: str):
  if launchFromLibrary(game):
    return {game: "OK"}
  else:
    return {game: "ERROR"}

@app.get("/image/{game}")
def stream_image(game: str):
  if game in library.keys() and library[game]['stadium']!=None:
    imgArray = library[game]['stadium'].screen().getByteArray()
    return StreamingResponse(io.BytesIO(imgArray), media_type="image/png")

class Data(BaseModel):
  event_input: List[str] = []

@app.post("/input/{game}")
def read_input(game: str, data: Data):
  if game in library.keys() and library[game]['stadium']:
    library[game]['stadium'].keyEvents().set(data.event_input)
  return {'message': 'ok'}

@app.on_event("shutdown")
def shutdown_event():
  stadium.shutdown()

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

app.mount("/client", StaticFiles(directory="../public", html=True), name="public")

#def launch(game):
#  stadium = Stadium(game)
#  stadium.run()

def launchFromLibrary(game):
  if game in library.keys():
    if library[game]['stadium']!=None:
      library[game]['stadium'].shutdown()
    stadium = Stadium()
    stadium.load(game,library[game]['path'])
    library[game]['stadium'] = stadium
    stadium.run()
    return True
  return False

