# Path hack.
import sys, os

main_path = os.path.abspath(".")
lib_path = os.path.abspath("lib")
print(f"{main_path=} {lib_path=}")
sys.path.append(main_path)
sys.path.append(lib_path)
from chls import bfch_pirate_bay
import pprint

f = bfch_pirate_bay.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_pirate_bay.feed(0)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_pirate_bay.search("building")
# pprint.pprint(f.to_dict())
print(len(f.to_dict()))
