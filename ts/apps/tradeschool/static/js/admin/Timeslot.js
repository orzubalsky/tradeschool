;(function($){
var Timeslot = window.Timeslot = new function() 
{
    this.init = function() 
    {
        this.end_date();
    };

    this.end_date = function()
    {
        $('.end_time .ui-datepicker-trigger').eq(0).hide();

        $('#id_start_time_0').on('change', function()
        {
            var date_value = this.value;
            $('#id_end_time_0').val(date_value);
        });

        $('.grp-fixed-footer input').on('click', function(e)
        {
            e.preventDefault(); 
            e.stopPropagation();

            var date_value = $('#id_start_time_0').val();
            $('#id_end_time_0').val(date_value);     

            $(this).unbind('click').click();
        });
    };
}
})(jQuery);


$(document).ready(function()
{
    Timeslot.init();
}); 
