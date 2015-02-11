import chanutils.reddit

_SUBREDDIT = 'videos'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/videos.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/videos/new.json'},
]

def name():
  return 'Reddit Videos'

def image():
  return "icon.png"

def description():
  return "All the latest videos from /r/videos subreddit (<a target='_blank' href='http://www.reddit.com/r/videos'>http://www.reddit.com/r/videos</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  return chanutils.reddit.get_feed(_FEEDLIST[idx])

def search(q):
  return chanutils.reddit.search(_SUBREDDIT, q)
