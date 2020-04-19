import io
from PIL import Image

class StadiumScreen:
  def __init__(self):
    self.imgByteArr = None
  
  def loadImageFile(self, path):
    img = Image.open("screenshot.jpeg")
    imgByteIO = io.BytesIO()
    img.save(imgByteIO, format='PNG')
    self.imgByteArr = imgByteIO.getvalue()

  def updateByteArray(self, byteArray):
    self.imgByteArr = byteArray

  def getByteArray(self):
    return self.imgByteArr
