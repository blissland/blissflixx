from threading import Thread
import shutil
import os, grp
import signal
import subprocess32 as subprocess
import cherrypy, select

MSG_PLAYER_PLAY = 1
MSG_PLAYER_MSG = 2
MSG_PLAYER_QUIT = 3

MSG_SOURCE_ERROR = 100
MSG_SOURCE_READY = 101 
MSG_SOURCE_STOPPED = 102

MSG_TARGET_ERROR = 200
MSG_TARGET_STARTED = 201
MSG_TARGET_STOPPED = 202

PROC_SOURCE = 1
PROC_TARGET = 2

class _DiscardFile(object):
  def write(self, *args):
    pass
  def close(self):
    pass

def _copypipe(src, dest):
  if not dest:
    dest = _DiscardFile()

  # Ignore broken pipe errors if process
  # are forced to stop
  try:
    shutil.copyfileobj(src, dest)
  except Exception:
    pass

  src.close()
  dest.close()

def bgcopypipe(src, dest):
  th = Thread(target=_copypipe, args=(src, dest))
  th.start()

class PlayerProcess(object):
  def __init__(self, ptype):
    self.ptype = ptype
    self.halted = False
    self.proc = None

  def stop(self):
    self.halted = True
    if self.proc is not None:
      # Stop gets called from a seperate thread 
      # so shutdown may already be in progress
      # when we try to kill - therefore ignore errors
      try:
        # kill - including all children of process
        os.killpg(self.proc.pid, signal.SIGKILL)
	if self.ptype == PROC_SOURCE:
	  cherrypy.log("KILLED SOURCE PROC")
        else:
	  cherrypy.log("KILLED OMXPLAYER")
      except Exception, e:
        cherrypy.log("GOT SOURCE STOP EXCEPTION:" + str(e))
    else:
      self._stopped() 

  def _stopped(self):
    if self.ptype == PROC_SOURCE:
      # Only send a stopped message from source if player forced a stop
      # or due to an error not if the source just stops au natural
      if self.halted:
        self._send(MSG_SOURCE_STOPPED)
    else:
      self._send(MSG_TARGET_STOPPED)

  def _popen(self, cmd, shell=False):
    try:
      # preexec_fn=os.setsid required to allow killing of process children
      if self.ptype == PROC_SOURCE:
        # Stderr redirected to stdout
        self.proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=shell)
      else:
        # Stderr redirected to stdout
        self.proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid, shell=shell)
      return True
    except Exception, e: 
      self._error(str(e))
      self._stopped()
      return False

  def _wait(self):
    # Drain stderr/stdout pipe to stop it filling up and blocking process
    bgcopypipe(self.proc.stdout, None)

    retcode = self.proc.wait()
    if retcode != 0:
      self.halted = True

    self.proc = None
    self._stopped()

  def _send(self, msg):
    self.msgq.put(msg)

  def _error(self, emsg):
    if self.ptype == PROC_SOURCE:
      self._send(MSG_SOURCE_ERROR)
    else:
      self._send(MSG_TARGET_ERROR)
    self._send(emsg)

  def _readline(self, timeout=None):
    poll_obj = select.poll()
    poll_obj.register(self.proc.stdout, select.POLLIN) 
    while self.proc.poll() is None:
      if timeout is not None:
        poll_result = poll_obj.poll(1000 * timeout)
        if not poll_result:
          return "timeout"
      line = self.proc.stdout.readline()
      # process died
      if not line:
        return None
      line = line.strip()
      if line.strip() != '':
        return line
    return None

