import chanutils.reddit
from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'https://vimeo.com/search'
_PREFIX = 'https://vimeo.com'

_FEEDLIST = [
  {'title':'Trending', 'url':'http://www.reddit.com/domain/vimeo.com/top/.json'},
  {'title':'Animation', 'url':'https://vimeo.com/categories/animation/videos'},
  {'title':'Arts & Design', 'url':'https://vimeo.com/categories/art/videos'},
  {'title':'Cameras & Techniques', 'url':'https://vimeo.com/categories/cameratechniques/videos'},
  {'title':'Comedy', 'url':'http://vimeo.com/categories/comedy/videos'},
  {'title':'Documentary', 'url':'http://vimeo.com/categories/documentary/videos'},
  {'title':'Experimental', 'url':'http://vimeo.com/categories/experimental/videos'},
  {'title':'Fashion', 'url':'http://vimeo.com/categories/fashion/videos'},
  {'title':'Food', 'url':'http://vimeo.com/categories/food/videos'},
  {'title':'Instructionals', 'url':'http://vimeo.com/categories/instructionals/videos'},
  {'title':'Music', 'url':'http://vimeo.com/categories/music/videos'},
  {'title':'Narrative', 'url':'http://vimeo.com/categories/narrative/videos'},
  {'title':'Personal', 'url':'http://vimeo.com/categories/personal/videos'},
  {'title':'Reporting & Journalism', 'url':'https://vimeo.com/categories/journalism/videos'},
  {'title':'Sports', 'url':'http://vimeo.com/categories/sports/videos'},
  {'title':'Talks', 'url':'http://vimeo.com/categories/talks/videos'},
  {'title':'Travel', 'url':'http://vimeo.com/categories/travel/videos'},
]

def name():
  return 'Vimeo'

def image():
  return "icon.png"

def description():
  return "Vimeo Channel (<a target='_blank' href='https://vimeo.com/'>https://vimeo.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  if url.endswith('.json'):
    return chanutils.reddit.get_feed(_FEEDLIST[idx])
  else:
    doc = get_doc(url)
    return _extract(doc)

def search(q):
  doc = get_doc(_SEARCH_URL, params={'q':q})
  return _extract(doc)

def _extract(doc):
  rtree = select_all(doc, '#browse_content li a')
  results = PlayItemList()
  for l in rtree:
    url = _PREFIX + l.get('href')
    title = get_attr(l, 'title')
    if title is None:
      break
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'time')
    subtitle = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results
