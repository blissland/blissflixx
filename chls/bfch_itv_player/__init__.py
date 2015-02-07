from chanutils import get_doc, select_one, select_all, img_prefix

_SEARCH_URL = 'https://www.itv.com/itvplayer/search/term/'
_PREFIX = 'https://www.itv.com'
_IMG = 'icon.png'
_IMGPATH = img_prefix() + '/itv_player/' + _IMG

_feedlist = [
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

def get_name():
  return 'ITV Player'

def get_image():
  return _IMG

def get_feedlist():
  return _feedlist

def get_feed(idx):
  url = _feedlist[idx]['url']
  doc = get_doc(url)
  rtree = select_all(doc, 'li.programme')
  results = []
  for l in rtree:
    el = select_one(l, ".programme-title a")
    url = _PREFIX + el.get('href')
    title = el.text
    el = select_one(l, "img")
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    subtitle = None
    el = select_one(l, ".episode-info span.episode-free")
    if el is not None:
      subtitle = el.text
    actions = None
    if (subtitle is not None) and (not subtitle.startswith("1 ")):
      actions = [{'label':'More Episodes', 'type':'showmore', 'link':url,
                  'title': title}]
    results.append({ 'title':title, 'img':img, 'url':url,
                     'subtitle':subtitle, 'actions':actions })
  return results

def search(q):
  q = q.replace(' ', '-')
  q = q.replace("'", '')
  doc = get_doc(_SEARCH_URL + q)
  rtree = select_all(doc, 'div.search-wrapper')
  results = []
  for l in rtree:
    el = select_one(l, "h4 a")
    url = el.get('href')
    title = el.text
    el = select_one(l, "div.search-result-image a img")
    # images may be missing
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    el = select_one(l, ".search-episode-count")
    matched = int(el.get('data-matched_episodes'))
    episodes = el.text.strip()
    episodes = int(episodes[0:episodes.find(' ')])
    actions = None
    if episodes > matched:
      actions = [{'label':'More Episodes', 'type':'showmore', 'link':url,
                  'title': title}]
    eps = select_all(l, ".episode")
    for e in eps:
      el = select_one(e, ".episode-title a")
      url = _PREFIX + el.get('href')
      subtitle = el.text
      el = select_one(e, ".description")
      synopsis = el.text_content().strip()
      results.append({ 'title':title, 'img':img, 'url':url,
                     'subtitle':subtitle, 'synopsis':synopsis,
                     'actions':actions })
      if actions:
        break

  return results

def showmore(link):
  doc = get_doc(link)
  list = select_all(doc, 'div.views-row')
  results = []
  for l in list:
    el = select_one(l, 'a')
    url = _PREFIX + el.get('href')
    el = select_one(el, 'img')
    img = _IMGPATH
    if el is not None:
      img = el.get('src')
    el = select_one(l, 'span.date-display-single')
    subtitle = el.text
    el = select_one(l, 'div.field-season-number')
    title1 = el.text_content()
    el = select_one(l, 'div.field-episode-number')
    title = title1 + " " + el.text_content()
    el = select_one(l, 'div.field-name-field-short-synopsis')
    synopsis = el.text_content()
    results.append({ 'title':title, 'img':img, 'url':url,
                      'subtitle':subtitle, 'synopsis':synopsis })

  return results
