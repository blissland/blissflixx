#!/usr/bin/env bash

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

echo ""
echo "============================================================"
echo ""
echo "Installing system dependencies... (This will take a while)"
echo ""
echo "============================================================"

# Update to latest packages
apt update

# Install npm 
apt -y install npm

# Install latest omxplayer
apt-get -y install omxplayer

# Install peerflix
npm install -g peerflix

# Install GIT
apt -y install git

# Install python pip
apt -y install python3-pip

# Install python venv
apt -y install python3-venv

# Install XML parser
apt -y install libxml2-dev

# Install XSLT package
apt -y install libxslt1-dev

# So server can run on port 80 without sudo
setcap 'cap_net_bind_service=+ep' /usr/bin/python3