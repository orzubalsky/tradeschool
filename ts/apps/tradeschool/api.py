from tastypie.resources import ModelResource
from tastypie import fields
from tradeschool.models import Branch, Venue


class BranchResource(ModelResource):
    class Meta:
        queryset = Branch.objects.public()
        resource_name = 'branch'
        fields = [
            'title',
            'slug',
            'city',
            'state',
            'country',
            'timezone',
            'langauge',
        ]
        allowed_methods = ['get']


class VenueResource(ModelResource):
    branch = fields.ForeignKey(BranchResource, 'branch')

    class Meta:
        queryset = Venue.objects.filter(is_active=True)
        resource_name = 'venue'
        fields = [
            'title',
            'branch',
            'address_1',
            'city',
            'state',
            'country',
            'phone',
            'max_capacity',
            'resources'
        ]
        allowed_methods = ['get']
