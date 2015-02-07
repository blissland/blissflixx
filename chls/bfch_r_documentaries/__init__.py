from chanutils import get_json, img_prefix
import chanutils.reddit

_SUBREDDIT = 'Documentaries'
_IMG = 'icon.png'
_IMGPATH = img_prefix() + '/bfch_r_documentaries/' + _IMG

_feedlist = [
  {'title':'Latest', 'url':'http://www.reddit.com/r/Documentaries.json'},
  {'title':'Anthropology', 'url':'http://www.reddit.com/r/documentaries/search.json?q=flair%3A%27Anthropology%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Art', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Art%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Biography', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Biography%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Crime', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Crime%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Cusine', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Cuisine%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Disaster', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Disaster%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Drugs', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Drugs%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Economics', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Economics%27&sort=top&restrict_sr=on&t=all'},
  {'title':'History', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27History%27&sort=top&restrict_sr=on&t=all'},
  {'title':'History (Ancient)', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Ancient+hist%27&sort=top&restrict_sr=on&t=all'},
  {'title':'History (20th Century)', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%2720th+century%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Intelligence', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Intelligence%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Literature', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Literature%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Medicine', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Medicine%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Music', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Music%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Nature', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Nature%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Offbeat', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Offbeat%27&sort=top&restrict_sr=on&t=all'},
  {'title':'American Politics', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27American+politics%27&sort=top&restrict_sr=on&t=all'},
  {'title':'International Politics', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Int+politics%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Psychology', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Psychology%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Religion', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Religion%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Science', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Science%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Sex', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Sex%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Sport', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Sport%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Tech/Internet', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Tech%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Travel', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Travel%27&sort=top&restrict_sr=on&t=all'},
  {'title':'War', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27War%27&sort=top&restrict_sr=on&t=all'},
  {'title':'World War 1', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27WW1%27&sort=top&restrict_sr=on&t=all'},
  {'title':'World War 2', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27WW2%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Vietnam War', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Vietnam+conflict%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Afghanistan War', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Afghanistan+conflict%27&sort=top&restrict_sr=on&t=all'},
  {'title':'Iraq War', 'url':'http://www.reddit.com/r/Documentaries/search.json?q=flair%3A%27Iraq+conflict%27&sort=top&restrict_sr=on&t=all'},
]

def get_name():
  return 'Documentary'

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
