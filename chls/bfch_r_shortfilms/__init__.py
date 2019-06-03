import chanutils.reddit

_SUBREDDIT = 'Shortfilms'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/Shortfilms.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/Shortfilms/new.json'},
  {'title':'Action & Adventure', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=action%20adventure&sort=top&restrict_sr=on'},
  {'title':'Animation', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=animation&sort=top&restrict_sr=on'},
  {'title':'Art Films', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=art%20films&sort=top&restrict_sr=on'},
  {'title':'Comedy', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=comedy&sort=top&restrict_sr=on'},
  {'title':'Crime', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=crime&sort=top&restrict_sr=on'},
  {'title':'Documentary', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=documentary&sort=top&restrict_sr=on'},
  {'title':'Drama', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=drama&sort=top&restrict_sr=on'},
  {'title':'Experimental', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=experimental&sort=top&restrict_sr=on'},
  {'title':'Film Noir', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=film%20noir&sort=top&restrict_sr=on'},
  {'title':'Gay & Lesbian', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=gay%20lesbian&sort=top&restrict_sr=on'},
  {'title':'Horror', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=horror&sort=top&restrict_sr=on'},
  {'title':'Musical', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=musical&sort=top&restrict_sr=on'},
  {'title':'Mystery', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=mystery&sort=top&restrict_sr=on'},
  {'title':'Parody', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=parody&sort=top&restrict_sr=on'},
  {'title':'Romance', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=romance&sort=top&restrict_sr=on'},
  {'title':'Sci-Fi & Fantasy', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=sci-fi%20fantasy&sort=top&restrict_sr=on'},
  {'title':'Surreal', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=surreal&sort=top&restrict_sr=on'},
  {'title':'Thriller', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=thriller&sort=top&restrict_sr=on'},
  {'title':'War', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=war&sort=top&restrict_sr=on'},
  {'title':'Western', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=western&sort=top&restrict_sr=on'},
  {'title':'World Cinema', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=world%20cinema&sort=top&restrict_sr=on'},
  {'title':'Amateur', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=amateur&sort=top&restrict_sr=on'},
  {'title':'Genre Defying', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=genre%20defying&sort=top&restrict_sr=on'},
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
