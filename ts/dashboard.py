"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'tradeschool.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


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
        self.children.append(modules.Group(
            column=1,
            collapsible=False,
            children = [
                modules.ModelList(
                    title=_('Classes'),
                    column=1,
                    collapsible=False,
                    models=(
                            'tradeschool.models.PendingSchedule',
                            'tradeschool.models.ApprovedSchedule',
                            'tradeschool.models.PastSchedule',
                            'tradeschool.models.Registration',
                            'tradeschool.models.Venue',
                            'tradeschool.models.BarterItem',
                            ),
                ),
                modules.ModelList(
                    title=_('Manage Times for Class Submissions'),
                    column=1,
                    collapsible=False,
                    models=(
                            'tradeschool.models.Time',
                            'tradeschool.models.TimeRange',
                            ),
                ), 
                modules.ModelList(
                    title=_('People'),
                    column=1,
                    collapsible=False,
                    models=(
                            'tradeschool.models.Student',
                            'tradeschool.models.Teacher',
                            'tradeschool.models.Organizer',                            
                            ),
                ),    
                modules.ModelList(
                    title=_('Settings'),
                    column=1,
                    collapsible=False,
                    models=(
                            'tradeschool.models.Branch',
                            'tradeschool.models.Cluster',                            
                            ),
                ),
                modules.ModelList(
                    title=_('Emails'),
                    collapsible=False,                    
                    column=1,
                    models=('tradeschool.models.DefaultEmailContainer', 
                            ),                    
                ),
                modules.ModelList(
                    title=_('Website Content'),
                    collapsible=False,                    
                    column=1,
                    models=('tradeschool.models.Photo',
                            'tradeschool.models.Page',                    
                            'django.contrib.flatpages.models.FlatPage',
                            ),
                ),   
                modules.ModelList(
                    title=_('Settings'),
                    collapsible=False,                    
                    column=1,
                    models=('django.contrib.auth.models.Group', 
                            'django.contrib.auth.models.User',),
                ),
                # modules.AppList(
                #                     title=_('Everything Else'),
                #                     column=1,
                #                     collapsible=False,
                #                     exclude=('',
                #                              ),
                #                 )                 
            ]
        ))
            
        self.children.append(modules.Group(
           column=2,
           collapsible=False,
           children = [
                
              # append a feed module for talk.tradeschool.coop posts
              # modules.Feed(
              #     title=_('Recent TalkTS Posts'),
              #     collapsible=False,                      
              #     column=1,
              #     limit=10,
              #     feed_url='http://talk.tradeschool.coop/rss',            
              # ),
              modules.LinkList(
                  layout='inline',
                  column=1,
                  children=(
                    ['Translate TS', '/rosetta/pick/'],
                    ['Talk TS', 'http://talk.tradeschool.coop', True],
                    ['Trade School', 'http://tradeschool.coop', True]
                  )
                  
              ),
           ]
      ))        