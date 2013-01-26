from django.conf.urls import patterns, include, url

urlpatterns = patterns('hub.views',
    url(r'^$', 'branch_list', name='branch-list'),
)
