import chanutils, json

_feedlist = [
  {'title':'Top Rentals','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=dvd-top-rentals&minTomato=0&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity&certified=false'},
  {'title':'Top Rated','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=cf-dvd-all&minTomato=75&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release&certified=true'},
  {'title':'New Releases','url':'http://www.rottentomatoes.com/api/private/v1.0/m/list/find?page=1&limit=30&type=dvd-new-releases&minTomato=0&maxTomato=100&minPopcorn=0&maxPopcorn=100&services=amazon;amazon_prime;flixster;hbo_go;itunes;netflix_iw;target;vudu&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=popularity&certified=false'},
]

def get_name():
  return 'Rotten Tomatoes'

def get_image():
  return 'icon.png'

def get_feedlist():
  return _feedlist

def get_feed(idx):
  data = chanutils.get_json(_feedlist[idx]['url'])
  return _extract(data['results'])

def _extract(items):
  results = []
  for i in items:
    img = i['posters']['primary']
    title = i['title']
    subtitle = "DVD Release Date: " + i['dvdReleaseDate']
    url = "search://" + title
    tomatoScore = "Unknown"
    if 'tomatoScore' in i:
      tomatoScore = str(i['tomatoScore']) + "%"
    popcornScore = "Unknown"
    if 'popcornScore' in i:
      popcornScore = str(i['popcornScore']) + "%"
    synopsis = "Tomato Score: " + tomatoScore
    synopsis = synopsis + ", Popcorn Score: " + popcornScore
    results.append({ 'title':title, 'img':img, 'url':url, 'subtitle':subtitle,
                     'synopsis': synopsis})
  return results
