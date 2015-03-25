import cherrypy
from processpipe import ExternalProcess, OUT_FILE

class RtmpProcess(ExternalProcess):

  def __init__(self, cmd):
    ExternalProcess.__init__(self)
    cmd.insert(0, 'rtmpdump')
    cmd.append('-o')
    cmd.append(OUT_FILE)
    self.cmd = cmd

  def name(self):
    return 'rtmpdump'

  def _get_cmd(self, args):
    return self.cmd

  def _ready(self):
    while True:
      line = self._readline()
      if line.startswith('Starting download at:'):
        return {'pid':self.proc.pid, 'outfile':OUT_FILE}
      else:
        cherrypy.log("RTMPDUMP: " + line)
