import os, cherrypy, locations, ythelper
import subprocess32 as subprocess
from Queue import Queue
from processpipe import ProcessPipe, _start_thread, MSG_PLAYER_PIPE_STOPPED
from pflixproc import PeerflixProcess
from rtmpproc import RtmpProcess
from ytdlproc import YoutubeDlProcess
from lvstrmrproc import LivestreamerProcess
from omxproc import OmxplayerProcess
from omxproc2 import OmxplayerProcess2
from dlsrvproc import DlsrvProcess
from subsproc import SubtitlesProcess

ST_NOT_RUNNING = 0
ST_STARTING = 1
ST_RUNNING = 3

MSG_PLAYER_PLAY = 1
MSG_PLAYER_STOP = 2
MSG_PLAYER_QUIT = 3

class _Player(object):

  def __init__(self):
    self.msgq = Queue(2)
    self.play_pipe = None
    self.play_thread = None
    self.main_thread = None
    self.error = None
    self.paused = False

  def _stop(self):
    if self.play_pipe:
      self.play_pipe.stop()

  def _play(self, pipe):
    self.error = None
    self.paused = False
    self.play_pipe = pipe
    self.play_thread = _start_thread(pipe.start, self.msgq)

  def _is_playing(self):
    if self.play_pipe is not None and self.play_pipe.is_started():
      return True
    else:
      return False

  def _is_stopping(self):
    if self.play_pipe is not None and self.play_pipe.is_stopping():
      return True
    else:
      return False

  def start(self):
    msgq = self.msgq
    nextpipe = None
    while True:
      m = msgq.get()
      if m == MSG_PLAYER_PLAY:
        if self.play_pipe is not None:
          nextpipe = msgq.get()
          self._stop()
        else:
          self._play(msgq.get())
      elif m == MSG_PLAYER_STOP:
         self._stop()
      elif m == MSG_PLAYER_PIPE_STOPPED:
        self.error = msgq.get()
        self.play_thread.join()
        cherrypy.log("PIPE STOPPED")
        if nextpipe is not None:
          self._play(nextpipe)
          nextpipe = None
        else:
          self.play_pipe = None
          self.play_thread = None
      elif m == MSG_PLAYER_QUIT:
        self._stop()
        break

  def quit(self):
    if self.main_thread is not None:
      self.msgq.put(MSG_PLAYER_QUIT)
      self.main_thread.join()

  def play(self, title, src, subs=None, http=False, dlsrv=True):
    if self.main_thread is None:
      self.main_thread = _start_thread(self.start)
    pipe = ProcessPipe(title)
    if subs is not None:
      pipe.add_process(SubtitlesProcess(subs))
    pipe.add_process(src)
    if not http:
      if dlsrv:
        pipe.add_process(DlsrvProcess())
        pipe.add_process(OmxplayerProcess2())
      else:
        pipe.add_process(OmxplayerProcess())
    else:
      pipe.add_process(OmxplayerProcess2())
    self.msgq.put(MSG_PLAYER_PLAY)
    self.msgq.put(pipe)

  def playYtdl(self, url, title=None, subs=None):
    if title is None:
      title = url
    http = ythelper.skip_download(url)
    self.play(title, YoutubeDlProcess(url), subs, http)

  def playRtmpdump(self, cmd, title):
    # Can't get itv to work with dlsrv
    self.play(title, RtmpProcess(cmd), dlsrv=False)

  def playTorrent(self, url, idx, title, subs):
    self.play(title, PeerflixProcess(url, idx), subs, True)

  def playLivestream(self, url, title):
    self.play(title, LivestreamerProcess(url), http=False, dlsrv=False)

  def status(self):
    play_pipe = self.play_pipe
    status  = {'State':ST_NOT_RUNNING, 'Msg':'', 'Title':'',
               'Paused':False, 'Error':False}

    if self.error is not None:
      status['Error'] = True
      status['Msg'] = self.error

    if play_pipe is None or self.error is not None:
      return status

    status['Title'] = play_pipe.status_msg()
    if self._is_playing():
      status['State'] = ST_RUNNING
    elif not self._is_stopping():
      status['State'] = ST_STARTING
    status['Paused'] = self.paused

    return status

  def control(self, action):
    if action == 'stop':
      self.msgq.put(MSG_PLAYER_STOP)
    elif self._is_playing():
      self.play_pipe.control(action)
      if action == 'pause' or action == 'resume':
        self.paused = not self.paused

Player = _Player()
