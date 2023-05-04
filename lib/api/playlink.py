import playitem, chanutils.torrent
import chanutils
from .common import ApiError

MAX_TITLE_LEN = 100

def item(link=None):
    if not link:
        raise ApiError("Item URL must be defined")
    results = playitem.PlayItemList()
    if link.lower().startswith('http'):
        title = chanutils.get_html_title(link)
    else:
        title = link
    if len(title) > MAX_TITLE_LEN:
        title = title[:MAX_TITLE_LEN] + "..."
    img = "/img/icons/file-o.svg"
    if chanutils.torrent.is_torrent(link):
        link = chanutils.torrent.set_torridx(link)
    results.add(playitem.PlayItem(title, img, link, subs={}))
    return results.to_dict()
