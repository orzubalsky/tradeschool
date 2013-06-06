import os
from django.template.defaultfilters import slugify
from django.db.models import AutoField
from django.template.loader import select_template


class Bunch:
    """ This is a fast way of creating dictionary-like objects with dotted syntax.

        For example:

        a_bunch = Bunch(something=4, something_else='fish')
        if a_bunch.something > 2:
            print a_bunch.something_else
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)



def branch_template(branch, template_file):
    """ Return a branch-specific template if it's found, 
        otherwise fall back to a template with the given name that's in the default folder.
    """
    branch_template = os.path.join(branch.slug, template_file)
    
    return select_template([branch_template, template_file])



def branch_templates(branch, template_file, extend_template):
    """ Return a Bunch with branch-specific templates (or default templates as a fallback).
        Also include the prefix for the template files according to whether branch-specific templates exist.
    """
    prefix = 'branches_default/'
    if branch.slug in branch_template(branch, template_file):
        prefix = branch.slug
    
    branch_templates = Bunch(
        template        = branch_template(branch, template_file),
        extend_template = branch_template(branch, extend_template),
        base_template   = branch_template(branch, 'base.html'),
        prefix          = prefix
    )

    return branch_templates
        
            
    
def copy_model_instance(obj):
    """ Create a copy of an instance of a model. 
        This is used to create Email objects from template objects.
    """
    initial = dict([(f.name, getattr(obj, f.name))
                    for f in obj._meta.fields
                    if not isinstance(f, AutoField) and\
                       not f in obj._meta.parents.values()])
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