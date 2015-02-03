from os import path
from common import ApiError
from chanutils import add_playitem_actions, get_json
from threading import Thread
from Queue import Queue
import glob, locations, settings, os, subprocess, shutil, gitutils

CHANID_GLOB = 'bfch_*'

class Channel:
  def __init__(self, cpath):
    chid = path.basename(cpath)
    module = __import__(chid, globals(), locals(), [], -1)
    name = module.get_name()
    image = "/api/chanimage/" + chid + "/" + module.get_image()
    search = False
    if hasattr(module, 'search'):
      search = True
    self.info = {'title': name, 'id': chid, 'img': image, 'search': search}
    self.chid = chid
    self.module = module

  def getId(self):
    return self.chid

  def getInfo(self):
    return self.info

  def getFeeds(self):
    if hasattr(self.module, 'get_feedlist'):
      return self.module.get_feedlist()
    else:
      return None

  def getFeed(self, idx):
    return self.module.get_feed(idx)

  def search(self, q):
    return self.module.search(q)

class InstalledChannels:
  def __init__(self, chanpath):
    self.chanpath = chanpath
    self._refresh()

  def _refresh(self):
    channels = []
    cpaths =  glob.glob(path.join(self.chanpath, CHANID_GLOB))
    for p in cpaths:
      channels.append(Channel(p))
    self.channels = channels
    self.settings = settings.load("channels")

  def _set_config(self, chid, key, value):
    settings = self.getChannelSettings(chid)
    settings[key] = value
    self.settings[chid] = settings
    self._save_config()
 
  def _save_config(self):
    settings.save("channels", self.settings)

  def enableChannel(self, chid):
    self._set_config(chid, 'disabled', False)

  def disableChannel(self, chid):
    self._set_config(chid, 'disabled', True)

  def getEnabled(self):
    enabled = []
    for c in self.channels:
      if self.isEnabled(c.getId()):
        enabled.append(c)
    return enabled

  def isInstalled(self, chid):
    try:
      self.getChannel(chid)
      return True
    except Exception, e:
      return False

  def installChannel(self, chid):
    channels = _available_channels()
    for chan in channels:
      if chan['id'] == chid:
        gitutils.clone(locations.CHAN_PATH, chan['repo'])
        break
    self._refresh()

  def removeChannel(self, chid):
    shutil.rmtree(path.join(locations.CHAN_PATH, chid))
    if chid in self.settings:
      del self.settings[chid]
      self._save_config()
    self._refresh()

  def getChannel(self, chid):
    for chan in self.channels:
      if chan.getId() == chid:
        return chan
    raise APIError("Unknown channel ID: '" + chid + "'")

  def isEnabled(self, chid):
    settings = self.getChannelSettings(chid)
    if 'disabled' in settings and settings['disabled'] == True:
      return False
    else:
      return True

  def getChannelSettings(self, chid):
    settings = {}
    if chid in self.settings:
      settings = self.settings[chid]
    return settings

def _available_channels():
 return get_json("http://blissflixx.rocks/feeds/channels.php")

installed = InstalledChannels(locations.CHAN_PATH)

def list_all():
  install_action = {'label':'Install', 'type':'installchannel'}
  remove_action = {'label':'Remove', 'type':'removechannel'}
  disable_action = {'label':'Disable', 'type':'disablechannel'}
  enable_action = {'label':'Enable', 'type':'enablechannel'}
  channels = _available_channels()
  for chan in channels:
    actions = []
    chid = chan['id']
    if installed.isInstalled(chid):
      if installed.isEnabled(chid):
        actions.append(disable_action)
      else:
        actions.append(enable_action)
      actions.append(remove_action)
    else:
      actions.append(install_action)
    chan['actions'] = actions
    chan['settings'] = installed.getChannelSettings(chid)
  return channels

def install(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  installed.installChannel(chid)

def remove(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  installed.removeChannel(chid)

def disable(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  installed.disableChannel(chid)

def enable(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  installed.enableChannel(chid)

def list_enabled():
  enabled = installed.getEnabled()
  info = []
  for c in enabled:
    info.append(c.getInfo())
  return info

def info(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  return installed.getChannel(chid).getInfo()

def feedlist(chid=None):
  if chid is None:
    raise APIError("Channel ID is missing")
  print installed.getChannel(chid).getFeeds()
  return installed.getChannel(chid).getFeeds()

def feed(chid=None, idx=None):
  if chid is None or idx is None:
    raise APIError("Both Channel ID and feed index must be defined")
  feed = installed.getChannel(chid).getFeed(idx)
  for item in feed:
    if not item['url'].startswith("search://"):
      add_playitem_actions(item)
  return feed

def search(chid=None, q=None):
  if chid is None or q is None:
    raise APIError("Both Channel ID and search query must be defined")
  results = installed.getChannel(chid).search(q)
  if not isinstance(results, (list, tuple)):
    results = []
  for r in results:
    add_playitem_actions(r)
  return results

def _search_thread(queue, chid, q):
  results = []
  try:
    results = search(chid, q)
  except Exception:
    pass
  queue.put((info(chid)['title'], results))

def search_all(q=None):
  if q is None:
    raise APIError("Search requires query")
  enabled = list_enabled()
  threads = []
  queue = Queue(len(enabled))
  for chan in enabled:
    if chan['search']:
      th = Thread(target=_search_thread, args=(queue, chan['id'], q))
      th.start()
      threads.append(th)

  results = []
  for thread in threads:
    thread.join()
    r = queue.get()
    if len(r[1]) > 0:
      results.append(r)
  return results
