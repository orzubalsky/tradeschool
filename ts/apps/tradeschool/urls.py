from django.conf.urls import patterns, include, url

# tradeschool application
urlpatterns = patterns('tradeschool.views',
 
    url(r'teacher-info$', 'teacher_info', name='teacher-info'),
    url(r'class/add$', 'schedule_add', name='schedule-add'),    
    url(r'class/past$', 'past_schedules', name='past-classes'),    
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)/added$', 'schedule_submitted', name='schedule-submitted'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)/register$', 'schedule_register', name='schedule-register'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)/unregister/(?P<student_slug>[0-9A-Za-z\-]+)$', 'schedule_unregister', name='schedule-unregister'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)/edit$', 'schedule_edit', name='schedule-edit'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)/feedback/(?P<feedback_type>[0-9A-Za-z\-]+)$', 'schedule_feedback', name='schedule-feedback'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-]+)$', 'schedule_list', name='schedule-view'),
    url(r'page/(?P<url>.*)$', 'branchpage'),
    url(r'$', 'schedule_list', name='schedule-list'),    
)
