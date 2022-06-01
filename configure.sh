#!/usr/bin/env bash

# Install system dependencies for blissflixx.

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

# Update software repositories 
apt update

# This includes nodejs
apt -y install npm

# Install raspberry pi optimized video player
apt -y install omxplayer

# Install version control software for updates and to install other packages like
# youtube-dl. It is probably already installed, but it is possible that the user
# got blissflixx other way, like downloading the source as a zip file.
apt -y install git

# Install python package manager
apt -y install python3-pip

# Install python virtual environment to keep blissflixx dependencies isolated
apt -y install python3-venv

# Install XML parser for screen scaping websites
apt -y install libxml2-dev

# Install XSLT package for screen scaping websites
apt -y install libxslt1-dev

# So server can run on port 80 without sudo
setcap 'cap_net_bind_service=+ep' "$(readlink -f "$(which python3)")"

# Install peerflix globally
npm install -g peerflix

# The user that started the command (since sudo was used, root is the active user)
user=$(logname)

# Configure python dependencies as a normal user
sudo -u $user ./configure_py.sh