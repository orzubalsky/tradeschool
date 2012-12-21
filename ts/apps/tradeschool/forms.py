from django.forms import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
from tradeschool.models import *


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


class TeacherForm (ExtendedMetaModelForm):
    class Meta:
        model       = Person
        fields      = ('fullname', 'email', 'phone', 'website')
        field_args  = {
                        "fullname"  : { "error_messages" : { "required" : _("Please enter your name") } },
                        "email"     : { "error_messages" : { "required" : _("Please enter your email") } },
                        "bio"       : { "error_messages" : { "required" : _("Please enter your bio") } },
                        "phone"     : { "error_messages" : { "required" : _("Please enter your phone number") } },
                      }

    # since bio is set to blank=True in the Person model to accommodate students, we're setting it here manually.
    bio = forms.CharField(required=True, label=_("A few sentences about you"), help_text=_("For prospective students to see on the website"), widget=forms.Textarea)


class CourseForm (ExtendedMetaModelForm):
    class Meta:
        model       = Course
        fields      = ('title', 'description', 'max_students')
        field_args  = {
                        "title"         : { "error_messages" : { "required" : _("Please enter a class title") } },
                        "description"   : { "error_messages" : { "required" : _("Please enter a class description") } },
                        "max_students"  : { "error_messages" : { "required" : _("Please enter the maximum number of students in your class") } }
                      }


class BarterItemForm (ModelForm):
    class Meta:
        model       = BarterItem
        fields      = ('title', 'requested')    
            
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class']          = 'barter_item'
        self.fields['title'].error_messages['required']     =  _("Barter item cannot be blank")
        self.fields['requested'].widget.attrs['class']      = 'barter_qty'
        self.fields['requested'].error_messages['required'] = _("Barter item quantity cannot be blank")
        


class BaseBarterItemFormSet(BaseFormSet):
    def clean(self):
        "Checks that at least one barter item form is filled"
        count = 0        
        required = 5
        
        if any(self.errors):
            return
        for form in self.forms:
            if form.is_bound:
                if form['title'].data:
                    count += 1
        if count < required:
            raise forms.ValidationError( _('Please add at least %i barter items' % required) ) 


class TimeSelectionForm(Form):
    "A simple dropdown menu for teachers to select an available time when submitting a class. Uses the Time model"
    time = forms.ModelChoiceField(queryset=Time.objects.all(), error_messages={'required': _('Please select a time') } )




class RegisteredItemForm(ModelForm):
    def __init__(self, schedule, *args, **kwargs):
           super (RegisteredItemForm,self ).__init__(*args,**kwargs) # populates the post
           self.fields['barter_item'].queryset = BarterItem.objects.filter(schedule=schedule)
           self.fields['barter_item'].empty_label = None
    
    class Meta:
        model       = RegisteredItem
        fields      = ('barter_item', )
        widgets = { 'barter_item': CheckboxSelectMultiple(), }        

            

class StudentForm (ExtendedMetaModelForm):
    class Meta:
        model       = Person
        fields      = ('fullname', 'email', 'phone')
        field_args  = {
                        "fullname"  : { "error_messages" : { "required" : _("Please enter your name") } },
                        "email"     : { "error_messages" : { "required" : _("Please enter your email") } },
                        "phone"     : { "error_messages" : { "required" : _("Please enter your phone number") } },
                      }