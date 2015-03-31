import chanutils.torrent, shutil
from processpipe import ExternalProcess, ProcessException

_PEERFLIX_PORT = "9696"

class PeerflixProcess(ExternalProcess):

  def __init__(self, torrent, idx):
    ExternalProcess.__init__(self)
    cmd = ["node", "--max-old-space-size=128",
            "/usr/local/bin/peerflix"]
    # Avoid problems with downloading torrent files
    torrent = chanutils.torrent.torrent2magnet(torrent)
    cmd.append(torrent)
    cmd.append("-q")
    cmd.append("-r")
    cmd.append("-p")
    cmd.append(_PEERFLIX_PORT)
    if idx is not None and idx >= 0:
      cmd.append("-i")
      cmd.append(str(idx))
    self.cmd = cmd 

  def name(self):
    return 'peerflix'

  def _get_cmd(self, args):
    self.args = args
    return self.cmd

  def _ready(self):
    while True:
      line = self._readline()
      if line.startswith('Bad Response'):
        raise ProcessException(line)
      # Get this error if site down/blocked
      # html page instead of torrent
      elif line.startswith('not a colon at'):
        raise ProcessException("Unable to retrieve torrent")
      elif line.startswith('server is listening'):
        self.args['outfile'] = 'http://127.0.0.1:' + _PEERFLIX_PORT
        return self.args

  def stop(self):
    try:
      shutil.rmtree('/tmp/torrent-stream')
    except Exception:
      pass
    ExternalProcess.stop(self)
