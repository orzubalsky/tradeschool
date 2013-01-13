from django.conf.urls import patterns, include, url

urlpatterns = patterns('tradeschool.views',
    url(r'^teacher-info$', 'teacher_info', name='teacher-info'),
    url(r'^class/add$', 'schedule_add', name='schedule-add'),
    url(r'^class/past$', 'past_schedules', name='past-classes'),    

    url(r'^class/(?P<schedule_slug>[-\w]+)/register$', 'schedule_register', name='schedule-register'),
    url(r'^class/(?P<schedule_slug>[-\w]+)/unregister/(?P<student_slug>[-\w]+)$', 'schedule_unregister', name='schedule-unregister'),
    url(r'^class/(?P<schedule_slug>[-\w]+)/edit$', 'schedule_edit', name='schedule-edit'),
    url(r'^class/(?P<schedule_slug>[-\w]+)/feedback$', 'schedule_feedback_student', name='schedule-feedback-student'),
    url(r'^class/(?P<schedule_slug>[-\w]+)/feedback$', 'schedule_feedback_teacher', name='schedule-feedback-teacher'),
        
    url(r'^class/(?P<schedule_slug>[-\w]+)$', 'schedule_list', name='schedule-view'),
    url(r'^$', 'schedule_list', name='schedule-list'),
)
