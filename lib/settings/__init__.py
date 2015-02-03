from os import path
import json

SETTINGS_PATH = path.split(path.abspath(path.dirname(__file__)))[0]
SETTINGS_PATH = path.join(path.split(SETTINGS_PATH)[0], "data", "settings")

def load(name):
  fullpath = _get_path(name)
  if path.isfile(fullpath):
    return json.load(open(fullpath, 'r'))
  else:
    return {}

def save(name, data):
  fullpath = _get_path(name)
  json.dump(data, open(fullpath, "w"))
 
def _get_path(name):
  return path.join(SETTINGS_PATH, name)
