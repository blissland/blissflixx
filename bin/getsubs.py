#!/usr/bin/python

import sys, requests, zipfile, io, socket, zlib
from argparse import ArgumentParser
from os import path
from xmlrpclib import ServerProxy, Transport
from httplib import HTTPConnection
from base64 import b64decode

OUT_DIR = "/tmp"

langMap = {
    'bul':'bulgarian',
    'chi':'chinese',
    'hrv':'croatian',
    'dan':'danish',
    'dut':'dutch',
    'eng':'english',
    'fin':'finnish',
    'fre':'french',
    'ger':'german',
    'ell':'greek',
    'hun':'hungarian',
    'ita':'italian',
    'mac':'macedonian',
    'pol':'polish',
    'por':'portuguese',
    'srp':'serbian',
    'slv':'slovenian',
    'spa':'spanish',
}

def error(msg):
  print('{"error":"' + msg + '"}')
  sys.exit(1)

class TimeoutTransport(Transport, object):
  def __init__(self, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *args, **kwargs):
    super(TimeoutTransport, self).__init__(*args, **kwargs)
    self.timeout = timeout

  def make_connection(self, host):
    h = HTTPConnection(host, timeout=self.timeout)
    return h

class OpensubSession(object):
  def __init__(self):
    self.con = ServerProxy("http://api.opensubtitles.org/xml-rpc",
                           transport=TimeoutTransport(10))
    # Use sibliminal user-agent
    r = self.con.LogIn('blissflixx', 'PREV-BLUE-SCOPE-FEAR', 'eng', "subliminal v0.8.0")
    self.ok(r)
    self.token = r['token']

  def search(self, params):
    r = self.con.SearchSubtitles(self.token, params)
    self.ok(r)
    return r['data']

  def decode(self, content, lang):
    encodings = ['utf-8']

    # add language-specific encodings
    if lang == 'zho':
      encodings.extend(['gb18030', 'big5'])
    elif lang == 'jpn':
      encodings.append('shift-jis')
    elif lang == 'ara':
      encodings.append('windows-1256')
    elif lang == 'heb':
      encodings.append('windows-1255')
    elif lang == 'tur':
      encodings.extend(['iso-8859-9', 'windows-1254'])
    elif lang == 'pol' or lang == 'hrv':
      # Eastern European Group 1
      encodings.extend(['windows-1250'])
    elif lang == 'bul':
      # Eastern European Group 2
      encodings.extend(['windows-1251'])
    else:
      # Western European (windows-1252)
      encodings.append('latin-1')

    for encoding in encodings:
      try:
        return content.decode(encoding)
      except UnicodeDecodeError:
        pass

    error("Could not decode subtitles")

  def download(self, lang, subid, subname):
    r = self.con.DownloadSubtitles(self.token, [subid])
    self.ok(r)
    if not r['data']:
      return error("Unable to download subs")
    content = zlib.decompress(b64decode(r['data'][0]['data']), 47)
    # Fix line endings
    content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    text = self.decode(content, lang)
    subs_path = path.join(OUT_DIR, subname)
    with io.open(subs_path, 'w', encoding="utf-8") as f:
      f.write(text)
    return subs_path

  def ok(self, r):
    status_code = int(r['status'][:3])
    if status_code > 301:
      error("Opensubtitles returned: " + str(status_code))

def yts_movie_subs(lang, imdb):
  r = requests.get("http://api.yifysubtitles.com/subs/" + imdb)
  if not r.ok:
    r = requests.get("http://api.ysubs.com/subs/" + imdb)
    if not r.ok:
      return None
  data = r.json()
  if not 'subs' in data:
    return None
  subs = r.json()['subs'][imdb]
  lang = langMap[lang]
  if not lang in subs:
    return None
  subs = subs[lang]
  url = "http://www.yifysubtitles.com" + subs[0]['url']
  r = requests.get(url)
  if not r.ok:
    return None
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall(OUT_DIR)
  return path.join(OUT_DIR, z.infolist()[0].filename)

def opensub_movie_subs(lang, title, year, imdb):
  sess = OpensubSession()
  results = None
  if imdb:
    if imdb[0:2] == 'tt':
      imdb = imdb[2:]
    results = sess.search([{'imdbid':imdb, 'sublanguageid': lang}])
  else:
    query = title
    if year:
      query = query + " (" + str(year) + ")"
    results = sess.search([{'query':query, 'sublanguageid': lang}])
  if not results:
    return None
  maxcnt = -1 
  chosen = None
  for r in results:
    if r['SubFormat'] != 'srt':
      continue
    if r['MovieKind'] != 'movie':
      continue
    if year and int(r['MovieYear']) != year:
      continue

    # Use YIFY above all others
    if 'YIFY' in r['SubFileName']:
      chosen = r
      break

    #cnt = int(r['SubDownloadsCnt'])
    cnt = float(r['SubRating'])
    if cnt > maxcnt:
      chosen = r
      maxcnt = cnt

  if chosen:
    return sess.download(lang, chosen['IDSubtitleFile'], chosen['SubFileName'])
  else:
    return None

def movie_subs(args):
  if args.imdb and args.lang in langMap:
    filename = yts_movie_subs(args.lang, args.imdb)
    if filename:
      return filename
  return opensub_movie_subs(args.lang, args.title, args.year, args.imdb)

def series_subs(args):
  params = [{'query': args.title, 'season': args.season,
             'episode': args.episode, 'sublanguageid': args.lang}]
  sess = OpensubSession()
  results = sess.search(params)
  if not results:
    return None
  chosen = results[0]
  return sess.download(args.lang, chosen['IDSubtitleFile'],
                       chosen['SubFileName'])

parser = ArgumentParser(description="Get subtitles for movies and TV series")
parser.add_argument('lang', help="Subtitle language")
parser.add_argument('-t', '--title', help="Movie title")
parser.add_argument('-y', '--year', type=int, help="Movie year")
parser.add_argument('-i', '--imdb', help="IMDB code")
parser.add_argument('-s', '--season', type=int, help="Series season")
parser.add_argument('-e', '--episode', type=int, help="Series episode")
args = parser.parse_args()

is_movie = True
if args.season or args.episode:
  if not (args.title and args.season and args.episode):
    error("Must specify title, season and episode for series")
  is_movie = False
elif not (args.title or args.imdb):
  error("Must specify title or imdb code for movie")

filename = None
for i in xrange(3):
  try:
    if is_movie:
      filename = movie_subs(args)
    else:
      filename = series_subs(args)
    break
  except Exception, e:
    filename = "ERROR: " + str(e)

if filename is None:
  print("{}")
elif filename.startswith("ERROR:"):
  error(filename[7:])
elif filename:
  print('{"filename":"' + filename + '"}')
else:
  print("{}")
