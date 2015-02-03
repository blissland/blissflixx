from threading import Thread
from player import Player

def start_thread():
  pt = Thread(target=Player.run)
  pt.daemon = True
  pt.start()
