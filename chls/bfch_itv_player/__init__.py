import chanutils

_SEARCH_URL = 'https://www.itv.com/itvplayer/search/term/'
_PREFIX = 'https://www.itv.com'
_IMG = 'icon.png'
_IMGPATH = chanutils.img_prefix() + '/itv_player/' + _IMG

_FEEDLIST = [
  {'title':'Popular', 'url':'https://www.itv.com/itvplayer/categories/browse/popular'},
  {'title':'Children', 'url':'https://www.itv.com/itvplayer/categories/children/popular'},
  {'title':'Comedy', 'url':'https://www.itv.com/itvplayer/categories/comedy/popular'},
  {'title':'Drama & Soaps', 'url':'https://www.itv.com/itvplayer/categories/drama-soaps/popular'},
  {'title':'Entertainment', 'url':'https://www.itv.com/itvplayer/categories/entertainment/popular'},
  {'title':'Factual', 'url':'https://www.itv.com/itvplayer/categories/factual/popular'},
  {'title':'Films', 'url':'https://www.itv.com/itvplayer/categories/films/popular'},
  {'title':'Lifestyle', 'url':'https://www.itv.com/itvplayer/categories/lifestyle/popular'},
  {'title':'Sport', 'url':'https://www.itv.com/itvplayer/categories/sport/popular'},
]

def name():
  return 'ITV Player'

def image():
  return _IMG

def description():
   return "ITV Player Channel (<a target='_blank' href='https://www.itv.com/itvplayer/'>https://www.itv.com/itvplayer</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  doc = chanutils.get_doc(url)
  rtree = chanutils.select_all(doc, 'li.programme')
  results = chanutils.PlayItemList()
  for l in rtree:
    el = chanutils.select_one(l, ".programme-title a")
    url = _PREFIX + el.get('href')
    title = el.text
    el = chanutils.select_one(l, "img")
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    subtitle = None
    el = chanutils.select_one(l, ".episode-info span.episode-free")
    if el is not None:
      subtitle = el.text
    actions = None
    item = chanutils.PlayItem(title, img, url, subtitle)
    if (subtitle is not None) and (not subtitle.startswith("1 ")):
      item.add_action(chanutils.ShowmoreAction('More Episodes', url, title))
    results.add(item)
  return results

def search(q):
  q = q.replace(' ', '-')
  q = q.replace("'", '')
  doc = chanutils.get_doc(_SEARCH_URL + q)
  rtree = chanutils.select_all(doc, 'div.search-wrapper')
  results = chanutils.PlayItemList()
  for l in rtree:
    el = chanutils.select_one(l, "h4 a")
    url = el.get('href')
    title = el.text
    el = chanutils.select_one(l, "div.search-result-image a img")
    # images may be missing
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    el = chanutils.select_one(l, ".search-episode-count")
    matched = int(el.get('data-matched_episodes'))
    episodes = el.text.strip()
    episodes = int(episodes[0:episodes.find(' ')])
    action = None
    if episodes > matched:
      action = chanutils.ShowmoreAction('More Episodes', url, title)
    eps = chanutils.select_all(l, ".episode")
    for e in eps:
      el = chanutils.select_one(e, ".episode-title a")
      url = _PREFIX + el.get('href')
      subtitle = el.text
      el = chanutils.select_one(e, ".description")
      synopsis = el.text_content().strip()
      item = chanutils.PlayItem(title, img, url, subtitle, synopsis)
      results.add(item)
      if action:
        item.add_action(action)
        break
  return results

def showmore(link):
  doc = chanutils.get_doc(link)
  list = chanutils.select_all(doc, 'div.views-row')
  results = chanutils.PlayItemList()
  for l in list:
    el = chanutils.select_one(l, 'a')
    url = _PREFIX + el.get('href')
    el = chanutils.select_one(el, 'img')
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    el = chanutils.select_one(l, 'span.date-display-single')
    subtitle = el.text
    el = chanutils.select_one(l, 'div.field-season-number')
    title1 = el.text_content()
    el = chanutils.select_one(l, 'div.field-episode-number')
    title = title1 + " " + el.text_content()
    el = chanutils.select_one(l, 'div.field-name-field-short-synopsis')
    synopsis = el.text_content()
    item = chanutils.PlayItem(title, img, url, subtitle, synopsis)
    results.add(item)
  return results
