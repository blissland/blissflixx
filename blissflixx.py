#!/usr/bin/python
from os import path
import sys, os
LIB_PATH = path.join(path.abspath(path.dirname(__file__)), "lib")
sys.path.append(LIB_PATH)
import locations, gitutils, cherrypy

# Do not allow running as root
if os.geteuid() == 0:
  print "BlissFlixx should not be run as superuser."
  print "Please run again but without using sudo."
  sys.exit(1)

# Check if first time run and need to finish install
if not path.exists(locations.YTUBE_PATH):
  cherrypy.log("Finishing Installation. Please wait...")
  gitutils.clone(locations.LIB_PATH,"https://github.com/rg3/youtube-dl.git")

  datapath = locations.DATA_PATH
  playlists = os.path.join(datapath, "playlists")
  settings = os.path.join(datapath, "settings")
  if not os.path.exists(locations.PLUGIN_PATH):
    os.makedirs(locations.PLUGIN_PATH)
  if not os.path.exists(datapath):
    os.makedirs(datapath)
  if not os.path.exists(playlists):
    os.makedirs(playlists)
  if not os.path.exists(settings):
    os.makedirs(settings)

sys.path.append(locations.YTUBE_PATH)
sys.path.append(locations.CHAN_PATH)
sys.path.append(locations.PLUGIN_PATH)

import json, shutil, subprocess
import signal, traceback, argparse
import api, pwd, grp
from cherrypy.process.plugins import Daemonizer
from cherrypy.process.plugins import DropPrivileges
from cherrypy._cplogging import LogManager

RESTARTING = False

class Api(object):

  def _error(self, status, msg):
    cherrypy.response.status = status
    return {'error': msg}

  def _server(self, fn=None, data=None):
    if fn == 'restart':
      global RESTARTING
      RESTARTING = True
      gitutils.pull(locations.YTUBE_PATH)
      gitutils.pull(locations.ROOT_PATH)
      gitutils.pull_subdirs(locations.PLUGIN_PATH)
      os.kill(os.getpid(), signal.SIGUSR2)
    else:
      return self._error(404, "API Function '" + fn + "' is not defined")

  @cherrypy.expose
  def chanimage(self, chid, img):
    path = os.path.join(locations.CHAN_PATH, chid, img)
    return cherrypy.lib.static.serve_file(path)

  @cherrypy.expose
  def pluginimage(self, chid, img):
    path = os.path.join(locations.PLUGIN_PATH, chid, img)
    return cherrypy.lib.static.serve_file(path)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def default(self, modname, fn=None, data=None):
    if modname == 'server':
      return self._server(fn, data)
    module = getattr(api, modname)
    if module is None:
      return self._error(404, "API Module '" + modname + "' is not defined")
    call = getattr(module, fn)
    if call is None:
      return self._error(404, "API Function '" + fn + "' is not defined")
    if data is not None:
      datadict = json.loads(data)
    else:
      datadict = {}
    try:
      ret = call(**datadict)
      if ret is not None:
        if RESTARTING and modname == 'playr' and fn == 'status':
          ret['Error'] = True
          ret['Msg'] = "Server Restarting & Updating..."
          ret['Restart'] = True
        return ret
    except Exception, e:
      return self._error(500, traceback.format_exc())

def cleanup():
  # Cleanup if previously crashed or was killed
  try:
    shutil.rmtree('/tmp/torrent-stream')
  except Exception:
    pass
  try:
    shutil.rmtree('/tmp/blissflixx')
  except Exception:
    pass
  try:
    home = os.path.expanduser("~")
    os.remove(home + "/.swfinfo")
  except Exception:
    pass
  kill_process("omxplayer")
  kill_process("peerflix")

def kill_process(name):
  s = subprocess.check_output("ps -ef | grep " + name, shell=True)
  lines = s.split('\n')
  for l in lines:
    items = l.split()
      # Don't kill our own command
    if len(items) > 2 and l.find("grep " + name) == -1:
      try:
        os.kill(int(items[1]), signal.SIGTERM)
      except Exception:
        pass

class IgnoreStatusLogger(LogManager):
  def __init__(self, *args, **kwargs):
    LogManager.__init__(self, *args, **kwargs)

  def access(self):
    request = cherrypy.serving.request
    # Ignore all status requests as they do nothing but fill up the log
    if request.request_line != "GET /api/playr?fn=status HTTP/1.1":
      return LogManager.access(self)

class Html(object): pass

parser = argparse.ArgumentParser()
parser.add_argument("--daemon", help="Run as daemon process", 
                    action="store_true")
parser.add_argument("--port", type=int, help="Listen port (default 6969)")
args = parser.parse_args()

engine = cherrypy.engine
if args.daemon:
  Daemonizer(engine).subscribe()

cleanup()

cherrypy.log = IgnoreStatusLogger()

cherrypy.tree.mount(Api(), '/api')
cherrypy.tree.mount(Html(), '/', config = {
  '/': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': locations.HTML_PATH,
          'tools.staticdir.index': 'index.html',
    },
  })

def exit():
  os.system('stty sane')
  engine.signal_handler.bus.exit()

engine.signal_handler.handlers['SIGINT'] = exit
engine.signal_handler.handlers['SIGUSR2'] = engine.signal_handler.bus.restart
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
port = 6969
if args.port:
  port = args.port
cherrypy.config.update({'server.socket_port': port})
cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.config.update({'checker.check_skipped_app_config': False})
engine.signals.subscribe()
engine.start()
engine.block()
