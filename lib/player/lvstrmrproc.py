from processpipe import ExternalProcess, ProcessException, OUT_FILE
import cherrypy

class LivestreamerProcess(ExternalProcess):
  _START_TIMEOUT = 5

  def __init__(self, url, quality='best'):
    ExternalProcess.__init__(self)
    cmd = [
      'livestreamer',
      url,
      quality,
      '--http-header',
      'Client-ID=tq6hq1srip0i37ipzuscegt7viex9fh',
      '--output',
      OUT_FILE,
      '--player-fifo'
    ]
    self.cmd = cmd 

  def name(self):
    return 'livestreamer'

  def _get_cmd(self, args):
    self.args = args
    return self.cmd

  def _ready(self):
    while True:
      #line = self._readline(self._START_TIMEOUT)
      # Twitch with timeout does not work for me 
      line = self._readline()
      if line.startswith('error: No streams found on this URL'):
        raise ProcessException("No stream currently available at this URL")
      elif "Opening stream: source" in line:
        return {'pid':self.proc.pid, 'outfile':OUT_FILE}
