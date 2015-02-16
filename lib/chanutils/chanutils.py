import requests, lxml.html, re
import htmlentitydefs, urllib, random
from lxml.cssselect import CSSSelector

_PROXY_LIST = None

_HEADERS = {
  'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'accept-language':'en-GB,en-US;q=0.8,en;q=0.6',
  'cache-control':'max-age=0',
  'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
}

def _get_proxy_url():
  global _PROXY_LIST
  if _PROXY_LIST is None:
    _PROXY_LIST = get_json("http://blissflixx.rocks/feeds/proxies.php")
  p = random.randint(0, len(_PROXY_LIST) - 1)
  return _PROXY_LIST[p]['url']

def get(url, params=None, proxy=False):
  headers = _HEADERS
  if proxy:
    if params is not None:
      url = url + "?" + urllib.urlencode(params)
    params = {'url': url}
    url = _get_proxy_url()
    headers = {'origin': 'blissflixx'}
  r = requests.get(url, params=params, headers=headers, verify=False)
  if r.status_code >= 300:
    raise Exception("Request : '" + url + "' returned: " + str(r.status_code))
  return r

def post(url, payload, proxy=False):
  headers = _HEADERS
  r = requests.post(url, data=payload, headers=headers, verify=False)
  if r.status_code >= 300:
    raise Exception("Request : '" + url + "' returned: " + str(r.status_code))
  return r

def post_doc(url, payload, proxy=False):
  r = post(url, payload, proxy=proxy)
  return lxml.html.fromstring(r.text)

def get_doc(url, params=None, proxy=False):
  r = get(url, params=params, proxy=proxy)
  return lxml.html.fromstring(r.text)

def get_json(url, params=None, proxy=False):
  r = get(url, params=params, proxy=proxy)
  return r.json()

def select_one(tree, expr):
  sel = CSSSelector(expr)
  el = sel(tree)
  if isinstance(el, list) and len(el) > 0:
    return el[0]
  else:
    return None

def select_all(tree, expr):
  sel = CSSSelector(expr)
  return sel(tree)

def get_attr(el, name):
  if el is not None:
    return el.get(name)
  else:
    return None

def get_text(el):
  if el is not None:
    return el.text.strip()
  else:
    return None

def get_text_content(el):
  if el is not None:
    return el.text_content().strip()
  else:
    return None

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
