#!/usr/bin/python

import sys, requests, zipfile, io, socket
from argparse import ArgumentParser
from os import path
from xmlrpclib import ServerProxy, Transport
from httplib import HTTPConnection

OUT_DIR = "/tmp"

OPENSUB_TOKEN = None

langMap = {
    'bul':'bulgarian',
    'zho':'chinese',
    'hrv':'croatian',
    'dan':'danish',
    'nld':'dutch',
    'eng':'english',
    'fin':'finnish',
    'fre':'french',
    'deu':'german',
    'ell':'greek',
    'hun':'hungarian',
    'ita':'italian',
    'mkd':'macedonian',
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

def opensub_ok(r):
  status_code = int(r['status'][:3])
  if status_code > 301:
    error("Opensubtitles returned: " + str(status_code))

def opensub_connect():
  global OPENSUB_TOKEN
  con = ServerProxy("http://api.opensubtitles.org/xml-rpc",
                       transport=TimeoutTransport(10))
  # Use sibliminal user-agent
  r = con.LogIn('', '', 'eng', "subliminal v0.8.0")
  opensub_ok(r)
  OPENSUB_TOKEN = r['token']
  return con


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

def movie_subs(args):
  if args.imdb and args.lang in langMap:
    filename = yts_movie_subs(args.lang, args.imdb)
    if filename:
      return filename

def series_subs(args):
  c = opensub_connect()
  params = [{'query': args.title, 'season': args.season,
             'episode': args.episode, 'sublanguageid': args.lang}]
  r = c.SearchSubtitles(OPENSUB_TOKEN, params)
  if not r['data']:
    return None
  url = r['data'][0]['ZipDownloadLink']
  r = requests.get(url)
  if not r.ok:
    return None
  z = zipfile.ZipFile(io.BytesIO(r.content))
  info = z.infolist()[0]
  z.extract(info, OUT_DIR)
  return path.join(OUT_DIR, info.filename)

parser = ArgumentParser(description="Get subtitles for movies and TV series")
parser.add_argument('lang', help="Subtitle language")
parser.add_argument('-t', '--title', help="Movie title")
parser.add_argument('-y', '--year', type=int, help="Movie year")
parser.add_argument('-i', '--imdb', help="IMDB code")
parser.add_argument('-s', '--season', type=int, help="Series season")
parser.add_argument('-e', '--episode', type=int, help="Series episode")
args = parser.parse_args()

if args.season or args.episode:
  if not (args.title and args.season and args.episode):
    error("Must specify title, season and episode for series")
  filename = series_subs(args)
elif not (args.title or args.imdb):
  error("Must specify title or imdb code for movie")
else:
  filename = movie_subs(args)

if filename:
  print('{"filename":"' + filename + '"}')
else:
  print("{}")
