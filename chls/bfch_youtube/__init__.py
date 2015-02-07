from chanutils import get_json, img_prefix
import chanutils.reddit

_SEARCH_URL = "http://gdata.youtube.com/feeds/api/videos"
_IMG = 'icon.png'
_IMGPATH = img_prefix() + '/youtube/' + _IMG

_feedlist = [
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

def get_name():
  return 'Youtube'

def get_image():
  return _IMG

def search(q):
  query = {'format':'5', 'v':'2', 'alt':'jsonc', 'q': q}
  data = get_json(_SEARCH_URL, params=query)
  return _extract(data)

def get_feedlist():
  return _feedlist

def get_feed(idx):
  url = _feedlist[idx]['url']
  data = get_json(url)
  if url.endswith('.json'):
    return chanutils.reddit.extract(data, thumbnail = _IMGPATH)
  else:
    return _extract(data)

def _extract(data):
  if not 'data' in data or data['data']['totalItems'] == 0:
    return []
  filtered = []
  results = data['data']['items']
  for r in results:
    m, s = divmod(r['duration'], 60)
    h, m = divmod(m, 60)
    subtitle = 'Duration: ' + "%d:%02d:%02d" % (h, m, s)
    if 'viewCount' in r:
      subtitle = subtitle + ', Views: ' + "{:,}".format(r['viewCount'])
    filtered.append({'title':r['title'], 'img':r['thumbnail']['sqDefault'],
            'subtitle': subtitle, 'url': r['player']['default']})

  return filtered
