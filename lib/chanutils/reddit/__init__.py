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
    thumb = thumbnail
    if r['thumbnail'] and r['thumbnail'].find('/') > -1:
      thumb = r['thumbnail']
    subtitle = "Score: " + str(r['score'])
    comments = "<a target='_blank' href='http://reddit.com" + r['permalink'] + "'>Comments:" + str(r['num_comments']) + "</a>" 
    subtitle = subtitle + ", " + comments
    title = replace_entity(r['title'])
    filtered.append({'title':title, 'img':thumb, 'url':r['url'],
                    'subtitle':subtitle})
  return filtered
