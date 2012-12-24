from notifications.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

# adding 'dispatch_uid' because this signal was getting reigstered twice. 'dispatch_uid' just needs to be some unique string.
#
# more info here on a better way to fix this problem:
# http://stackoverflow.com/questions/2345400/why-is-post-save-being-raised-twice-during-the-save-of-a-django-model
@receiver(post_save, sender=Branch, dispatch_uid="ts.apps.tradeschool.signals")
def branch_save_callback(sender, instance, **kwargs):
    """ create notifications on creation of a new branch."""    
    if instance.notifications.count() == 0:
        instance.populate_notifications()


@receiver(post_save, sender=Schedule, dispatch_uid="ts.apps.tradeschool.signals")
def schedule_save_callback(sender, instance, **kwargs):
    """ create notifications on creation of a new schedule."""
    if instance.notifications.count() == 0:
        instance.populate_notifications()