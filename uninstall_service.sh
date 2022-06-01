#!/usr/bin/env bash

# Uninstall blissflixx sytem service so that it won't run at boot.
# Blissflixx can still be run using the start.sh script.

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

systemctl stop blissflixx.service
systemctl disable blissflixx.service
rm /etc/systemd/system/blissflixx.service
systemctl daemon-reload

echo blissflixx service uninstalled
