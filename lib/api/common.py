from urlparse import urlparse, parse_qs

class ApiError(Exception):
  pass

def is_torrent(url):
  obj = urlparse(url)
  if obj.path.endswith(".torrent") or url.startswith('magnet:'):
    return True
  else:
    return False

def torrent_idx(url):
  obj = urlparse(url)
  idx = None
  if obj.query:
    params = parse_qs(obj.query)
    if 'fileidx' in params:
      idx = params['fileidx'][0]
  return idx
