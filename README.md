# ABOUT

BlissFlixx allows you to stream various types of video and audio content directly from the internet to your television. Supported media sources include:

 - Youtube
 - Vimeo
 - Facebook
 - Catchup TV services such as BBC iPlayer
 - Torrents (including magnet links)
 - Video/Audio from hundreds of other websites

All media (including torrents) are streamed on demand and you do not need to wait for a download to complete. 

BlissFlixx allows for easy discovery of media by installing channels which group related content by category and allow user defined searches. e.g Documentary channel, Youtube channel, BBC iPlayer channel etc. New channels are easily created.

The user may also create multiple playlists to organise their favourite content.

The media server can be controlled via a web interface from any computer, tablet or phone.

# PREREQUISITES

 - Raspberry Pi (Not model A) with at least 8Gb SD card running Raspbian.
 - Broadband connection with enough speed to support video streaming.
 - Television plugged into Raspberry Pi.
 - Computer, tablet or smartphone for controlling server.

# INSTALLATION

To install you can either git clone this repository:

    git clone https://github.com/blissland/blissflixx.git

or download and extract the zip file:

    https://github.com/blissland/blissflixx/archive/master.zip
    unzip master.zip
    mv blissflixx-master blissflixx


MORE DOCS SOON...


# SUPPORTED MEDIA SITES

Blissflixx relies on youtube-dl for extracting media so a list of supported sites can be found on it's project site: https://github.com/rg3/youtube-dl/blob/master/docs/supportedsites.md

In addition BlissFlixx has support for ITV Player (https://www.itv.com/itvplayer/) which is not currently supported by youtube-dl.

# CREDITS

Blissflixx relies on the following projects to do all the heavy lifting:

 - youtube-dl for media extraction: https://github.com/rg3/youtube-dl
 - peerflix for torrent streaming: https://github.com/mafintosh/peerflix
 - omxplayer for media playback: https://github.com/popcornmix/omxplayer
