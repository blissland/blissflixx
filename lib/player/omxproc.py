import os, time
from processpipe import ExternalProcess, ProcessException

OMX_CMD = "omxplayer -b --timeout 120 -I --no-keys "
_INPUT_TIMEOUT = 10
_START_TIMEOUT = 120

class OmxplayerProcess(ExternalProcess):

  def __init__(self):
    ExternalProcess.__init__(self, True)

  def _get_cmd(self, args):
     return self.cmd

  def name(self):
    return 'omxplayer'

  def _wait_input(self, fname):
    for i in xrange(_INPUT_TIMEOUT):
      if os.path.isfile(fname):
        return True
      time.sleep(1)
    return False

  def start(self, args):
    self.cmd = OMX_CMD
    if 'subtitles' in args:
      self.cmd = self.cmd + "--subtitles '" + args['subtitles'] + "' "
    fname = args['outfile']
    if fname.startswith('http'):
      self.cmd = self.cmd + "'" + fname + "'"
    elif not self._wait_input(fname):
        self._set_error("Omxplayer timed out waiting for input file")
        self.msg_halted()
        return
    else:
      pid = args['pid']
      tail = "tail -f --pid=" + str(pid) + " --bytes=+0 \"" + fname + "\""
      self.cmd = tail + ' | ' + self.cmd + 'pipe:0'
      # Wait a bit for input
      time.sleep(5)

    ExternalProcess.start(self, args)

  def _ready(self):
    while True:
      line = self._readline(_START_TIMEOUT)
      if line.startswith('have a nice day'):
        raise ProcessException("omxplayer failed to start")
      elif line.startswith('Vcodec id unknown:'):
        raise ProcessException("Unsupported video codec")
      elif "Metadata:" in line:
        break
      elif "Duration:" in line:
        break
