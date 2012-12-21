from django.conf.urls import patterns, include, url

urlpatterns = patterns('tradeschool.views',
    url(r'^teacher-info$', 'teacher_info', name='teacher-info'),
    url(r'^add$', 'add_class', name='add-class'),
    url(r'^past$', 'past_classes', name='past-classes'),    
    url(r'^(?P<course_slug>[-\w]+)/register$', 'class_register', name='class-register'),    
    url(r'^(?P<course_slug>[-\w]+)$', 'class_list', name='class-view'),
    url(r'^$', 'class_list', name='class-list'),    
)
