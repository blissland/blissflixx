#!/bin/bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

# Update to latest packages
apt-get update

# Fix broken packages
apt-get -y -f install

# Install node.js
wget http://node-arm.herokuapp.com/node_latest_armhf.deb 
dpkg -i node_latest_armhf.deb
rm node_latest_armhf.deb

# Install latest omxplayer
wget -O omxplayer.deb http://omxplayer.sconde.net/builds/omxplayer_0.3.6~git20150217~5337be8_armhf.deb
dpkg -i omxplayer.deb
rm omxplayer.deb

# Install peerflix
npm install -g peerflix

# Install GIT
apt-get -y install git

# Install ffmpeg
apt-get -y install ffmpeg

# Install rtmpdump
apt-get -y install rtmpdump

# Install python pip
apt-get -y install python-pip

# Install python build tools
apt-get -y install python-dev

# Install CherryPy
pip install cherrypy

# Install subprocess32 module
pip install subprocess32

# Install requests module
pip install requests

# Install subliminal subtitles module
pip install subliminal

# Install XML parser
apt-get -y install libxml2-dev

# Install XSLT package
apt-get -y install libxslt1-dev

# Install lxml module
pip install lxml

# Install cssselect module
pip install cssselect

# Required for setcap
apt-get -y install libcap2-bin

# So server can run on port 80 without sudo
setcap 'cap_net_bind_service=+ep' /usr/bin/python2.7

# Install bonjour for raspberrypi.local 
apt-get -y install libnss-mdns
