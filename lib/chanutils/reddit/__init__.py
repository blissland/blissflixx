from chanutils import replace_entity, get_json

def search(subreddit, q):
  url = "http://www.reddit.com/r/" + subreddit + "/search.json"
  return get_json(url, params={'q':q, 'restrict_sr':'on'})

def extract(data, thumbnail='/img/reddit_channel.png'):
  if not 'data' in data or len(data['data']['children']) == 0:
    return []
  filtered = []
  results = data['data']['children']
  for r in results:
    r = r['data']
    # Internal reddit question/discussion
    if r['is_self']:
      continue
    if r['thumbnail'] and r['thumbnail'].find('/') > -1:
      thumbnail = r['thumbnail']
    subtitle = "Score: " + str(r['score'])
    subtitle = subtitle + ", Comments: " + str(r['num_comments'])
    title = replace_entity(r['title'])
    filtered.append({'title':title, 'img':thumbnail, 'url':r['url'],
                    'subtitle':subtitle})
  return filtered
