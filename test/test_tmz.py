import bfch_tmz
import pprint

f = bfch_tmz.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_tmz.feed(0)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_tmz.search('bodak')
pprint.pprint(f.to_dict())
print(len(f.to_dict()))
