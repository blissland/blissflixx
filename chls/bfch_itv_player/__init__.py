from chanutils import get_doc, select_all, select_one
from chanutils import get_attr, get_text, get_text_content
from playitem import PlayItem, PlayItemList, MoreEpisodesAction

_PREFIX = 'https://www.itv.com'
_SEARCH_URL = _PREFIX + '/itvplayer/search/term/'

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
  return 'icon.png'

def description():
   return "ITV Player Channel (<a target='_blank' href='https://www.itv.com/itvplayer/'>https://www.itv.com/itvplayer</a>). Geo-restricted to UK."

def feedlist():
  return _FEEDLIST

def feed(idx):
  url = _FEEDLIST[idx]['url']
  doc = get_doc(url)
  rtree = select_all(doc, 'li.programme')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, '.programme-title a')
    url = _PREFIX + get_attr(el, 'href')
    title = get_text(el)
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    subtitle = get_text(select_one(l, '.episode-info span.episode-free'))
    item = PlayItem(title, img, url, subtitle)
    if (subtitle is not None) and (not subtitle.startswith('1 ')):
      item.add_action(MoreEpisodesAction(url, title))
    results.add(item)
  return results

def search(q):
  q = q.replace(' ', '-')
  q = q.replace("'", '')
  doc = get_doc(_SEARCH_URL + q)
  rtree = select_all(doc, 'div.search-wrapper')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'h4 a')
    url = get_attr(el, 'href')
    title = get_text(el)
    el = select_one(l, "div.search-result-image a img")
    img = get_attr(el, 'src')
    el = select_one(l, ".search-episode-count")
    matched = int(get_attr(el, 'data-matched_episodes'))
    episodes = get_text(el)
    episodes = int(episodes[0:episodes.find(' ')])
    action = None
    if episodes > matched:
      action = MoreEpisodesAction(url, title)
    eps = select_all(l, ".episode")
    for e in eps:
      el = select_one(e, ".episode-title a")
      url = _PREFIX + get_attr(el, 'href')
      subtitle = get_text(el)
      el = select_one(e, ".description")
      synopsis = get_text_content(el)
      item = PlayItem(title, img, url, subtitle, synopsis)
      results.add(item)
      if action:
        item.add_action(action)
        break
  return results

def showmore(link):
  doc = get_doc(link)
  rtree = select_all(doc, 'div.views-row')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    url = _PREFIX + get_attr(el, 'href')
    el = select_one(el, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'span.date-display-single')
    subtitle = get_text(el)
    el = select_one(l, 'div.field-season-number')
    title1 = get_text_content(el)
    el = select_one(l, 'div.field-episode-number')
    title = title1 + " " + get_text_content(el)
    el = select_one(l, 'div.field-name-field-short-synopsis')
    synopsis = get_text_content(el)
    item = PlayItem(title, img, url, subtitle, synopsis)
    results.add(item)
  return results
