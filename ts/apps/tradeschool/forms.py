from django.forms import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
from tradeschool.models import *


class TeacherForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].error_messages['required'] = _("Please enter your name")
        self.fields['email'].error_messages['required']    = _("Please enter your email")
        self.fields['bio'].error_messages['required']      = _("Please enter your bio")
        self.fields['phone'].error_messages['required']    = _("Please enter phone number")
    
    class Meta:
        model       = Person
        fields      = ('fullname', 'email', 'phone', 'website')

    # since bio is set to blank=True in the Person model to accommodate students, we're setting it here manually.
    bio = forms.CharField(required=True, label=_("A few sentences about you"), help_text=_("For prospective students to see on the website"), widget=forms.Textarea)


class CourseForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages['required']        = _("Please enter a class title")
        self.fields['description'].error_messages['required']  = _("Please enter a class description")
        self.fields['max_students'].error_messages['required'] = _("Please enter the maximum number of students in your class")
            
    class Meta:
        model       = Course
        fields      = ('title', 'description', 'max_students')


class BarterItemForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class']          = 'barter_item'
        self.fields['requested'].widget.attrs['class']      = 'barter_qty'
        self.fields['title'].error_messages['required']     = _("Barter item cannot be blank")        
        self.fields['requested'].error_messages['required'] = _("Barter item quantity cannot be blank")
        
        class Meta:
            model       = BarterItem
            fields      = ('title', 'requested')


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


class RegistrationForm(ModelForm):
    def __init__(self, schedule, *args, **kwargs):
           super (RegistrationForm,self ).__init__(*args,**kwargs) # populates the post
           self.fields['items'].queryset = BarterItem.objects.filter(schedule=schedule)
           self.fields['items'].error_messages['required'] =  _("Please select at least one item")           
           self.fields['items'].empty_label = None
    
    class Meta:
        model       = Registration
        fields      = ('items', )
        widgets     = { 'items': CheckboxSelectMultiple(), }        
            

class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
           super (StudentForm,self ).__init__(*args,**kwargs) 
           self.fields['fullname'].error_messages['required'] =  _("Please enter your name")
           self.fields['email'].error_messages['required']    =  _("Please enter your email") 
           self.fields['phone'].error_messages['required']    =  _("Please enter your name number")           
               
    class Meta:
        model       = Person
        fields      = ('fullname', 'email', 'phone')
