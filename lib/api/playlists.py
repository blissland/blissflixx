import os, json, locations, playitem, glob
from common import ApiError

def new(name=None):
  plid = _create_plid(name)
  path = _get_path(plid)
  if os.path.isfile(path):
    idx = 1
    while True:
      plid = _create_plid(name, idx)
      path = _get_path(plid)
      if not os.path.isfile(path):
        break
      idx = idx + 1
  playlist = _empty_playlist(name)
  playlist['plid'] = plid
  save(playlist)
  return get(plid)

def delete(plid=None):
  path = _get_path(plid)
  try:
    os.remove(path)
  except Exception:
    pass

def list():
  names = _get_playlists()
  actions = [{'label':'Delete Playlist', 'type':'delplaylist'},
              {'label':'Edit Playlist', 'type':'editplaylist'}]
  results = []
  for n in names:
    playlist = get(n)
    if not 'img' in playlist:
      playlist['img'] = '/img/icons/list.svg'
    playlist['actions'] = actions;
    results.append(playlist);
  return results

def add_item(plid=None, item=None):
  if (plid is None) or (item is None):
    raise ApiError("Playlist ID and item must be defined")
  playlist = get(plid)
  playlist['items'].append(item)
  save(playlist)

def del_item(plid=None, item=None):
  if (plid is None) or (item is None):
    raise ApiError("Playlist ID and item must be defined")
  playlist = get(plid)
  items = playlist['items']
  for i in items:
    if i['url'] == item['url']:
      items.remove(i)
      break
  save(playlist)

def get(plid=None):
  if plid is None:
    raise ApiError("Playlist ID must be defined")
  playlist = json.load(open(_get_path(plid), 'r'))
  if not playlist:
    playlist = _empty_playlist()
  playlist['plid'] = plid
  results = playitem.PlayItemList()
  itemnum = 0
  for item in playlist['items']:
    results.add(playitem.PlaylistItem(item, plid, itemnum))
    itemnum = itemnum + 1
  playlist['items'] = results.to_dict()
  return playlist

def save(playlist=None):
  if playlist is None:
    raise ApiError("Playlist must be defined")
  plid = playlist.pop("plid", None)
  playlist.pop("actions", None)
  for item in playlist['items']:
    item.pop('actions', None)
    item.pop('playlist', None)
    item.pop('itemnum', None)
    if 'subs' in item:
      item['subs'].pop('lang', None)
  json.dump(playlist, open(_get_path(plid), "w"))

def _empty_playlist(title=""):
  return {'title': title, 'items':[]}

def _get_path(plid):
  return locations.PLIST_PATH + "/" + plid + ".bfpl"

def _get_playlists():
  paths =  glob.glob(os.path.join(locations.PLIST_PATH, "*.bfpl"))
  playlists = []
  for p in paths:
    playlists.append(os.path.basename(p)[:-5])
  return sorted(playlists)

def _create_plid(name, idx=None):
  plid = name.replace(" ", "_")
  if idx is not None:
    plid = plid + "_" + str(idx)
  return plid
