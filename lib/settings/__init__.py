from os import path
import json, locations

_cache = {}

def load(name):
  if name in _cache:
    return _cache[name]
  fullpath = _get_path(name)
  if path.isfile(fullpath):
    data = json.load(open(fullpath, 'r'))
    _cache[name] = data
    return data
  else:
    return {}

def save(name, data):
  _cache[name] = data
  fullpath = _get_path(name)
  json.dump(data, open(fullpath, "w"))
 
def _get_path(name):
  return path.join(locations.SETTINGS_PATH, name)
