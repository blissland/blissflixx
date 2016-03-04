#!/bin/bash
#
# Run this script if you want to make Blissflixx
# automatically run on boot. 
#
# Edit the following file:
#   sudo vi /etc/init.d/superscript
#
# Add these lines to the file:
#   #!/bin/bash
#   cd /home/pi/blissflixx
#   sudo -u pi "./boot.sh"
#
# Now make the script executable:
#   sudo chmod 755 /etc/init.d/superscript
# 
# Thats it. Blissflixx should now run on boot
#
echo "------------------------------------------"
echo "Waiting for 10 seconds for WIFI to connect"
echo "------------------------------------------"
sleep 10
./blissflixx.py --port 80 --daemon
