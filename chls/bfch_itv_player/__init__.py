from chanutils import get_doc, select_all, select_one, get_json
from chanutils import get_attr, get_text, get_text_content
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_FEEDLIST = [
  {'title':'Popular', 'url':'http://www.itv.com'},
  {'title':'All Shows', 'url':'http://www.itv.com/hub/shows'},
  {'title':'Children', 'url':'http://www.itv.com/hub/categories/children'},
  {'title':'Comedy', 'url':'http://www.itv.com/hub/categories/comedy'},
  {'title':'Drama & Soaps', 'url':'http://www.itv.com/hub/categories/drama-soaps'},
  {'title':'Entertainment', 'url':'http://www.itv.com/hub/categories/entertainment'},
  {'title':'Factual', 'url':'http://www.itv.com/hub/categories/factual'},
  {'title':'Films', 'url':'http://www.itv.com/hub/categories/films'},
  {'title':'Sport', 'url':'http://www.itv.com/hub/categories/sport'},
]

_ALL_SHOWS_URL = "https://www.itv.com/hub/api/sayt"

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
    el = select_one(l, '.tout__title')
    if el is None:
      continue
    title = get_text(el)
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'p.tout__meta')
    subtitle = get_text_content(el)
    if subtitle == 'No episodes available':
      continue    
    item = PlayItem(title, img, url, subtitle)
    if subtitle != '1 episode':
      item.add_action(MoreEpisodesAction(url, title))
    results.add(item)
  return results

def search(q):
  shows = get_json(_ALL_SHOWS_URL)
  results = PlayItemList()
  for i in shows:
    print(i['title'])
    if q.lower() in i['title'].lower():
      results.add(PlayItem(i['title'], i['image']['jelly'], i['url']['episode'], i['synopses']))
  return results

def showmore(link):
  doc = get_doc(link)
  rtree = select_all(doc, "a.complex-link")
  results = PlayItemList()
  for l in rtree:
    url = get_attr(l, 'href')
    el = select_one(l, 'img.fluid-media__media')
    img = get_attr(el, 'src')
    el = select_one(l, 'h3')
    title = get_text(el)
    el = select_one(l, 'time')
    subtitle = ""
    if el is not None and el.text is not None:
      subtitle = get_text(el)
    el = select_one(l, 'p.tout__summary')
    synopsis = get_text(el)
    item = PlayItem(title, img, url, subtitle, synopsis)
    results.add(item)
  return results
