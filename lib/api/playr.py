from player import Player
from common import ApiError
import re, chanutils.torrent
import extractor, cherrypy, urlparse, settings

def _save_subs_prefs(subs):
  if 'lang' in subs:
    settings.save('subtitles', {'lang':subs['lang']})

def play(url=None, title=None, subs=None):
  if url is None:
    raise ApiError("Play url is undefined")
  if subs is not None:
    _save_subs_prefs(subs)
  obj = urlparse.urlparse(url)
  if obj.netloc == "www.itv.com":
    cmd = extractor.itv.extract(url)
    Player.playRtmpdump(cmd, title)
  elif obj.netloc == "www.twitch.tv":
    Player.playLivestream(url, title)
  elif chanutils.torrent.is_torrent_url(url):
    Player.playTorrent(url, chanutils.torrent.torrent_idx(url), title, subs)
  else:
    Player.playYtdl(url, title, subs)

def control(action=None):
  if action is None:
    raise ApiError("Action is undefined")
  Player.control(action)

def status():
  return Player.status()
