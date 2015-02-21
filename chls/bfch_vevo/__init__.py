from chanutils import get_json, select_all, select_one, get_attr, post_json
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'https://apiv2.vevo.com/search?artistsLimit=6&videosLimit=18&skippedVideos=0'

_FEEDLIST = [
  {'title':'Premieres', 'url':'https://apiv2.vevo.com/videos?page=1&size=30&sort=MostRecent&ispremiere=true'},
  {'title':'Top This Week', 'url':'https://apiv2.vevo.com/videos?page=1&size=30&sort=MostViewedLastWeek'},
  {'title':'Live Performances', 'url':'https://apiv2.vevo.com/videos?page=1&size=30&sort=MostViewedLastWeek&islive=true'},
]

def name():
  return 'VEVO'

def image():
  return "icon.png"

def description():
  return "VEVO Music Channel (<a target='_blank' href='https://www.vevo.com/'>https://www.vevo.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  data = get_json(_FEEDLIST[idx]['url'], params={'token':_token()})
  return _extract(data)

def search(q):
  data = get_json(_SEARCH_URL, params={'q':q, 'token':_token()})
  return _extract(data)

def _token():
  data = post_json("http://www.vevo.com/auth", b'')
  return data["access_token"]

def _extract(data):
  videos = data['videos']
  results = PlayItemList()
  for v in videos:
    title = v['title']
    img = v['thumbnailUrl']
    if 'shortUrl' in v:
      url = v['shortUrl']
    else:
      url = "http://www.vevo.com/watch/" + v['isrc']
    if 'artists' in v:
      subtitle = v['artists'][0]['name']
    else: 
      subtitle = v['primaryArtists'][0]['name']
    results.add(PlayItem(title, img, url, subtitle))
  return results
