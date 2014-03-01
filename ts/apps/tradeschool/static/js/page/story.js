;(function($){
var page = window.page = new function() 
{
    this.last_scroll_value;
    this.total_height;
    this.is_scrolling = false;
    this.ignore_scroll_event = false;
    this.page_height;
    this.video_height;
    this.$pages;
    this.current_page = 0;
    this.total_pages;

    this.init = function() 
    {
        this.$pages = $('.section');
        this.page_height = $('#container').outerHeight(true) - 50;
        this.video_height = $('#video').outerHeight(true);
        this.total_pages = this.$pages.size() - 1;
        this.last_scroll_value = Math.round($(document).scrollTop());
        this.total_height = $(document).height();

        $('.section').css({'height': this.page_height + 'px', 'max-height': this.page_height});

        this.navigation_buttons_display(this.last_scroll_value);
        this.navigation();
        this.set_scroll_functionality();
    };

    this.navigation = function() 
    {
        var self = this;

        $('#previous').on('click', function(e)
        {
            e.preventDefault();
            
            // console.log('preivous');

            self.ignore_scroll_event = true;

            self.scroll_to(self.get_target_scroll_position(false));
        });

        $('#next').on('click', function(e)
        {
            e.preventDefault();
            
            // console.log('next');
            // console.log(self.last_scroll_value);

            self.ignore_scroll_event = true;

            self.scroll_to(self.get_target_scroll_position(true));          
        });
    };

    this.set_scroll_functionality = function()
    {
        var self = this;

        $(window).scroll(function(scroll_event)
        {
            if (self.is_scrolling)
            {
                clearTimeout(self.is_scrolling);
            }
            
            self.is_scrolling = setTimeout(function()
            { 
                if (self.ignore_scroll_event)
                {
                    self.ignore_scroll_event = false;

                    return false;
                }
                else
                {
                    self.after_scroll_callback(scroll_event);
                }
            }, 400);
        });        
    };

    this.after_scroll_callback = function(e)
    {
        // console.log('after_scroll_callback');
        
        var self = this;

        self.ignore_scroll_event = true;
        
        var current_scroll_position = $(document).scrollTop();

        if (Math.abs(current_scroll_position - self.last_scroll_value) > 10)
        {

            var scroll_down = (current_scroll_position > self.last_scroll_value) ? true : false;

            self.scroll_to(self.get_target_scroll_position(scroll_down));            
        }
    };

    this.scroll_to = function(top_value)
    {
        // console.log('scroll_to');

        var self = this;

        var target_scroll_position = Math.round(top_value);

        $('html, body').animate(
        {
            scrollTop: target_scroll_position
        }, 100, function()
        {
            self.last_scroll_value = target_scroll_position;

            self.navigation_buttons_display(target_scroll_position); 
        });
    };

    this.navigation_buttons_display = function(scroll_position)
    {
        var self = this;

        (scroll_position <= 0) ? $('#previous').hide() : $('#previous').show();
        (scroll_position >= self.total_height - 2 * self.page_height) ? $('#next').hide() : $('#next').show();   
    };

    this.get_target_scroll_position = function(scroll_down)
    {
        // console.log('get_target_scroll_position');

        var self = this;

        var current_scroll_position = Math.round($(document).scrollTop());

        var target_scroll_position;

        if (scroll_down)
        {
            for (var i=self.total_pages; i>=0; i--)
            {
                var page_top = Math.round(self.$pages.eq(i).position().top);

                // console.log('page_top: ' + page_top);

                if (page_top > current_scroll_position)
                {
                    target_scroll_position = page_top;
                    // console.log('setting target_scroll_position to: ' + target_scroll_position);                    
                }
            }            
        }
        else
        {
            for (var i=0; i<self.total_pages; i++)
            {
                var page_top = Math.round(self.$pages.eq(i).position().top);

                if (page_top < current_scroll_position)
                {
                    target_scroll_position = page_top;
                }
            }
        }
        // console.log('target_scroll_position: ' + target_scroll_position);

        return Math.round(target_scroll_position);

    };

};
})(jQuery);

$(document).ready(function()
{
	page.init();
});		