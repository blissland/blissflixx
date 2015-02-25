from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'http://www.muzu.tv/search/'
_PREFIX = 'http://www.muzu.tv'

_FEEDLIST = [
  {'title':'Popular', 'url':'http://www.muzu.tv/music-videos/all/'},
  {'title':'New Releases', 'url':'http://www.muzu.tv/music-videos/new-releases/'},
  {'title':'Staff Picks', 'url':'http://www.muzu.tv/music-videos/our-picks/'},
  {'title':'Electronic', 'url':'http://www.muzu.tv/music-videos/electronic/'},
  {'title':'Dubstep', 'url':'http://www.muzu.tv/music-videos/dubstep/'},
  {'title':'RnB', 'url':'http://www.muzu.tv/music-videos/rnb/'},
  {'title':'Pop', 'url':'http://www.muzu.tv/music-videos/pop/'},
  {'title':'Metal', 'url':'http://www.muzu.tv/music-videos/metal/'},
  {'title':'Rock', 'url':'http://www.muzu.tv/music-videos/rock/'},
  {'title':'Indie', 'url':'http://www.muzu.tv/music-videos/indie/'},
  {'title':'Acoustic', 'url':'http://www.muzu.tv/music-videos/acoustic/'},
  {'title':'Alternative','url':'http://www.muzu.tv/music-videos/alternative/'},
  {'title':'Jazz','url':'http://www.muzu.tv/music-videos/jazz/'},
  {'title':'Soul','url':'http://www.muzu.tv/music-videos/soul/'},
  {'title':'Punk','url':'http://www.muzu.tv/music-videos/punk/'},
]

def name():
  return 'MUZU'

def image():
  return "icon.png"

def description():
  return "MUZU Music Videos Channel (<a target='_blank' href='http://www.muzu.tv/'>http://www.muzu.tv/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  return _extract(doc)

def search(q):
  doc = get_doc(_SEARCH_URL, params={'mySearch':q})
  if select_one(doc, 'li.search-no-videos-heading') is None:
    return _extract(doc)
  else:
    return PlayItemList()

def _extract(doc):
  rtree = select_all(doc, 'li.browse-content-item-videos')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    href = get_attr(el, 'href')
    if href is None:
      continue
    url = _PREFIX + href
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'div.browse-content-top-line')
    subtitle = get_text(el)
    el = select_one(l, 'div.browse-content-second-line')
    title = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results

  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    url = get_attr(el, 'href')
    if not url.startswith('/talks/'):
      continue
    url = _PREFIX + url
    title = get_text(el)
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'div.search__result__description')
    synopsis = get_text(el)
    results.add(PlayItem(title, img, url, synopsis=synopsis))
  return results
