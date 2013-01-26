from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config


admin.autodiscover()
dajaxice_autodiscover()

# direct browser requests to the different apps
urlpatterns = patterns('',
    url(r'^rosetta/', include('rosetta.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    (r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^tinymce/', include('tinymce.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),    
)

if settings.SITE_ID == 1:
    urlpatterns += patterns('', url(r'^', include('hub.urls')),)

urlpatterns += patterns('',
    url(r'^', include('tradeschool.urls')),
)

# static files url patterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
   )


urlpatterns += patterns('django.contrib.flatpages.views',
    #(r'^(?P<url>.*)$', 'flatpage'),
)
