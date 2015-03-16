from chanutils import get_json, number_commas
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://api-v2.soundcloud.com/search"

_FEEDLIST = [
  {'title':'Trending', 'url':'https://api-v2.soundcloud.com/explore/Popular+Music?limit=50&offset=0'},
  {'title':'Alternative Rock', 'url':'https://api-v2.soundcloud.com/explore/alternative+rock?limit=50&offset=0'},
  {'title':'Ambient', 'url':'https://api-v2.soundcloud.com/explore/ambient?limit=50&offset=0'},
  {'title':'Classical', 'url':'https://api-v2.soundcloud.com/explore/classical?limit=50&offset=0'},
  {'title':'Country', 'url':'https://api-v2.soundcloud.com/explore/country?limit=50&offset=0'},
  {'title':'Dance & Edm', 'url':'https://api-v2.soundcloud.com/explore/dance+&+edm?limit=50&offset=0'},
  {'title':'Dancehall', 'url':'https://api-v2.soundcloud.com/explore/dancehall?limit=50&offset=0'},
  {'title':'Deep House', 'url':'https://api-v2.soundcloud.com/explore/deep+house?limit=50&offset=0'},
  {'title':'Disco', 'url':'https://api-v2.soundcloud.com/explore/disco?limit=50&offset=0'},
  {'title':'Drum & Bass', 'url':'https://api-v2.soundcloud.com/explore/drum+&+bass?limit=50&offset=0'},
  {'title':'Dubstep', 'url':'https://api-v2.soundcloud.com/explore/dubstep?limit=50&offset=0'},
  {'title':'Electronic', 'url':'https://api-v2.soundcloud.com/explore/electronic?limit=50&offset=0'},
  {'title':'Folk', 'url':'https://api-v2.soundcloud.com/explore/folk+&+singer-songwriter?limit=50&offset=0'},
  {'title':'Hip Hop & Rap', 'url':'https://api-v2.soundcloud.com/explore/hip+hop+&+rap?limit=50&offset=0'},
  {'title':'House', 'url':'https://api-v2.soundcloud.com/explore/house?limit=50&offset=0'},
  {'title':'Indie', 'url':'https://api-v2.soundcloud.com/explore/indie?limit=50&offset=0'},
  {'title':'Jazz & Blues', 'url':'https://api-v2.soundcloud.com/explore/jazz+&+blues?limit=50&offset=0'},
  {'title':'Latin', 'url':'https://api-v2.soundcloud.com/explore/latin?limit=50&offset=0'},
  {'title':'Metal', 'url':'https://api-v2.soundcloud.com/explore/metal?limit=50&offset=0'},
  {'title':'Piano', 'url':'https://api-v2.soundcloud.com/explore/piano?limit=50&offset=0'},
  {'title':'Pop', 'url':'https://api-v2.soundcloud.com/explore/pop?limit=50&offset=0'},
  {'title':'R&B & Soul', 'url':'https://api-v2.soundcloud.com/explore/r&b+&+soul?limit=50&offset=0'},
  {'title':'Reggae', 'url':'https://api-v2.soundcloud.com/explore/reggae?limit=50&offset=0'},
  {'title':'Reggaeton', 'url':'https://api-v2.soundcloud.com/explore/reggaeton?limit=50&offset=0'},
  {'title':'Rock', 'url':'https://api-v2.soundcloud.com/explore/rock?limit=50&offset=0'},
  {'title':'Soundtrack', 'url':'https://api-v2.soundcloud.com/explore/soundtrack?limit=50&offset=0'},
  {'title':'Techno', 'url':'https://api-v2.soundcloud.com/explore/techno?limit=50&offset=0'},
  {'title':'Trance', 'url':'https://api-v2.soundcloud.com/explore/trance?limit=50&offset=0'},
  {'title':'Trap', 'url':'https://api-v2.soundcloud.com/explore/trap?limit=50&offset=0'},
  {'title':'Trip Hop', 'url':'https://api-v2.soundcloud.com/explore/trip+hop?limit=50&offset=0'},
  {'title':'World', 'url':'https://api-v2.soundcloud.com/explore/world?limit=50&offset=0'},
]

def name():
  return 'SoundCloud Music'

def image():
  return "icon.png"

def description():
  return "SoundCloud Music Channel (<a target='_blank' href='https://www.soundcloud.com/'>https://www.soundcloud.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  data = get_json(url)
  return _extract(data)

def search(q):
  query = {'limit':'20', 'offset':'0', 'q': q}
  data = get_json(_SEARCH_URL, params=query)
  return _extract(data)

def _extract(data):
  results = PlayItemList()
  if not('tracks' in data or 'collection' in data):
    return results
  if 'tracks' in data:
    rtree = data['tracks']
  else:
    rtree = data['collection']
  for r in rtree:
    if not 'title' in r:
      continue
    if not r['streamable']:
      continue
    title = r['title']
    if r['artwork_url']: 
      img = r['artwork_url']
    else:
      img = r['user']['avatar_url']
    url = r['permalink_url']
    subtitle = 'Plays: ' + number_commas(r['playback_count'])
    subtitle = subtitle + ', Likes: ' + number_commas(r['likes_count'])
    results.add(PlayItem(title, img, url, subtitle))
  return results
