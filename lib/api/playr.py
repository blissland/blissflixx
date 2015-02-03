from urlparse import urlparse, parse_qs
from player import Player
from common import ApiError, is_torrent, torrent_idx
import time
import re

import extractor

def play(url=None, title=None):
  if url is None:
    raise ApiError("Play url is undefined")
  obj = urlparse(url)
  if obj.netloc == "www.itv.com":
      cmd = extractor.itv.extract(url)
      Player.playRtmpDump(cmd, title)
  elif is_torrent(url):
    Player.playTorrent(url, torrent_idx(url), title)
  else:
    Player.play(url, title, skipdl=_skipdl(url))

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

def stop():
	Player.stop()
	while True:
		status = Player.statusdict()
		if status['State'] == 0:
			break
		time.sleep(1)

directUrls = [  
  # Uses avconv to download
  re.compile(r'http://www\.vice\.com/.*?/(?P<name>.+)'),
  re.compile(r'(?:ooyala:|https?://.+?\.ooyala\.com/.*?(?:embedCode|ec)=)(?P<id>.+?)(&|$)'),
  # Player gets stuck waiting
  re.compile(r'https?://(?:www\.)?vine\.co/v/(?P<id>\w+)'),
]

def _skipdl(url):
  for url_re in directUrls:
    if url_re.match(url):
      return True
  return False
