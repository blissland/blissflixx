import chanutils.reddit

_SUBREDDIT = 'fullmoviesonyoutube'

_FEEDLIST = [
  {'title':'Latest', 'url':'http://www.reddit.com/r/fullmoviesonyoutube.json'},
  {'title':'Action', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AAction&sort=top&restrict_sr=on'},
  {'title':'Adventure', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AAdventure&sort=top&restrict_sr=on&t=all'},
  {'title':'Animation', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AAnimation&sort=top&restrict_sr=on&t=all'},
  {'title':'Biography', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ABiography&sort=top&restrict_sr=on&t=all'},
  {'title':'Comedy', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AComedy&sort=top&restrict_sr=on&t=all'},
  {'title':'Crime', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ACrime&sort=top&restrict_sr=on&t=all'},
  {'title':'Documentary', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ADocumentary&sort=top&restrict_sr=on&t=all'},
  {'title':'Drama', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ADrama&sort=top&restrict_sr=on&t=all'},
  {'title':'Family', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AFamily&sort=top&restrict_sr=on&t=all'},
  {'title':'Fantasy', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AFantasy&sort=top&restrict_sr=on&t=all'},
  {'title':'Film-Noir', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ANoir&sort=top&restrict_sr=on&t=all'},
  {'title':'History', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AHistory&sort=top&restrict_sr=on&t=all'},
  {'title':'Horror', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AHorror&sort=top&restrict_sr=on&t=all'},
  {'title':'Misc/Adult', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AMisc+OR+flair%3AAdult&sort=top&restrict_sr=on'},
  {'title':'Musical', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AMusical&sort=top&restrict_sr=on&t=all'},
  {'title':'Mystery', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AMystery&sort=top&restrict_sr=on&t=all'},
  {'title':'Romance', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ARomance&sort=top&restrict_sr=on&t=all'},
  {'title':'Sci-Fi', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ASci-Fi&sort=top&restrict_sr=on&t=all'},
  {'title':'Sport', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3ASport&sort=top&restrict_sr=on&t=all'},
  {'title':'Thriller', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AThriller&sort=top&restrict_sr=on&t=all'},
  {'title':'War', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AWar&sort=top&restrict_sr=on&t=all'},
  {'title':'Western', 'url':'http://www.reddit.com/r/fullmoviesonyoutube/search.json?q=flair%3AWestern&sort=top&restrict_sr=on&t=all'},
]

def name():
  return 'Youtube Movies'

def image():
  return "icon.png"

def description():
  return "Full movies available on Youtube. Data imported from /r/fullmoviesonyoutube subreddit (<a target='_blank' href='http://www.reddit.com/r/fullmoviesonyoutube/'>http://www.reddit.com/r/fullmoviesonyoutube</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  return chanutils.reddit.get_feed(_FEEDLIST[idx], moviesubs=True)

def search(q):
  return chanutils.reddit.search(_SUBREDDIT, q, moviesubs=True)
