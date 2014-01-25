"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'tradeschool.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from tradeschool.models import Person

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

        user = Person.objects.get(fullname=context['user'])

        self.children.append(modules.Group(
            column=1,
            collapsible=False,
            children=[
                modules.ModelList(
                    title=_('Classes'),
                    column=1,
                    collapsible=False,
                    models=(
                        'tradeschool.models.TemplateFile',
                        'tradeschool.models.PendingCourse',
                        'tradeschool.models.ApprovedCourse',
                        'tradeschool.models.PastCourse',
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
                        'tradeschool.models.PendingBranch',
                    ),
                ),
                modules.ModelList(
                    title=_('Website Content'),
                    collapsible=False,
                    column=1,
                    models=(
                        'tradeschool.models.Photo',
                        'tradeschool.models.Page',
                    ),
                ),
            ]
        ))

        if user.is_superuser:
            self.children.append(
                modules.ModelList(
                    collapsible=False,
                    column=1,
                    models=(
                        'django.contrib.auth.models.Group',
                        'django.contrib.sites.models.Site',
                        'django.contrib.flatpages.models.FlatPage',
                        'tradeschool.models.Cluster',
                        'tradeschool.models.DefaultEmailContainer',
                    ),
                ),
            )

        self.children.append(modules.Group(
            column=2,
            collapsible=False,
            children=[
                modules.LinkList(
                    layout='inline',
                    column=1,
                    children=(
                        ['Translate TS', '/rosetta/pick/'],
                        ['Edit HTML Templates', '/admin/templatesadmin/'],
                        ['Talk TS', 'http://talk.tradeschool.coop', True],
                        ['Trade School', 'http://tradeschool.coop', True]
                    )
                ),
            ]
        ))
