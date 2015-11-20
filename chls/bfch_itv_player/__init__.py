from chanutils import get_doc, select_all, select_one
from chanutils import get_attr, get_text, get_text_content
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_FEEDLIST = [
  {'title':'Shows', 'url':'http://www.itv.com/hub/shows'},
]

_SHOWLIST = []

def name():
  return 'ITV Player'

def image():
  return 'icon.png'

def description():
   return "ITV Player Channel (<a target='_blank' href='https://www.itv.com/hub'>https://www.itv.com/hub</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  doc = get_doc(url)
  rtree = select_all(doc, "a.complex-link")
  results = PlayItemList()
  for l in rtree:
    url = get_attr(l, 'href')
    el = select_one(l, 'h3.tout__title')
    title = get_text(el)
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'p.tout__meta')
    subtitle = get_text(el)
    if subtitle == 'No episodes available':
      continue    
    item = PlayItem(title, img, url, subtitle)
    item.add_action(MoreEpisodesAction(url, title))
    results.add(item)
  global _SHOWLIST
  _SHOWLIST = results
  return results

def search(q):
  results = PlayItemList()
  items = _SHOWLIST.to_list()
  for i in items:
    title = i.title 
    if q.lower() in title.lower():
      results.add(i)
  return results

def showmore(link):
  doc = get_doc(link)
  rtree = select_all(doc, "a.complex-link")
  results = PlayItemList()
  for l in rtree:
    url = get_attr(l, 'href')
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'h2')
    title = get_text(el)
    el = select_one(l, 'time')
    subtitle = get_text(el)
    el = select_one(l, 'p.tout__summary theme__subtle')
    synopsis = get_text(el)
    item = PlayItem(title, img, url, subtitle, synopsis)
    results.add(item)
  return results
