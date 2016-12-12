import re, json
import chanutils.reddit
from chanutils import get, get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = 'https://vimeo.com/search'

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
    r = get(url)
    return _extract(r.text)
    

def search(q):
  r = get(_SEARCH_URL, params={'q':q})
  return _extract(r.text)

def _extract(text):
    start = text.find('var data = {')
    end = text.find('console.debug(data);', start)
    data = json.loads(text[start+11:end-14])
    results = PlayItemList()
    for item in data['filtered']['data']:
      url = item['clip']['link']
      title = item['clip']['name']
      img = item['clip']['pictures']['sizes'][-1]['link']
      results.add(PlayItem(title, img, url))
    return results
