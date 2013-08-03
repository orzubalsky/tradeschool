from django.conf.urls import patterns, url

# tradeschool application
urlpatterns = patterns('tradeschool.views',
 
    url(r'teacher-info$', 'teacher_info', name='teacher-info'),
    url(r'class/add$', 'schedule_add', name='schedule-add'),    
    url(r'class/past$', 'schedule_list_past', name='schedule-list-past'),    
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)/added$', 'schedule_submitted', name='schedule-submitted'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)/register$', 'schedule_register', name='schedule-register'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)/unregister/(?P<student_slug>[0-9A-Za-z\-_]*)$', 'schedule_unregister', name='schedule-unregister'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)/edit$', 'schedule_edit', name='schedule-edit'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)/feedback/(?P<feedback_type>[0-9A-Za-z\-_]+)$', 'schedule_feedback', name='schedule-feedback'),
    url(r'class/(?P<schedule_slug>[0-9A-Za-z\-_]+)$', 'schedule_list', name='schedule-view'),
    url(r'class/$', 'redirect_to_schedule_list', name='redirect-to-schedule-list'),
    url(r'class$', 'redirect_to_schedule_list', name='redirect-to-schedule-list'),    
    url(r'page/(?P<url>.*)$', 'branch_page', name='branch-page'),
    url(r'$', 'schedule_list', name='schedule-list'),    
)
