#!/usr/bin/python
from os import path
import sys, os
LIB_PATH = path.join(path.abspath(path.dirname(__file__)), "lib")
sys.path.append(LIB_PATH)
import locations
sys.path.append(locations.CHAN_PATH)

import bfch_twitch
import pprint

f = bfch_twitch.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_twitch.feed(0)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_twitch.search('flor')
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

