import chanutils.reddit

_SUBREDDIT = 'happycrowds'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/happycrowds.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/happycrowds/new.json'},
]

def name():
  return 'Happy Crowds'

def image():
  return "icon.png"

def description():
  return "Happy crowd videos from /r/happycrowds subreddit (<a target='_blank' href='http://www.reddit.com/r/happycrowds'>http://www.reddit.com/r/happycrowds</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  return chanutils.reddit.get_feed(_FEEDLIST[idx])

def search(q):
  return chanutils.reddit.search(_SUBREDDIT, q)
