#!/usr/bin/env bash

# Install blissflixx as a sytem service so that it will run at boot.

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

systemctl stop blissflixx.service
systemctl disable blissflixx.service

cat << _contents > /etc/systemd/system/blissflixx.service
[Unit]
Description=Blissflixx service
After=network-online.target

[Service]
Type=simple
Restart=always
User=$(logname)
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/run.sh

[Install]
WantedBy=default.target
_contents

systemctl daemon-reload
systemctl enable blissflixx.service

echo blissflixx service installed - it will run at the next boot
echo if you want to run it now, type:
echo sudo systemctl start blissflixx.service
