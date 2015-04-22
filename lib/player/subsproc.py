import cherrypy, locations, os, json
from processpipe import ExternalProcess, ProcessException

GETSUBS_PATH = os.path.join(locations.BIN_PATH, "getsubs.py")

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
    cmd = [GETSUBS_PATH, self.subs['lang']]
    if 'series' in self.subs:
      cmd = cmd + ['-t', self.subs['series']]
      cmd = cmd + ['-s', self.subs['season']]
      cmd = cmd + ['-e', self.subs['episode']]
    else:
      cmd = cmd + ['-t', self.subs['title']]
      if 'year' in self.subs and self.subs['year']:
        cmd = cmd + ['-y', self.subs['year']]
      if 'imdb' in self.subs and self.subs['imdb']:
        cmd = cmd + ['-i', self.subs['imdb']]
    return cmd

  def _ready(self):
    while True:
      line = self._readline()
      if line.startswith("{"):
        obj = json.loads(line)
        if 'filename' in obj:
          self.subsfile = obj['filename']
          return {'subtitles':self.subsfile}
        elif 'error' in obj:
          raise ProcessException(obj['error'])
        else:
          raise ProcessException('No subtitles found')

  def stop(self):
    if self.subsfile is not None and os.path.exists(self.subsfile):
      try:
        os.remove(self.subsfile)
      except Exception:
        pass
    ExternalProcess.stop(self)
