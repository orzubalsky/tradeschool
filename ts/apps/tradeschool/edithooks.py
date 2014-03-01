from templatesadmin.edithooks import TemplatesAdminHook
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django import forms


class CollectStaticFilesHook(TemplatesAdminHook):
    """
    Run collectstatic mangagement command after saving.
    """

    @classmethod
    def post_save(cls, request, form, template_path):
        call_command('collectstatic', interactive=False)

    @classmethod
    def contribute_to_form(cls, template_path):
        return dict(backup=forms.BooleanField(
            label=_('Update site?'),
            initial=True,
            required=False,
        ))
