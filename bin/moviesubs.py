#!/usr/bin/python
import sys
from subliminal.video import Movie
from subliminal.api import list_subtitles, download_best_subtitles, save_subtitles
from babelfish import Language

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

print("LANG", lang)
print("TITLE", title)
print("YEAR", year)

m = Movie(title + '.mp4', title, year=year)
l = Language(lang)

subtitles = download_best_subtitles(set((m,)), set((l,)))
save_subtitles(subtitles, directory='/tmp') 
