from chanutils import get_json, select_all, select_one, get_attr
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'https://apiv2.vevo.com/search?artistsLimit=6&videosLimit=18&skippedVideos=0&token=_TMw_fGgJHvzr84MqwK1eWhBgbdebZhAm_y3W1ou-sU1.1424588400.LKBaQhteDi8dJCv_aPAc7M0AGJ9Iosllug3Dik-um7rbx-w56CymsfJte0PEQh_zPmVg2A2'

_FEEDLIST = [
  {'title':'Premieres', 'url':'https://apiv2.vevo.com/videos?page=1&size=30&sort=MostRecent&ispremiere=true&token=_TMw_fGgJHvzr84MqwK1eWhBgbdebZhAm_y3W1ou-sU1.1424588400.LKBaQhteDi8dJCv_aPAc7M0AGJ9Iosllug3Dik-um7rbx-w56CymsfJte0PEQh_zPmVg2A2'},
  {'title':'Top This Week', 'url':'https://apiv2.vevo.com/videos?page=1&size=30&sort=MostViewedLastWeek&token=_TMw_fGgJHvzr84MqwK1eWhBgbdebZhAm_y3W1ou-sU1.1424588400.LKBaQhteDi8dJCv_aPAc7M0AGJ9Iosllug3Dik-um7rbx-w56CymsfJte0PEQh_zPmVg2A2'}
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
  data = get_json(_FEEDLIST[idx]['url'])
  return _extract(data)

def search(q):
  data = get_json(_SEARCH_URL, params={'q':q})
  return _extract(data)

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
