from threading import Thread
from Queue import Queue
from common import *
import os
import shutil
import re
import cherrypy
import chanutils.torrent

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
        cherrypy.log("RTMPDUMP: " + line)

  def _stopped(self):
    if self.halted:
      try:
        os.remove(OUTFILE)
      except Exception:
        pass
    Source._stopped(self)

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
    if idx is not None:
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
