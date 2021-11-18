import chanutils.reddit
from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList
from urllib.parse import quote

_SEARCH_URL = "https://www.tmz.com/search/videos/"

_FEEDLIST = [
    {"title": "Beauty", "url": "http://www.tmz.com/categories/beauty/videos/"},
    {
        "title": "Celeb Justice",
        "url": "http://www.tmz.com/categories/celebrity-justice/videos/",
    },
    {"title": "Dating", "url": "http://www.tmz.com/categories/dating/videos/"},
    {"title": "Family", "url": "http://www.tmz.com/categories/family/videos/"},
    {"title": "Fashion", "url": "http://www.tmz.com/categories/fashion/videos/"},
    {"title": "Fights", "url": "http://www.tmz.com/categories/fights/videos/"},
    {"title": "Hook Ups", "url": "http://www.tmz.com/categories/hook-ups/videos/"},
    {"title": "LGBT", "url": "http://www.tmz.com/categories/lgbt/videos/"},
    {"title": "Money", "url": "http://www.tmz.com/categories/money/videos/"},
    {"title": "Movies", "url": "http://www.tmz.com/categories/movies/videos/"},
    {"title": "Music", "url": "http://www.tmz.com/categories/music/videos/"},
    {
        "title": "Relationships",
        "url": "http://www.tmz.com/categories/relationships/videos/",
    },
    {"title": "Sex", "url": "http://www.tmz.com/categories/sex/videos/"},
    {"title": "Sports", "url": "http://www.tmz.com/categories/tmzsports/videos/"},
    {"title": "Television", "url": "http://www.tmz.com/categories/tv/videos/"},
    {"title": "Vacations", "url": "http://www.tmz.com/categories/vacations/videos/"},
]


def name():
    return "TMZ"


def image():
    return "icon.png"


def description():
    return "TMZ Channel (<a target='_blank' href='https://www.tmz.com/'>https://www.tmz.com/</a>)."


def feedlist():
    return _FEEDLIST


def feed(idx):
    doc = get_doc(_FEEDLIST[idx]["url"])
    return _extract(doc)


def search(q):
    doc = get_doc(_SEARCH_URL + "?q=" + quote(q))
    return _extract(doc)


def _extract(doc):
    results = PlayItemList()
    rtree = select_all(doc, "div.col")
    for r in rtree:
        el = select_one(r, "h4")
        title = get_text(el)
        if not title:
            continue
        el = select_one(r, "img")
        img = get_attr(el, "src")
        el = select_one(r, "a.js-click-video")
        url = get_attr(el, "href")
        results.add(PlayItem(title, img, url))
    return results
