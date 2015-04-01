import re, base64, subprocess, chanutils, playitem, urlparse
from torrentparse import TorrentParser

hash_re = re.compile("xt=urn:btih:([A-Za-z0-9]+)")
base32_re = re.compile("[A-Z2-7]{32}")
valid_re = re.compile("[A-F0-9]{40}")

torr_sites = ("torcache.net", "torrage.com", "zoink.it")

def torrent_from_hash(hashid):
  path = "/torrent/" + hashid + ".torrent"
  for site in torr_sites:
    try:
      r = chanutils.get("http://" + site + path)
      return r.content
    except Exception:
      pass
  return None

def magnet2torrent(link):
  matches = hash_re.search(link)
  if not matches or len(matches.groups()) != 1:
    raise Exception("Unable to find magnet hash")
  hashid = matches.group(1).upper()

  #If hash is base32, convert it to base16
  if len(hashid) == 32 and base32_re.search(hashid):
    s = base64.b32decode(hashid)
    hashid = base64.b16encode(s)
  elif not (len(hashid) == 40 and valid_re.search(hashid)):
    raise Exception("Invalid magnet hash")

  return torrent_from_hash(hashid)

def peerflix_metadata(link):
  # stdin=PIPE so peerflix does not enter interactive mode
  s = subprocess.check_output(["peerflix", link, "-l"], stdin=PIPE)
  lines = s.split('\n')
  files = []
  for l in lines:
    delim = l.rfind(':')
    if delim == -1:
      break
    files.append((l[20:delim-6], l[delim+7:-5]))
  return files

def torrent_files(link):
  if link.startswith("magnet:"):
    torrent = magnet2torrent(link)
  else:
    # Remove any parameters from torrent link
    # as some sites may not download if wrong
    idx = link.find('?')
    if idx > -1:
      link = link[:idx]
    r = chanutils.get(link)
    torrent = r.content

  files = None
  if torrent:
    try:
      parser = TorrentParser(torrent)
      files =  parser.get_files_details()
    except Exception, e:
      pass
  if not files:
    files = peerflix_metadata(link)
  return files

def showmore(link):
  files = torrent_files(link)
  if not files:
    raise Exception("Unable to retrieve torrent files")
  results = playitem.PlayItemList()
  idx = 0
  for f in files:
    subtitle = ''
    if isinstance(f[1], basestring):
      subtitle = 'Size: ' + f[1]
    else:
      subtitle = 'Size: ' + chanutils.byte_size(f[1])
    url = set_torridx(link, idx)
    img = '/img/icons/file-o.svg'
    idx = idx + 1
    item = playitem.PlayItem(f[0], img, url, subtitle)
    results.add(item)
  return results

TRACKERS = ("udp://open.demonii.com:1337/announce", "udp://tracker.istole.it:6969/announce", "udp://www.eddie4.nl:6969/announce", "udp://coppersurfer.tk:6969/announce", "udp://tracker.btzoo.eu:80/announce", "http://explodie.org:6969/announce", "udp://9.rarbg.me:2710/announce")
HASH_RE = re.compile("[A-F0-9]{40}")

def torrent2magnet(torrent):
  if torrent.startswith("magnet"):
    return torrent
  matches = HASH_RE.search(torrent.upper())
  if not matches:
    return torrent
  magnet = "magnet:?xt=urn:btih:" + matches.group(0) + "&tr="
  return  magnet + "&tr=".join(TRACKERS)

def showmore_action(url, title):
  return playitem.ShowmoreAction('View Files', url, title)

def subtitle(size, seeds, peers):
  subtitle = 'Size: ' + str(size)
  subtitle = subtitle + ', Seeds: ' + str(seeds)
  subtitle = subtitle + ', Peers: ' + str(peers)
  return subtitle

def is_torrent(url):
  obj = urlparse.urlparse(url)
  if obj.path.endswith(".torrent") or url.startswith('magnet:'):
    return True
  else:
    return False

def torrent_idx(url):
  obj = urlparse.urlparse(url)
  idx = None
  if obj.query:
    params = urlparse.parse_qs(obj.query)
    if 'bf_torr_idx' in params:
      idx = params['bf_torr_idx'][0]
  if idx is not None:
    idx = int(idx)
  return idx

def set_torridx(url, idx=-1):
  if is_torrent_url(url):
    return re.sub('bf_torr_idx\=-?\d+', 'bf_torr_idx=' + str(idx), url)
  else:
    if url.find('?') > -1:
      url = url + '&'
    else:
      url = url + '?'
    return url + "bf_torr_idx=" + str(idx)

def is_torrent_url(url):
  return "bf_torr_idx=" in url

def is_main(url):
  return torrent_idx(url) == -1

