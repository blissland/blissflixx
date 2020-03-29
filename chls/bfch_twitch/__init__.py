from chanutils import get_json
from playitem import LiveStreamPlayItem, PlayItemList
from urllib import quote_plus, unquote_plus

_CLIENT_ID = 'yicd1x2uyrhazbdc4n7zba4yzrjlx0'
_HEADER = {'Client-ID': _CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
_FEEDLIST_URL = 'https://api.twitch.tv/helix/games/top'
_STREAM_URL = 'https://api.twitch.tv/helix/streams'
_SEARCH_URL = 'https://api.twitch.tv/kraken/search/streams'
_BASE_URL = 'https://twitch.tv/'

def name():
  return 'Twitch'

def image():
  return "icon.png"

def description():
  return "Twitch Channel (<a target='_blank' href='http://www.twitch.tv/'>http://www.twitch.tv/</a>)."

def feedlist():
  return map(lambda x: {'id': x['id'], 'title': x['name'], 'name': x['id']}, get_json(_FEEDLIST_URL, {'first':50}, headers=_HEADER)['data'])
#return map(lambda x: {'id': x['id'], 'title': x['name'], 'name': quote_plus(x['name'].encode('utf-8'))}, get_json(_FEEDLIST_URL, {'first':50}, headers=_HEADER)['data'])

def feed(idx):
  game_id = feedlist()[idx]['id']
  streams = get_json(_STREAM_URL, {'first':50, 'game_id': game_id}, headers=_HEADER)['data']
  return _extract(streams)

def feed_by_name(idx, name):
  streams = get_json(_STREAM_URL, {'limit':50, 'game_id': unquote_plus(name.encode('utf-8'))}, headers=_HEADER)['data']
  return _extract(streams)

def search(q):
  streams = get_json(_SEARCH_URL, {'limit':50, 'query': q}, headers=_HEADER)['streams']
  return _extract_streams(streams)

def _extract_streams(stream_json):
  results = PlayItemList()
  for stream in stream_json:
    title = stream['channel']['display_name'] if 'display_name' in stream['channel'] else ''
    status = stream['channel']['status'] if 'status' in stream['channel'] else ''
    viewers = stream['viewers'] if 'viewers' in stream else ''
    subtitle = 'viewers: ' + str(viewers) + '<br>' + status
    img = stream['channel']['logo']
    url = stream['channel']['url'] if 'url' in stream['channel'] else ''
    results.add(LiveStreamPlayItem(title, img, url, subtitle))
  return results

def _extract(stream_json):
  results = PlayItemList()
  for stream in stream_json:
    title = stream['user_name'] if 'user_name' in stream else ''
    status = stream['title'] if 'title' in stream else ''
    viewers = stream['viewer_count'] if 'viewer_count' in stream else ''
    subtitle = 'viewers: ' + str(viewers) + '<br>' + status
    img = stream['thumbnail_url'].replace('{width}','165').replace('{height}','124')
    url = _BASE_URL + stream['user_name'] if 'user_name' in stream else ''
    results.add(LiveStreamPlayItem(title, img, url, subtitle))
  return results
