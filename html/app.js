'use strict';

var myApp = angular.module('myApp', [
  'ui.router',
  'classy',
  'nsPopover',
]);

/*
 * Routes
 */
myApp.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/home");

  $stateProvider
    .state('home', {
       url: "/home",
       templateUrl: "views/home.html",
       controller: 'HomeCtrl'
    })
    .state('channels', {
       url: "/channels",
       templateUrl: "views/channels.html",
    })
    .state('channels.manage', {
       url: "/manage",
       templateUrl: "views/itemlist.html",
       controller: 'ChanManCtrl'
    })
    .state('channels.home', {
       url: "/home",
       templateUrl: "views/channelslist.html",
       controller: 'ChannelsCtrl'
    })
    .state('channels.view', {
		   url: "/view/:chid",
       templateUrl: "views/chanhome.html",
       controller: 'ChanHomeCtrl',
       resolve:{
         promise: function(getChanSvc, $stateParams) {
				   return getChanSvc($stateParams.chid);
				 }
       }
    })
    .state('channels.showmore', {
       url: "/showmore/:chid?link&title",
       templateUrl: "views/itemlist.html",
       controller: 'ShowMoreCtrl',
       resolve:{
         promise: function(getChanSvc, $stateParams) {
				   return getChanSvc($stateParams.chid);
				 }
       }
    })
    .state('channels.view.items', {
		   url: "/items",
       templateUrl: "views/itemlist.html",
    })
    .state('playlists', {
       url: "/playlists",
       templateUrl: "views/playlists.html",
       controller: 'PlaylistsCtrl'
    })
    .state('playlists.home', {
       url: "/home",
       templateUrl: "views/itemlist.html",
       controller: 'PlaylistsHomeCtrl'
    })
    .state('playlists.items', {
       url: "/items?name",
       templateUrl: "views/itemlist.html",
       controller: 'PlaylistItemsCtrl'
    })
    .state('playlists.torrfiles', {
       url: "/torrfiles?link&title",
       templateUrl: "views/itemlist.html",
       controller: 'TorrFilesCtrl'
    })
    .state('playlists.edit', {
       url: "/edit?name&itemnum",
       templateUrl: "views/editplaylist.html",
       controller: 'PlayListEditCtrl',
       resolve:{
         playlistPromise: function(getPlaylistSvc, $stateParams) {
				   return getPlaylistSvc($stateParams.name);
				 }
       }
    })
    .state('playlink', {
		   url: "/playlink",
       templateUrl: "views/playlink.html",
       controller: 'PlayLinkCtrl',
    })
    .state('playlink.items', {
       templateUrl: "views/itemlist.html",
		   url: "/items",
    })
    .state('playlink.torrfiles', {
       url: "/torrfiles?link&title",
       templateUrl: "views/itemlist.html",
       controller: 'TorrFilesCtrl'
    })
    .state('search', {
		   url: "/search",
       templateUrl: "views/search.html",
       controller: 'SearchCtrl',
    })
    .state('search.home', {
		   url: "/home?q",
       templateUrl: "views/itemlist.html",
       controller: 'SearchHomeCtrl',
    })
});

/*
 * Services
 */
myApp.factory('getChanSvc', ['rpcSvc', '$rootScope', function(rpcSvc, $rootScope) {
	return function(chid) {
    if ($rootScope.currChan && $rootScope.currChan.id == chid) {
      return {data: $rootScope.currChan }
    }
		var lookup = $rootScope.chanLookup;
		if (lookup) {
		  $rootScope.currChan =  lookup[chid]
      $rootScope.currChan.activeFeed = null;
      return {data: $rootScope.currChan }
	  }
		return rpcSvc('channels', 'info', {chid:chid}, function(data) {
			$rootScope.currChan = data;
      return $rootScope.currChan;
		});
	}
}]);

myApp.factory('getPlaylistSvc', ['rpcSvc', function(rpcSvc) {
  return function(name) {
    return rpcSvc('playlists', 'get', {name:name}, function(data) {
      return data;
		});
  }
}]);

myApp.factory('newPlaylistSvc', ['rpcSvc', function(rpcSvc) {
  return function(name, success, error) {
    if (!name) {
	  	error("You must enter a name");
	  }
	  else if (name.length > 100) {
	  	error("Name is to long");
	  }
    else {
    	rpcSvc('playlists', 'new', {name:name}, function(data) {
        if (data && data.msg) {
				  error(data.msg)
        } else { 
				  success();
        }
			}, function(data) {
				  error("Got server error");
     	})
	  }
  }
}]);

