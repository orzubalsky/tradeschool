from django.conf.urls import patterns, url

# tradeschool application
urlpatterns = patterns(
    'tradeschool.views',

    url(r'admin$', 'redirect_to_admin', name='redirect-to-admin'),
    url(r'admin/$', 'redirect_to_admin', name='redirect-to-admin'),
    url(r'teacher-info$', 'teacher_info', name='teacher-info'),
    url(r'class/add$', 'course_add', name='course-add'),
    url(r'class/past$', 'course_list_past', name='course-list-past'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)/added$', 'course_submitted', name='course-submitted'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)/register$', 'course_register', name='course-register'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)/unregister/(?P<student_slug>[0-9A-Za-z\-_]*)$', 'course_unregister', name='course-unregister'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)/edit$', 'course_edit', name='course-edit'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)/feedback/(?P<feedback_type>[0-9A-Za-z\-_]+)$', 'course_feedback', name='course-feedback'),
    url(r'class/(?P<course_slug>[0-9A-Za-z\-_]+)$', 'course_view', name='course-view'),
    url(r'class/$', 'redirect_to_course_list', name='redirect-to-course-list'),
    url(r'class$', 'redirect_to_course_list', name='redirect-to-course-list'),
    url(r'page/(?P<url>.*)$', 'branch_page', name='branch-page'),
    url(r'page/(?P<url>.*)/$', 'branch_page', name='branch-page'),
    url(r'$', 'course_list', name='course-list'),
)
