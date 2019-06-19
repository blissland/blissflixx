import chanutils.torrent
from chanutils import get_doc, get_json, select_all, select_one, get_attr, new_session
from chanutils import get_text, get_text_content, replace_entity, byte_size
from chanutils import movie_title_year, series_season_episode
from playitem import TorrentPlayItem, PlayItemList

_SEARCH_URL = "https://katcr.co/katsearch/page/1/"
_CAT_WHITELIST = ['Movies', 'TV', 'Anime', 'Music']

_FEEDLIST = [
  {'title':'Movies', 'url':'https://katcr.co/torrents/top-100-movies-uploads.html'},
  {'title':'TV', 'url':'https://katcr.co/torrents/top-100-tv-uploads.html'},
  {'title':'Anime', 'url':'https://katcr.co/torrents/top-100-anime-uploads.html'},
  {'title':'Music', 'url':'https://katcr.co/torrents/top-100-music-uploads.html'}
]

def name():
  return 'Kickass Torrents'

def image():
  return 'icon.png'

def description():
  return "Kickass Torrents Channel (<a target='_blank' href='https://katcr.co'>https://katcr.co</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  return _extract(doc)

def _extract_list(doc):
  rtree = select_all(doc, 'tr')
  results = []
  for l in rtree:
    el = select_one(l, 'a.torrents_table__torrent_title > b')
    # tr is not a result
    if el is None:    
      continue
    title = get_text(el)
    el = select_one(l, 'a[title="Torrent magnet link"]')
    # DMCA takedown
    if el is None:    
      continue
    url = get_attr(el, 'href')
    img = '/img/icons/film.svg'    
    el = select_one(l, 'span.torrents_table__upload_info > a.text--muted > strong')
    cat = get_text(el)    
    if not (cat in _CAT_WHITELIST):
      continue
    if cat.endswith('Music'):
      img = '/img/icons/music.svg'
    subs = None
    if cat == 'Movies':
      subs = movie_title_year(title)
    elif cat == 'TV':
      subs = series_season_episode(title)      
    el = select_one(l, 'td[data-title="Size"]')
    size = get_text_content(el)
    el = select_one(l, 'td[data-title="Seed"]')
    seeds = get_text(el)
    el = select_one(l, 'td[data-title="Leech"]')
    peers = get_text(el)    
    result = {}
    result['title'] = title 
    result['url'] = url
    result['img'] = img
    result['subs'] = subs
    result['size'] = size
    result['seeds'] = seeds
    result['peers'] = peers
    results.append(result)
  return results

def _extract(doc):
  result_list = _extract_list(doc)
  results = PlayItemList()
  for l in result_list:
    subtitle = chanutils.torrent.subtitle(l['size'], l['seeds'], l['peers'])
    results.add(TorrentPlayItem(l['title'], l['img'], l['url'], subtitle, subs=l['subs']))
  return results

def _extract_sort(doc):
  result_list = _extract_list(doc)
  # sort by seeds (removing dots and commas)
  result_list.sort(key=lambda el: int(el['seeds'].translate(None, ".,")), reverse = True)
  results = PlayItemList()
  for l in result_list:
    subtitle = chanutils.torrent.subtitle(l['size'], l['seeds'], l['peers'])
    results.add(TorrentPlayItem(l['title'], l['img'], l['url'], subtitle, subs=l['subs']))
  return results

def search(q):
  session = new_session()
  doc = get_doc(_SEARCH_URL + q, session = session)  
  title = get_text(select_one(doc, 'head > title'))
  if title.startswith('Cookies - '):
    doc = get_doc(_SEARCH_URL + q, session = session)  
  return _extract_sort(doc)
