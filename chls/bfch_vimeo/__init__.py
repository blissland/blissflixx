from chanutils import get_json, get_doc, select_one, select_all, img_prefix
import chanutils.reddit

_SEARCH_URL = 'https://vimeo.com/search'
_PREFIX = 'https://vimeo.com'
_IMG = 'icon.png'
_IMGPATH = img_prefix() + '/vimeo/' + _IMG

feedlist = [
  {'title':'Trending', 'url':'http://www.reddit.com/domain/vimeo.com/top/.json'},
  {'title':'Animation', 'url':'https://vimeo.com/categories/animation/videos'},
  {'title':'Arts', 'url':'https://vimeo.com/categories/art/videos'},
  {'title':'Causes', 'url':'http://vimeo.com/categories/nonprofit/videos'},
  {'title':'Comedy', 'url':'http://vimeo.com/categories/comedy/videos'},
  {'title':'Design', 'url':'http://vimeo.com/categories/design/videos'},
  {'title':'Documentary', 'url':'http://vimeo.com/categories/documentary/videos'},
  {'title':'Experimental', 'url':'http://vimeo.com/categories/experimental/videos'},
  {'title':'Fashion', 'url':'http://vimeo.com/categories/fashion/videos'},
  {'title':'Food', 'url':'http://vimeo.com/categories/food/videos'},
  {'title':'For Kids', 'url':'http://vimeo.com/categories/kids/videos'},
  {'title':'Instructionals', 'url':'http://vimeo.com/categories/instructionals/videos'},
  {'title':'Music', 'url':'http://vimeo.com/categories/music/videos'},
  {'title':'Narrative', 'url':'http://vimeo.com/categories/narrative/videos'},
  {'title':'Nature', 'url':'http://vimeo.com/categories/nature/videos'},
  {'title':'Personal', 'url':'http://vimeo.com/categories/personal/videos'},
  {'title':'Sports', 'url':'http://vimeo.com/categories/sports/videos'},
  {'title':'Talks', 'url':'http://vimeo.com/categories/talks/videos'},
  {'title':'Tech', 'url':'http://vimeo.com/categories/technology/videos'},
  {'title':'The Big Picture', 'url':'http://vimeo.com/categories/bigpicture/videos'},
  {'title':'Timelapse', 'url':'http://vimeo.com/categories/cameratechniques/videos'},
  {'title':'Travel', 'url':'http://vimeo.com/categories/travel/videos'},
  {'title':'Video School', 'url':'http://vimeo.com/categories/videoschool/videos'},
  {'title':'Vimeo', 'url':'http://vimeo.com/categories/vimeoprojects/videos'},
]

def get_name():
  return 'Vimeo'

def get_image():
  return _IMG

def search(q):
  doc = get_doc(_SEARCH_URL, params={'q':q})
  return _extract(doc)

def get_feedlist():
  return feedlist

def get_feed(idx):
  url = feedlist[idx]['url']
  if url.endswith('.json'):
    data = get_json(url)
    return chanutils.reddit.extract(data, thumbnail = _IMGPATH)
  else:
    doc = get_doc(url)
    return _extract(doc)

def _extract(doc):
  rtree = select_all(doc, '#browse_content li a')
  results = []
  for l in rtree:
    url = _PREFIX + l.get('href')
    title = l.get('title')
    if title is None:
      break
    el = select_one(l, 'img')
    img = el.get('src')
    el = select_one(l, 'time')
    subtitle = el.text
    results.append({ 'title':title, 'img':img, 'url':url, 'subtitle':subtitle })
  return results
