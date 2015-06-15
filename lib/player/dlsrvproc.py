import cherrypy, locations, os
from processpipe import ExternalProcess, ProcessException

DLSRV_PATH = os.path.join(locations.BIN_PATH, "dlsrv")
_DLSRV_PORT = "9696"

class DlsrvProcess(ExternalProcess):

  def __init__(self):
    ExternalProcess.__init__(self)

  def name(self):
    return 'dlsrv'

  def _get_cmd(self, args):
    self.args = args
    cmd = [DLSRV_PATH, args['outfile']]
    if 'pid' in args:
      cmd.append(unicode(args['pid']))
    return cmd

  def _ready(self):
    while True:
      line = self._readline()
      if line.startswith("Listening"):
	self.args['outfile'] = 'http://127.0.0.1:' + _DLSRV_PORT
        return self.args
      else:
        raise ProcessException(line)
