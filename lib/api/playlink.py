import playitem, chanutils.torrent
import chanutils
from .common import ApiError

MAX_TITLE_LEN = 100


def item(link=None):
    if not link:
        raise ApiError("Item URL must be defined")
    info = chanutils.UrlInfo(link)
    results = playitem.PlayItemList()
    if link.lower().startswith("http"):
        title = info.get_html_title()
    else:
        title = link
    if len(title) > MAX_TITLE_LEN:
        title = title[:MAX_TITLE_LEN] + "..."
    lowercase_link = link.lower()
    subtitle = None
    img = "/img/icons/file-o.svg"
    synopsis = None
    if "youtube.com/" in lowercase_link or "youtu.be/" in lowercase_link:
        subtitle = (
            info.get_youtube_video_length_from_url()
            + " - "
            + info.get_youtube_video_publish_date_from_url()
        )
        img = info.get_youtube_video_thumbnail_from_url()
        synopsis = info.get_youtube_video_description_from_url()
    if chanutils.torrent.is_torrent(link):
        link = chanutils.torrent.set_torridx(link)
    results.add(
        playitem.PlayItem(
            title, img, link, subtitle=subtitle, synopsis=synopsis, subs={}
        )
    )
    return results.to_dict()
