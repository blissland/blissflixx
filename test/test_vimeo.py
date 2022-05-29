# Path hack.
import sys, os
import pprint

main_path = os.path.abspath(".")
lib_path = os.path.abspath("lib")
print(f"{main_path=} {lib_path=}")
sys.path.append(main_path)
sys.path.append(lib_path)
from chls import bfch_vimeo

f = bfch_vimeo.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_vimeo.feed(2)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_vimeo.search("building")
pprint.pprint(f.to_dict())
print(len(f.to_dict()))
