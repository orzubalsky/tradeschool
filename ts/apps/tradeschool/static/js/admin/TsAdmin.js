;(function($){
var TsAdmin = window.TsAdmin = new function() 
{
    this.init = function() 
    {
        this.replace_add_links();
    };

    this.replace_add_links = function()
    {
    	this.replace_add_link($('#add_id_teacher'), 'teacher');
    	this.replace_add_link($('#add_id_organizers'), 'organizer');
        this.replace_add_link($('#add_id_student'), 'student');        
        this.replace_add_link($('#edit_id_student'), 'student');
    };

    this.replace_add_link = function($element, proxy_model_name)
    {
    	if ($element.size() > 0)
    	{
    		var href = $element.attr('href').replace('person', proxy_model_name);
    		$element.attr('href', href);
    	}
    }
}
})(jQuery);


$(document).ready(function()
{
    TsAdmin.init();
}); 
