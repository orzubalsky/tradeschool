;(function($){
	var calendar = window.site.calendar = new function() {
		this.classes = [];
		this.venues = [];
		this.season = [];
		this.eventSources = [];
		this.selectedEvents = [];
		this.init = function() {
			this.getBranchData();
		},
		this.calendars = function() {
			var self = this;
			
			self.generateEventSources();
			var seasonStartTime = new Date(self.season.unix_start_time * 1000);
			var year = parseInt(seasonStartTime.toString('yyyy'));
			var month = parseInt(seasonStartTime.toString('MM'));
			var day = parseInt(seasonStartTime.toString('dd'));
			
			var calendar = $('#calendar').fullCalendar({
				year: year,
				month: month,
				day: day,
				header: {
					left: 'today',
					center: 'title',
					right: 'prev,next'
				}, 		
				editable: false,
				eventSources: self.getEventSources(), 
				eventClick: function(calEvent, jsEvent, view) {

					if (calEvent.type == 'available')
					{
						// fill in start time, end time, and venue_id in class registration form
						self.populateTimeFields(calEvent.start, calEvent.end, calEvent.start_unix, calEvent.end_unix, calEvent.venue_id, calEvent.time_id);
						
						// get DOM element -- this is the inner event div. both this and its parent affect the way events look
						var event = $(jsEvent.target).closest('.fc-event-inner');
						var eventContainer = $(event).parent();
						
						// reset event colors so we can use css classes to style it
						$(event).css({'background-color':'', 'border-color':''});
						$(eventContainer).css({'background-color':'', 'border-color':''});
						
						// toggle css classes
						if ($(eventContainer).hasClass('selected')) 
						{
							// make event available
							$(eventContainer).removeClass('selected').addClass('available');
							
							// clear all stored selected events
							self.removeFromSelectedEvents(calEvent, eventContainer);
							
							// set form start, end & venue_id fields
							var range = self.findSelectedEventsRange();
							self.populateTimeFields(range.start, range.end, range.start_unix, range.end_unix, calEvent.venue_id, calEvent.time_id);
						}
						else 
						{
							// reset all other events
							$('#calendar .fc-event').removeClass('selected').addClass('available');
							
							// make event selected
							$(eventContainer).removeClass('available').addClass('selected');
							
							// check if this is an adjacent event
							for(var i=0; i < self.selectedEvents.length; i++)
							{
								var storedEvent = self.selectedEvents[i];

								// if the clicked event follows a stored selected event
								if (calEvent.start.getTime() == storedEvent.end.getTime() && calEvent.venue_id == storedEvent.venue_id)
								{
									// make stored event selected
									storedEvent.$element.removeClass('available').addClass('selected');									
								}
								
								// if the clicked event precends a stored selected event
								else if (calEvent.end.getTime() == storedEvent.start.getTime() && calEvent.venue_id == storedEvent.venue_id)
								{
									// make stored event selected
									storedEvent.$element.removeClass('available').addClass('selected');									
								} 
								else 
								{
									// clear all selected events
									self.clearSelectedEvents();
								}
							}
							self.addToSelectedEvents(calEvent, eventContainer);
							
							// set form start, end & venue_id fields
							var range = self.findSelectedEventsRange();
							self.populateTimeFields(range.start, range.end, range.start_unix, range.end_unix, calEvent.venue_id, calEvent.time_id);
						}
						
						// if there are no selected events, 
						if (self.selectedEvents.length == 0)
						{
							// clear time & venue fields
							self.clearTimeFields();
						}
						
					}
			    },			
				loading: function(bool) {
					if (bool) $('#loading').show();
					else $('#loading').hide();
				},
				editable: true
			});
		},
		this.findSelectedEventsRange = function() 
		{
			var self = this;
			var startTimes	= [];
			var endTimes	= [];
			var unixStartTimes = [];
			var unixEndTimes = [];
			
			for(var i=0; i<self.selectedEvents.length; i++)
			{
				var event = self.selectedEvents[i];
				startTimes.push(event.start.getTime());
				endTimes.push(event.end.getTime());
				
				unixStartTimes.push(event.start_unix.getTime());
				unixEndTimes.push(event.end_unix.getTime());				
			}
			
			var minStart= Math.min.apply(null, startTimes);
			var maxEnd	= Math.max.apply(null, endTimes);

			var minStart_unix = Math.min.apply(null, unixStartTimes);
			var maxEnd_unix = Math.max.apply(null, unixEndTimes);
			
			
			return {start:minStart, end:maxEnd, start_unix:minStart_unix , end_unix:maxEnd_unix};
		},
		this.addToSelectedEvents = function(calEvent, element)
		{
			var self = this;
			
			self.selectedEvents.push({
				id		: calEvent.id,
				$element: element,
				start	: calEvent.start,
				end		: calEvent.end,
				venue_id: calEvent.venue_id
			});	
		},
		this.removeFromSelectedEvents = function(calEvent, element)
		{
			var self = this;
			
			for(var i=0; i<self.selectedEvents.length; i++)
			{
				var event = self.selectedEvents[i];
				if (event.id == calEvent.id) {
					self.selectedEvents.splice(i,1);
			    }
			}
			
			
		},		
		this.clearSelectedEvents = function()
		{
			var self = this;
			
			self.selectedEvents = [];
		},
		this.populateTimeFields = function(start, end, start_unix, end_unix, venueId, timeId) {
			var self = this;
			
			self.clearTimeFields();
			
			$('input#unix_start_time').val(start_unix);

			$('input#unix_end_time').val(end_unix);
			
			$('input#venue_id').val(venueId);
			
			$('input#time_id').val(timeId);
			
		},
		this.clearTimeFields = function() {

			$('input#unix_start_time').val('');
			$('input#unix_end_time').val('');
			$('input#venue_id').val('');
			$('input#time_id').val('');
		},
		this.generateEventSources = function() {
			
			var self = this;
			var colors = ['#fff','#eee', '#ddd', 'green', 'red'];
			
			for(var i=0; i<self.venues.length; i++)
			{
				var venue = self.venues[i];
				var url = baseUrl + '/../ajax/' + branchUrl + '/venue/data/id/' + venue.id;
			
				self.eventSources.push({
					name		: 'times_eventSource_' + i,
					venueId		: venue.id,
					type		: 'times',
					eventSource	: {
						url		: baseUrl + '/../ajax/' + branchUrl + '/venue/data/id/'+venue.id+'/type/times',
				   		color	: '#fff',   
				   		textColor: 'black',
				   		className : 'available'
					}
				});
				/*
				self.eventSources.push({
					name		: 'classes_eventSource_' + i,
					venueId		: venue.id,
					type		: 'classes',
					eventSource	: {
						url		: baseUrl + '/../ajax/venue/data/id/'+venue.id+'/type/classes',
					   	color	: colors[4],   
					   	textColor: 'black',
				   		className : 'classTime'
					}
				});
				*/							
			}
		
		},		
		this.getEventSources = function(action) {
			
			var self = this;
			var eventSources = [];
			
			for(var i=0; i<self.eventSources.length; i++)
			{
				eventSources.push(self.eventSources[i].eventSource);
			}
			
			return eventSources;
		
		},
		this.getBranchData = function() {
			var self = this;
			
			var pathname = window.location.pathname;
			var query = new RegExp('class/add', 'i');
			var query2 = new RegExp('class/edit', 'i');

			if (pathname.search(query) > 0 || pathname.search(query2) > 0) 
			{ 
				$.ajax({ url: baseUrl + '/../ajax/' + branchUrl + '/branch/data/', dataType: 'json', type: 'post', data: {},
		            success: function(data) {
		                self.venues = data.venues;
		                self.classes = data.classes;
		                self.season = data.season;
		                self.calendars();
		            }
				});		
			}
		};
	};
})(jQuery);

$(document).ready(function(){
	site.calendar.init();
});		