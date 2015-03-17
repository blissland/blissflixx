function JQueryStore() {
  riot.observable(this)
  var self = this

  self.oldHide = $.fn.hide;
  $.fn.hide = function() {
    self.trigger('jq_hide')
    return self.oldHide.apply(null, arguments)
  }
}
