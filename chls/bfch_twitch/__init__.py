from chanutils import get_json
from playitem import LiveStreamPlayItem, PlayItemList

_FEEDLIST_URL = 'https://api.twitch.tv/kraken/games/top?limit=50'
_STREAM_URL = 'https://api.twitch.tv/kraken/streams'
_SEARCH_URL = 'https://api.twitch.tv/kraken/search/streams'

def name():
  return 'Twitch'

def image():
  return "icon.png"

def description():
  return "Twitch Channel (<a target='_blank' href='http://www.twitch.tv/'>http://www.twitch.tv/</a>)."

def feedlist():
  return map(lambda x: {'title' : x['game']['name']}, get_json(_FEEDLIST_URL)['top'])

def feed(idx):
  gameName = feedlist()[idx]['title']
  streams = get_json(_STREAM_URL, {'limit':50, 'game': gameName})['streams']
  return _extract(streams)

def search(q):
  streams = get_json(_SEARCH_URL, {'limit':50, 'q': q})['streams']
  return _extract(streams)

def _extract(stream_json):
  results = PlayItemList()
  for stream in stream_json:
    title = stream['channel']['name'] if 'name' in stream['channel'] else ''
    status = stream['channel']['status'] if 'status' in stream['channel'] else ''
    viewers = stream['viewers'] if 'viewers' in stream else ''
    subtitle = 'viewers: ' + str(stream['viewers']) + '<br>' + status
    img = stream['channel']['logo']
    url = stream['channel']['url'] if 'url' in stream['channel'] else ''
    results.add(LiveStreamPlayItem(title, img, url, subtitle))
  return results