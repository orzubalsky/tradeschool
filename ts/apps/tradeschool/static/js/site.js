;(function($){
var site = window.site = new function() 
{
    this.workingClassSlug;


    this.init = function() 
    {
        //this.classMatch();
        this.schedule_toggle();
        this.schedule_load_register_form();
        this.schedule_submit_register_form();
        this.add_barter_items();
        this.gallery();        
    };


    this.schedule_load_register_form = function() 
    {
        var self = this;

        $('#closePreview, #matte').live('click', function(e)
        {
            e.preventDefault();
            $('#matte').fadeOut(100, function() 
            {
                $('#preview').empty().hide();
                $('#previewContainer').hide();
            });
        });
                    
        $('.classInfo .join').bind('click', function(e) 
        {
            e.preventDefault();

            var slug = $(this).attr('id');				

            $('#matte').fadeIn(100, function() 
            {
                $('#loader').show();

                $('#previewContainer').fadeIn(100, function() 
                {
                    Dajaxice.tradeschool.schedule_load_form(self.schedule_load_register_form_callback, {'branch_slug': branchUrl, 'schedule_slug': slug});				    
                });
            });
        });		    
    };


    this.schedule_load_register_form_callback = function(data)	
    {
        $('#loader').hide();
        $('#preview').html(data);

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
    };


    this.schedule_submit_register_form = function(href) 
    {
        var self = this;
        
        $('#registerToClass').live('submit', function(e) 
        {            
            e.preventDefault();

            var slug = $(this).attr('class');
            var data = $(this).serialize();

            Dajaxice.tradeschool.schedule_submit_form(self.schedule_submit_register_form_callback, {'data': data, 'schedule_slug': slug});				    
        });
    }; 
	

    this.schedule_submit_register_form_callback = function(data)	
    {
        $('#preview').empty().append(data).show();

        var height    = $('#preview #classPopup').height();
        var width     = $('#preview #classPopup').width();
        var topOffset = $(document).scrollTop() + 50;

        $('#preview, #previewContainer').css({
            'height': height + 'px', 
            'width'	: width + 'px',
            'top'	: topOffset
        }).show();
    };


    this.classMatch = function() 
    {
        var self = this;
        var classMatch = window.location.href.match(/\/class\/(.*)/);

        if (classMatch) 
        {
            var id = '#class_' + classMatch[1];
            self.workingClassId = classMatch[1];	
            window.scrollTo(0, $(id).position().top - 10);
            $(id).find('.classBody').slideToggle('slow');
        }
    };


    this.schedule_toggle = function() 
    {
        var self = this;

        var past = ($('#past').size() > 0) ? true : false;

        $('.classHeader').live('click', function(e) 
        {
            e.preventDefault();

            var classElement = $(this).parent().parent();
            self.workingClassSlug = $(classElement).attr('id');
            var open = ($(classElement).hasClass('open')) ? true : false;

            if (open)
            {
                $('.classBody', classElement).slideUp(300);
                $(classElement).removeClass('open');
            } 
            else 
            {	
                $('.classBody', classElement).slideDown(300);
                $(classElement).addClass('open');
            }
        });
    };


    this.add_barter_items = function() 
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

            var field_1 = $('.barter_item:first').clone(true).get(0);
            var field_2 = $('.barter_qty:first').clone(true).get(0);
            $(field_1).val('').insertAfter($('.barter_qty:last')).children('.hidden').removeClass('hidden');
            $(field_2).val(1).insertAfter($('.barter_item:last')).children('.hidden').removeClass('hidden');            
            updateElementIndex($(field_1), prefix, formCount);
            updateElementIndex($(field_2), prefix, formCount);
            
            $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
            return false;
        });
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
    };
};
})(jQuery);

$(document).ready(function()
{
	site.init();
});		