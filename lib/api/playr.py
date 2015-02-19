from player import Player
from common import ApiError
import re, chanutils.torrent
import extractor, cherrypy, urlparse

def play(url=None, title=None):
  cherrypy.log("PLAYING: " + url)
  if url is None:
    raise ApiError("Play url is undefined")
  obj = urlparse.urlparse(url)
  if obj.netloc == "www.itv.com":
    cmd = extractor.itv.extract(url)
    Player.playRtmpDump(cmd, title)
  elif chanutils.torrent.is_torrent_url(url):
    Player.playTorrent(url, chanutils.torrent.torrent_idx(url), title)
  else:
    Player.play(url, title)

def control(action=None):
  if action is None:
    raise ApiError("Action is undefined")
  if action == "stop":
    Player.stop()
  elif action == "pause":
    Player.pause()
  elif action == "resume":
    Player.resume()

def status():
  return Player.statusdict()
