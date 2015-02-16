from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_SEARCH_URL = 'http://www.bbc.co.uk/iplayer/search'

_FEEDLIST = [
  {'title':'Most Popular','url':'http://www.bbc.co.uk/iplayer/group/most-popular'},
  {'title':'Arts','url':'http://www.bbc.co.uk/iplayer/categories/arts/all?sort=dateavailable'},
  {'title':'CBBC','url':'http://www.bbc.co.uk/iplayer/categories/cbbc/all?sort=dateavailable'},
  {'title':'CBeebies','url':'http://www.bbc.co.uk/iplayer/categories/cbeebies/all?sort=dateavailable'},
  {'title':'Comedy','url':'http://www.bbc.co.uk/iplayer/categories/comedy/all?sort=dateavailable'},
  {'title':'Documentaries','url':'http://www.bbc.co.uk/iplayer/categories/documentaries/all?sort=dateavailable'},
  {'title':'Drama & Soaps','url':'http://www.bbc.co.uk/iplayer/categories/drama-and-soaps/all?sort=dateavailable'},
  {'title':'Entertainment','url':'http://www.bbc.co.uk/iplayer/categories/entertainment/all?sort=dateavailable'},
  {'title':'Films','url':'http://www.bbc.co.uk/iplayer/categories/films/all?sort=dateavailable'},
  {'title':'Food','url':'http://www.bbc.co.uk/iplayer/categories/food/all?sort=dateavailable'},
  {'title':'History','url':'http://www.bbc.co.uk/iplayer/categories/history/all?sort=dateavailable'},
  {'title':'Lifestyle','url':'http://www.bbc.co.uk/iplayer/categories/lifestyle/all?sort=dateavailable'},
  {'title':'Music','url':'http://www.bbc.co.uk/iplayer/categories/music/all?sort=dateavailable'},
  {'title':'News','url':'http://www.bbc.co.uk/iplayer/categories/news/all?sort=dateavailable'},
  {'title':'Science & Nature','url':'http://www.bbc.co.uk/iplayer/categories/science-and-nature/all?sort=dateavailable'},
  {'title':'Sport','url':'http://www.bbc.co.uk/iplayer/categories/sport/all?sort=dateavailable'},
]

def name():
  return 'BBC iPlayer'

def image():
  return 'icon.png'

def description():
  return "BBC iPlayer Channel (<a target='_blank' href='http://www.bbc.co.uk/iplayer'>http://www.bbc.co.uk/iplayer</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  return _extract(doc)

def search(q):
  doc = get_doc(_SEARCH_URL, params = { 'q':q })
  return _extract(doc)

def showmore(link):
  doc = get_doc(link)
  return _extract(doc)

def _extract(doc):
  rtree = select_all(doc, 'li.list-item')
  results = PlayItemList()
  for l in rtree:
    a = select_one(l, 'a')
    url = get_attr(a, 'href')
    if url is None or not url.startswith('/iplayer'):
      continue
    url = "http://www.bbc.co.uk" + url

    pdiv = select_one(l, 'div.primary')
    idiv = select_one(pdiv, 'div.r-image')
    img = get_attr(idiv, 'data-ip-src')

    sdiv = select_one(l, 'div.secondary')
    title = get_text(select_one(sdiv, 'div.title'))
    subtitle = get_text(select_one(sdiv, 'div.subtitle'))
    synopsis = get_text(select_one(sdiv, 'p.synopsis'))
    item = PlayItem(title, img, url, subtitle, synopsis)
    a = select_one(l, 'a.view-more-container')
    if a is not None:
      link = "http://bbc.co.uk" + a.get('href')
      item.add_action(MoreEpisodesAction(link, title))
    results.add(item)
  return results
