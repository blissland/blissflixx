import requests, lxml.html, re
import html.entities, urllib.parse, urllib.error, random
from lxml.cssselect import CSSSelector
import html

_PROXY_LIST = [{"url": "http://blissflixx-proxy1.appspot.com"}]


_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "en-GB,en-US;q=0.8,en;q=0.6",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (page) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36",
    #'Client-ID':'tq6hq1srip0i37ipzuscegt7viex9fh'   # Just for Twitch API
}


def _get_proxy_url():
    global _PROXY_LIST
    if _PROXY_LIST is None:
        _PROXY_LIST = get_json("http://blissflixx.rocks/feeds/proxies.json")
    p = random.randint(0, len(_PROXY_LIST) - 1)
    return _PROXY_LIST[p]["url"]


def _get_proxy_headers(headers):
    headers = headers.copy()
    headers["origin"] = "blissflixx"
    return headers


def get(url, params=None, proxy=False, session=None, headers=None):
    if not headers:
        headers = _HEADERS
    else:
        headers = headers.copy()
        headers.update(_HEADERS)
    if proxy:
        if params is not None:
            utfparams = {}
            for k, v in params.items():
                utfparams[k] = str(v).encode("utf-8")
            url = url + "?" + urllib.parse.urlencode(utfparams)
        params = {"url": url}
        url = _get_proxy_url()
        headers = _get_proxy_headers(headers)

    if session is None:
        session = new_session()
    r = session.get(url, params=params, headers=headers)
    if r.status_code >= 300:
        raise Exception(
            "Request : '"
            + url
            + "' returned: "
            + str(r.status_code)
            + "\nparams:"
            + str(params)
            + "\nheaders:"
            + str(headers)
        )
    return r


def post(url, payload, proxy=False, session=None):
    headers = _HEADERS

    if proxy:
        payload["__url__"] = url
        url = _get_proxy_url()
        headers = _get_proxy_headers(headers)

    if session is None:
        session = new_session()
    r = session.post(url, data=payload, headers=headers)
    if r.status_code >= 300:
        raise Exception("Request : '" + url + "' returned: " + str(r.status_code))

    return r


def post_doc(url, payload, **kwargs):
    r = post(url, payload, **kwargs)
    return lxml.html.fromstring(r.text)


def post_json(url, payload, **kwargs):
    r = post(url, payload, **kwargs)
    return r.json()


def get_doc(url, params=None, **kwargs):
    r = get(url, params=params, **kwargs)
    return lxml.html.fromstring(r.text)


def get_json(url, params=None, **kwargs):
    r = get(url, params=params, **kwargs)
    return r.json()


def new_session():
    return requests.session()


def select_one(tree, expr):
    sel = CSSSelector(expr)
    el = sel(tree)
    if isinstance(el, list) and len(el) > 0:
        return el[0]
    else:
        return None


def select_all(tree, expr):
    sel = CSSSelector(expr)
    return sel(tree)


def get_attr(el, name):
    if el is not None:
        return el.get(name)
    else:
        return None


def get_text(el):
    if el is not None and el.text is not None:
        return el.text.strip()
    else:
        return None


def get_text_content(el):
    if el is not None:
        return el.text_content().strip()
    else:
        return None


def byte_size(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, "Y", suffix)


def replace_entity(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(html.entities.name2codepoint[text[1:-1]])
            except KeyError:
                pass
            return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


def number_commas(x):
    if type(x) not in [type(0), type(0)]:
        return "0"
    if x < 0:
        return "-" + number_commas(-x)
    result = ""
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


MOVIE_RE = re.compile(r"(.*)[\(\[]?([12][90]\d\d)[^pP][\(\[]?.*$")
SERIES_RE = re.compile(r"(.*)S(\d\d)E(\d\d).*$")


def movie_title_year(name):
    name = name.replace(".", " ")
    m = MOVIE_RE.match(name)
    if m is None:
        return {"title": name}
    title = m.group(1)
    if title.endswith("(") or title.endswith("["):
        title = title[:-1]
    title = title.strip()
    year = int(m.group(2))
    return {"title": title, "year": year}


def series_season_episode(name):
    name = name.replace(".", " ")
    m = SERIES_RE.match(name)
    if m is None:
        return {"series": name}
    series = m.group(1).strip()
    season = int(m.group(2))
    episode = int(m.group(3))
    return {"series": series, "season": season, "episode": episode}


class UrlInfo:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url).text
        self.tree = lxml.html.fromstring(self.page)

    def get_html_title(self):
        text = self.tree.find(".//title").text
        decoded = html.unescape(text)
        return text

    def get_youtube_video_description(self):
        return self.tree.find(".//meta[@property='og:description']").get("content")

    def get_youtube_video_thumbnail(self):
        return self.tree.find(".//meta[@property='og:image']").get("content")

    def get_youtube_video_publish_date(self):
        return self.tree.find(".//meta[@itemprop='datePublished']").get("content")

    def get_youtube_video_length(self):
        """
        Returns youtube video length in the format minute(s): seconds from the url
        """
        return convert_duration(
            self.tree.find(".//meta[@itemprop='duration']").get("content")
        )

    def get_youtube_video_channel(self):
        return self.tree.find(".//span[@itemprop='author']/link[@itemprop='name']").get(
            "content"
        )


def convert_duration(iso8601):
    """
    "duration": "PT4M13S",
    The time is formatted as an ISO 8601 string. PT stands for Time Duration, 4M is
    4 minutes, and 13S is 13 seconds.
    For example, "P3Y6M4DT12H30M5S" represents a duration of "three years, six months,
    four days, twelve hours, thirty minutes, and five seconds".
    """
    per_pos = iso8601.find("T")
    per = ""
    if per_pos > 0:
        per = iso8601[1:per_pos]
        iso8601 = iso8601[per_pos + 1 :]
    h_pos = iso8601.find("H")
    h = ""
    if h_pos > 0:
        h = iso8601[:h_pos]
        iso8601 = iso8601[h_pos + 1 :]
    m = ""
    m_pos = iso8601.find("M")
    if m_pos > 0:
        m = iso8601[:m_pos]
        iso8601 = iso8601[m_pos + 1 :]
    if h:
        if len(m) == 0:
            m = "00"
        if len(m) == 1:
            m = "0" + m
    else:
        if not m:
            m = "0"
    s = ""
    s_pos = iso8601.find("S")
    if s_pos > 0:
        s = iso8601[:s_pos]
    if len(s) == 0:
        s = "00"
    elif len(s) == 1:
        s = "0" + s
    if per:
        return f"{per} {h}:{m}:{s}" if h else f"{per} {m}:{s}"
    return f"{h}:{m}:{s}" if h else f"{m}:{s}"
