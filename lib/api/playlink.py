import playitem, chanutils.torrent
from common import ApiError

def item(link=None):
  if not link:
    raise APIError("Item URL must be defined")
  results = playitem.PlayItemList()
  title = link
  if len(title) > 30:
    title = title[:30] + "..."
  img = '/img/icons/file-o.svg'
  if chanutils.torrent.is_torrent(link):
    link = chanutils.torrent.set_torridx(link)
  results.add(playitem.PlayItem(title, img, link))
  return results.to_dict()
