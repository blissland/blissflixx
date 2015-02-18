from common import *
from Queue import Queue
from threading import Thread
import signal
import time
import source
import target
import ytdl
import cherrypy

ST_NOT_RUNNING = 0
ST_SOURCE_STARTING = 1
ST_TARGET_STARTING = 2
ST_RUNNING = 3

class _Status(object):
  def __init__(self):
    self.status = {}
    self.reset()

  def reset(self):
    status = self.status
    status['State'] = ST_NOT_RUNNING
    status['Msg'] = ''
    status['Title'] = ''
    status['Paused'] = False
    status['Error'] = False

  def state(self):
    return self.status['State']

  def setstate(self, state):
    self.status['State'] = state

  def setmsg(self, msg):
    cherrypy.log("MSG: " + msg)
    self.status['Msg'] = msg

  def settitle(self, title):
    self.status['Title'] = title

  def seterror(self, msg):
    self.status['Error'] = True
    self.setmsg(msg)

  def togglepause(self):
    self.status['Paused'] = not self.status['Paused']

  def dictval(self):
    return self.status

class _Player(object):
  def __init__(self):
    self.msgq = Queue(2)
    self.status = _Status()

  def _play(self, item):
    self.source = item['source']
    self.target = item['target']
    self.targetRunning = False

    status = self.status
    status.reset()
    status.setstate(ST_SOURCE_STARTING)
    status.settitle(self.source.title())

    self.sthd = Thread(target=self.source.run, args=(self.msgq,))
    self.sthd.start()

  def stop(self):
    state = self.status.state()
    if state == ST_TARGET_STARTING or state == ST_RUNNING:
      cherrypy.log("DOING TARGET STOP")
      self.target.stop()
    elif state == ST_SOURCE_STARTING:
      cherrypy.log("DOING SOURCE STOP")
      self.source.stop()

  def _setmsg(self):
    self.status.setmsg(self.msgq.get())

  def run(self):
    nextitem = None
    status = self.status

    while True:
      m = self.msgq.get()

      if m == MSG_PLAYER_PLAY:
        cherrypy.log("MSG_PLAYER_PLAY")
        item = self.msgq.get()
        if status.state() == ST_NOT_RUNNING:
          self._play(item)
        else:
          nextitem = item
          self.stop()

      elif m == MSG_SOURCE_READY:
        cherrypy.log("MSG_SOURCE_READY")
        status.setstate(ST_TARGET_STARTING)
        name = self.msgq.get()
        pid = self.msgq.get()
        self.tthd = Thread(target=self.target.run, args=(self.msgq, name, pid))
        self.tthd.start()

      elif m == MSG_TARGET_STARTED:
        cherrypy.log("MSG_TARGET_STARTED")
        self.targetRunning = True
        status.setstate(ST_RUNNING)

      elif m == MSG_TARGET_STOPPED:
        cherrypy.log("MSG_TARGET_STOPPED")
        self.targetRunning = False
        self.source.stop()

      elif m == MSG_SOURCE_STOPPED: 
        cherrypy.log("MSG_SOURCE_STOPPED")
        state = status.state()
        if self.targetRunning:
          # this should only happen if source died unnaturally
          # e.g crashed or was killed
          self.target.stop()
        else:
          status.setstate(ST_NOT_RUNNING)

      elif m == MSG_PLAYER_MSG:
        cherrypy.log("MSG_PLAYER_MSG")
        status.setmsg(self.msgq.get())

      elif m == MSG_SOURCE_ERROR:
        cherrypy.log("MSG_SOURCE_ERROR")
        status.setstate(ST_NOT_RUNNING)
        status.seterror(self.msgq.get())

      elif m == MSG_TARGET_ERROR:
        cherrypy.log("MSG_TARGET_ERROR")
        status.setstate(ST_NOT_RUNNING)
        status.seterror(self.msgq.get())
        self.source.stop()

      elif m == MSG_PLAYER_QUIT:
        cherrypy.log("MSG_PLAYER_QUIT")
        return
  
      if status.state() == ST_NOT_RUNNING and nextitem:
        self._play(nextitem)
        nextitem = None

  def play(self, url, title, skipdl=False):
    if not title:
      title = url
    t = target.OmxPlayer()
    s = source.YoutubeDlSource(url, title, skipdl)
    self.msgq.put(MSG_PLAYER_PLAY)
    self.msgq.put({'source':s, 'target':t})

  def playRtmpDump(self, cmd, title):
    if not title:
      title = "Unknown"
    t = target.OmxPlayer()
    s = source.RtmpDumpSource(cmd, title)
    self.msgq.put(MSG_PLAYER_PLAY)
    self.msgq.put({'source':s, 'target':t})

  def playTorrent(self, torrent, idx, title):
    t = target.OmxPlayer()
    s = source.PeerflixSource(torrent, idx, title)
    self.msgq.put(MSG_PLAYER_PLAY)
    self.msgq.put({'source':s, 'target':t})

  def statusdict(self):
    return self.status.dictval()

  def pause(self):
    self.target.pause()
    self.status.togglepause()

  def resume(self):
    self.target.resume()
    self.status.togglepause()

  def quit(self):
    self.msgq.put(MSG_PLAYER_QUIT)


Player = _Player()
