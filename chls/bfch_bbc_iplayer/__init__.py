import chanutils

_SEARCH_URL = 'http://www.bbc.co.uk/iplayer/search'

_feedlist = [
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

def get_name():
  return 'iPlayer'

def get_image():
  return 'icon.png'

def get_description():
  return "BBC iPlayer Channel (<a target='_blank' href='http://www.bbc.co.uk/iplayer'>http://www.bbc.co.uk/iplayer</a>). Geo-restricted to UK."

def search(q):
  doc = chanutils.get_doc(_SEARCH_URL, params={'q':q})
  return _extract(doc)

def showmore(link):
  doc = chanutils.get_doc(link)
  return _extract(doc)

def get_feedlist():
  return _feedlist

def get_feed(idx):
  doc = chanutils.get_doc(_feedlist[idx]['url'])
  return _extract(doc)

def _extract(doc):
  rtree = chanutils.select_all(doc, 'li.list-item')
  results = chanutils.PlayItemList()
  for l in rtree:
    a = chanutils.select_one(l, 'a')
    if a is None:
      continue
    url = a.get('href')
    if not url.startswith('/iplayer'):
      continue
    url = "http://www.bbc.co.uk" + url

    pdiv = chanutils.select_one(l, 'div.primary')
    idiv = chanutils.select_one(pdiv, 'div.r-image')
    img = idiv.get('data-ip-src')

    sdiv = chanutils.select_one(l, 'div.secondary')
    title = chanutils.select_one(sdiv, 'div.title').text.strip()
    el = chanutils.select_one(sdiv, 'div.subtitle')
    subtitle = None
    if el is not None:
      subtitle = el.text
    synopsis = chanutils.select_one(sdiv, 'p.synopsis').text
    item = chanutils.PlayItem(title, img, url, subtitle, synopsis)
    a = chanutils.select_one(l, 'a.view-more-container')
    if a is not None:
      link = "http://bbc.co.uk" + a.get('href')
      item.add_action(chanutils.ShowmoreAction('More Episodes', link, title))
    results.add(item)
  return results
