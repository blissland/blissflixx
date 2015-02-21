from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'http://www.ted.com/search'
_PREFIX = 'http://www.ted.com'

_FEEDLIST = [
  {'title':'Latest', 'url':'http://www.ted.com/talks'},
  {'title':'Most Viewed', 'url':'http://www.ted.com/talks?sort=popular'},
  {'title':'Jaw-dropping', 'url':'http://www.ted.com/talks?sort=jaw-dropping'},
  {'title':'Funny', 'url':'http://www.ted.com/talks?sort=funny'},
  {'title':'Persuasive', 'url':'http://www.ted.com/talks?sort=persuasive'},
  {'title':'Courageous', 'url':'http://www.ted.com/talks?sort=courageous'},
  {'title':'Ingenious', 'url':'http://www.ted.com/talks?sort=ingenious'},
  {'title':'Fascinating', 'url':'http://www.ted.com/talks?sort=fascinating'},
  {'title':'Inspiring', 'url':'http://www.ted.com/talks?sort=inspiring'},
  {'title':'Beautiful', 'url':'http://www.ted.com/talks?sort=beautiful'},
  {'title':'Informative', 'url':'http://www.ted.com/talks?sort=informative'},
]

def name():
  return 'TED'

def image():
  return "icon.png"

def description():
  return "TED Talks Channel (<a target='_blank' href='http://www.ted.com/'>http://www.ted.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  rtree = select_all(doc, 'div.talk-link')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    url = _PREFIX + get_attr(el, 'href')
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'h4.talk-link__speaker')
    subtitle = get_text(el)
    el = select_one(l, 'h4.h9 a')
    title = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results

def search(q):
  doc = get_doc(_SEARCH_URL, params={'q':q})
  rtree = select_all(doc, 'article.search__result')
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
