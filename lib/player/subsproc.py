import cherrypy, locations, os, json
from processpipe import ExternalProcess, ProcessException

MSUBS_PATH = os.path.join(locations.BIN_PATH, "moviesubs.py")
ESUBS_PATH = os.path.join(locations.BIN_PATH, "episubs.py")

class SubtitlesProcess(ExternalProcess):

  def __init__(self, subs):
    ExternalProcess.__init__(self)
    self.subs = subs
    self.subsfile = None

  def status_msg(self):
    return "FETCHING SUBTITLES"

  def name(self):
    return 'subtitles'

  def _get_cmd(self, args):
    if 'series' in self.subs:
      cmd = [ESUBS_PATH, self.subs['lang'], self.subs['series'],
            self.subs['season'], self.subs['episode']]
    else:
      cmd = [MSUBS_PATH, self.subs['lang'], self.subs['title']]
      if 'year' in self.subs and self.subs['year']:
        cmd.append(self.subs['year'])
    return cmd

  def _ready(self):
    while True:
      line = self._readline()
      if line.startswith("{"):
        obj = json.loads(line)
        if 'filename' in obj:
          self.subsfile = obj['filename']
          return {'subtitles':self.subsfile}
        else:
          raise ProcessException('No subtitles found')

  def stop(self):
    if self.subsfile is not None and os.path.exists(self.subsfile):
      try:
        os.remove(self.subsfile)
      except Exception:
        pass
    ExternalProcess.stop(self)
