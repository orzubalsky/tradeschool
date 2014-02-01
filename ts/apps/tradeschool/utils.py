import os
from django.template.defaultfilters import slugify
from django.db.models import AutoField
from django.template.loader import select_template
from datetime import timedelta
from django.db import transaction
from django.db import IntegrityError
from django.db.models import get_models, Model
from django.contrib.contenttypes.generic import GenericForeignKey


class Bunch:
    """
    This is a fast way of creating dictionary-like objects with dotted syntax.

    For example:

        a_bunch = Bunch(something=4, something_else='fish')
        if a_bunch.something > 2:
            print a_bunch.something_else
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def branch_template(branch, template_file):
    """
    Return a branch-specific template if it's found,
    otherwise fall back to a template with the given name
    that's in the default folder.
    """
    branch_template = os.path.join(branch.slug, template_file)

    return select_template([branch_template, template_file])


def branch_templates(branch, template_file, extend_template):
    """
    Return a Bunch with branch-specific templates
    (or default templates as a fallback).
    Also include the prefix for the template files
    according to whether branch-specific templates exist.
    """
    prefix = 'branches_default/'
    if branch.slug in branch_template(branch, template_file):
        prefix = branch.slug

    branch_templates = Bunch(
        template=branch_template(branch, template_file),
        extend_template=branch_template(branch, extend_template),
        base_template=branch_template(branch, 'base.html'),
        prefix=prefix
    )
    return branch_templates


def copy_model_instance(obj):
    """
    Create a copy of an instance of a model.
    This is used to create Email objects from template objects.
    """
    initial = dict([(f.name, getattr(obj, f.name))
                    for f in obj._meta.fields
                    if not isinstance(f, AutoField)
                    and not f in obj._meta.parents.values()])
    return obj.__class__(**initial)


def unique_slugify(model, value, slugfield="slug"):
        """Returns a slug on a name which is unique within a model's table

        This code suffers a race condition between when a unique
        slug is determined and when the object with that slug is saved.
        It's also not exactly database friendly if there is a high
        likelyhood of common slugs being attempted.

        A good usage pattern for this code would be to add a custom save()
        method to a model with a slug field along the lines of:

                from django.template.defaultfilters import slugify

                def save(self):
                    if not self.id:
                        # replace self.name with your prepopulate_from field
                        self.slug = SlugifyUniquely(self.name, self.__class__)
                super(self.__class__, self).save()

        Original pattern discussed at
        http://www.b-list.org/weblog/2006/11/02/django-tips-auto-populated-fields
        """
        suffix = 0
        potential = base = slugify(value)
        while True:
                if suffix:
                        potential = "-".join([base, str(suffix)])
                if not model.objects.filter(**{slugfield: potential}).count():
                        return potential
                # we hit a conflicting slug, so bump the suffix & try again
                suffix += 1


def daterange(start_date, end_date):
    """ construct a date range from start and end dates."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@transaction.commit_on_success
def merge_model_objects(primary_object, alias_objects=[], keep_old=False):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.
    
    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """
    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]
    
    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__
    
    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')
    
    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError('Only models of same class can be merged')
    
    # Get a list of all GenericForeignKeys in all models
    # TODO: this is a bit of a hack, since the generics framework should provide a similar
    # method to the ForeignKey field for accessing the generic related fields.
    generic_fields = []
    for model in get_models():
        for field_name, field in filter(lambda x: isinstance(x[1], GenericForeignKey), model.__dict__.iteritems()):
            generic_fields.append(field)
            
    blank_local_fields = set([field.attname for field in primary_object._meta.local_fields if getattr(primary_object, field.attname) in [None, '']])
    
    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to primary object.
        for related_object in alias_object._meta.get_all_related_objects():
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            related_objects = getattr(alias_object, alias_varname)
            for obj in related_objects.all():
                setattr(obj, obj_varname, primary_object)
                try:
                    obj.save()
                except IntegrityError:
                    print obj
                    print obj.pk

        # Migrate all many to many references from alias object to primary object.
        for related_many_object in alias_object._meta.get_all_related_many_to_many_objects():
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name
            
            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()
            for obj in related_many_objects.all():
                try:
                    getattr(obj, obj_varname).remove(alias_object)
                    getattr(obj, obj_varname).add(primary_object)
                except AttributeError:
                    print obj
                    print obj.pk

        # Migrate all generic foreign key references from alias object to primary object.
        for field in generic_fields:
            filter_kwargs = {}
            filter_kwargs[field.fk_field] = alias_object._get_pk_val()
            filter_kwargs[field.ct_field] = field.get_content_type(alias_object)
            for generic_related_object in field.model.objects.filter(**filter_kwargs):
                setattr(generic_related_object, field.name, primary_object)
                generic_related_object.save()
                
        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()
        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name) 
            if val not in [None, '']:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        blank_local_fields -= filled_up
            
        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object
