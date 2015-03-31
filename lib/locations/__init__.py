from os import path

LIB_PATH = path.split(path.abspath(path.dirname(__file__)))[0]
ROOT_PATH = path.split(LIB_PATH)[0]
HTML_PATH = path.join(ROOT_PATH, "html")
YTUBE_PATH = path.join(LIB_PATH, "youtube-dl")
DATA_PATH = path.join(ROOT_PATH, "data")
BIN_PATH = path.join(ROOT_PATH, "bin")
PLIST_PATH = path.join(DATA_PATH, "playlists")
SETTINGS_PATH = path.join(DATA_PATH, "settings")
CHAN_PATH = path.join(ROOT_PATH, "chls")
PLUGIN_PATH = path.join(ROOT_PATH, "plugins")
