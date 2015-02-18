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

directUrls = [  
  # Uses avconv to download
  re.compile(r'http://www\.vice\.com/.*?/(?P<name>.+)'),
  re.compile(r'(?:ooyala:|https?://.+?\.ooyala\.com/.*?(?:embedCode|ec)=)(?P<id>.+?)(&|$)'),
  # Player gets stuck waiting
  re.compile(r'https?://(?:www\.)?vine\.co/v/(?P<id>\w+)'),
  # Youtube
  re.compile(r"""(?x)^
                     (
                         (?:https?://|//)                                    # http(s):// or protocol-independent URL
                         (?:(?:(?:(?:\w+\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie)?\.com/|
                            (?:www\.)?deturl\.com/www\.youtube\.com/|
                            (?:www\.)?pwnyoutube\.com/|
                            (?:www\.)?yourepeat\.com/|
                            tube\.majestyc\.net/|
                            youtube\.googleapis\.com/)                        # the various hostnames, with wildcard subdomains
                         (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
                         (?:                                                  # the various things that can precede the ID:
                             (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/
                             |(?:                                             # or the v= param in all its forms
                                 (?:(?:watch|movie)(?:_popup)?(?:\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
                                 (?:\?|\#!?)                                  # the params delimiter ? or # or #!
                                 (?:.*?&)?                                    # any other preceding param (like /?s=tuff&v=xxxx)
                                 v=
                             )
                         ))
                         |youtu\.be/                                          # just youtu.be/xxxx
                         |(?:www\.)?cleanvideosearch\.com/media/action/yt/watch\?videoId=
                         )
                     )?                                                       # all until now is optional -> you can pass the naked ID
                     ([0-9A-Za-z_-]{11})                                      # here is it! the YouTube video ID
                     (?!.*?&list=)                                            # combined list/video URLs are handled by the playlist IE
                     (?(1).+)?                                                # if we found the ID, everything can follow
                     $"""),
]

def _skipdl(url):
  for url_re in directUrls:
    if url_re.match(url):
      return True
  return False
