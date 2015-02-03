from multiprocessing import Process, Pipe
from common import *
import youtube_dl
import os
import json

class Logger(object):

  def __init__(self, pipe):
    self.pipe = pipe

  def debug(self, msg):
    print("DEBUG: " + msg)
    if msg.startswith("[download] Destination:"):
      self.pipe.send([MSG_SOURCE_READY, msg[24:]])
    elif msg.startswith("{"):
      obj = json.loads(msg)
      self.pipe.send([MSG_SOURCE_READY, obj['url']])

  def error(self, msg):
    print("ERROR: " + msg)
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

    self.pipe.send([MSG_SOURCE_ERROR, msg])

  def warning(self, msg):
    print("WARNING: " + msg)

class YoutubeDlSource(object):

  def __init__(self, url, title, skipdl=False):
    self.url = url
    self._title = title
    self._skipdl = skipdl
    self.halted = False
    self.filename = None

  def title(self):
    return self._title

  def stop(self):
    self.halted = True
    if self.proc:
      # Stop gets called from a seperate thread 
      # so shutdown may already be in progress
      # when we try to kill - therefore ignore errors
      try:
        self.proc.terminate()
      except Exception, e:
        pass
    else:
      self._stopped()

  def _stopped(self):
    # Only send a stopped message from source if player forced a stop
    # or due to an error not if the source just stops au natural
    if self.halted:
      if self.filename and not self._skipdl:
        try:
          os.remove(self.filename)
        except Exception:
          pass
      self._send(MSG_SOURCE_STOPPED)

  def run(self, msgq):
    self.msgq = msgq
    parent_conn, child_conn = Pipe()

    self._send(MSG_PLAYER_MSG)
    self._send("LOADING STREAM...")

    self.proc = Process(target=self._runproc, args=(self.url, child_conn))
    self.proc.start()
    msg = parent_conn.recv()
    if msg[0] == MSG_SOURCE_READY:
      self.filename = msg[1]
      self._send(msg[0])
      self._send(msg[1])
      self._send(self.proc.pid)
    elif msg[0] == MSG_SOURCE_ERROR:
      self.halted = True
      self._send(msg[0])
      self._send(msg[1])

    self.proc.join()
    if self.proc.exitcode != 0:
      self.halted = True
    self.proc = None
    self._stopped()

  def _runproc(self, url, pipe):
    ydl_opts = {'nopart': True, 'continuedl': False, 'noplaylist': True,
                'noprogress': True, 'logger': Logger(pipe), 'max_downloads': 1,
                'outtmpl': '/tmp/blissflixx/%(title)s'}
    if self._skipdl:
      ydl_opts['simulate'] = True
      ydl_opts['dump_single_json'] = True
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    try:
      ydl.download([url])
    except Exception:
      # Errors are captured by logger
      pass
    except KeyboardInterrupt:
      pass

  def _send(self, msg):
    self.msgq.put(msg)

