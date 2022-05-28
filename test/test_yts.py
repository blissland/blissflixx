# Path hack.
import sys, os
import pprint

main_path = os.path.abspath(".")
lib_path = os.path.abspath("lib")
print(f"{main_path=} {lib_path=}")
sys.path.append(main_path)
sys.path.append(lib_path)
from chls import bfch_yts_torrents

f = bfch_yts_torrents.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_yts_torrents.feed(1)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_yts_torrents.search("building")
pprint.pprint(f.to_dict())
print(len(f.to_dict()))
