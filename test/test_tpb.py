import chls/bfch_pirate_bay
import pprint

f = bfch_pirate_bay.feedlist()
pprint.pprint(f)
print(len(f))

f = bfch_pirate_bay.feed(0)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

f = bfch_pirate_bay.search('beasts')
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

