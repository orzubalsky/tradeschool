;(function($){
	var site = window.site = new function() 
	{
        this.workingClassId;
        
        this.init = function() 
        {
            this.gallery();

            //this.classMatch();
            this.schedule_toggle();
            this.schedule_preview();

            this.addClassItems();
            //this.registerForm();
		};

        this.gallery = function() 
        {
            var images = $('.gallery img');
            var count = $(images).size();

            $(images).css({'opacity':0});
            $(images).eq(0).css({'opacity':1});

            var i = 0;
            var interval = setInterval(function() 
            {
                var next = (i < count-1) ? i+1 : 0;

                $(images).eq(i).animate({
                    opacity	: 0
                }, 3000);
                $(images).eq(next).animate({
                    opacity	: 1
                }, 3000);	
                i = (i < count-1) ? i+1 : 0;
            }, 9000);

        },
        
        this.schedule_preview = function(href) 
        {
            var self = this;
                        
            $('.join').bind('click', function(e) 
            {
                e.preventDefault();

                var href = $(this).attr('href');				

                $('#matte').fadeIn(100, function() 
                {
                    $('#loader').show();

                    $('#previewContainer').fadeIn(100, function() 
                    {
                        Dajaxice.tradeschool.schedule_form(self.preview_callback(), {'schedule_slug': href});				    
                    });
                });
            });		    
		},	
		
		this.preview_callback = function(data)	
		{
    	    if (data.success == true)
		    {
				$('#loader').hide();
				$('#preview').html(data.html);
                
                var height = $('#preview #classPopup').height();
				var width = $('#preview #classPopup').width();
				var topOffset = $(document).scrollTop() + 50;
				
				$('#preview, #previewContainer')
				.css({
					'height': height+'px', 
					'width'	: width+'px',
					'top'	: topOffset
				})
				.show();				
		    }
		},
		
		this.previewControls = function() {
			var self = this;
			
			$('#closePreview').live('click', function(e) {
				e.preventDefault();
				$('#matte').fadeOut(100, function() {
					$('#preview').empty().hide();
					$('#previewContainer').hide();
				});
			});
		},
		this.addClassItems = function() 
		{
		    var self = this; 
		    
    		function updateElementIndex($el, prefix, ndx) 
    		{
                var id_regex = new RegExp('(' + prefix + '-\\d+)');
                var replacement = prefix + '-' + ndx;
                $el.attr("id", $el.attr("id").replace(id_regex, replacement));
                $el.attr("name", $el.attr("name").replace(id_regex, replacement));
            };

			$('#addItem').live('click', function(e) 
			{
			    e.preventDefault();
			    var prefix = 'item';
			    
                var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
                console.log(formCount);
                var field_1 = $('.barter_item:first').clone(true).get(0);
                var field_2 = $('.barter_qty:first').clone(true).get(0);
                $(field_1).val('').insertAfter($('.barter_qty:last')).children('.hidden').removeClass('hidden');
                $(field_2).val(1).insertAfter($('.barter_item:last')).children('.hidden').removeClass('hidden');            
        	    updateElementIndex($(field_1), prefix, formCount);
        	    updateElementIndex($(field_2), prefix, formCount);
                
                $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
                return false;
			});
		},
		this.classMatch = function() 
		{
		    var self = this;
			var classMatch = window.location.href.match(/\/class\/(.*)/);
			lib.log(classMatch);
			
			if (classMatch) 
			{
				var id = '#class_' + classMatch[1];
			    self.workingClassId = classMatch[1];					
				window.scrollTo(0, $(id).position().top - 10);
				$(id).find('.classBody').slideToggle('slow');
			}			
		},
		this.schedule_toggle = function() 
		{
			var self = this;
			
			var past = ($('#past').size() > 0) ? true : false;
			
			$('.classHeader').live('click', function(e) {
				e.preventDefault();
				
				var classElement = $(this).parent().parent();
				var classId = self.getId($(classElement).attr('id'));
				self.workingClassId = classId;				
				var open = ($(classElement).hasClass('open')) ? true : false;
				
				if (open) {
					$('.classBody', classElement).slideUp(300);
	            	$(classElement).removeClass('open');
				} 
				else 
				{	
					$('.classBody', classElement).slideDown(300);
	            	$(classElement).addClass('open');
				}
			});			
		},
		this.registerForm = function() {
			var self = this;
			
			$('#matte').live('click', function(e) {
				e.preventDefault();
				$('#preview').empty();				
				$('#previewContainer').hide();
				$(this).hide();
			});
			
			$('#registerToClass').live('submit', function(e) {
				e.preventDefault();

				var form = this;
				var params = $(this).serialize();
                
				$.ajax({
					type: "post",
					url :baseUrl + '/../ajax/' + branchUrl + '/class/register/id/' + self.workingClassId,
					data: params,
					dataType: 'json',
					success: function(data){
						if (data.result == true) {

							$('#preview').empty().append(data.template).show();
						
							var height = $('#preview #classPopup').height();
							var width = $('#preview #classPopup').width();
							var topOffset = $(document).scrollTop() + 50;
							
							$('#preview, #previewContainer').css({
								'height': height+'px', 
								'width'	: width+'px',
								'top'	: topOffset
							}).show();							
							
						} else {
							
							$('#preview').empty().append(data.template).show();
							
						}
					},
				});
			});
		},		
		this.getId = function(idString) {
			 return idString.substring((idString.search('_')+1));
		};
	};
})(jQuery);

$(document).ready(function(){
	site.init();
});		