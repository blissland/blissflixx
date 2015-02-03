from common import ApiError, add_playlist
from chanutils.torrent import showmore

def files(link=None):
  if not link:
    raise APIError("Torrent URL must be defined")
  results = showmore(link)
  return add_playlist(results)

