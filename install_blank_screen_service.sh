#!/usr/bin/env bash

# Install a sytem service to blank the screen at boot.
# It runs 'tvservice -p' that turns on the hdmi output with preferred settings,
# physically blanking the screen and removing any output left from the boot process. 
# It is useful to force the tv to enable power saving measures.
# To use the console from a connected keyboard try <alt+f2>.

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run using sudo" 1>&2
   exit 1
fi

systemctl stop blankscreen.service
systemctl disable blankscreen.service

cat << _contents > /etc/systemd/system/blankscreen.service
[Unit]
Description=Blank screen after boot by turning on the hdmi output with preferred settings

[Service]
Type=simple
ExecStart=tvservice -p

[Install]
WantedBy=default.target
_contents

systemctl daemon-reload
systemctl enable blankscreen.service

echo blankscreen service installed - it will run at the next boot
echo if you want to run it now, type:
echo sudo systemctl start blankscreen.service