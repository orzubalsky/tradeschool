;(function($){
var page = window.page = new function() 
{
    this.page_height;
    this.video_height;
    this.current_page = 0;
    this.total_pages;

    this.init = function() 
    {
        this.page_height = $('#container').outerHeight(true) + 50;
        this.video_height = $('#video').outerHeight(true);
        this.total_pages = $('.section').size() - 1;
        console.log(this.video_height);
        this.navigation();
    };


    this.navigation = function() 
    {
        var self = this;

        $('#previous').on('click', function(e)
        {
            e.preventDefault();
            
            // console.log('preivous');

            self.previous_page();
        });

        $('#next').on('click', function(e)
        {
            e.preventDefault();
            
            // console.log('next');

            self.next_page();            
        });

        // $(window).on('mousewheel', function(e)
        // {
        //     if (e.deltaY > 0)
        //     {
        //         // console.log('up');
        //         self.previous_page();
        //     }
        //     else
        //     {
        //         // console.log('down');
        //         self.next_page();
        //     }
        // }); 

    };

    this.previous_page = function()
    {
        var self = this;

        if (self.current_page > 0)
        {
            var top = $('#content').position().top;        

            var scroll_to = (self.current_page == 4) ? top + self.video_height : top + self.page_height;

            $('#content').animate({ 'top': scroll_to + 'px' }, 100, function()
            {
                self.current_page--;

                (self.current_page == 0) ? $('#previous').hide() : $('#previous').show();
                (self.current_page == self.total_pages) ? $('#next').hide() : $('#next').show();                
            });
        }
    };

    this.next_page = function()
    {
        var self = this;

        if (self.current_page < self.total_pages)
        {
            var top = $('#content').position().top;        

            var scroll_to = (self.current_page == 2) ? top - self.video_height : top - self.page_height;

            $('#content').animate({ 'top': scroll_to + 'px' }, 100, function()
            {
                self.current_page++;

                (self.current_page == 0) ? $('#previous').hide() : $('#previous').show();
                (self.current_page == self.total_pages) ? $('#next').hide() : $('#next').show();                
            });
        }
    };

};
})(jQuery);

$(document).ready(function()
{
	page.init();
});		