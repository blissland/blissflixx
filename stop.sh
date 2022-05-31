#!/usr/bin/env bash

# Stop the blissflixx process. Be aware that if blissflixx was 
# installed as a service, the system will restart blissflixx.
# In that case you should use:
# sudo systemctl stop blissflixx.service

pkill --signal SIGTERM -f blissflixx.py
