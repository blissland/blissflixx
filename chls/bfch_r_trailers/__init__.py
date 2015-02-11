import chanutils.reddit

_SUBREDDIT = 'trailers'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/trailers.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/trailers/new.json'},
]

def name():
  return 'Movie Trailers'

def image():
  return "icon.png"

def description():
  return "All the latest movie trailers from /r/trailers subreddit (<a target='_blank' href='http://www.reddit.com/r/trailers'>http://www.reddit.com/r/trailers</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  return chanutils.reddit.get_feed(_FEEDLIST[idx])

def search(q):
  return chanutils.reddit.search(_SUBREDDIT, q)
