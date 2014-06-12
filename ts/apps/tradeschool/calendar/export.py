"""
Export a list of :class:`tradeschool.model.Course` as an icalendar.
"""
import datetime

from icalendar import Calendar, Event, vDatetime, vText, vUri


def _build_uid_for_course(course):
    """Construct an event UID from a :class:`tradeschool.models.Course`.
    """
    return "{label}-{id}@{site}".format(
        label=unicode(course.slug),
        id=course.id,
        site=course.branch.site.domain)


def _build_location_for_venue(venue):
    return "{title}, {address} {city}, {state}, {country}".format(
        title=unicode(venue.title),
        address=unicode(venue.address_1),
        state=unicode(venue.state),
        city=unicode(venue.city),
        country=unicode(venue.country)
    )


def course_to_event(course):
    """Convert a Course into a icalendar event.

    :param course: a :class:`tradeschool.models.Course` to export as an Event
    :returns: :class:`icalendar.Event`
    """
    return Event(**{
        'uid': vText(_build_uid_for_course(course)),
        'created': vDatetime(course.created),
        'description': vText(unicode(course.description)),
        'dtstart': vDatetime(course.start_time),
        'dtend': vDatetime(course.end_time),
        'last-mod': vDatetime(course.updated),
        'dtstamp': vDatetime(datetime.datetime.now()),
        'location': vText(_build_location_for_venue(course.venue)),
        'summary': vText(unicode(course.title)),
        'url': vUri(course.course_view_url),
    })


def build_calendar_for_courses(courses, domain):
    """Build an icalendar from a list of Courses.

    :param courseis: list of :class:`tradeschool.model.Course`
    :returns: :class:`icalendar.Calendar`
    """

    cal = Calendar(
        version='2.0',
        prodid='-//{domain}//Calendar Export//'.format(domain=domain)
    )
    for course in courses:
        cal.add_component(course_to_event(course))
    return cal
