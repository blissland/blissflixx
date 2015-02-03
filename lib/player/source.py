from threading import Thread
from Queue import Queue
from common import *
import os
import shutil
import re

class Source(PlayerProcess):
  def __init__(self, cmd, title, fname):
    PlayerProcess.__init__(self, PROC_SOURCE) 
    self.cmd = cmd
    self._title = title
    self._fname = fname

  def title(self):
    return self._title

  def run(self, msgq):
    self.msgq = msgq

    if not self._popen(self.cmd):
      return

    self._send(MSG_PLAYER_MSG)
    self._send("LOADING STREAM...")
    try:
      if self._ready():
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
    PlayerProcess._stopped(self)

OUTFILE = "/tmp/rtmpdump.out"

class RtmpDumpSource(Source):
  def __init__(self, cmd, title):
    cmd.insert(0, 'rtmpdump')
    cmd.append('-o')
    cmd.append(OUTFILE)
    Source.__init__(self, cmd, title, OUTFILE)

  def _ready(self):
    while True:
      line = self.proc.stdout.readline()
      # process died
      if not line:
        return False
      if line.startswith('Starting download at:'):
        return True
      else:
        print(line)

  def _stopped(self):
    if self.halted:
      try:
        os.remove(OUTFILE)
      except Exception:
        pass
    Source._stopped(self)

TRACKERS = ("udp://open.demonii.com:1337/announce", "udp://tracker.istole.it:6969/announce", "udp://www.eddie4.nl:6969/announce", "udp://coppersurfer.tk:6969/announce", "udp://tracker.btzoo.eu:80/announce", "http://explodie.org:6969/announce", "udp://9.rarbg.me:2710/announce")
HASH_RE = re.compile("[A-F0-9]{40}")

class PeerflixSource(Source):
  def __init__(self, torrent, idx, title):
    cmd = ["node", "--max-old-space-size=128", 
            "/usr/local/bin/peerflix"]
    torrent = self.torr2mag(torrent)
    cmd.append(torrent)
    cmd.append("-q")
    cmd.append("-r")
    #cmd.append("-c")    # Should be this a config option
    #cmd.append("15")
    if idx is not None:
      cmd.append("-i")
      cmd.append(str(idx))
    Source.__init__(self, cmd, title, 'http://127.0.0.1:8888')

  def torr2mag(self, torrent):
    if torrent.startswith("magnet"):
      return torrent
    matches = HASH_RE.search(torrent.upper())
    if not matches:
      return torrent
    magnet = "magnet:?xt=urn:btih:" + matches.group(0) + "&tr="
    return  magnet + "&tr=".join(TRACKERS)
      
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

def test(url, expected):
  msgq = Queue(1)
  src = YoutubeDlSource(url, "title")
  th = Thread(target=src.run, args=(msgq,))
  th.start()
  curr = 0
  while True:
    m = msgq.get()
    if m != expected[curr]:
      print 'Failed on step: %d' % (curr)
      return False
    curr = curr + 1
    if curr == len(expected):
      return True
              
if __name__ == '__main__':
# myThreadOb1 = MyThread(msgq, 'https://www.youtube.com/watch?v=XXCbffp7jLM')
  #Not available in your country

  tests = [
    ['https://www.youtube.com/watch?v=aIMgfBZrrZ8', [MSG_SOURCE_ERROR, "The uploader has not made this video available in your country.", MSG_SOURCE_STOPPED]],
    ['https://www.youtube.com/watch?v=sghDNe1co40', [MSG_SOURCE_ERROR, "This video has been removed by the user.", MSG_SOURCE_STOPPED]],
    ['https://news.ycombinator.com', [MSG_SOURCE_ERROR, "Unsupported URL", MSG_SOURCE_STOPPED]]
  ]

  for t in tests:
    if not test(t[0], t[1]):
      print 'TEST FAILED'
      break

