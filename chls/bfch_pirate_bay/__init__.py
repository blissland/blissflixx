import chanutils.torrent, urllib.request, urllib.parse, urllib.error
from chanutils import get_doc, get_json, select_all, select_one, get_attr
from chanutils import get_text, get_text_content, replace_entity, byte_size
from chanutils import movie_title_year, series_season_episode
from playitem import TorrentPlayItem, PlayItemList

_SEARCH_URL = "https://thepiratebay0.org/search/%s/0/99/100,200"

_FEEDLIST = [
    {"title": "Movies", "url": "https://thepiratebay0.org/top/201"},
    {"title": "HD - Movies", "url": "https://thepiratebay0.org/top/207"},
    {"title": "TV Shows", "url": "https://thepiratebay0.org/top/205"},
    {"title": "HD - TV Shows", "url": "https://thepiratebay0.org/top/208"},
    {"title": "Music", "url": "https://thepiratebay0.org/top/101"},
    {"title": "FLAC", "url": "https://thepiratebay0.org/top/104"},
    {"title": "Audio Books", "url": "https://thepiratebay0.org/top/102"},
]


def name():
    return "Pirate Bay"


def image():
    return "icon.png"


def description():
    return "The Pirate Bay Channel (<a target='_blank' href='https://thepiratebay0.org'>https://thepiratebay0.org</a>)."


def feedlist():
    return _FEEDLIST


def feed(idx):
    doc = get_doc(_FEEDLIST[idx]["url"])
    return _extract(doc)


def search(q):
    url = _SEARCH_URL % urllib.parse.quote(q.encode("utf8"))
    doc = get_doc(url)
    return _extract(doc)


def _extract(doc):
    results = PlayItemList()
    rtree = select_all(doc, "tr")
    for l in rtree[1:]:  # skip the header row
        el = select_one(l, "a[title='More from this category']")
        maincat = get_text(el)
        img = "/img/icons/film.svg"
        if maincat is not None:
            if maincat == "Video":
                img = "/img/icons/film.svg"
            elif maincat == "Audio":
                img = "/img/icons/music.svg"
            else:
                continue
        else:
            continue
        el = select_one(l, "a.detLink")
        title = get_text(el)
        el = select_one(l, "a[title='Download this torrent using magnet']")
        url = get_attr(el, "href")
        el = select_one(l, "font.detDesc")
        desc = get_text(el)
        start = desc.find("Uploaded")
        if start == -1:
            continue
        start = start + 8
        end = desc.find(",", start)
        if end == -1:
            continue
        uploaded = desc[start:end]
        start = desc.find(", Size ")
        if start == -1:
            continue
        start = start + 7
        end = desc.find(",", start)
        if end == -1:
            continue
        size = desc[start:end].replace("iB", "B")
        el = select_one(l, "td:nth-child(3)")
        seeds = get_text(el)
        el = select_one(l, "td:nth-child(4)")
        peers = get_text(el)
        subtitle = _subtitle(
            {"Uploaded": uploaded, "Size": size, "Seeds": seeds, "Peers": peers}
        )
        subcat = "Movies"
        el = select_one(l, ":nth-child(3)")
        if el.text and not el.text.isspace():
            subcat = get_text(el)
        subs = None
        if subcat.endswith("Movies"):
            subs = movie_title_year(title)
        elif subcat.endswith("shows"):
            subs = series_season_episode(title)
        if not url:
            continue
        results.add(TorrentPlayItem(title, img, url, subtitle, subs=subs))
    return results


def _subtitle(dict):
    return ", ".join(
        ["%s: %s" % (key, str(value)) for (key, value) in list(dict.items())]
    )
