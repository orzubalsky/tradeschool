"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'tradeschool.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
from django.conf import settings


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    class Media:
        css = {
            'all': (
                'css/admin.css',
            ),
        }
                
    columns = 3
    template = 'admin/dashboard.html'
    
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # tradeschool.coop admin displays all apps        
        if settings.SITE_ID == 1:
            self.children.append(modules.Group(
                title=_('Admin'),
                column=3,
                collapsible=False,
                children= [
                    modules.ModelList(
                        title=_('Everything'),
                        column=1,
                    ),
                ]
            ))
            
        # individual school admin displays only relevant apps
        else:        
            self.children.append(modules.Group(
                column=1,
                collapsible=False,
                children = [
                    modules.ModelList(
                        title=_('Scheduling'),
                        column=1,
                        collapsible=True,
                        models=('tradeschool.models.Schedule', 
                                'tradeschool.models.Time',
                                'tradeschool.models.TimeRange',
                                'tradeschool.models.Student',
                                'tradeschool.models.Teacher',
                                'tradeschool.models.Course',
                                'tradeschool.models.Venue'),
                    ),
                    modules.ModelList(
                        title=_('Emails'),
                        column=1,
                        models=('notifications.models.BranchNotificationTemplate', 
                                'notifications.models.BranchNotification',
                                'notifications.models.ScheduleNotification',
                                'mailer.models.MessageLog',
                                'mailer.models.Message'),                    
                    ),
                    modules.ModelList(
                        title=_('Website Content'),
                        column=1,
                        models=('website.models.Photo', 
                                'django.contrib.flatpages.models.FlatPage',),
                    ),   
                    modules.ModelList(
                        title=_('Settings'),
                        column=1,
                        models=('django.contrib.auth.models.Group', 
                                'django.contrib.auth.models.User',),
                    ),
                    modules.AppList(
                        title=_('Everything Else'),
                        column=1,
                        collapsible=True,
                        exclude=('django.contrib.*',),
                    )                 
                ]
            ))
                
            self.children.append(modules.Group(
               column=2,
               collapsible=False,
               children = [
          
                  # append a feed module for talk.tradeschool.coop posts
                  modules.Feed(
                      title=_('Recent TalkTS Posts'),
                      collapsible=False,                      
                      column=1,
                      limit=10,
                      feed_url='http://talk.tradeschool.coop/rss',            
                  ),
          
                  # append a recent actions module
                  # modules.RecentActions(
                  #     title=_('Recent Actions'),
                  #     column=1,
                  #     limit=5,
                  # )
               ]
          ))        