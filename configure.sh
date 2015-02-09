#!/bin/bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

# Install node.js
wget http://node-arm.herokuapp.com/node_latest_armhf.deb 
dpkg -i node_latest_armhf.deb
rm node_latest_armhf.deb

# Install latest omxplayer
wget http://omxplayer.sconde.net/builds/omxplayer_0.3.6~git20150128~18f051d_armhf.deb
dpkg -i omxplayer_0.3.6~git20150128~18f051d_armhf.deb
rm omxplayer_0.3.6~git20150128~18f051d_armhf.deb

# Install peerflix
npm install -g peerflix

# Update to latest packages
apt-get update

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

# Install XML parser
apt-get -y install libxml2-dev

# Install XSLT package
apt-get -y install libxslt1-dev

# Install lxml module
pip install lxml

# Install cssselect module
pip install cssselect
