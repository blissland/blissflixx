import random
import chanutils.reddit
import html
from datetime import time
from chanutils import get_json
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
_INFO_URL = "https://www.googleapis.com/youtube/v3/videos"

_YT_API_KEY = "AIzaSyBMibJZj9EHclomSio3etfmvrdWticfjwU"

_FEEDLIST = [
    {"title": "Trending", "url": "http://www.reddit.com/domain/youtube.com/top/.json"},
    {
        "title": "Popular",
        "url": _INFO_URL
        + "?maxResults=50&key="
        + _YT_API_KEY
        + "&part=snippet,contentDetails&chart=mostPopular",
    },
]


def name():
    return "Youtube"


def image():
    return "icon.png"


def description():
    return "Youtube Channel (<a target='_blank' href='https://www.youtube.com/'>https://www.youtube.com/</a>)."


def feedlist():
    return _FEEDLIST


def feed(idx):
    url = _FEEDLIST[idx]["url"]
    if url.endswith(".json"):
        return chanutils.reddit.get_feed(_FEEDLIST[idx])
    else:
        data = get_json(url)
        return _extract(data)


def search(q):
    query = {"part": "snippet", "q": q, "maxResults": 50, "key": _YT_API_KEY}
    data = get_json(_SEARCH_URL, params=query)
    add_duration(data)
    return _extract(data)


def add_duration(data):
    ids = []
    new_items = []
    data_items = data["items"]
    for item in data_items:
        if isinstance(item["id"], str):
            vid = item["id"]
        elif "videoId" in item["id"]:
            vid = item["id"]["videoId"]
        else:
            continue
        new_items.append(item)
        ids.append(vid)
    data["items"] = new_items
    query = {"part": "contentDetails", "key": _YT_API_KEY, "id": ",".join(ids)}
    info = get_json(_INFO_URL, query)
    for d, i in zip(data["items"], info["items"]):
        d["contentDetails"] = i["contentDetails"]
    return data


def _extract(data):
    results = PlayItemList()
    data_items = data["items"]
    for item in data_items:
        title = html.unescape(item["snippet"]["title"])
        if "contentDetails" in item:
            duration = item["contentDetails"]["duration"]
            subtitle = (
                chanutils.convert_duration(duration)
                + " - "
                + item["snippet"]["publishedAt"][:10]
            )
        else:
            subtitle = item["snippet"]["publishedAt"][:10]
        synopsis = item["snippet"]["description"]
        if len(synopsis) > 200:
            synopsis = synopsis[:200] + "..."
        try:
            img = item["snippet"]["thumbnails"]["default"]["url"]
        except KeyError:
            img = "/img/icons/film.svg"
        if isinstance(item["id"], str):
            vid = item["id"]
        elif "videoId" in item["id"]:
            vid = item["id"]["videoId"]
        else:
            continue
        url = "https://www.youtube.com/watch?v=" + vid
        results.add(PlayItem(title, img, url, subtitle, synopsis))
    return results