myApp.factory('rpcSvc', ['$http', '$rootScope', function($http, $rootScope) {
	return function(module, fn, data, success, error) {
		var url = '/api/' + module + '?fn=' + encodeURIComponent(fn);
		if (data) {
			url += "&data=" + encodeURIComponent(JSON.stringify(data));
		}
    return $http.get(url)
			.success(function(data) {
        $rootScope.error = null;
        if (success) {
				  success(data);
        }
			})
			.error(function(data, status) {
        var msg
	      if (data && data.error) {
        	msg = "Error: (" + status + ") " + data.error;
      	} else if (status) {
        	msg = "Error: (" + status + ")";
	      } else {
  	      msg = "Error: Unspecified";
	      }
        $rootScope.error = msg;
				if (error) {
					error();
				}
			});
	}
}]);

/*
 * controllers
 */
myApp.classy.controller({
  name: 'MainCtrl',
  inject: ['$scope', '$rootScope', '$state', '$timeout', '$http', '$document',
					  'rpcSvc', 'newPlaylistSvc'],
  init: function() {
		var self = this, $s = this.$;
    var poller = function() {
      self.$http.get('api/playr?fn=status')
			  .success(function(data) {
          setGlobal(self, 'status', data)
          self.$timeout(poller, 1000);
        })
			  .error(function() {
          self.$timeout(poller, 1000);
        });
    };
    poller();

		// Press spacebar to pause/resume
		this.$document.bind('keypress', function(e) {
			var tag = e.target.tagName.toLowerCase(e);
			if (e.which === 32 && tag != 'input' && tag != 'textarea') {
				var status = $s.status
				if (status.State) {
					if (status.Paused) {
  					$s.controlPlayer('resume');
					} else {
  					$s.controlPlayer('pause');
					}
					e.preventDefault();
				}
			}
		})
  },

  goBack: function() {
    window.history.back();
  },

  stateGo: function(name, params) {
		if (!params) {
			params = {};
		}
		if (!params.chid) {
			// Pass channel id along to next state
		  params.chid = getChid(this)
		}
    this.$state.go(name, params);
	},

  play: function(url, title) {
    var query = "?url=" + encodeURIComponent(url)
    if (title) query += "&title=" + encodeURIComponent(title) 
		// Stop any previous error briefly appearing 
		this.$.status.Error = false;
    self = this
    this.rpcSvc('playr', 'play', {url:url, title:title}, function(data) {
      setGlobal(self, 'clearedPlayerError', false);
    }, function(data) {
      setGlobal(self, 'clearedPlayerError', false);
    });
  },

  breakword: function(word) {
    return word.replace(/\./g, ' ');
  },

  clearPlayerError: function() {
    setGlobal(this, 'clearedPlayerError', true);
  },

  controlPlayer: function(fn) {
    this.rpcSvc('playr', 'control', {action:fn})
  },

	showAddPlaylist: function(item, evt) {
    var $s = this.$;
    $s.currItem = item;
    $s.value = '';
    $s.selected = '';
    $s.playlist_error = null;
    $s.$emit("showAddToPlaylist", evt.target);
    this.rpcSvc('playlists', 'namelist', null, function(data) {
      $s.playlistNames = data;
    });
	},

  addPlaylistItem : function(playlist) {
    var $s = this.$;
    this.$.closePopover();
    var item = $s.currItem;
    var store = {title: item.title, img: item.img, url: item.url, 
                  subtitle: item.subtitle, synopsis: item.synopsis};
    this.rpcSvc('playlists', 'add_item', {name:playlist, item:store})
  },

  addNewPlaylistItem : function(playlist) {
    var $s = this.$
	  this.newPlaylistSvc(playlist, function() {
      $s.playlist_error = null;
      $s.addPlaylistItem(playlist);
      $s.$broadcast('refreshPlaylists')
		}, function(msg) {
      $s.playlist_error = msg;
		});
    return true;
  },

  closePopover : function() {
    this.$.$emit("hidePopover");
  },

	itemClicked : function(item) {
    var url = item.url
    if (url.indexOf("search://") == 0) {
      this.$state.go('search.home', {'q': url.substring(9)});
    } else {
      this.$.play(url, item.title);
    }
	},

	doAction: function(item, action, evt, success, error) {
		switch (action.type) { 
		case 'showmore':
			this.$.stateGo('channels.showmore', action);
      if (success) success();
			break;
		case 'torrfiles':
      this.$state.go('playlists.torrfiles', action);
      if (success) success();
			break;
		case 'playlink-torrfiles':
      this.$state.go('playlink.torrfiles', action);
      if (success) success();
			break;
		case 'editplaylist':
      this.$state.go('playlists.edit', {name: item.title});
      if (success) success();
			break;
		case 'editplaylistitem':
      this.$state.go('playlists.edit', {name:item.playlist, itemnum:item.itemnum });
      if (success) success();
			break;
		case 'addplaylist':
			this.$.showAddPlaylist(item, evt);
      if (success) success();
			break;
		case 'delplaylist':
      this.rpcSvc('playlists', 'delete', {name:item.title}, success, error);
			break;
		case 'delplaylistitem':
      this.rpcSvc('playlists', 'del_item', {name:action.playlist, item:item},
                  success, error);
			break;
		case 'disablechannel':
      this.rpcSvc('channels', 'disable', {chid:item.id}, success, error);
			break;
		case 'enablechannel':
      this.rpcSvc('channels', 'enable', {chid:item.id}, success, error);
			break;
		case 'installchannel':
      this.rpcSvc('channels', 'install', {chid:item.id}, success, error);
			break;
		case 'removechannel':
      this.rpcSvc('channels', 'remove', {chid:item.id}, success, error);
			break;
		}
	},
});

