import io
from PIL import Image
from starlette.responses import StreamingResponse
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/image/{image_name}")
def read_image(image_name: str):
    img = Image.open("picture.jpg")
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return StreamingResponse(io.BytesIO(imgByteArr), media_type="image/png")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
