;(function($){
var site = window.site = new function() 
{
    this.workingClassSlug;


    this.init = function() 
    {
        //this.classMatch();
        this.course_toggle();
        this.course_load_register_form();
        this.course_submit_register_form();
        this.add_barter_items();
        this.gallery();        
    };


    this.course_load_register_form = function() 
    {
        var self = this;

        $('#closePreview, #matte').on('click', function(e)
        {
            e.preventDefault();
            $('#matte').fadeOut(100, function() 
            {
                $('#preview').empty().hide();
                $('#previewContainer').hide();
            });
        });
                    
        $('.classInfo .join').on('click', function(e) 
        {
            if (!$(this).hasClass('fromHub'))
            {
                e.preventDefault();

                var slug = $(this).attr('id');              

                $('#matte').fadeIn(100, function() 
                {
                    $('#previewContainer').fadeIn(100, function() 
                    {
                        Dajaxice.tradeschool.course_load_form(
                            self.course_load_register_form_callback, 
                            {
                                'branch_slug'   : branchUrl, 
                                'course_slug' : slug
                            }
                        );
                    });
                });
            }
        });	
    };


    this.course_load_register_form_callback = function(data)	
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


    this.course_submit_register_form = function(href) 
    {
        var self = this;
        
        $(document).on('submit', '#registerToClass', function(e) 
        {            
            e.preventDefault();

            $('#registerToClass').animate({'opacity':0}, 100, function()
            {
                $('.seatsLeft').hide();
            });
            $('#loader').show();                

            var slug = $(this).attr('class');
            var data = $(this).serialize();

            Dajaxice.tradeschool.course_submit_form(
                self.course_submit_register_form_callback, 
                {
                    'data'          : data, 
                    'branch_slug'   : branchUrl,
                    'course_slug' : slug
                }
            );				    
        });
    }; 
	

    this.course_submit_register_form_callback = function(data)	
    {
        $('#loader').hide();    
        
        $('#registerToClass').animate({'opacity':1}, 100, function()
        {
            $('.seatsLeft').show();
        });

        $('#preview').empty().append(data).show();

        var height    = $('#preview #classPopup').height();
        var width     = $('#preview #classPopup').width();
        var topOffset = $(document).scrollTop() + 50;
        
        if ($('#previewContainer').hasClass('visible'))
        {
            
        }
        else
        {
            $('#preview, #previewContainer').css({
                'height': height + 'px', 
                'width'	: width + 'px',
                'top'	: topOffset
            }).show();
        }
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


    this.course_toggle = function() 
    {
        var self = this;

        var past = ($('#past').size() > 0) ? true : false;

        $('.classHeader').on('click', function(e) 
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

        $('#addItem').on('click', function(e) 
        {
            e.preventDefault();
            var prefix = 'item';
            
            var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

            var field_1 = $('.barter_item:first').clone(true).get(0);
            $(field_1).val('').insertAfter($('.barter_item:last')).children('.hidden').removeClass('hidden');
            updateElementIndex($(field_1), prefix, formCount);
            
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

        if (count > 1)
        {
            var i = 0;
            var interval = setInterval(function() 
            {
                var next = (i < count-1) ? i+1 : 0;

                $(images).eq(i).animate({
                    opacity : 0
                }, 3000);
                $(images).eq(next).animate({
                    opacity : 1
                }, 3000);   
                i = (i < count-1) ? i+1 : 0;
            }, 9000);            
        }

    };
};
})(jQuery);

$(document).ready(function()
{
	site.init();
});		