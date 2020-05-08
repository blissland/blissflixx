import random
import chanutils.reddit
from chanutils import get_json
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

_API_KEY_POOL = [
#  "AIzaSyC76A-MHHypf-kv-4l-dEPPCK65C38lMt4", # newbliss
#  "AIzaSyArJTw6o9Tl6DLrETTxHXmxOEmuPcJUuQk", # blissflixx1
#  "AIzaSyBFQq1lIlQKlGRvCu45RhlDTXx4bGziByY", # blissflixx2
#  "AIzaSyCOwS8E3Vr70bj5dQqXJX6PPnla9j7VokA", # blissflixx3
#  "AIzaSyAw10CnwxuKV2Z9vW6ehXUDPslpCgQ93NA", # blissflixx4
  "AIzaSyB9i9vu-Kwd7kiKwDalH06fMjLjYeylZsg", # test0
  "AIzaSyBkr7KZdZ33IKcdXWb8RmQZZQB3K8Uow0s", # test1
  "AIzaSyAYg7qdi6SnSjJUgiccOXSyOoxlAG0wHIw", # test2
  "AIzaSyBt-OPrCrXF0oIf9FkXRdd142f7cDdZubk", # test3
  "AIzaSyAdRojg4iwdHY6wvirXhikfFXTZ0rpgfNg", # test4
  "AIzaSyCof4H5PpGCq5NSdqNEWgM7p1rNgzTTR-0", # test5
  "AIzaSyBxZbYSU7V4cG73Gnj3MjlbSPAWsV1Rugs", # test6
  "AIzaSyCh0nZGziipkXz8FdVlLQ2ea4kXBtD4ku0", # test7
  "AIzaSyAdF6_MjwSo0r3q40xj7NlySvaM0kCdfb0", # test8
  "AIzaSyBO0U1YrpT6Gf3Ehz3UfuKjzi8sQdKUcgc", # test9
  "AIzaSyB7Jn8hKG-vc4snUrZVcZ25R8UnhmeRLBM", # test10
  "AIzaSyC55Q8NmG72-KqiEru54CpcRIrwcu5yRFU", # test11

]

_API_KEY = random.choice(_API_KEY_POOL)

_FEEDLIST = [
  {'title':'Trending', 'url':'http://www.reddit.com/domain/youtube.com/top/.json'},
  {'title':'Popular', 'url':'https://www.googleapis.com/youtube/v3/videos?maxResults=50&key=' + _API_KEY + '&part=snippet&chart=mostPopular'},
]

def name():
  return 'Youtube'

def image():
  return "icon.png"

def description():
  return "Youtube Channel (<a target='_blank' href='https://www.youtube.com/'>https://www.youtube.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  if url.endswith('.json'):
    return chanutils.reddit.get_feed(_FEEDLIST[idx])
  else:
    data = get_json(url)
    return _extract(data)

def search(q):
  query = {'part':'snippet', 'q':q, 'maxResults': 50,
	    'key': _API_KEY}
  data = get_json(_SEARCH_URL, params=query)
  return _extract(data)

def _extract(data):
  results = PlayItemList()
  rtree = data['items']
  for r in rtree:
    title= r['snippet']['title']
    subtitle= r['snippet']['publishedAt'][:10]
    synopsis= r['snippet']['description']
    if len(synopsis) > 200:
      synopsis = synopsis[:200] + "..."
    try:
      img = r['snippet']['thumbnails']['default']['url']
    except KeyError:
      img = '/img/icons/film.svg'
    if isinstance(r['id'], basestring):
      vid = r['id']
    elif 'videoId' in r['id']:
      vid = r['id']['videoId']
    else:
      continue
    url = 'https://www.youtube.com/watch?v=' + vid
    results.add(PlayItem(title, img, url, subtitle, synopsis))
  return results
