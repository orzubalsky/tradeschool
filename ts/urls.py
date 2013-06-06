from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config


admin.autodiscover()
dajaxice_autodiscover()


# administration apps
urlpatterns = patterns('',
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# administration password reset urls
urlpatterns += patterns('',
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

# tinyMCE editor
urlpatterns += patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
)
    
# dajaxice urls
urlpatterns += patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

# flat pages
urlpatterns += patterns('django.contrib.flatpages.views',
    # it's probably better to specify specific flat page urls here so they don't interfere with branch slugs
    #(r'^(?P<url>[0-9A-Za-z]+)$', 'flatpage'),
)

# static files url patterns
urlpatterns += staticfiles_urlpatterns()

# serve static files from media directory when in debug mode
if settings.DEBUG: 
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
   )
   
# tradeschool app urls
urlpatterns += patterns('',
   url(r'^(?P<branch_slug>[0-9A-Za-z\-]+)/', include('tradeschool.urls')),
   url(r'^$', 'tradeschool.views.branch_list', name='branch-list'),    
)    
