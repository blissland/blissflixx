import re

BBC_URL = re.compile(r'https?://(?:www\.)?bbc\.co\.uk/(?:(?:(?:programmes|iplayer(?:/[^/]+)?/(?:episode|playlist))/)|music/clips[/#])(?P<id>[\da-z]{8})')
YOUTUBE_URL = re.compile(r"""(?x)^
                     (
                         (?:https?://|//)                                    # http(s):// or protocol-independent URL
                         (?:(?:(?:(?:\w+\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie)?\.com/|
                            (?:www\.)?deturl\.com/www\.youtube\.com/|
                            (?:www\.)?pwnyoutube\.com/|
                            (?:www\.)?yourepeat\.com/|
                            tube\.majestyc\.net/|
                            youtube\.googleapis\.com/)                        # the various hostnames, with wildcard subdomains
                         (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
                         (?:                                                  # the various things that can precede the ID:
                             (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/
                             |(?:                                             # or the v= param in all its forms
                                 (?:(?:watch|movie)(?:_popup)?(?:\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
                                 (?:\?|\#!?)                                  # the params delimiter ? or # or #!
                                 (?:.*?&)?                                    # any other preceding param (like /?s=tuff&v=xxxx)
                                 v=
                             )
                         ))
                         |youtu\.be/                                          # just youtu.be/xxxx
                         |(?:www\.)?cleanvideosearch\.com/media/action/yt/watch\?videoId=
                         )
                     )?                                                       # all until now is optional -> you can pass the naked ID
                     ([0-9A-Za-z_-]{11})                                      # here is it! the YouTube video ID
                     (?!.*?&list=)                                            # combined list/video URLs are handled by the playlist IE
                     (?(1).+)?                                                # if we found the ID, everything can follow
                     $""")
ITV_URL = re.compile(r'https?://www\.itv\.com/(.+?)')

DL_URLS = [  
#  BBC_URL,
  ITV_URL,
]

def skip_download(url):
  for url_re in DL_URLS:
    if url_re.match(url):
      return False
  return True

def get_format(url):
  if BBC_URL.match(url):
    # Don't download hd 1280 x 720 but the next best quality
    # (usaully 832 x 468). Sometimes rtmpdump aborts before downloading
    # all of hd quality. Lower quality seems more reliable.
    return "best[height<720]"
  elif YOUTUBE_URL.match(url):
    # Otherwise may download in webm format
    return "(mp4)"
  else:
    return None


