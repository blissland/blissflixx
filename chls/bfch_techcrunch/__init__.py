from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://techcrunch.com/"

_FEEDLIST = [
  {'title':'All Videos', 'url':'http://techcrunch.com/video/'},
  {'title':'TCTV News', 'url':'http://techcrunch.com/shows/tctv-news/'},
  {'title':'TC Gadgets', 'url':'http://techcrunch.com/shows/gadgets/'},
  {'title':'Features', 'url':'http://techcrunch.com/shows/features/'},
  {'title':'Reviews', 'url':'http://techcrunch.com/shows/reviews/'},
  {'title':'TC Interviews', 'url':'http://techcrunch.com/shows/interviews/'},
  {'title':'Apps', 'url':'http://techcrunch.com/shows/apps/'},
  {'title':'Disrupt', 'url':'http://techcrunch.com/shows/techcrunch-disrupt/'},
  {'title':'Battlefield', 'url':'http://techcrunch.com/shows/techcrunch-battlefield/'},
  {'title':'Sessions', 'url':'http://techcrunch.com/shows/tc-sessions/'},
  {'title':'Crunch Reports', 'url':'http://techcrunch.com/shows/crunch-report/'},
  {'title':'Judah vs the Machines', 'url':'http://techcrunch.com/shows/judah-vs-the-machines/'},
  {'title':'Down Round', 'url':'http://techcrunch.com/shows/down-round/'},
  {'title':'Trust Disrupted', 'url':'http://techcrunch.com/shows/trust-disrupted/'},
  {'title':'Built in Brooklyn', 'url':'http://techcrunch.com/shows/built-in-brooklyn/'},
  {'title':'TC Cribs', 'url':'http://techcrunch.com/shows/tc-cribs/'},
  {'title':'Bullish', 'url':'http://techcrunch.com/shows/bullish/'},
  {'title':'CrunchWeek', 'url':'http://techcrunch.com/shows/crunchweek/'},
  {'title':'Fly or Die', 'url':'http://techcrunch.com/shows/fly-or-die/'},
]
def name():
  return 'Tech Crunch'

def image():
  return 'icon.png'

def description():
  return "Tech Crunch (<a target='_blank' href='https://techcrunch.com'>https://techcrunch.com/a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  rtree = select_all(doc, 'div.post-block')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    url = get_attr(el, 'href')
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'div.post-block__content')
    subtitle = get_text(el)
    el = select_one(l, 'a.post-block__title__link')
    title = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results

