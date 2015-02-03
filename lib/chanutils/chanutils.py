import requests
import lxml.html
from lxml.cssselect import CSSSelector
import re
import htmlentitydefs
import urllib
import random

PROXY_LIST = None

def _get_proxy_url():
  global PROXY_LIST
  if PROXY_LIST is None:
    PROXY_LIST = get_json("http://blissflixx.rocks/feeds/proxies.php")
  p = random.randint(0, len(PROXY_LIST) - 1)
  return PROXY_LIST[p]['url']

def get(url, params=None, proxy=False):
  # Pretend to be a real browser
  headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-language':'en-GB,en-US;q=0.8,en;q=0.6',
    'cache-control':'max-age=0',
    'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
  }
  if proxy:
    if params:
      url = url + "?" + urllib.urlencode(params)
    params = {}
    params['url'] = url
    url = _get_proxy_url()
    headers['origin'] = 'blissflixx'
  r = requests.get(url, params=params, headers=headers)
  if r.status_code >= 300:
    raise Exception("Request : '" + url + "' returned: " + str(r.status_code) + " - " + r.text)
  return r

def get_doc(url, params=None, proxy=False):
  r = get(url, params=params, proxy=proxy)
  return lxml.html.fromstring(r.text)

def get_json(url, params=None, proxy=False):
  r = get(url, params=params, proxy=proxy)
  try:
    return r.json()
  except Exception, e:
    print(r.text)
    raise 

def select_one(tree, expr):
  sel = CSSSelector(expr)
  el = sel(tree)
  # A failed selection seems to return empty list
  if isinstance(el, list) and len(el) == 0:
    return None
  if el:
    el = el[0]
  return el

def select_all(tree, expr):
  sel = CSSSelector(expr)
  return sel(tree)

def byte_size(num, suffix='B'):
  for unit in ['','K','M','G','T','P','E','Z']:
    if abs(num) < 1024.0:
      return "%3.1f %s%s" % (num, unit, suffix)
    num /= 1024.0
  return "%.1f %s%s" % (num, 'Y', suffix)

def replace_entity(text):
  def fixup(m):
    text = m.group(0)
    if text[:2] == "&#":
      # character reference
      try:
        if text[:3] == "&#x":
          return unichr(int(text[3:-1], 16))
        else:
          return unichr(int(text[2:-1]))
      except ValueError:
        pass
    else:
      # named entity
      try:
        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
      except KeyError:
        pass
      return text # leave as is
  return re.sub("&#?\w+;", fixup, text)

action = {'label':'Add To Playlist', 'type':'addplaylist'}

def add_playitem_actions(item):
  if 'actions' in item and item['actions'] is not None:
    item['actions'].append(action)
  else:
    item['actions'] = [action]

def img_prefix():
  return "/api/chanimage"
