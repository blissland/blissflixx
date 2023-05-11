from chanutils import post_json, get_json
from playitem import LiveStreamPlayItem, PlayItemList

_CLIENT_ID = "yicd1x2uyr" + "hazbdc4n7zba4yzrjlx0"
_CLIENT_SECRET = "9dbytqxr6vpza42wexs1zjx" + "2cmjq56"
_TOP_GAMES_URL = "https://api.twitch.tv/helix/games/top"
_STREAM_URL = "https://api.twitch.tv/helix/streams"
_SEARCH_URL = "https://api.twitch.tv/helix/search/channels"
_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
__access_headers = dict()


def get_acccess_token():
    global __access_headers
    response = post_json(
        _TOKEN_URL,
        {
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    access_token = response["access_token"]
    __access_headers = {
        "Authorization": "Bearer " + access_token,
        "Client-Id": _CLIENT_ID,
    }


def retry_if_token_expired(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            get_acccess_token()
            kwargs.update({"headers": __access_headers})
        return func(*args, **kwargs)

    return wrapper


# apply decorator manually
get_json = retry_if_token_expired(get_json)


def name():
    return "Twitch"


def image():
    return "icon.png"


def description():
    return "Twitch Channel (<a target='_blank' href='http://www.twitch.tv/'>http://www.twitch.tv/</a>)."


def feedlist():
    data = get_json(_TOP_GAMES_URL, headers=__access_headers)["data"]
    return list(map(lambda x: {"title": x["name"], "id": x["id"]}, data))


def feed(idx):
    game_id = feedlist()[idx]["id"]
    streams = get_json(
        _STREAM_URL, {"first": "50", "game_id": game_id}, headers=__access_headers
    )["data"]
    return _extract(streams)


def search(q):
    streams = get_json(
        _SEARCH_URL,
        {"first": 50, "query": q, "live_only": True},
        headers=__access_headers,
    )["data"]
    return _extract_channels(streams)


def _extract_channels(stream_json):
    results = PlayItemList()
    for stream in stream_json:
        title = stream["display_name"] + " - " + stream["title"]
        game = stream["game_name"]
        tags = stream["tags"]
        subtitle = "tags: " + ", ".join(tags) + "<br>" + game
        img = (
            stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "200")
        )
        url = "https://www.twitch.tv/" + stream["broadcaster_login"]
        results.add(LiveStreamPlayItem(title, img, url, subtitle))
    return results


def _extract(stream_json):
    results = PlayItemList()
    for stream in stream_json:
        title = stream["user_name"] + " - " + stream["title"]
        status = stream["type"]
        viewers = stream["viewer_count"]
        subtitle = "viewers: " + str(viewers) + "<br>" + status
        img = (
            stream["thumbnail_url"].replace("{width}", "300").replace("{height}", "200")
        )
        url = "https://www.twitch.tv/" + stream["user_name"]
        results.add(LiveStreamPlayItem(title, img, url, subtitle))
    return results
