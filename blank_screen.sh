#!/usr/bin/env bash

# turn on the tv with preferred options efectively blanking the screen
tvservice -p

# Set the screensaver timeout when an x environment exists
until which xinit && DISPLAY=:0 xset dpms 10 10 10
do
  echo '.'
  sleep 1
done

