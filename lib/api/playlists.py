import os
import json
from common import ApiError, is_torrent, torrent_idx
from chanutils import add_playitem_actions

_PLAYLIST_DIR = '/home/pi/blissflixx/data/playlists'

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
  names = os.listdir(_PLAYLIST_DIR)
  return sorted(names)

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
  for item in playlist['items']:
    actions = [{'label':'Remove From Playlist', 'type':'delplaylistitem'},
              {'label': 'Edit Item', 'type':'editplaylistitem'}]
    if is_torrent(item['url']) and not 'target' in item:
      actions.insert(0, {'label':'Show Files','type':'torrfiles','link':item['url'],'title':item['title']})
    item['actions'] = actions
    item['playlist'] = name
    item['itemnum'] = itemnum
    add_playitem_actions(item)
    itemnum = itemnum + 1
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
  return _PLAYLIST_DIR + "/" + name
