import playitem, chanutils.torrent
import chanutils
from .common import ApiError

MAX_TITLE_LEN = 100


def item(link=None):
    if not link:
        raise ApiError("Item URL must be defined")
    results = playitem.PlayItemList()
    if link.lower().startswith("http"):
        title = chanutils.get_html_title(link)
    else:
        title = link
    if len(title) > MAX_TITLE_LEN:
        title = title[:MAX_TITLE_LEN] + "..."
    lowercase_link = link.lower()
    subtitle = None
    if "youtube.com/" in lowercase_link or "youtu.be/" in lowercase_link:
        subtitle = chanutils.get_youtube_video_length_from_url(link)
    img = "/img/icons/file-o.svg"
    if chanutils.torrent.is_torrent(link):
        link = chanutils.torrent.set_torridx(link)
    results.add(playitem.PlayItem(title, img, link, subtitle=subtitle, subs={}))
    return results.to_dict()
