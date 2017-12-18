#!/bin/bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

echo ""
echo "============================================================"
echo ""
echo "Installing necessary dependencies... (This will take a while)"
echo ""
echo "============================================================"

# Update to latest packages
apt-get update

# Fix broken packages
apt-get -y -f install

# Remove old version of node
apt-get -y remove nodejs-legacy

# Install latest node.js
wget http://node-arm.herokuapp.com/node_latest_armhf.deb
dpkg -i node_latest_armhf.deb
rm node_latest_armhf.deb

# Install npm 
apt-get -y install npm

# Install latest omxplayer
wget -O omxplayer.deb http://omxplayer.sconde.net/builds/omxplayer_0.3.7~git20160923~dfea8c9_armhf.deb
dpkg -i omxplayer.deb
rm omxplayer.deb

# Install peerflix
npm install -g peerflix

# Install GIT
apt-get -y install git

# Install libav for Jessie
apt-get -y install libav-tools

# Install rtmpdump
apt-get -y install rtmpdump

# See https://github.com/blissland/blissflixx/issues/31
apt-get -y install gcc

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

# Install livestreamer module
pip install livestreamer

# Required for setcap
apt-get -y install libcap2-bin

# So server can run on port 80 without sudo
setcap 'cap_net_bind_service=+ep' /usr/bin/python2.7

# Install bonjour for raspberrypi.local 
apt-get -y install libnss-mdns

# Install phantomjs (required by youtube-dl for some extractors)
apt-get -y install libfontconfig1 libfreetype6
wget https://github.com/fg2it/phantomjs-on-raspberry/releases/download/v2.1.1-wheezy-jessie-armv6/phantomjs_2.1.1_armhf.deb
sudo dpkg -i phantomjs_2.1.1_armhf.deb
rm phantomjs_2.1.1_armhf.deb
