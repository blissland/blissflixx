function PlayerStore() {
  riot.observable(this)
  var self = this
  self.status = {}

  window.setInterval(function(){
    Utils.rpc('playr', 'status', null, function(err, data) {
      if (err) return /* Ignore errors - probably server not running */
      self.status = data
      self.trigger('se_status_changed') 
    })
  }, 1000);

  self.play = function(url, title, cb) {
    Utils.rpc('playr', 'play', {url: url, title: title}, cb)
  }

  self.playWithSubs = function(url, title, subs, cb) {
    Utils.rpc('playr', 'play', {url: url, title: title, subs:subs}, cb)
  }

  self.control = function(action, cb) {
    Utils.rpc('playr', 'control', {action: action}, cb)
  }

  self.getStatus = function() {
    return self.status
  }
}
