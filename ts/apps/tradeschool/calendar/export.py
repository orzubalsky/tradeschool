"""
Export a list of :class:`tradeschool.model.Course` as an icalendar.
"""

from icalendar import Calendar, Event



def course_to_event(course):
    """Convert a Course into a icalendar event.
    
    :param course: 
    :returns: :class:`icalendar.Event`
    """


def build_calendar_for_courses(courses):
    """Build an icalendar from a list of Courses.

    :param courseis: list of :class:`tradeschool.model.Course`
    :returns: :class:`icalendar.Calendar`
    """

    cal = Calendar(
            version='2.0',
            prodid='-//TradeSchool.coop//Export//EN'
    )
    for course in courses:
        cal.add_component(course_to_event(course))
    return cal

