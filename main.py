import io
from time import sleep
import threading
import signal

from PIL import Image

from starlette.responses import StreamingResponse
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

app.mount("/client", StaticFiles(directory="public", html=True), name="public")

imgByteArr = None

@app.get("/health-check")
def read_root():
    return {"Hello": "World"}

@app.get("/image/{image_name}")
def read_image(image_name: str):
    global imgByteArr
    return StreamingResponse(io.BytesIO(imgByteArr), media_type="image/png")

def thread_func():
    import random
    global imgByteArr
    while True:
        path = random.choice(['bh.jpg','bonn.jpg','itacolomi.jpg'])
        print('ImageUpdate:',path)
        img = Image.open(path)
        imgByteIO = io.BytesIO()
        img.save(imgByteIO, format='PNG')
        imgByteArr = imgByteIO.getvalue()
        sleep(1)

x = threading.Thread(target=thread_func)
x.start()
