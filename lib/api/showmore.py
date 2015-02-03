import channels
from common import ApiError, add_playlist

def showmore(chid=None, link=None):
  if (chid is None) or (link is None):
    raise ApiError("Both channel ID and link must be defined")
  ch = channls.get(chid)
  if not ch:
    raise ApiError("Unknown channel ID")
  results = ch.showmore(link)
  return add_playlist(results)
