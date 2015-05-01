#!/bin/bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

# Check for debian system
cat /etc/debian_version | grep 7. > /dev/null
if [ "$?" = "1" ]
then
  echo "This script was designed to run on Rasbian or a similar Debian 7.x distro"
  echo "Do you wish to continue anyway [Y/N]?"
  while true; do
    read -p "" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 0;;
        * ) echo "Please answer with Yes or No [y|n].";;
    esac
  done
  echo ""
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

# Install node.js
wget http://node-arm.herokuapp.com/node_latest_armhf.deb 
dpkg -i node_latest_armhf.deb
rm node_latest_armhf.deb

# Install latest omxplayer
wget -O omxplayer.deb http://omxplayer.sconde.net/builds/omxplayer_0.3.6~git20150402~74aac37_armhf.deb
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
