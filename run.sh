#!/usr/bin/env bash

# Run blissflixx using it's virtual environment. This is a helper method 
# for the blissflixx service that runs forever.

echo $(pwd)
. ./virtualenv/bin/activate
echo running blissflixx using 
echo python3=$(which python3) 
echo pip3=$(which pip3)
echo user=$(whoami)
echo pwd=$(pwd)
./blissflixx.py --port 80 
