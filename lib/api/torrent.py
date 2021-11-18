from .common import ApiError
from chanutils.torrent import showmore


def files(link=None):
    if not link:
        raise ApiError("Torrent URL must be defined")
    return showmore(link).to_dict()
