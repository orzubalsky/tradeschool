from django.forms import *
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from tradeschool.models import *


class DefaultBranchForm(Form):
    def __init__(self, user, redirect_to, *args, **kwargs):
        super(DefaultBranchForm, self).__init__(*args, **kwargs)

        if user.is_superuser:
            branches = Branch.objects.all()
        else:
            branches = Branch.objects.filter(pk__in=user.branches_organized.all)

        choices = [(o.id, unicode(o.title)) for o in branches]

        self.fields['default_branch'] = forms.ChoiceField(choices=choices)

        if user.default_branch:
            self.initial['default_branch'] = user.default_branch.pk
        self.initial['organizer_id'] = user.pk
        self.initial['redirect_to'] = redirect_to

    default_branch = forms.ChoiceField()
    organizer_id = forms.IntegerField(widget=forms.HiddenInput)
    redirect_to = forms.CharField(widget=forms.HiddenInput)


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
    """
    """
    def __init__(self, *args, **kwargs):
        "Sets custom meta data to the form's fields"
        super(TeacherForm, self).__init__(*args, **kwargs)

        self.fields['names_of_co_organizers'].error_messages['required'] = _(
            "Please enter the names of at least one or two more organizers")
        self.fields['bio'].error_messages['required'] = _(
            "Please tell us about why you would like to open a Trade School in your area")

    class Meta:
        model = Person
        fields = (
            'fullname',
            'names_of_co_organizers',
            'email',
            'bio',
        )

    # since names_of_co_organizers is set to blank=True in the Person model
    # to accommodate students and teachers, we're setting it here manually.
    names_of_co_organizers = forms.CharField(
        required=True,
        label=_("Names of Co-Organizers"),
    )
    bio = forms.CharField(
        required=True,
        label=_("A few sentences about why your group wants to open a Trade School"),
        widget=forms.Textarea
    )


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


class RegistrationForm(ModelForm):
    def __init__(self, course, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['items'].queryset = BarterItem.objects.filter(
            course=course)
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
