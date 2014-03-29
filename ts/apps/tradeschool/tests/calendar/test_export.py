import datetime
import textwrap

from django.contrib.sites.models import Site
from django.test import TestCase
import mock

from tradeschool import models
from tradeschool.calendar import export


def build_course(course_id):
    return models.Course(
        id=course_id,
        created=datetime.datetime(2013, 1, 1, 3, 2, 1),
        description="A course about learning. Full text.",
        start_time=datetime.datetime(2013, 3, 1, 10),
        end_time=datetime.datetime(2013, 3, 1, 12),
        teacher=models.Teacher(fullname='The Teacher'),
        title="A course about learning",
        venue=models.Venue(
            title='The place',
            address_1='2 Bay Street',
            city='Toronto',
            state='Ontario',
            country='Canada'),
        updated=datetime.datetime(2013, 2, 1, 15, 0, 23),
        branch=models.Branch(
            site=Site(id=1, domain='tradeschool.test'),
            slug='branch-slug'),
        slug='a-course-about-learning',
    )


class CalendarExportTestCase(TestCase):

    # Let us see the full diff when comparing multiline strings
    maxDiff = None

    def test_course_to_event(self):
        expected = textwrap.dedent("""
            BEGIN:VEVENT\r
            SUMMARY:A course about learning\r
            DTSTART:20130301T100000\r
            DTEND:20130301T120000\r
            DTSTAMP:20140101T000000\r
            UID:a-course-about-learning-12345@tradeschool.test\r
            CREATED:20130101T030201\r
            DESCRIPTION:A course about learning. Full text.\r
            LAST-MOD:20130201T150023\r
            LOCATION:The place\, 2 Bay Street Toronto\, Ontario\, Canada\r
            URL:http://example.com/branch-slug/class/a-course-about-learning/\r
            END:VEVENT\r
        """).lstrip()

        with mock.patch(
            'tradeschool.calendar.export.datetime',
            autospec=True
        ) as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime.datetime(2014, 1, 1)
            event = export.course_to_event(build_course(12345))
        self.assertMultiLineEqual(event.to_ical(), expected)

    def test_build_calendar_for_courses(self):
        courses = [build_course(1), build_course(2)]
        calendar = export.build_calendar_for_courses(
            courses,
            'TradeSchool.coop'
        ).to_ical()

        expected = [
            'BEGIN:VCALENDAR\r',
            'VERSION:2.0\r',
            'PRODID:-//TradeSchool.coop//Calendar Export//\r',
        ]
        self.assertSequenceEqual(calendar.split('\n')[:3], expected)
        self.assertIn(
            'UID:a-course-about-learning-1@tradeschool.test\r',
            calendar
        )
        self.assertIn(
            'UID:a-course-about-learning-2@tradeschool.test\r',
            calendar
        )
