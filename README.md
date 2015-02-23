# ABOUT

BlissFlixx allows you to stream various types of video and audio content directly from the internet to your television. Supported media sources include:

 - Youtube
 - Vimeo
 - Facebook
 - Catchup TV services such as BBC iPlayer
 - Full movies and documentaries on Youtube
 - Torrents (including magnet links)
 - Video/Audio from hundreds of other websites

All media (including torrents) are streamed on demand and you do not need to wait for a download to complete. 

BlissFlixx allows for easy discovery of media by installing channels which group related content by category and allow user defined searches. e.g Documentary channel, Youtube channel, BBC iPlayer channel etc. New channels are easily created.

The user may also create multiple playlists to organise their favourite content.

The media server can be controlled via a web interface from any computer, tablet or phone.

# SCREENSHOTS

![BlissFlixx Channels](http://blissland.github.io/blissflixx/img/channels.png)

![Youtube Movies Channel](http://blissland.github.io/blissflixx/img/movies_chan.png)

![Documentary Channel](http://blissland.github.io/blissflixx/img/doc_chan.png)

![BBC iPlayer Channel](http://blissland.github.io/blissflixx/img/iplayer_chan.png)

# PREREQUISITES

 - Raspberry Pi (Not model A) with at least 8Gb SD card running Raspbian. You should also have about 2 Gb of free space on the card.
 - Broadband connection with enough speed to support video streaming. Ideally you should have a wired ethernet connection into your Pi as some WiFi adapters may have problems with streaming.
 - Television plugged into Raspberry Pi.
 - Computer, tablet or smartphone for controlling server.

# INSTALLATION

To install you can either git clone this repository:

    git clone https://github.com/blissland/blissflixx.git

or download and extract the zip file:

    wget https://github.com/blissland/blissflixx/archive/master.zip
    unzip master.zip
    mv blissflixx-master blissflixx

Now enter the blissflixx folder and run the configure script which will install all the required external dependencies:

    cd blissflixx
    sudo ./configure.sh

It may take a while for this script to complete so now might be a good time to wash the dishes or take the dog for a walk.

# RUNNING THE SERVER

Once the configuration script is complete you can start the server by running:

    ./blissflixx.py
    
Note that the first time you start the server it will first take a few moments to complete the installation.

Once you see the message "ENGINE Bus STARTED" the server will be up and running. Now open up a browser on your phone, tablet or PC and point it at:

    http://ip-address-of-your-pi:6969
    
So for example if the IP address of the Raspberry Pi is  192.168.1.4. Then you need to point your browser to:

    http://192.168.1.4:6969
    
If you want to run the server on the default port 80 then you will need start the server with the --port flag:

    ./blissflixx.py --port 80
    
Finally if you want the server to continue running even after you log out of your session (which is usaully the case) then specify the --daemon flag:

    ./blissflixx.py --port 80 --daemon
    
Fortunately there is a script to run the above command:

    ./start.sh

# USER GUIDE

Usage instructions are provided on the [main website](http://blissflixx.rocks/#using)

# SUPPORTED MEDIA SITES

Blissflixx relies on youtube-dl for extracting media so a list of supported sites can be found on it's project site: https://github.com/rg3/youtube-dl/blob/master/docs/supportedsites.md

In addition BlissFlixx has support for ITV Player (https://www.itv.com/itvplayer/) which is not currently supported by youtube-dl.

# CREDITS

Blissflixx relies on the following projects to do all the heavy lifting:

 - youtube-dl for media extraction: https://github.com/rg3/youtube-dl
 - peerflix for torrent streaming: https://github.com/mafintosh/peerflix
 - omxplayer for media playback: https://github.com/popcornmix/omxplayer
