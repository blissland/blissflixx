#!/usr/bin/env bash

# Uninstall blankscreen sytem service so that it won't run at boot.

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

systemctl stop blankscreen.service
systemctl disable blankscreen.service
rm /etc/systemd/system/blankscreen.service
systemctl daemon-reload

echo blankscreen service uninstalled
