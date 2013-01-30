from tradeschool.models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from time import strftime
from datetime import datetime

# adding 'dispatch_uid' because this signal was getting reigstered twice. 'dispatch_uid' just needs to be some unique string.
#
# more info here on a better way to fix this problem:
# http://stackoverflow.com/questions/2345400/why-is-post-save-being-raised-twice-during-the-save-of-a-django-model
@receiver(post_save, sender=Branch, dispatch_uid="ts.apps.tradeschool.signals")
def branch_save_callback(sender, instance, **kwargs):
    """ create notifications on creation of a new branch."""    
    try:
        emails = BranchEmailContainer.objects.get(branch=instance)
    except BranchEmailContainer.DoesNotExist:
        instance.populate_notifications()


@receiver(post_save, sender=Schedule, dispatch_uid="ts.apps.tradeschool.signals")
def schedule_save_callback(sender, instance, **kwargs):
    """ create notifications on creation of a new schedule"""
    try:
        emails = ScheduleEmailContainer.objects.get(schedule=instance)
    except ScheduleEmailContainer.DoesNotExist:
        instance.populate_notifications()


@receiver(post_save, sender=TimeRange, dispatch_uid="ts.apps.tradeschool.signals")
def timerange_save_callback(sender, instance, **kwargs):
    """ create single time slots based on the creation of a time range object."""

    # empty list for bulk_create
    timeList = []    

    # iterate over days in date range set in the form
    for single_date in daterange(instance.start_date, instance.end_date):

        # add a time object only when the day in range is a weekday that was checked by the user
        weekday = single_date.weekday()

        if (weekday == 0 and instance.monday) or (weekday == 1 and instance.tuesday) or (weekday == 2 and instance.wednesday) or (weekday == 3 and instance.thursday) or (weekday == 4 and instance.friday) or (weekday == 5 and instance.saturday) or (weekday == 6 and instance.sunday):

            # add the start time & end time from the form in order to 
            # create a datetime object, as required by the Time model
            start_time  = datetime.combine(single_date, instance.start_time)
            end_time    = datetime.combine(single_date, instance.end_time)

            # append a time object to the list so all of them can be inserted in one query
            timeList.append(Time(start_time=start_time, end_time=end_time, site=instance.site))                                    

    # save time slots
    Time.objects.bulk_create(timeList)
        

@receiver(post_delete, sender=TimeRange, dispatch_uid="ts.apps.tradeschool.signals")
def timerange_delete_callback(sender, instance, **kwargs):
    """ delete all time slots within a time range object."""
    
    # iterate over days in date range set in the form
    for single_date in daterange(instance.start_date, instance.end_date):

        # add a time object only when the day in range is a weekday that was checked by the user
        weekday = single_date.weekday()

        if (weekday == 0 and instance.monday) or (weekday == 1 and instance.tuesday) or (weekday == 2 and instance.wednesday) or (weekday == 3 and instance.thursday) or (weekday == 4 and instance.friday) or (weekday == 5 and instance.saturday) or (weekday == 6 and instance.sunday):

            # add the start time & end time from the form in order to 
            # create a datetime object, as required by the Time model
            start_time  = datetime.combine(single_date, instance.start_time)
            end_time    = datetime.combine(single_date, instance.end_time)

            # delete time
            Time.objects.filter(start_time=start_time, end_time=end_time)[0].delete()


def daterange(start_date, end_date):
    """ construct a date range from start and end dates."""
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)