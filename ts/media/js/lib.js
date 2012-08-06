;(function($){
	var lib = window.lib = new function() 
	{
		this.center = function(element, container) 
		{
			var containerWidth = $(container).outerWidth();
			var containerHeight = $(container).outerHeight();
			
			var width = $(element).width();
			var height = $(element).height();
			
			
			var top = (containerHeight - height) / 2;
			var left = (containerWidth - width ) / 2;
						
			$(element).css({'top':top+'px', 'left':left+'px'});
		},
        this.editUrl = function(targetUrl) 
		{
			var self = this;
			var base = window.location.href;

			var baseArray = new Array();
			baseArray = base.split('/');
			
			var urlPath = base.replace(currentPage, targetUrl);

			if ( history.pushState ) {
				window.history.pushState({'page':self.subpage, 'mirror':self.mirror},"", urlPath);	
			}		
			
			window.onpopstate = function(e)
			{

			}				
		},		
		this.postAjaxCalls = function() 
		{
            //
		},
		this.customScrollbars = function() 
		{
			 $("#story").mCustomScrollbar("vertical",400,"easeOutCirc",1.05,"auto","yes","yes",10);
			 $("#previewedSoundComments").mCustomScrollbar("vertical",400,"easeOutCirc",1.05,"auto","yes","no",10);
		},
		this.cycle = function(items, intervalMs) 
		{
			var count = $(items).size();
			
			$(items).css({'opacity':0});
			$(items).eq(0).css({'opacity':1});
			
			var i = 0;
			var interval = setInterval(function() 
			{
				var next = (i < count-1) ? i+1 : 0;
				
				$(items).eq(i).animate({
					opacity	: 0
				}, 1000);
				$(items).eq(next).animate({
					opacity	: 1
				}, 1000);	
				i = (i < count-1) ? i+1 : 0;
			}, intervalMs);
		},				
		this.ajax = function(url, data, dataType, container, successCallback) 
		{
			var self = this;
	
			// $('#slothLoader').appendTo(container).show();
			
			$.ajax({
				type: 'post',
				dataType: dataType,
				url: url,
				data: data,
				success: function(data)
				{
					// $('#slothLoader').hide().appendTo('body');
					successCallback(data);
					self.postAjaxCalls();
				}
			});
		},
		this.lightbox = function(openCallback, closeCallback)
		{
			var self = this;
			
			$('#screen').fadeIn(300, function() {
				$(this).addClass('open');
				openCallback();
				
				$('#screen').click(function(e) {
					closeCallback();
					self.hideLightbox();
				});
			});				
		},
		this.hideLightbox = function() 
		{
			$('#screen').fadeOut(200);
		},
		this.getController = function(controllers) {
			var self = this;
			var pathname = window.location.pathname;
			var controller;
			for (var i=0; i<controllers.length; i++) {
				var query = new RegExp(controllers[i], 'i');
				if (pathname.search(query) > 0) { controller = controllers[i]; }
			}
			return controller;
		},	
		this.isLoaded = function(elementId)
		{
			// try to get the contents of an element
			var element = document.getElementById(elementId).contentDocument;

			// if nothing is returned (not loaded), return false, otherwise (loaded!) return true
			return (element == null) ? false : true;
		},			
		this.inArray = function(needle, haystack) {
		    var length = haystack.length;
		    for(var i = 0; i < length; i++) {
		        if(haystack[i] == needle) return true;
		    }
		    return false;
		},
		this.log = function(s) {
			if (window.console) {
				console.log(s);
			}
		},
		this.random = function(max, add) {
			return Math.floor(Math.random()*max+add);
		},
		this.isEmail = function isEmail(email){
			return /^[\w-+\.]+@([\w-]+\.)+[\w-]{2,}$/i.test(email);
		},
		this.getId = function(idString) {
			 return idString.substring((idString.search('_')+1));
		},
		this.partial = function(func /*, 0..n args */) {
			var args = Array.prototype.slice.call(arguments, 1);
			return function() {
				var allArguments = args.concat(Array.prototype.slice.call(arguments));
				return func.apply(this, allArguments);
			};
		},
		this.include = function(script,callback){
		    $.getScript(script, function() {
		        if(typeof callback == 'function')
		        callback.apply({},arguments);
		    });
		};		
	};
})(jQuery);


$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
