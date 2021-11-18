import os
from playitem import PlayItem, PlayItemList

try:
    from .config import _FEEDLIST
except ImportError:
    raise Exception("You need to copy sample.py to config.py in Local Media Plugin")


def name():
    return "Local Media"


def image():
    return "icon.png"


def description():
    return "Local Media Files"


def feedlist():
    return _FEEDLIST


def feed(idx):
    folder = _FEEDLIST[idx]["folder"]
    results = PlayItemList()
    files = os.listdir(folder)
    for f in files:
        title = os.path.splitext(f)[0]
        url = "file://" + os.path.join(folder, f)
        results.add(PlayItem(title, "/img/icons/file-o.svg", url))
    return results
