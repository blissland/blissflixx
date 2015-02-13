class Action:
  def get_dict(self):
    pass

class AddPlaylistAction(Action):
  def __init__(self):
    pass

  def to_dict(self):
    return {  'type':   'addplaylist',
              'label':  'Add To Playlist'  }

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

class PlaylistTorrentFilesAction(Action):
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

  def to_dict(self):
    if len(self.alist) == 0:
      return None
    dlist = []
    for a in self.alist:
      dlist.append(a.to_dict())
    return dlist

class PlayItem:
  def __init__(self, title, img, url, subtitle=None, synopsis=None):
    self.title = title
    self.img = img
    self.url = url
    self.subtitle = subtitle
    self.synopsis = synopsis
    self.actions = ActionList()
    self.add_default_actions()

  def add_default_actions(self):
    self.add_action(AddPlaylistAction())

  def add_action(self, action):
    self.actions.add(action)

  def to_dict(self):
    d = { 'title': self.title, 'img': self.img, 'url': self.url }
    if self.subtitle is not None:
       d['subtitle'] = self.subtitle
    if self.synopsis is not None:
       d['synopsis'] = self.synopsis
    d['actions'] = self.actions.to_dict()
    return d

class PlaylistItem(PlayItem):
  def __init__(self, playlist, itemnum, title, img, url, 
                    subtitle=None, synopsis=None, target=None):
    PlayItem.__init__(self, title, img, url, subtitle, synopsis)
    self.playlist = playlist
    self.itemnum = itemnum
    self.target = target

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

class PlayItemList:
  def __init__(self):
    self.itemlist = []

  def add(self, item):
    self.itemlist.append(item)

  def to_dict(self):
    dlist = []
    for i in self.itemlist:
      dlist.append(i.to_dict())
    return dlist
