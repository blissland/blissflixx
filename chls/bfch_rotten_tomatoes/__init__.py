from playitem import SearchItem, PlayItemList
from chanutils import get_json

_FEEDLIST = [
  {'title':'Top Rentals','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=dvd-top-rentals&minTomato=0&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity&certified=false'},
  {'title':'Top Rated','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=cf-dvd-all&minTomato=75&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release&certified=true'},
  {'title':'New Releases','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=dvd-new-releases&minTomato=0&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity&certified=false'},
]

def name():
  return 'Rotten Tomatoes'

def image():
  return 'icon.png'

def description():
  return "Rotten Tomatoes Channel (<a target='_blank' href='http://www.rottentomatoes.com/'>http://www.rottentomatoes.com/</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  data = get_json(_FEEDLIST[idx]['url'])
  return _extract(data['results'])

def _extract(rtree):
  results = PlayItemList()
  for i in rtree:
    img = i['posters']['primary']
    title = i['title']
    subtitle = "DVD Release Date: " + i['dvdReleaseDate']
    tomatoScore = "Unknown"
    if 'tomatoScore' in i:
      tomatoScore = str(i['tomatoScore']) + "%"
    popcornScore = "Unknown"
    if 'popcornScore' in i:
      popcornScore = str(i['popcornScore']) + "%"
    synopsis = "Tomato Score: " + tomatoScore
    synopsis = synopsis + ", Popcorn Score: " + popcornScore
    results.add(SearchItem(title, img, subtitle, synopsis))
  return results
