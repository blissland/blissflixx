from threading import Thread
import shutil
from common import *
import subprocess32 as subprocess
import time
import os
import cherrypy

_INPUT_TIMEOUT = 10

CMD = "omxplayer -b -r --timeout 100 -I --no-keys "

class OmxPlayer(PlayerProcess):
  def __init__(self):
    PlayerProcess.__init__(self, PROC_TARGET)

  def _wait_input(self, fname):
    for i in xrange(_INPUT_TIMEOUT):
      if os.path.isfile(fname):
        return True
      time.sleep(1)
    return False

  def run(self, msgq, fname, pid):
    self.msgq = msgq

    if fname.startswith('http'):
      cmd = CMD + "'" + fname + "'"
    else:
      if not self._wait_input(fname):
        self._error("Player timed out waiting for input file")
        return

      escname = fname.replace("$", "\$")
      tail = "tail -f --pid=" + str(pid) + " --bytes=+0 \"" + escname + "\""
      cmd = tail + ' | ' + CMD + 'pipe:0'

    # Wait a bit for input
    time.sleep(5)

    if not self._popen(cmd, shell=True):
      return

    try:
      if self._ready():
        self._send(MSG_TARGET_STARTED)
    except Exception, e: 
      self._error(str(e))

    self._wait()

  def _ready(self):
    cherrypy.log("WAITING FOR TARGET READY")
    while True:
      line = self.proc.stdout.readline()
      # process died
      if not line or line.startswith('have a nice day'):
       self._error("omxplayer failed to start")
       return False
      elif line.startswith('Vcodec id unknown:'):
       self._error("Unsupported video codec")
       return False
      elif "Metadata:" in line:
        return True
      elif "Duration:" in line:
        return True
      else:
        cherrypy.log("OMXPLAYER: " + line)

  def dbus(self, cmd):
    p = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dbus.sh")
    subprocess.call([p, cmd])

  def pause(self):
    self.dbus("pause")

  def resume(self):
    self.dbus("pause")
