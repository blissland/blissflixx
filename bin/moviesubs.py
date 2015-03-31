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

OUT_DIR = "/tmp"

def usage():
  print "Usage: " + sys.argv[0] + " lang title [year]"
  sys.exit(1)

numargs = len(sys.argv)
if numargs < 3 or numargs > 4:
  usage()

lang = sys.argv[1]
title = sys.argv[2]
year=None
if numargs == 4:
  year = int(sys.argv[3])

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
  print('{"filename":"' + pathname + '"}')
else:
  print("{}")
