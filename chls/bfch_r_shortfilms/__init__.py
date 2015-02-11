import chanutils.reddit

_SUBREDDIT = 'Shortfilms'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/Shortfilms.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/Shortfilms/new.json'},
]

def name():
  return 'Short Films'

def image():
  return "icon.png"

def description():
  return "Short Films from /r/Shortfilms subreddit (<a target='_blank' href='http://www.reddit.com/r/Shortfilms'>http://www.reddit.com/r/Shortfilms</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  return chanutils.reddit.get_feed(_FEEDLIST[idx])

def search(q):
  return chanutils.reddit.search(_SUBREDDIT, q)
