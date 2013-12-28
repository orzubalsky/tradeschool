from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from datetime import *
from tradeschool.models import *


class Command(BaseCommand):
    help = 'send the unsent timed emails from the past hour'

    def handle(self, *args, **options):
        """ """
        site = Site(domain='http://test.com', name='test test site', id=1)
        site.save()

        admin_01 = Person.objects.get(fullname='ny admin', email='test@ny.com')

        admin_02 = Person.objects.get(
            fullname='barcelona admin',
            email='test@barcelona.com'
        )

        admin_03 = Person.objects.get(
            fullname='berlin admin',
            email='test@berlin.com'
        )

        test_branch_01 = Branch(
            title='test new york',
            city='new york',
            state='NY',
            country='US',
            slug='test-new-york',
            email='newyork@test.com',
            timezone='America/New_York',
            language='en',
            site=site
        )
        test_branch_01.save()
        test_branch_01.organizers.add(admin_01)

        test_branch_02 = Branch(
            title='test barcelone',
            city='Barcelona',
            country='GB',
            slug='test-barcelone',
            email='barcelona@test.com',
            timezone='Europe/London',
            language='es',
            site=site
        )
        test_branch_02.save()
        test_branch_02.organizers.add(admin_02)

        test_branch_03 = Branch(
            title='test berlin',
            city='Berlin',
            country='DE',
            slug='test-berlin',
            email='berlin@test.com',
            timezone='Europe/London',
            language='de',
            site=site
        )
        test_branch_03.save()
        test_branch_03.organizers.add(admin_03)
        test_branch_03.organizers.add(admin_02)

        test_venue_01 = Venue(
            title='venue newyork',
            address_1='10 test st.',
            city='New York',
            state='NY',
            country='US',
            branch=test_branch_01
        )
        test_venue_01.save()

        test_venue_02 = Venue(
            title='venue barcelona',
            address_1='10 test st.',
            city='Barcelona',
            country='GB',
            branch=test_branch_02
        )
        test_venue_02.save()

        test_venue_03 = Venue(
            title='venue berlin',
            address_1='10 test st.',
            city='Berlin',
            country='DE',
            branch=test_branch_03
        )
        test_venue_03.save()
