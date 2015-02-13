class Action:
  def get_dict(self):
    pass

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

class TorrentFilesAction(Action):
  def __init__(self, link, title):
    self.link = link
    self.title = title

  def to_dict(self):
    return {  'type':   'showmore',
              'label':  'View Files',
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
