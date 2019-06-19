# About

Plugin for BlissFlixx media player to allow playing of local files.

# Installation

To install first go to your BlissFlixx directory and make sure you are running the latest version with local media playback support by running:

```
git pull
```
Now install the actual plugin:

```
cd plugins
git clone https://github.com/blissland/bfch_local_media.git
cd bfch_local_media
cp sample.py config.py
vi config.py
```
You now need to edit the config.py file to add your local media directories.

Finally restart the BlissFlixx server.
