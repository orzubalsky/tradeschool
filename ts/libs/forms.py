from django.forms import *

class ExtendedMetaModelForm(ModelForm):
    """
    Allow the setting of any field attributes via the Meta class.
    http://blog.brendel.com/2012/01/django-modelforms-setting-any-field.html
    """

    def __init__(self, *args, **kwargs):
        "Iterate over fields, set attributes from Meta.field_args."
        super(ExtendedMetaModelForm, self).__init__(*args, **kwargs)
        if hasattr(self.Meta, "field_args"):
            # Look at the field_args Meta class attribute to get
            # any (additional) attributes we should set for a field.
            field_args = self.Meta.field_args
            # Iterate over all fields...
            for fname, field in self.fields.items():
                # Check if we have something for that field in field_args
                fargs = field_args.get(fname)
                if fargs:
                    # Iterate over all attributes for a field that we
                    # have specified in field_args
                    for attr_name, attr_val in fargs.items():
                        if attr_name.startswith("+"):
                            merge_attempt = True
                            attr_name = attr_name[1:]
                        else:
                            merge_attempt = False
                        orig_attr_val = getattr(field, attr_name, None)
                        if orig_attr_val and merge_attempt and \
                                    type(orig_attr_val) == dict and \
                                    type(attr_val) == dict:
                            # Merge dictionaries together
                            orig_attr_val.update(attr_val)
                        else:
                            # Replace existing attribute
                            setattr(field, attr_name, attr_val)