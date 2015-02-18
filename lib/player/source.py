from threading import Thread
from Queue import Queue
from common import *
import os, re, shutil, cherrypy, locations, json
import chanutils.torrent

TMP_DIR = "/tmp/blissflixx"
OUT_FILE = "/tmp/blissflixx/bf.out"

class Source(PlayerProcess):
  def __init__(self, cmd, title, fname):
    PlayerProcess.__init__(self, PROC_SOURCE) 
    self.cmd = cmd
    self._title = title
    self._fname = fname
    if not os.path.exists(TMP_DIR):
      os.makedirs(TMP_DIR)

  def title(self):
    return self._title

  def run(self, msgq):
    self.msgq = msgq

    if not self._popen(self.cmd):
      return

    self._send(MSG_PLAYER_MSG)
    self._send("LOADING STREAM...")
    try:
      r = self._ready()
      if isinstance(r, basestring):
        self._fname = r
        r = True
      if r:
        self._send(MSG_SOURCE_READY)
        self._send(self._fname)
        self._send(self.proc.pid)
    except Exception, e: 
      self._error(str(e))
      self.halted = True

    self._wait()

  def _ready(self):
    return True

  def _error(self, emsg):
    PlayerProcess._error(self, emsg)

  def _stopped(self):
    try:
      if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)
    except Exception:
      pass
    PlayerProcess._stopped(self)

class RtmpDumpSource(Source):
  def __init__(self, cmd, title):
    cmd.insert(0, 'rtmpdump')
    cmd.append('-o')
    cmd.append(OUT_FILE)
    Source.__init__(self, cmd, title, OUT_FILE)

  def _ready(self):
    while True:
      line = self.proc.stdout.readline()
      # process died
      if not line:
        return False
      if line.startswith('Starting download at:'):
        return True
      else:
        cherrypy.log("RTMPDUMP: " + line)

class PeerflixSource(Source):
  def __init__(self, torrent, idx, title):
    cmd = ["node", "--max-old-space-size=128", 
            "/usr/local/bin/peerflix"]
    # Avoid problems with downloading torrent files
    torrent = chanutils.torrent.torrent2magnet(torrent)
    cmd.append(torrent)
    cmd.append("-q")
    cmd.append("-r")
    #cmd.append("-c")    # Should be this a config option
    #cmd.append("15")
    if idx is not None and idx >= 0:
      cmd.append("-i")
      cmd.append(str(idx))
    Source.__init__(self, cmd, title, 'http://127.0.0.1:8888')

  def _ready(self):
    while True:
      line = self.proc.stdout.readline()
      # process died
      if not line:
        return False
      elif line.startswith('Bad Response'):
        self._error(line.strip())
        return False
      # Get this error if site down/blocked
      # html page instead of torrent
      elif line.startswith('not a colon at'):
        self._error("Unable to retrieve torrent")
        return False
      elif line.startswith('server is listening'):
        return True

  def _stopped(self):
    try:
      shutil.rmtree('/tmp/torrent-stream')
    except Exception:
      pass
    Source._stopped(self)

YTDL_PATH = os.path.join(locations.YTUBE_PATH, "youtube_dl")
YTDL_PATH = os.path.join(YTDL_PATH, "__main__.py")

BBC_URL = re.compile(r'https?://(?:www\.)?bbc\.co\.uk/(?:(?:(?:programmes|iplayer(?:/[^/]+)?/(?:episode|playlist))/)|music/clips[/#])(?P<id>[\da-z]{8})')

class YoutubeDlSource(Source):
  def __init__(self, url, title, skipdl=False):
    cmd = [YTDL_PATH, "--no-part", "--no-continue", "--no-playlist",
	   "--max-downloads", "1", "--no-progress", "--output", OUT_FILE]
    if skipdl:
      cmd.append("--simulate")
      cmd.append("--dump-single-json")
    if BBC_URL.match(url):
      # Don't download hd 1280 x 720 but the next best quality
      # (usaully 832 x 468). Sometimes rtmpdump aborts before downloading
      # all of hd quality. Lower quality seems more reliable.
      cmd.append("--format")
      cmd.append("best[height<720]")
    cmd.append(url)
    Source.__init__(self, cmd, title, OUT_FILE)

  def _ready(self):
    lastline = "Unexpected error from youtube-dl"
    while True:
      line = self.proc.stdout.readline()	
      if line is None:
        self._error(lastline)
        return False
      line = line.strip()
      if line.strip() != '':      
	cherrypy.log("YTDL: " + line)
      if line.startswith("[download] Destination:"):
        return True
      elif line.startswith("{"):
        obj = json.loads(line)
        return obj['url']
      lastline = line
