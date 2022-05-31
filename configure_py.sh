#!/usr/bin/env bash

# Install python dependencies into their own virtual environment.
# This is done to reduce conflicts with system defaults or other
# installed applications.

# Make sure script is not run by root
if [ "$(id -u)" == "0" ]; then
   echo "This script must NOT be run using sudo" 1>&2
   exit 1
fi

echo ""
echo "============================================================"
echo ""
echo "Installing python dependencies... "
echo ""
echo "============================================================"

# Create virtual environment
python3 -m venv virtualenv

# Activate virtual environment
. virtualenv/bin/activate

# Install requests module
pip3 install requests

# Install lxml module
pip3 install lxml

# Install cssselect module
pip3 install cssselect

# Install CherryPy
pip3 install cherrypy
