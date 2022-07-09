# Path hack.
import sys, os
from pprint import pp

main_path = os.path.abspath(".")
lib_path = os.path.abspath("lib")
print(f"{main_path=} {lib_path=}")
sys.path.append(main_path)
sys.path.append(lib_path)
from chls import bfch_iptv_org as bfch_iptv_org

f = bfch_iptv_org.feedlist()
# pp(f)
# print(len(f))

f = bfch_iptv_org.feed(0)
# pprint.pprint(f)
print(type(f))
# print(len(f))
# print(type(f[0]))
# print(len(f[0]))
# pp(f[0:4])
# chids = [s["channel"] for s in f[0:4]]
# pp(chids)
# print(len(chids))

f = bfch_iptv_org.search("kids")
pp(f)
print(type(f))
# print(len(f))
