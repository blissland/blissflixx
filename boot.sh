#!/bin/bash
echo "------------------------------------------"
echo "Waiting for 10 seconds for WIFI to connect"
echo "------------------------------------------"
sleep 10
./blissflixx.py --port 80 --daemon
./wificonf.py
