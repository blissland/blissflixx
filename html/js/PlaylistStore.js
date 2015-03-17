function PlaylistStore() {
  riot.observable(this)
  var self = this
  self.playlists = null

  self.getCachedPlaylists = function() {
    return self.playlists
  }

  self.getPlaylists = function(cb) {
    Utils.rpc('playlists', 'list', null, function(err, data) {
      if (err) return cb(err)
      self.playlists = data
      cb(null, data)
    })
  }

  self.getCachedPlaylist = function(plid) {
    if (self.playlists) {
      for (i=0; i<self.playlists.length; i++) {
        if (self.playlists[i].plid === plid) {
          return self.playlists[i]
        }
      }
    }
  } 

  self.getPlaylist = function(plid, cb) {
    self.getPlaylists(function(err) { 
      if (err) return cb(err)
      return cb(null, self.getCachedPlaylist(plid))
    })
  }

  self.newPlaylist = function(name, cb) {
    Utils.rpc('playlists', 'new', {name:name}, function(err, playlist) {
      if (err) return cb(err)
      cb(null, playlist)
      self.trigger('se_playlists_changed')
    })
  }

  self.deletePlaylist = function(plid, cb) {
    Utils.rpc('playlists', 'delete', {plid:plid}, function(err) {
      if (err) return cb(err)
      cb()
      self.trigger('se_playlists_changed')
    })
  }

  self.addItem = function(plid, item, cb) {
    Utils.rpc('playlists', 'add_item', {plid:plid, item:item}, function(err) {
      if (err) return cb(err)
      cb()
      self.trigger('se_playlists_changed')
    })
  }

  self.removeItem = function(plid, item, cb) {
    Utils.rpc('playlists', 'del_item', {plid:plid, item:item}, function(err) {
      if (err) return cb(err)
      cb()
      self.getPlaylists(function(err) {
        self.trigger('se_playlists_changed')
      })
    })
  }

  self.savePlaylist = function(playlist, cb) {
    Utils.rpc('playlists', 'save', {playlist:playlist}, function(err) {
      if (err) return cb(err)
      cb()
      self.trigger('se_playlists_changed')
    })
  }

  self.getPlaylists(function() {})
}
