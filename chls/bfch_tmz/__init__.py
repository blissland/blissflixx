import chanutils.reddit
from chanutils import get_json, replace_entity
from playitem import PlayItem, PlayItemList
from urllib import quote

_SEARCH_URL = "http://www.tmz.com/search/json/videos/"

_FEEDLIST = [
  {'title':'Latest', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1'},
  {'title':'Beauty', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=beauty'},
  {'title':'Celeb Justice', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=celebrity-justice'},
  {'title':'Dating', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=dating'},
  {'title':'Family', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=family'},
  {'title':'Fashion', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=fashion'},
  {'title':'Fights', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=fights'},
  {'title':'Hook Ups', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=hook-ups'},
  {'title':'LGBT', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=lgbt'},
  {'title':'Money', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=money'},
  {'title':'Movies', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=movies'},
  {'title':'Music', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=music'},
  {'title':'Relationships', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=relationships'},
  {'title':'Sex', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=sex'},
  {'title':'Sports', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=tmzsports'},
  {'title':'Television', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=tv'},
  {'title':'Vacations', 'url':'http://www.tmz.com/video-feed-categories/tmz-owned.json?pagesize=30&page=1&tmz-category=vacations'},
]

def name():
  return 'TMZ'

def image():
  return "icon.png"

def description():
  return "TMZ Channel (<a target='_blank' href='https://www.tmz.com/'>https://www.tmz.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  data = get_json(_FEEDLIST[idx]['url'])
  return _extract(data)

def search(q):
  data = get_json(_SEARCH_URL + quote(q) + '/1.json')
  return _extract(data)

def _extract(data):
  results = PlayItemList()
  rtree = data['results']
  for r in rtree:
    title = replace_entity(r['title'])
    img = r['thumbnailUrl']
    if 'url' in r:
      url = r['url']
    else:
      url = r['URL']
    results.add(PlayItem(title, img, url))
  return results
