import re
from torrentparse import TorrentParser
import base64
import subprocess
import chanutils

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
  s = subprocess.check_output(["peerflix", link, "-l"])
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
    except Exception:
      pass
  if not files:
    files = peerflix_metadata(link)
  return files

def showmore(link):
  # More reliable (although slower) to use magnet link
  link = torrent2magnet(link)
  files = torrent_files(link)
  if not files:
    raise Exception("Unable to retrieve torrent files")
  results = chanutils.PlayItemList()
  idx = 0
  for f in files:
    subtitle = ''
    if isinstance(f[1], basestring):
      subtitle = 'Size: ' + f[1]
    else:
      subtitle = 'Size: ' + chanutils.byte_size(f[1])
    url = link
    if link.find('?') > -1:
      url = url + '&'
    else:
      url = url + '?'
    url = url + "fileidx=" + str(idx)
    img = '/img/icons/file-o.svg'
    idx = idx + 1
    item = chanutils.PlayItem(f[0], img, url)
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
  return chanutils.ShowmoreAction('Show Files', url, title)

def subtitle(size, seeds, peers):
  subtitle = 'Size: ' + str(size)
  subtitle = subtitle + ', Seeds: ' + str(seeds)
  subtitle = subtitle + ', Peers: ' + str(peers)
  return subtitle
