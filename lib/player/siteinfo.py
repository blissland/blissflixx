import re

BBC_URL = re.compile(r'https?://(?:www\.)?bbc\.co\.uk/(?:(?:(?:programmes|iplayer(?:/[^/]+)?/(?:episode|playlist))/)|music/clips[/#])(?P<id>[\da-z]{8})')
TED_URL = re.compile(r'''(?x)
        (?P<proto>https?://)
        (?P<type>www|embed(?:-ssl)?)(?P<urlmain>\.ted\.com/
        (
            (?P<type_playlist>playlists(?:/\d+)?) # We have a playlist
            |
            ((?P<type_talk>talks)) # We have a simple talk
            |
            (?P<type_watch>watch)/[^/]+/[^/]+
        )
        (/lang/(.*?))? # The url may contain the language
        /(?P<name>[\w-]+) # Here goes the name and then ".html"
        .*)$
        ''')
VICE_URL = re.compile(r'http://www\.vice\.com/.*?/(?P<name>.+)')
OOYALA_URL = re.compile(r'(?:ooyala:|https?://.+?\.ooyala\.com/.*?(?:embedCode|ec)=)(?P<id>.+?)(&|$)')
VEVO_URL = re.compile(r'''(?x)
        (?:https?://www\.vevo\.com/watch/(?:[^/]+/(?:[^/]+/)?)?|
           https?://cache\.vevo\.com/m/html/embed\.html\?video=|
           https?://videoplayer\.vevo\.com/embed/embedded\?videoId=|
           vevo:)
        (?P<id>[^&?#]+)''')
VINE_URL = re.compile(r'https?://(?:www\.)?vine\.co/v/(?P<id>\w+)')
VIMEO_URL = re.compile(r'''(?x)
        https?://
        (?:(?:www|(?P<player>player))\.)?
        vimeo(?P<pro>pro)?\.com/
        (?!channels/[^/?#]+/?(?:$|[?#])|album/)
        (?:.*?/)?
        (?:(?:play_redirect_hls|moogaloop\.swf)\?clip_id=)?
        (?:videos?/)?
        (?P<id>[0-9]+)
        /?(?:[?&].*)?(?:[#].*)?$''')

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
MUZU_URL = re.compile(r'https?://www\.muzu\.tv/(.+?)/(.+?)/(?P<id>\d+)')

SKIP_DL_URLS = [  
  YOUTUBE_URL,
  VICE_URL,
  OOYALA_URL,
  VINE_URL,
  VEVO_URL,
  VIMEO_URL,
  TED_URL,
  MUZU_URL,
]

def skip_download(url):
  for url_re in SKIP_DL_URLS:
    if url_re.match(url):
      return True
  return False

def get_format(url):
  if BBC_URL.match(url):
    # Don't download hd 1280 x 720 but the next best quality
    # (usaully 832 x 468). Sometimes rtmpdump aborts before downloading
    # all of hd quality. Lower quality seems more reliable.
    return "best[height<720]"
  else:
    return None


