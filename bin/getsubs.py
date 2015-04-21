#!/usr/bin/python

import sys, requests, zipfile, io
from argparse import ArgumentParser
from os import path

OUT_DIR = "/tmp"

langMap = {
    'bul':'bulgarian',
    'zho':'chinese',
    'hrv':'croatian',
    'dan':'danish',
    'nld':'dutch',
    'eng':'english',
    'fin':'finnish',
    'fra':'french',
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
  print "Series subs"

def error(msg):
  print('{"error":"' + msg + '"}')
  sys.exit(1)

parser = ArgumentParser(description="Get subtitles for movies and TV series")
parser.add_argument('lang', help="Subtitle language")
parser.add_argument('-t', '--title', help="Movie title")
parser.add_argument('-y', '--year', help="Movie year")
parser.add_argument('-i', '--imdb', help="IMDB code")
parser.add_argument('-s', '--season', help="Series season")
parser.add_argument('-e', '--episode', help="Series episode")
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
