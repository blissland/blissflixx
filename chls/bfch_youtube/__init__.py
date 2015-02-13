import chanutils, chanutils.reddit, playitem

_SEARCH_URL = "http://gdata.youtube.com/feeds/api/videos"

_FEEDLIST = [
  {'title':'Trending', 'url':'http://www.reddit.com/domain/youtube.com/top/.json'},
  {'title':'Popular Today', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular?time=today&v=2&alt=jsonc'},
  {'title':'Animals', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Animals?time=today&v=2&alt=jsonc'},
  {'title':'Comedy', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Comedy?time=today&v=2&alt=jsonc'},
  {'title':'Entertainment', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Entertainment?time=today&v=2&alt=jsonc'},
  {'title':'Games', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Games?time=today&v=2&alt=jsonc'},
  {'title':'Movies', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Movies?time=today&v=2&alt=jsonc'},
  {'title':'Music', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Music?time=today&v=2&alt=jsonc'},
  {'title':'News', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_News?time=today&v=2&alt=jsonc'},
  {'title':'Sports', 'url':'https://gdata.youtube.com/feeds/api/standardfeeds/most_popular_Sports?time=today&v=2&alt=jsonc'},
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
    data = chanutils.get_json(url)
    return _extract(data)

def search(q):
  query = {'format':'5', 'v':'2', 'alt':'jsonc', 'q': q}
  data = chanutils.get_json(_SEARCH_URL, params=query)
  return _extract(data)

def _extract(data):
  if not 'data' in data or data['data']['totalItems'] == 0:
    return []
  rtree = data['data']['items']
  results = playitem.PlayItemList()
  for r in rtree:
    title = r['title']
    img = r['thumbnail']['sqDefault']
    url = r['player']['default']
    m, s = divmod(r['duration'], 60)
    h, m = divmod(m, 60)
    subtitle = 'Duration: ' + "%d:%02d:%02d" % (h, m, s)
    if 'viewCount' in r:
      subtitle = subtitle + ', Views: ' + "{:,}".format(r['viewCount'])
    item = playitem.PlayItem(title, img, url, subtitle)
    results.add(item)
  return results
