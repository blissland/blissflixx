function ChannelStore() {
  riot.observable(this)
  var self = this
  self.channels = null
  self.cache = new Cache()

  self.getChannels = function(cb) {
    if (self.channels) {
      return cb(null, self.channels)
    } else {
      Utils.rpc('channels', 'list_all', null, function(err, data) {
        if (err) return cb(err)
        self.channels = data
        return self.getChannels(cb)
      })
    }
  }

  self.getEnabledChannels = function(cb) {
    self.getChannels(function(err, channels) {
      if (err) return cb(err)
      var enabled = []
      for (i=0; i<channels.length; i++) {
        if (!channels[i].settings.disabled) {
          enabled.push(channels[i])
        }
      }
      cb(null, enabled)
    })
  }

  self.getChannel = function(chid, cb) {
    self.getChannels(function(err, channels) {
      if (err) return cb(err)
      var len = channels.length
      for (i=0; i < len; i++) {
        if (channels[i].id === chid) return cb(null, channels[i])
      }
      cb(Utils.createError('Internal Error', 'Unable to find channel: ' + chid))
    })
  }

  self.createKey = function() {
    var key = ''
    for (i=0; i<arguments.length; i++) {
      key += "/" + arguments[i] 
    }
    return key
  }

  self.getResults = function(key, module, fn, args, cb) {
    results = self.cache.getItem(key)
    if (results) {
      cb(null, results) 
    } else {
      Utils.rpc(module, fn, args, function(err, data) {
        if (err) return cb(err)
        self.cache.setItem(key, data, {expirationSliding: 60})
        cb(err, data) 
      })
    }
  }

  self.getFeed = function(chid, idx, cb) {
    var key = self.createKey(chid, idx)
    self.getResults(key, 'channels', 'feed', {chid:chid, idx:idx}, cb)
  }

  self.showMore = function(chid, link, cb) {
    var key = self.createKey(chid, link)
    self.getResults(key, 'channels', 'showmore', {chid:chid, link:link}, cb)
  }

  self.searchChannel = function(chid, q, cb) {
    var key = self.createKey(chid, q)
    self.getResults(key, 'channels', 'search', {chid:chid, q:q}, cb)
  }

  self.searchAll = function(q, cb) {
    var key = self.createKey('search_all', q)
    self.getResults(key, 'channels', 'search_all', {q:q}, cb)
  }

  self.toggleChannel = function(chid, disable, cb) {
    var fn = disable ? 'disable' : 'enable'
    Utils.rpc('channels', fn, {chid:chid}, function(err, data) {
      if (err) return cb(err)
      self.channels = data
      self.trigger('se_channels_changed')
    })
  }
}
