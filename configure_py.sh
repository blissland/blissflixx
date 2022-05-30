#!/usr/bin/env bash

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
python -m venv virtualenv

# Activate virtual environment
. virtualenv/bin/activate

# Install requests module
pip install requests

# Install lxml module
pip install lxml

# Install cssselect module
pip install cssselect

# Install CherryPy
pip install cherrypy
