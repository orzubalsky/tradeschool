from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from tradeschool.models import Branch

admin.autodiscover()

# direct browser requests to the different apps
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ts.views.home', name='home'),
    # url(r'^ts/', include('ts.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    (r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^class/', include('tradeschool.urls')),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),     
    (r'^.*/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
