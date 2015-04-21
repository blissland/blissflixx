#!/usr/bin/python
import warnings
warnings.simplefilter("ignore", UserWarning)

import sys, os
from os import path

subpath = path.dirname(path.abspath(path.dirname(__file__)))
subpath = path.join(subpath, "lib", "subliminal")
sys.path.insert(0, subpath)

from subliminal.video import Movie
from subliminal.api import download_best_subtitles, save_subtitles
from subliminal.subtitle import get_subtitle_path
from babelfish import Language
import guessit
import requests, zipfile, io

OUT_DIR = "/tmp"

languageMapping = {
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

def out_error(msg):
  print('{"error":"' + msg + '"}')
  return True

def out_file(filepath):
  print('{"filename":"' + filepath + '"}')
  return True

def out_nosubs():
  print("{}")

def yts_sub(lang, imdb):
  if lang in languageMapping:
    lang = languageMapping[lang]
  else:
    return False
  r = requests.get("http://api.yifysubtitles.com/subs/" + imdb)
  if not r.ok:
    return out_error("yify subs api1 error: " + str(r.status_code))
  data = r.json()
  if not 'subs' in data:
    return False
  subs = r.json()['subs'][imdb]
  if not lang in subs:
    return False
  subs = subs[lang]
  url = "http://www.yifysubtitles.com" + subs[0]['url']
  r = requests.get(url)
  if not r.ok:
    return out_error("yify subs api2 error: " + str(r.status_code))
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall(OUT_DIR)
  filename = path.join(OUT_DIR, z.infolist()[0].filename)
  return out_file(filename)

def usage():
  print "Usage:"
  print "\t" + sys.argv[0] + " lang title [year] [imdbid]"
  sys.exit(1)

numargs = len(sys.argv)
if numargs < 3 or numargs > 5:
  usage()

lang = sys.argv[1]
title = sys.argv[2]
year=None
imdb=None
if numargs >= 4:
  arg3 = sys.argv[3]
  if len(arg3) == 4:
    year = int(arg3)
  else:
    imdb = arg3
if numargs == 5:
  if year is None:
    year = int(sys.argv[4])
  else:
    imdb = sys.argv[4]
print(lang, title, year, imdb)

if imdb:
  if yts_sub(lang, imdb):
    sys.exit(0)

m = Movie(title + '.mp4', title, year=year)
l = Language(lang)

pathname = None
subtitles = download_best_subtitles(set((m,)), set((l,)))
for video, video_subtitles in subtitles.items():
  for video_subtitle in video_subtitles:
     filename = get_subtitle_path(video.name, video_subtitle.language)
     pathname = os.path.join(OUT_DIR, filename)
     break
save_subtitles(subtitles, directory=OUT_DIR, encoding='utf-8')
if pathname is not None:
  out_file(pathname)
else:
  out_nosubs()
