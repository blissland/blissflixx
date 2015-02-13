import os, json, locations, playitem
from common import ApiError, is_torrent, torrent_idx
from chanutils import add_playitem_actions

def new(name=None):
  path = _get_path(name)
  if os.path.isfile(path):
    return {'msg': 'Playlist name already exists'}
  save(name, _empty_playlist())

def delete(name=None):
  path = _get_path(name)
  try:
    os.remove(path)
  except Exception:
    pass

def namelist():
  names = os.listdir(locations.PLIST_PATH)
  filtered = []
  for n in names:
    if n != ".git":
      filtered.append(n)
  return sorted(filtered)

def list():
  names = namelist()
  actions = [{'label':'Delete Playlist', 'type':'delplaylist'},
              {'label':'Edit Playlist', 'type':'editplaylist'}]
  results = []
  for n in names:
    playlist = get(n)
    if not 'title' in playlist:
      playlist['title'] = n
    if not 'img' in playlist:
      playlist['img'] = '/img/icons/list.svg'
    playlist['actions'] = actions;
    results.append(playlist);
  return results

def add_item(name=None, item=None):
  if (name is None) or (item is None):
    raise ApiError("Playlist name and item must be defined")
  playlist = get(name)
  playlist['items'].append(item)
  save(name, playlist)

def del_item(name=None, item=None):
  if (name is None) or (item is None):
    raise ApiError("Playlist name and item must be defined")
  playlist = get(name)
  items = playlist['items']
  for i in items:
    if i['url'] == item['url']:
      items.remove(i)
      break
  save(name, playlist)

def get(name=None):
  if name is None:
    raise ApiError("Playlist name must be defined")
  playlist = json.load(open(_get_path(name), 'r'))
  if not playlist:
    playlist = _empty_playlist()
  playlist['title'] = name
  itemnum = 0
  results = playitem.PlayItemList()
  for i in playlist['items']:
    item = playitem.PlaylistItem(i, name, itemnum)
    url = i['url']
    target = None
    if 'target' in i:
      target = i['target']
    if is_torrent(url) and target is None:
      title = i['title']
      item.add_action(playitem.PlaylistTorrentFilesAction(url, title))
    results.add(item)
    itemnum = itemnum + 1
  playlist['items'] = results.to_dict()
  return playlist

def save(name=None, playlist=None):
  if (name is None) or (playlist is None):
    raise ApiError("Playlist name and data must be defined")
  if 'title' in playlist and playlist['title'] != name:
    delete(name)
    name = playlist['title']
  playlist.pop("actions", None)
  for i in playlist['items']:
    i.pop('actions', None)
    i.pop('playlist', None)
    i.pop('itemnum', None)
    if is_torrent(i['url']):
      idx = torrent_idx(i['url'])
      if idx is not None:
        i['target'] = idx
  json.dump(playlist, open(_get_path(name), "w"))

def _empty_playlist():
  return {'items':[]}

def _get_path(name):
  return locations.PLIST_PATH + "/" + name
