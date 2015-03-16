from threading import Thread
from Queue import Queue
from common import *
import chanutils.torrent, os,re, shutil
import cherrypy, locations, json, siteinfo

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
    if self.halted and os.path.exists(OUT_FILE):
      try:
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
      line = Source._readline(self)
      if line is None:
        return False
      elif line.startswith('Starting download at:'):
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
      line = Source._readline(self)
      if line is None:
        return False
      elif line.startswith('Bad Response'):
        self._error(line)
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

class YoutubeDlSource(Source):
  def __init__(self, url, title):
    cmd = [YTDL_PATH, "--no-part", "--no-continue", "--no-playlist",
	   "--max-downloads", "1", "--no-progress", "--output", OUT_FILE]
    if siteinfo.skip_download(url):
      cmd.append("--simulate")
      cmd.append("--dump-single-json")
    fmat = siteinfo.get_format(url)
    if fmat is not None:
      cmd.append("--format")
      cmd.append(fmat)
    cmd.append(url)
    Source.__init__(self, cmd, title, OUT_FILE)

  def _ready(self):
    while True:
      line = Source._readline(self)
      if line is None:
        return False
      cherrypy.log("YTDL: " + line)
      if line.startswith("[download] Destination:"):
        return True
      elif line.startswith("{"):
        obj = json.loads(line)
        return obj['url']
      elif line.startswith("ERROR:"):
        self._error(self._get_ytdl_err(line[7:]))
        return False

  def _get_ytdl_err(self, msg):
    if msg.strip() == "":
      return
    idx = msg.find('YouTube said:')
    if idx > -1:
      msg = msg[idx+14:]

    idx = msg.find('Unsupported URL:')
    if idx > -1:
      msg = 'Unsupported URL'

    idx = msg.find('is not a valid URL.')
    if idx > -1:
      msg = msg[:idx+18]

    idx = msg.find('This video is no longer available')
    if idx > -1:
      msg = 'No longer available'

    # Assume 403 is because wrong country
    idx = msg.find('HTTP Error 403: FORBIDDEN')
    if idx > -1:
      msg = 'This video is not available in your country'

    idx = msg.find('ERROR:')
    if idx > -1:
      idx = msg.find(' ', idx)
      msg = msg[idx+1:]

    return msg
