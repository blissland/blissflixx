from chanutils import get_json, img_prefix
import chanutils.reddit

_SUBREDDIT = 'videos'
_IMG = 'icon.png'
_IMGPATH = img_prefix() + '/bfch_r_' + _SUBREDDIT + '/' + _IMG

_feedlist = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/videos.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/videos/new.json'},
]

def get_name():
  return 'Reddit Videos'

def get_image():
  return _IMG

def search(q):
  data = chanutils.reddit.search(_SUBREDDIT, q)
  return chanutils.reddit.extract(data, thumbnail = _IMGPATH)

def get_feedlist():
  return _feedlist

def get_feed(idx):
  data = get_json(_feedlist[idx]['url'])
  return chanutils.reddit.extract(data, thumbnail = _IMGPATH)
