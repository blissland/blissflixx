import chanutils.reddit

_SUBREDDIT = 'Shortfilms'

_FEEDLIST = [
  {'title':'Hot', 'url':'http://www.reddit.com/r/Shortfilms.json'},
  {'title':'New', 'url':'http://www.reddit.com/r/Shortfilms/new.json'},
  {'title':'Action & Adventure', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f01%27+&sort=top&restrict_sr=on'},
  {'title':'Animation', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f02%27+&sort=top&restrict_sr=on'},
  {'title':'Art Films', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f17%27+&sort=top&restrict_sr=on'},
  {'title':'Comedy', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f05%27+&sort=top&restrict_sr=on'},
  {'title':'Crime', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f06%27+&sort=top&restrict_sr=on'},
  {'title':'Documentary', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f07%27+&sort=top&restrict_sr=on'},
  {'title':'Drama', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f08%27+&sort=top&restrict_sr=on'},
  {'title':'Experimental', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f09%27+&sort=top&restrict_sr=on'},
  {'title':'Film Noir', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f10%27+&sort=top&restrict_sr=on'},
  {'title':'Gay & Lesbian', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f11%27+&sort=top&restrict_sr=on'},
  {'title':'Horror', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f12%27+&sort=top&restrict_sr=on'},
  {'title':'Musical', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f13%27+&sort=top&restrict_sr=on'},
  {'title':'Mystery', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f14%27+&sort=top&restrict_sr=on'},
  {'title':'Parody', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f26%27+&sort=top&restrict_sr=on'},
  {'title':'Romance', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f16%27+&sort=top&restrict_sr=on'},
  {'title':'Sci-Fi & Fantasy', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f03%27+&sort=top&restrict_sr=on'},
  {'title':'Surreal', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f23%27+&sort=top&restrict_sr=on'},
  {'title':'Thriller', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f18%27+&sort=top&restrict_sr=on'},
  {'title':'War', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f19%27+&sort=top&restrict_sr=on'},
  {'title':'Western', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f20%27+&sort=top&restrict_sr=on'},
  {'title':'World Cinema', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f21%27+&sort=top&restrict_sr=on'},
  {'title':'Amateur', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f22%27+&sort=top&restrict_sr=on'},
  {'title':'Genre Defying', 'url':'http://www.reddit.com/r/Shortfilms/search.json?q=flair%3A%27f27%27+&sort=top&restrict_sr=on'},
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
