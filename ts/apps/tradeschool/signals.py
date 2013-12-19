from tradeschool.models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
from tradeschool.utils import daterange


# adding 'dispatch_uid' because this signal was getting reigstered twice.
# 'dispatch_uid' just needs to be some unique string.
#
# more info here on a better way to fix this problem:
# http://stackoverflow.com/questions/2345400/why-is-post-save-being-raised-twice-during-the-save-of-a-django-model
@receiver(post_save, sender=Branch, dispatch_uid="ts.apps.tradeschool.signals")
def branch_save_callback(sender, instance, **kwargs):
    """
    Create notifications on creation of a new branch.
    Create a copy of the default template files when a new branch is created.
    """
    # create files
    if kwargs.get('created'):
        instance.generate_files()

    # don't generate emails if this is branch is created when running
    # loaddata command. apparently saving from a fixture has the
    # 'raw' key argument
    if kwargs.get('created') and not kwargs.get('raw', False):
        if instance.emails is None:
            instance.populate_notifications()

    # Create Teacher Info Page
    # but don't create it if this branch is created when running
    # loaddata command. saving from a fixture has the 'raw' key argument
    if kwargs.get('created') and not kwargs.get('raw', False):
        try:
            Page.objects.get(url='/teacher-info/', branch=instance)
        except Page.DoesNotExist:
            instance.copy_teacher_info_page()


@receiver(post_save, sender=Schedule, dispatch_uid="ts.apps.tradeschool.signals")
def schedule_save_callback(sender, instance, **kwargs):
    """ create notifications on creation of a new schedule"""

    # don't generate emails if this is branch is created when running
    # loaddata command. apparently saving from a fixture has the
    # 'raw' key argument
    if kwargs.get('created') and not kwargs.get('raw', False):
        if instance.emails is None:
            instance.populate_notifications()


@receiver(post_save, sender=TimeRange, dispatch_uid="ts.apps.tradeschool.signals")
def timerange_save_callback(sender, instance, **kwargs):
    """
    create single time slots based on the creation of a time range object.
    """
    # empty list for bulk_create
    timeList = []

    # iterate over days in date range set in the form
    for single_date in daterange(instance.start_date, instance.end_date):

        # add a time object only when the day in range
        # is a weekday that was checked by the user
        weekday = single_date.weekday()

        if (weekday == 0 and instance.monday) \
                or (weekday == 1 and instance.tuesday) \
                or (weekday == 2 and instance.wednesday) \
                or (weekday == 3 and instance.thursday) \
                or (weekday == 4 and instance.friday) \
                or (weekday == 5 and instance.saturday) \
                or (weekday == 6 and instance.sunday):

            # add the start time & end time from the form in order to
            # create a datetime object, as required by the Time model
            start_time = datetime.combine(single_date, instance.start_time)
            end_time = datetime.combine(single_date, instance.end_time)

            # now do timezone conversion
            current_tz = timezone.get_current_timezone()
            utc = pytz.timezone('UTC')

            localized_start_time = current_tz.localize(start_time)
            localized_end_time = current_tz.localize(end_time)

            normalized_start_time = utc.normalize(
                localized_start_time.astimezone(utc))

            normalized_end_time = utc.normalize(
                localized_end_time.astimezone(utc))

            #aware_start_time = timezone.make_aware(start_time, timezone.utc)
            #aware_end_time   = timezone.make_aware(end_time, timezone.utc)

            now = timezone.now()

            # append a time object to the list so
            # all of them can be inserted in one query
            timeList.append(Time(
                start_time=normalized_start_time,
                end_time=normalized_end_time,
                branch=instance.branch,
                venue=instance.venue,
                created=now,
                updated=now)
            )

    # save time slots
    Time.objects.bulk_create(timeList)


@receiver(post_delete, sender=TimeRange, dispatch_uid="ts.apps.tradeschool.signals")
def timerange_delete_callback(sender, instance, **kwargs):
    """
    delete all time slots within a time range object.
    """
    # iterate over days in date range set in the form
    for single_date in daterange(instance.start_date, instance.end_date):

        # add a time object only when the day in range
        # is a weekday that was checked by the user
        weekday = single_date.weekday()

        if (weekday == 0 and instance.monday) \
                or (weekday == 1 and instance.tuesday) \
                or (weekday == 2 and instance.wednesday) \
                or (weekday == 3 and instance.thursday) \
                or (weekday == 4 and instance.friday) \
                or (weekday == 5 and instance.saturday) \
                or (weekday == 6 and instance.sunday):

            # add the start time & end time from the form in order to
            # create a datetime object, as required by the Time model
            start_time = datetime.combine(single_date, instance.start_time)
            end_time = datetime.combine(single_date, instance.end_time)

            # delete time
            try:
                Time.objects.filter(
                    start_time=start_time,
                    end_time=end_time)[0].delete()
            except IndexError:
                pass