myApp.classy.controller({
  name: 'HomeCtrl',
  inject: ['$scope', '$rootScope', 'rpcSvc'],
  init: function() {
  },
  restart: function() {
		this.rpcSvc('server', 'restart');
  },
});

myApp.classy.controller({
  name: 'ChannelsCtrl',
  inject: ['$scope', '$rootScope', '$http', 'rpcSvc'],
  init: function() {
		setGlobal(this, 'currChan', null);
		var self = this, $s = this.$;
		this.rpcSvc('channels', 'list_enabled', null, function(data) {
			$s.channels = data
			var lookup = {}
			for (var i=0; i < data.length; i++) {
			  lookup[data[i].id] = data[i]; 
			}
		  setGlobal(self, 'chanLookup', lookup);
		})
  }
});

myApp.classy.controller({
  name: 'PlaylistsCtrl',
  inject: ['$scope', '$state', '$timeout', 'rpcSvc', 'newPlaylistSvc'],

  init: function() {
    var $s = this.$;
		$s.refreshPlaylists();
    $s.$on('refreshPlaylists', $s.refreshPlaylists);
  },

  newPlaylist : function(name) {
    var self = this, $s = this.$;
	  this.newPlaylistSvc(name, function() {
      $s.closePopover();
      $s.refreshPlaylists();
      self.$state.go('playlists.home');
		}, function(msg) {
      $s.playlist_error = msg;
		});
    return true;
  },

  deleteItem : function() {
    var $s = this.$;
    $s.closePopover();
    if ($s.currItem.playlist) {
      this.rpcSvc('playlists', 'del_item', {name:$s.currItem.playlist,
                                            item:$s.currItem}, function() {
        $s.$broadcast('refreshItems')
      });
    }
    else {
      this.rpcSvc('playlists', 'delete', {name:$s.currItem.title}, function() {
	      $s.refreshPlaylists();
      });
    }
  },

  newPlaylistPopover : function(evt) {
    var $s = this.$;
    $s.value = '';
    $s.playlist_error = null;
    $s.$emit("showNewPlaylist", evt.target);
		this.$timeout(function() {
      document.getElementById('playlistName').focus();
		});
  },

  doAction : function(item, action, evt, success, error) {
    var $s = this.$;
    if (action.type === 'delplaylist' || action.type === 'delplaylistitem') {
      $s.currItem = item;
      $s.$emit("showDelItemSure", evt.target);
    }
    else {
      $s.$parent.doAction(item, action, evt, success, error);
    };
  },

	refreshPlaylists : function() {
		var $s = this.$;
		$s.list = {};
		$s.list.no_items_msg = "There are currently no playlists";
		$s.list.has_img = true;
		$s.list.fetched = false;
    this.rpcSvc('playlists', 'list', null, function(data) {
      $s.list.items = data;
		  $s.list.fetched = true;
    });
  },
});
 

myApp.classy.controller({
  name: 'PlaylistsHomeCtrl',
  inject: ['$scope', '$state'],

	itemClicked : function(playlist) {
    this.$state.go('playlists.items', {'name': playlist.title});
	},
});

