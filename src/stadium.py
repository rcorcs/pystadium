import io
from PIL import Image, ImageDraw

class Screen:
  def __init__(self, width, height):
    self._imgByteArr = None

  def loadImageFile(self, path):
    self.updateImage(Image.open(path))

  def updateByteArray(self, byteArray):
    self._imgByteArr = byteArray

  def updateImage(self,img):
    imgByteIO = io.BytesIO()
    img.save(imgByteIO, format='PNG')
    self._imgByteArr = imgByteIO.getvalue()

  def getByteArray(self):
    return self._imgByteArr

class KeyEvents:
  def __init__(self):
    self._keys = []

  def consume(self):
    k = self._keys
    self._keys = []
    return k

  def set(self, keys):
    self._keys = keys

class Stadium:
  def __init__(self):
    self._screen = Screen(500, 500)
    self._keyEvents = KeyEvents()
    self._online = True

  def shutdown(self):
    self._online = False

  def online(self):
    return self._online

  def screen(self):
    return self._screen

  def keyEvents(self):
    return self._keyEvents

