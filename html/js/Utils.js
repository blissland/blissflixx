var Utils = {
  rpc: function(module, fn, data, cb) {
    var url = '/api/' +  module
    payload = { fn: fn }
    if (data) payload['data'] = JSON.stringify(data)
    $.getJSON(url, payload, function(data) {
      cb(null, data)
    }).fail(function(xhr, textStatus) {
      var msg = ''
      if (xhr.status === 0) {
        return cb(Utils.createError('offline','offline'))
      }
      else if (xhr.responseText.lastIndexOf('{', 0) === 0) {
        obj = JSON.parse(xhr.responseText)
        msg = obj.error
      } else {
        msg = xhr.responseText
      }
      cb(Utils.createError(textStatus + ": " + xhr.status, msg))
    })
  },
  goRoute: function() {
    var route = arguments[0]
    for (i=1; i<arguments.length; i++) {
      route += '/' + encodeURIComponent(arguments[i])
    }
    riot.route(route)
  },
  createError: function(type, msg) {
    return '/' + encodeURIComponent(type) + '/' + encodeURIComponent(msg)
  },
  showError: function(err) {
    riot.route('error' + err)
  },
}