myApp.classy.controller({
  name: 'PlaylistItemsCtrl',
  inject: ['$scope', '$rootScope', '$timeout', '$state', '$stateParams',
            'rpcSvc'],
  init: function() {
		var $s = this.$;
    var name = this.$stateParams.name;
    if (!name) this.$state.go("playlists");
    $s.name = name;
    $s.refreshItems();
    $s.$on('refreshItems', $s.refreshItems);
	},

  refreshItems : function() {
		var $s = this.$;
    var name = $s.name;
		$s.list = {};
    $s.list.title = name;
		$s.list.no_items_msg = "There are currently no items in this playlist";
    this.rpcSvc('playlists', 'get', {name:name}, function(data) {
      $s.list.items = data.items;
	  	$s.list.fetched = true;
    });
  }
});

myApp.classy.controller({
  name: 'PlayListEditCtrl',
  inject: ['$scope', '$rootScope', '$timeout', '$state', '$stateParams',
           'rpcSvc', 'playlistPromise'],

  init: function() {
    var $s = this.$;
    if (!this.playlistPromise.data) this.$state.go("playlists");
    $s.playlist = this.playlistPromise.data;
    $s.oldname = this.$.playlist.title;
    $s.itemnum = this.$stateParams.itemnum;
    if ($s.editPlaylist()) {
      $s.item = $s.playlist;
    } else {
      $s.item = $s.playlist.items[$s.itemnum];
    }
	},

  moveUp: function(item) {
     var itemlist = this.$.item.items
     var to = item.itemnum-1;
     var from = item.itemnum;
     itemlist.splice(to, 0, itemlist.splice(from, 1)[0]);
     item.itemnum = item.itemnum-1;
  },

  moveDown: function(item) {
     var itemlist = this.$.item.items
     var to = item.itemnum+1;
     var from = item.itemnum;
     itemlist.splice(to, 0, itemlist.splice(from, 1)[0]);
     item.itemnum = item.itemnum+1;
  },

  editPlaylist: function() {
    return isNaN(this.$.itemnum);
  },

  saveItem: function(item) {
    var self = this;
    var playlist = this.$.playlist;
    this.rpcSvc('playlists', 'save', {name:this.$.oldname, playlist:playlist}, function() {
      if (self.$.editPlaylist()) {  
	      self.$.refreshPlaylists();
        self.$state.go("playlists.home");
      } else {
        self.$state.go('playlists.items', {'name': playlist.title});
      }
    });
   return true;
  },
});

myApp.classy.controller({
  name: 'TorrFilesCtrl',
  inject: ['$scope', '$state', '$stateParams', 'rpcSvc'],

  init: function() {
    var link = this.$stateParams.link;
    var title = this.$stateParams.title;

    var $s = this.$;
		$s.list = {};
		$s.list.no_items_msg = "Did not any files for: '" + title + "'";
		$s.list.busy_msg = "Retrieving...";
		$s.list.title = title;

    this.rpcSvc('torrent', 'files', {link:link}, function(data) {
      $s.list.items = data;
	  	$s.list.fetched = true;
    });
  },
});

myApp.classy.controller({
  name: 'ShowMoreCtrl',
  inject: ['$scope', '$rootScope', '$state', '$stateParams', 'rpcSvc'],

  init: function() {
    var link = this.$stateParams.link;
    var title = this.$stateParams.title;
    if (!link || !title || !getChid(this)) this.$state.go("home");

    var $s = this.$;
		$s.list = {};
		$s.list.no_items_msg = "Did not find any more files for: '" + title + "'";
		$s.list.busy_msg = "Retrieving...";
		$s.list.title = title;

    var chid = getChid(this);
    this.rpcSvc('channels', 'showmore', {chid:chid, link:link},function(data) {
      $s.list.items = data;
	  	$s.list.fetched = true;
    });
  },
});

myApp.classy.controller({
  name: 'PlayLinkCtrl',
  inject: ['$scope', '$rootScope', '$state', '$timeout'],

  init: function() {
    setInputFocus(this.$timeout);
  },

  createitem: function(url) {
    var title = url;
    if (title.length > 30) {
      title = title.substring(0, 30) + "..."; 
    }
    var actions = [{'label':'Add To Playlist', 'type':'addplaylist'}];
    if (url.indexOf("magnet") == 0  || url.indexOf(".torrent") > -1) {
      actions.unshift({'label':'Show Files','type':'playlink-torrfiles',
                       'link':url,'title':title});
    }
    var item = {title:title, url:url, actions:actions,img:'/img/icons/file-o.svg'};

    var $s = this.$;
		$s.list = {};
    $s.list.items = [item];
		$s.list.fetched = true;
    this.$state.go('playlink.items');
  }
});

