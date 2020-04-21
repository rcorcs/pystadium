import io
import threading
import importlib.util

from PIL import Image, ImageDraw

class Screen:
  def __init__(self,game=None):
    self._game = game
    self._img = None

  def loadImageFile(self, path):
    self.updateImage(Image.open(path))

  def updateImage(self,img):
    self._img = img

  def getByteArray(self,fmt='PNG'):
    imgByteArr = None
    if self._img:
      imgByteIO = io.BytesIO()
      self._img.save(imgByteIO, format=fmt)
      imgByteArr = imgByteIO.getvalue()
    return imgByteArr

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
    self._screen = Screen()
    self._keyEvents = KeyEvents()
    self._online = False

  def load(self,name,path):
    spec = importlib.util.spec_from_file_location(name, path)
    self._game = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(self._game)

  def run(self):
    self._online = True
    self._thread = threading.Thread(target=self._game.run,args=(self,))
    self._thread.start()

  def shutdown(self):
    self._online = False

  def online(self):
    return self._online

  def screen(self):
    return self._screen

  def keyEvents(self):
    return self._keyEvents

