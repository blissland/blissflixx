import chanutils, playitem

def search(subreddit, q):
  url = "http://www.reddit.com/r/" + subreddit + "/search.json"
  data = chanutils.get_json(url, params={'q':q, 'restrict_sr':'on'})
  return _extract(data)

def get_feed(feed):
  data = chanutils.get_json(feed['url'])
  return _extract(data)

def _extract(data):
  results = playitem.PlayItemList()
  if not 'data' in data or len(data['data']['children']) == 0:
    return results
  rtree = data['data']['children']
  for r in rtree:
    r = r['data']
    # Internal reddit question/discussion
    if r['is_self']:
      continue
    thumb = None
    if r['thumbnail'] and r['thumbnail'].find('/') > -1:
      thumb = r['thumbnail']
    subtitle = "Score: " + str(r['score'])
    comments = "<a target='_blank' href='http://reddit.com" + r['permalink'] + "'>Comments:" + str(r['num_comments']) + "</a>" 
    subtitle = subtitle + ", " + comments
    title = chanutils.replace_entity(r['title'])
    url = chanutils.replace_entity(r['url'])
    item = playitem.PlayItem(title, thumb, url, subtitle)
    results.add(item)
  return results