myApp.classy.controller({
  name: 'SearchCtrl',
  inject: ['$scope', '$state', 'rpcSvc'],

  init: function() {
  },

  doSearch: function(q) {
    this.$state.go('search.home', {q:q});
  },

  searchAll: function(q) {
    var $s = this.$;
    $s.allResults = null;
		$s.list = {};
	 	$s.list.fetched = false;
		$s.list.no_items_msg = "The query did not find any results";
		$s.list.busy_msg = "Searching...";
    this.rpcSvc('channels', 'search_all', {q:q}, function(data) {
      $s.allResults = data;
      if (data.length > 0) {
        $s.showResults(0);
      }
	  	$s.list.fetched = true;
    });
  },

  isActive: function(idx) {
    return idx == this.$.activeIdx ? 'active' : '';
  },

  showResults: function(idx) {
    var $s = this.$;
    $s.list.items = $s.allResults[idx][1];
    $s.activeIdx = idx;
  },
});

myApp.classy.controller({
  name: 'SearchHomeCtrl',
  inject: ['$scope', '$state', '$stateParams', 'rpcSvc'],

  init: function() {
    var query = this.$stateParams.q;
    if (query) {
      this.$.$parent.query = query;
      this.$.searchAll(query);
    }
  },
});

myApp.classy.controller({
  name: 'ChanManCtrl',
  inject: ['$scope', '$state', 'rpcSvc'],

  init: function() {
    this.$.refresh();
  },

  doAction : function(item, action, evt, success, error) {
    var self = this
    if (action.type === 'installchannel') {
      item.title = "Installing - Please Wait";
      item.actions = [];
    }
    this.$.$parent.doAction(item, action, evt, function() {
      self.$.refresh();
    });
  },

  refresh: function() {
		var $s = this.$;
		$s.list = {};
    $s.list.title = name;
		$s.list.no_items_msg = "There are no channels available";
    this.rpcSvc('channels', 'list_all', null, function(data) {
      $s.list.items = data;
	  	$s.list.fetched = true;
    });
  },
});


myApp.classy.controller({
  name: 'ChanHomeCtrl',
  inject: ['$scope', '$rootScope', '$state', 'rpcSvc', 'promise'],

  init: function() {
    if (!this.promise.data) this.$state.go("home");
    var $s = this.$;
    if ($s.currChan.feedlist != null) {
      $s.showDefaultFeed();
    }
    else {
		  this.rpcSvc('channels', 'feedlist', {chid:getChid(this)}, function(data) {
        $s.currChan.feedlist = data;
        $s.currChan.activeFeed = null;
        $s.showDefaultFeed();
      });
    }
  },

  showDefaultFeed: function() {
    var $s = this.$;
    if ($s.currChan.activeFeed == null) {
      $s.currChan.activeFeed = 0
      $s.showFeed(0);
    } else {
		  $s.initList();
	  	$s.list.fetched = true;
      $s.list.items = $s.currChan.feedItems;
    }
  },

  initList: function() {
		this.$.list = {};
		this.$.list.no_items_msg = "There are no feeds for this channel";
		this.$.list.busy_msg = "Loading...";
  },

  showFeed: function(idx) {
    var $s = this.$;
    // Clear any search query
    $s.query = null;
    $s.initList();

    if ($s.currChan.feedlist) {
      if ($s.currChan.activeFeed != null) {
        $s.currChan.feedlist[$s.currChan.activeFeed].active = null;
      }
      $s.currChan.activeFeed = idx;
      $s.currChan.feedlist[$s.currChan.activeFeed].active = "active"
    }

		this.rpcSvc('channels', 'feed', {chid:getChid(this), idx:idx}, function(data) {
      $s.currChan.feedItems = data;
      $s.list.items = data;
	  	$s.list.fetched = true;
    });
  },

  search: function(q) {
    var $s = this.$;
    // Clear active feed
    if ($s.currChan.feedlist && $s.currChan.activeFeed != null) {
      $s.currChan.feedlist[$s.currChan.activeFeed].active = null;
      $s.currChan.activeFeed = null;
    }
		$s.list = {};
	 	$s.list.fetched = false;
		$s.list.no_items_msg = "The query did not find any results";
		$s.list.busy_msg = "Searching...";
    this.rpcSvc('channels', 'search', {q:q,chid:getChid(this)}, function(data) {
      $s.list.items = data;
	  	$s.list.fetched = true;
    });
  },
});

/*
 * Function library
 */
function setGlobal(self, name, value) {
	self.$rootScope[name] = value;
}

function getChid(self) {
	if (self.$.currChan) {
	  return self.$.currChan.id
	}
}

function setInputFocus($timeout) {
    angular.forEach(document.querySelectorAll('input'), function(elem) {
      $timeout(function() {elem.focus()});
    });
}
