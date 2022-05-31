#!/usr/bin/env bash

# Start blissflixx within it's virtual environment and return 
# leaving the process running in the background.
# Useful when using a console interactively.

echo $(pwd)
. ./virtualenv/bin/activate
echo running blissflixx using 
echo python3=$(which python3) 
echo pip3=$(which pip3)
echo user=$(whoami)
echo pwd=$(pwd)
./blissflixx.py --port 80 --daemon
