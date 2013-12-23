from django.forms import *
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from tradeschool.models import *


class BranchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)

        self.fields['city'].error_messages['required'] = _(
            "Please enter a city")
        self.fields['country'].error_messages['required'] = _(
            "Please enter a country")

        self.initial['site'] = Site.objects.get_current()

    class Meta:
        model = Branch
        fields = (
            'city',
            'state',
            'country',
        )


class TeacherForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].error_messages['required'] = _(
            "Please enter your name")
        self.fields['email'].error_messages['required'] = _(
            "Please enter your email")
        self.fields['bio'].error_messages['required'] = _(
            "Please tell us about yourself")
        self.fields['phone'].error_messages['required'] = _(
            "Please enter phone number")

    class Meta:
        model = Person
        fields = ('fullname', 'email', 'phone', 'bio', 'website')

    # since bio is set to blank=True in the Person model
    # to accommodate students, we're setting it here manually.
    bio = forms.CharField(
        required=True,
        label=_("A few sentences about you"),
        help_text=_("For prospective students to see on the website"),
        widget=forms.Textarea
    )


class OrganizerForm(TeacherForm):
    pass


class CourseForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages['required'] = _(
            "Please enter a class title")
        self.fields['description'].error_messages['required'] = _(
            "Please enter a class description")
        self.fields['max_students'].error_messages['required'] = _(
            "Please enter the maximum number of students in your class")

    class Meta:
        model = Course
        fields = ('title', 'description', 'max_students')


class BarterItemForm (ModelForm):
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'barter_item'
        self.fields['title'].error_messages['required'] = _(
            "Barter item cannot be blank")

    class Meta:
        model = BarterItem
        fields = ('title',)


class BaseBarterItemFormSet(BaseFormSet):
    def clean(self):
        "Checks that at least 5 barter items form are filled"
        count = 0
        required = 5

        if any(self.errors):
            return
        for form in self.forms:
            if form.is_bound:
                if form['title'].data:
                    count += 1
        if count < required:
            raise forms.ValidationError(
                _("Please add at least 5 barter items")
            )


class TimeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        from django.utils import timezone

        current_tz = timezone.get_current_timezone()
        date = obj.start_time.astimezone(current_tz).strftime('%A, %b %d')
        time = obj.start_time.astimezone(current_tz).strftime(
            '%I:%M%p').lstrip('0').lower()

        if obj.venue is not None:
            return "%s %s at %s" % (date, time, obj.venue)
        return "%s %s" % (date, time)


class TimeSelectionForm(Form):
    """
    A simple dropdown menu for teachers to select an available time
    when submitting a class. Uses the Time model
    """
    time = TimeModelChoiceField(
        queryset=Time.objects.all(),
        error_messages={'required': _('Please select a time'), }
    )


class RegistrationForm(ModelForm):
    def __init__(self, schedule, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['items'].queryset = BarterItem.objects.filter(
            schedule=schedule)
        self.fields['items'].error_messages['required'] = _(
            "Please select at least one item")
        self.fields['items'].empty_label = None

    class Meta:
        model = Registration
        fields = ('items', )
        widgets = {'items': CheckboxSelectMultiple(), }


class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['fullname'].error_messages['required'] = _(
            "Please enter your name")
        self.fields['email'].error_messages['required'] = _(
            "Please enter your email")
        self.fields['phone'].error_messages['required'] = _(
            "Please enter your phone number")

    class Meta:
        model = Person
        fields = ('fullname', 'email', 'phone')


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['content'].error_messages['required'] = _(
            "Please enter your feedback")

    class Meta:
        model = Feedback
        fields = ('content',)
