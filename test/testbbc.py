import bfch_bbc_iplayer
import pprint

f =  bfch_bbc_iplayer.feedlist()
pprint.pprint(f)
print(len(f))

f =  bfch_bbc_iplayer.feed(0)
pprint.pprint(f.to_dict())
print(len(f.to_dict()))

#f = bfch_twitch.search('flor')
#pprint.pprint(f.to_dict())
#print len(f.to_dict())
#
