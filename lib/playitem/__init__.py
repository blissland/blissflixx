import chanutils.torrent, settings

class Action:
  def get_dict(self):
    pass

class AddPlaylistAction(Action):
  def __init__(self):
    pass

  def to_dict(self):
    return {  'type':   'addplaylist',
              'label':  'Add To Playlist'  }

class PlayWithSubsAction(Action):
  def __init__(self):
    pass

  def to_dict(self):
    return {  'type':   'playwithsubs',
              'label':  'Play With Subtitles'  }

class RemoveFromPlaylistAction(Action):
  def __init__(self):
    pass

  def to_dict(self):
    return {  'type':   'delplaylistitem',
              'label':  'Remove From Playlist'  }

class EditPlaylistItemAction(Action):
  def __init__(self):
    pass

  def to_dict(self):
    return {  'type':   'editplaylistitem',
              'label':  'Edit Item'  }

class ShowmoreAction(Action):
  def __init__(self, label, link, title):
    self.label = label
    self.link = link
    self.title = title

  def to_dict(self):
    return {  'type':   'showmore',
              'label':  self.label,                  
              'link':   self.link,                  
              'title':  self.title  }

class MoreEpisodesAction(ShowmoreAction):
  def __init__(self, link, title):
    ShowmoreAction.__init__(self, "More Episodes...", link, title)

class TorrentFilesAction(Action):
  def __init__(self, link, title):
    self.link = link
    self.title = title

  def to_dict(self):
    return {  'type':   'showmore',
              'label':  'View Files...',
              'link':   self.link,                  
              'title':  self.title  }

class TorrentFilesAction(Action):
  def __init__(self, link, title):
    self.link = link
    self.title = title

  def to_dict(self):
    return {  'type':   'torrfiles',
              'label':  'View Files...',
              'link':   self.link,                  
              'title':  self.title  }


class ActionList:
  def __init__(self, action=None):
    self.alist = []
    if action is not None:
      self.alist.append(action)

  def add(self, action):
    self.alist.append(action)

  def empty(self):
    if len(self.alist) == 0:
      return True
    else:
      return False

  def to_dict(self):
    if len(self.alist) == 0:
      return None
    dlist = []
    for a in self.alist:
      dlist.append(a.to_dict())
    return dlist

class PlayItem:
  def __init__(self, title, img, url, subtitle=None, synopsis=None, subs=None):
    self.title = title
    self.img = img
    self.url = url
    self.subtitle = subtitle
    self.synopsis = synopsis
    self.subs = self._set_subs_lang(subs)
    self.actions = ActionList()
    self.add_default_actions()

  def _set_subs_lang(self, subs):
    if subs is not None:
      sub_settings = settings.load("subtitles")
      if 'lang' in sub_settings:
        subs['lang'] = sub_settings['lang']
      else:
        subs['lang'] = 'eng'
    return subs

  def add_default_actions(self):
    if self.subs is not None:
      self.add_action(PlayWithSubsAction())
    self.add_action(AddPlaylistAction())
    if chanutils.torrent.is_main(self.url):
      self.add_action(TorrentFilesAction(self.url, self.title))

  def add_action(self, action):
    self.actions.add(action)

  def to_dict(self):
    d = { 'title': self.title, 'img': self.img, 'url': self.url }
    if self.subtitle is not None:
       d['subtitle'] = self.subtitle
    if self.synopsis is not None:
       d['synopsis'] = self.synopsis
    if self.subs is not None:
       d['subs'] = self.subs
    if not self.actions.empty():
      d['actions'] = self.actions.to_dict()
    return d

class TorrentPlayItem(PlayItem):
  def __init__(self, title, img, url, subtitle=None, synopsis=None, subs=None):
    url = chanutils.torrent.set_torridx(url)
    PlayItem.__init__(self, title, img, url, subtitle, synopsis, subs)

class PlaylistItem(PlayItem):
  def __init__(self, item, playlist, itemnum):
    title = item['title']
    img = item['img']
    url = item['url']
    subtitle = None
    if 'subtitle' in item:
      subtitle = item['subtitle']
    synopsis = None
    if 'synopsis' in item:
      synopsis = item['synopsis']
    subs = None
    if 'subs' in item:
      subs = item['subs']
    PlayItem.__init__(self, title, img, url, subtitle, synopsis, subs)
    self.playlist = playlist
    self.itemnum = itemnum
    self.target = None
    if 'target' in item:
      self.target = item['target']

  def add_default_actions(self):
    PlayItem.add_default_actions(self)
    self.add_action(EditPlaylistItemAction())
    self.add_action(RemoveFromPlaylistAction())

  def to_dict(self):
    d = PlayItem.to_dict(self)
    d['playlist'] = self.playlist
    d['itemnum'] = self.itemnum
    if self.target is not None:
      d['target'] = self.target
    return d

class SearchItem(PlayItem):
  def __init__(self, title, img, subtitle=None, synopsis=None):
    url = "search://" + title
    PlayItem.__init__(self, title, img, url, subtitle, synopsis)

  def add_default_actions(self):
    pass

class ShowMoreItem(PlayItem):
  def __init__(self, title, img, url, subtitle=None, synopsis=None):
    url = "showmore://" + url
    PlayItem.__init__(self, title, img, url, subtitle, synopsis)

  def add_default_actions(self):
    pass

class PlayItemList:
  def __init__(self):
    self.itemlist = []

  def add(self, item):
    self.itemlist.append(item)

  def to_dict(self):
    dlist = []
    for item in self.itemlist:
      dlist.append(item.to_dict())
    return dlist

