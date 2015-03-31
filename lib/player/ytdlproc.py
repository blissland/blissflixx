import cherrypy, locations, os, ythelper, json
from processpipe import ExternalProcess, ProcessException, OUT_FILE

YTDL_PATH = os.path.join(locations.YTUBE_PATH, "youtube_dl")
YTDL_PATH = os.path.join(YTDL_PATH, "__main__.py")

class YoutubeDlProcess(ExternalProcess):

  def __init__(self, url):
    ExternalProcess.__init__(self)
    self.url = url

  def name(self):
    return 'youtube-dl'

  def _get_cmd(self, args):
    self.args = args
    cmd = [YTDL_PATH, "--no-part", "--no-continue", "--no-playlist", 
           "--max-downloads", "1", "--no-progress", "--output", OUT_FILE]

    if ythelper.skip_download(self.url):
      cmd.append("--simulate")
      cmd.append("--dump-single-json")

    fmat = ythelper.get_format(self.url)
    if fmat is not None:
      cmd.append("--format")
      cmd.append(fmat)

    cmd.append(self.url)
    return cmd

  def _ready(self):
    self.args['pid'] = self.proc.pid
    while True:
      line = self._readline()
      if line.startswith("[download] Destination:"):
        self.args['outfile'] = OUT_FILE
        return self.args
      elif line.startswith("{"):
        obj = json.loads(line)
        self.args['outfile'] = obj['url']
        return self.args
      elif line.startswith("ERROR:"):
        raise ProcessException(self._get_ytdl_err(line[7:]))

  def _get_ytdl_err(self, msg):
    if msg.strip() == "":
      return
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

    return msg

