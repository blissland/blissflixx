from chanutils import get_json
from playitem import PlayItem, PlayItemList
from datetime import timedelta

_TRACKS_URL = "https://api-v2.soundcloud.com/charts?kind=top&genre={genre}&client_id={client_id}&limit={limit}"
_SEARCH_URL = (
    "https://api-v2.soundcloud.com/search?q={query}&client_id={client_id}&limit={limit}"
)
_CLIENT_ID = "08f79801a998c381762ec5b15e4914d5"

_GENRES = [
    {"genre": "soundcloud:genres:all-music", "title": "All music genres"},
    {"genre": "soundcloud:genres:all-audio", "title": "All audio genres"},
    {"genre": "soundcloud:genres:alternativerock", "title": "Alternative Rock"},
    {"genre": "soundcloud:genres:ambient", "title": "Ambient"},
    {"genre": "soundcloud:genres:classical", "title": "Classical"},
    {"genre": "soundcloud:genres:country", "title": "Country"},
    {"genre": "soundcloud:genres:danceedm", "title": "Dance & EDM"},
    {"genre": "soundcloud:genres:dancehall", "title": "Dancehall"},
    {"genre": "soundcloud:genres:deephouse", "title": "Deep House"},
    {"genre": "soundcloud:genres:disco", "title": "Disco"},
    {"genre": "soundcloud:genres:drumbass", "title": "Drum & Bass"},
    {"genre": "soundcloud:genres:dubstep", "title": "Dubstep"},
    {"genre": "soundcloud:genres:electronic", "title": "Electronic"},
    {
        "genre": "soundcloud:genres:folksingersongwriter",
        "title": "Folk & Singer-Songwriter",
    },
    {"genre": "soundcloud:genres:hiphoprap", "title": "Hip-hop & Rap"},
    {"genre": "soundcloud:genres:house", "title": "House"},
    {"genre": "soundcloud:genres:indie", "title": "Indie"},
    {"genre": "soundcloud:genres:jazzblues", "title": "Jazz & Blues"},
    {"genre": "soundcloud:genres:latin", "title": "Latin"},
    {"genre": "soundcloud:genres:metal", "title": "Metal"},
    {"genre": "soundcloud:genres:piano", "title": "Piano"},
    {"genre": "soundcloud:genres:pop", "title": "Pop"},
    {"genre": "soundcloud:genres:rbsoul", "title": "R&B & Soul"},
    {"genre": "soundcloud:genres:reggae", "title": "Reggae"},
    {"genre": "soundcloud:genres:reggaeton", "title": "Reggaeton"},
    {"genre": "soundcloud:genres:rock", "title": "Rock"},
    {"genre": "soundcloud:genres:soundtrack", "title": "Soundtrack"},
    {"genre": "soundcloud:genres:techno", "title": "Techno"},
    {"genre": "soundcloud:genres:trance", "title": "Trance"},
    {"genre": "soundcloud:genres:trap", "title": "Trap"},
    {"genre": "soundcloud:genres:triphop", "title": "Triphop"},
    {"genre": "soundcloud:genres:world", "title": "World"},
    {"genre": "soundcloud:genres:audiobooks", "title": "Audiobooks"},
    {"genre": "soundcloud:genres:business", "title": "Business"},
    {"genre": "soundcloud:genres:comedy", "title": "Comedy"},
    {"genre": "soundcloud:genres:entertainment", "title": "Entertainment"},
    {"genre": "soundcloud:genres:learning", "title": "Learning"},
    {"genre": "soundcloud:genres:newspolitics", "title": "News & Politics"},
    {
        "genre": "soundcloud:genres:religionspirituality",
        "title": "Religion & Spirituality",
    },
    {"genre": "soundcloud:genres:science", "title": "Science"},
    {"genre": "soundcloud:genres:sports", "title": "Sports"},
    {"genre": "soundcloud:genres:storytelling", "title": "Storytelling"},
    {"genre": "soundcloud:genres:technology", "title": "Technology"},
]


def name():
    return "SoundCloud"


def image():
    return "icon.png"


def description():
    return "SoundCloud Channel (<a target='_blank' href='https://soundcloud.com/'>https://soundcloud.com/</a>)."


def feedlist():
    return _GENRES


def feed(idx):
    genre = feedlist()[idx]["genre"]
    url = _TRACKS_URL.format(genre=genre, client_id=_CLIENT_ID, limit=50)
    tracks = get_json(url)["collection"]
    return _extract(tracks)


def search(q):
    url = _SEARCH_URL.format(query=q, client_id=_CLIENT_ID, limit=50)
    tracks = get_json(url)["collection"]
    return _extract_search(tracks)


def human_format(num):
    if not num:
        return "0"
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


def _extract(tracks_json):
    results = PlayItemList()
    for t in tracks_json:
        track = t["track"]
        title = track["title"]
        user = track["user"]["username"]
        if track["duration"] != track["full_duration"]:
            continue
        duration_s = track["duration"] // 1000
        duration = str(timedelta(seconds=duration_s))
        plays = (
            "this week: "
            + human_format(t["score"])
            + " all time: "
            + human_format(track["playback_count"])
        )
        subtitle = user + "<br/>duration: " + duration + " plays: " + plays
        if track["artwork_url"] and track["artwork_url"] != "":
            img = track["artwork_url"].replace("-large.", "-t300x300.")
        elif track["user"]["avatar_url"] and track["user"]["avatar_url"] != "":
            img = track["user"]["avatar_url"].replace("-large.", "-t300x300.")
        else:
            img = "/img/icons/music.svg"
        url = track["permalink_url"]
        results.add(PlayItem(title, img, url, subtitle))
    return results


def _extract_search(search_json):
    results = PlayItemList()
    for track in search_json:
        kind = track["kind"]
        if kind != "track":
            continue
        title = track["title"]
        user = track["user"]["username"]
        if track["duration"] != track["full_duration"]:
            continue
        duration_s = track["duration"] // 1000
        duration = str(timedelta(seconds=duration_s))
        plays = (
            "likes: "
            + human_format(track["likes_count"])
            + " plays: "
            + human_format(track["playback_count"])
        )
        subtitle = user + "<br/> duration: " + duration + " " + plays
        if track["artwork_url"] and track["artwork_url"] != "":
            img = track["artwork_url"].replace("-large.", "-t300x300.")
        elif track["user"]["avatar_url"] and track["user"]["avatar_url"] != "":
            img = track["user"]["avatar_url"].replace("-large.", "-t300x300.")
        else:
            img = "/img/icons/music.svg"
        url = track["permalink_url"]
        results.add(PlayItem(title, img, url, subtitle))
    return results
