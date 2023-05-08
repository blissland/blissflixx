from chanutils import get_json
from pprint import pp
from playitem import PlayItemList, PlayItem

_API = {
    "channels": "https://iptv-org.github.io/api/channels.json",
    "streams": "https://iptv-org.github.io/api/streams.json",
    "categories": "https://iptv-org.github.io/api/categories.json",
    "languages": "https://iptv-org.github.io/api/languages.json",
    "countries": "https://iptv-org.github.io/api/countries.json",
}
_FEEDLIST = [
    {"title": "Colombia", "filter": {"country": "CO"}},
    {"title": "Great Britain", "filter": {"country": "UK"}},
    {"title": "China", "filter": {"country": "CN"}},
    {"title": "India", "filter": {"country": "IN"}},
    {"title": "Indonesia", "filter": {"country": "ID"}},
    {"title": "Pakistan", "filter": {"country": "PK"}},
    {"title": "Nigeria", "filter": {"country": "NG"}},
    {"title": "Brazil", "filter": {"country": "BR"}},
    {"title": "Bangladesh", "filter": {"country": "BD"}},
    {"title": "Russia", "filter": {"country": "RU"}},
    {"title": "Mexico", "filter": {"country": "MX"}},
    {"title": "United States", "filter": {"country": "US"}},
    {"title": "Spanish", "filter": {"language": "spa"}},
    {"title": "English", "filter": {"language": "eng"}},
    {"title": "French", "filter": {"language": "fra"}},
    {"title": "German", "filter": {"language": "deu"}},
    {"title": "Japanese", "filter": {"language": "jpn"}},
    {"title": "Portuguese", "filter": {"language": "por"}},
    {"title": "NSFW", "filter": {"nsfw": True}},
]
_MAXRESULTS = 300


def name():
    return "/iptv-org"


def image():
    return "icon.png"


def description():
    return "Collection of publicly available IPTV channels from all over the world (<a target='_blank' href='https://iptv-org.github.io/'>https://iptv-org.github.io/</a>). IPTV = Internet Protocol TeleVision."


def feedlist():
    return _FEEDLIST


def load_all_streams():
    """link each of the streams with it's corresponding channel"""
    streams = get_json(_API["streams"])
    channels = get_json(_API["channels"])
    channels_idx = {ch["id"]: ch for ch in channels}
    num_channels_added = 0
    for stream in streams:
        if stream["channel"] and stream["channel"] in channels_idx:
            stream["channel_info"] = channels_idx[stream["channel"]]
            num_channels_added += 1
    return streams


def feed(idx):
    streams = load_all_streams()
    filter = _FEEDLIST[idx]["filter"]
    data = []
    if "country" in filter:
        data = [
            s
            for s in streams
            if "channel_info" in s and s["channel_info"]["country"] == filter["country"]
        ]
    elif "language" in filter:
        data = [
            s
            for s in streams
            if "channel_info" in s
            and filter["language"] in s["channel_info"]["languages"]
        ]
    elif "nsfw" in filter:
        data = [
            s for s in streams if "channel_info" in s and s["channel_info"]["is_nsfw"]
        ]
    return _extract(data[:_MAXRESULTS])


def search(q):
    streams = load_all_streams()
    result = [
        s
        for s in streams
        if "channel_info" in s and q.lower() in s["channel_info"]["name"].lower()
    ]
    return _extract(result[:_MAXRESULTS])


def _extract(data):
    results = PlayItemList()
    for stream in data:
        info = stream["channel_info"]
        title = info["name"]
        thumb = info["logo"]
        url = stream["url"]
        subtitle_strings = []
        if "width" in stream and "height" in stream:
            subtitle_strings.append(
                f"size: <b>{stream['width']}x{stream['height']}</b>"
            )
        if "city" in info and info["city"]:
            subtitle_strings.append(f"city: <b>{info['city']}</b>")
        if "country" in info:
            subtitle_strings.append(f"country: <b>{info['country']}</b>")
        if "languages" in info:
            subtitle_strings.append(f"languages: <b>{' '.join(info['languages'])}</b>")
        if "categories" in info and info["categories"]:
            subtitle_strings.append(
                f"categories: <b>{' '.join(info['categories'])}</b>"
            )
        subtitle = " - ".join(subtitle_strings)
        item = PlayItem(title, thumb, url, subtitle)
        results.add(item)
    return results
