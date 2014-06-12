from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

from tradeschool.calendar import export
from tradeschool.utils import unique_slugify, branch_templates
from tradeschool.models import *
from tradeschool.forms import *


def branch_list(request):
    """display all branches in current site."""

    branches = Branch.objects.public()
    pages = FlatPage.objects.all()

    return render_to_response('hub/branch_list.html', {
        'branches': branches,
        'pages': pages,
    }, context_instance=RequestContext(request))


def cluster_list(request, slug=None):
    """display all branches related to a cluster."""

    cluster = get_object_or_404(Cluster, slug=slug)
    branches = Branch.objects.public().filter(clusters=cluster)

    return render_to_response('hub/cluster_list.html', {
        'cluster': cluster,
        'branches': branches,
    }, context_instance=RequestContext(request))


def course_list(request, branch_slug=None):
    """display all upcoming courses for branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)

    view_templates = branch_templates(
        branch, 'course_list.html', 'base.html')

    return render_to_response(view_templates.template.name, {
        'templates': view_templates,
    }, context_instance=RequestContext(request))


def course_view(request, branch_slug=None, course_slug=None):
    """
    """
    course = get_object_or_404(
        Course, slug=course_slug, branch__slug=branch_slug)

    view_templates = branch_templates(
        course.branch, 'course_view.html', 'base.html')

    return render_to_response(view_templates.template.name, {
        'course': course,
        'templates': view_templates,
    }, context_instance=RequestContext(request))


def redirect_to_course_list(request, branch_slug=None):
    """
    """
    return HttpResponseRedirect(reverse_lazy(
        course_list, kwargs={'branch_slug': branch_slug, }))


def course_register(request, branch_slug=None, course_slug=None, data=None):
    """
    """
    branch = get_object_or_404(Branch, slug=branch_slug)
    course = get_object_or_404(Course, slug=course_slug)
    open_seat_percentage = round(
        (float(course.total_registered_students) /
            float(course.max_students)) * 100)
    seats_left = course.max_students - course.total_registered_students

    if request.method == 'POST' and not request.is_ajax():
        data = request.POST

    if data is not None or request.method == 'POST':
        student_form = StudentForm(data=data, prefix="student")
        registration_form = RegistrationForm(
            data=data, course=course, prefix="item")

        if registration_form.is_valid() and student_form.is_valid():
            # save student
            student = student_form.save(commit=False)
            student_data = student_form.cleaned_data
            student_data['slug'] = unique_slugify(Student, student.fullname)

            student = Person.objects.filter(email=student.email)

            if student.exists():
                student = student[0]

                # keep this object in case something goes wrong
                # when saving the registration
                original_student = student

                # update student data from form
                student.fullname = student_data['fullname']
                student.phone = student_data['phone']
            else:
                student = Person.objects.create_user(**student_data)

            student.is_student = True
            student.save()
            student.branches.add(branch)

            # save registration
            registration = registration_form.save(commit=False)
            registration.student = student
            registration.course = course

            # try saving the registration.
            # this may fail because of the unique_together db constraint
            # on student and course fields
            # if this Student is registered to this Course
            # an IntegrityError will occur
            try:
                registration.save()

                # save items in registration through RegisteredItem
                for barter_item in registration_form.cleaned_data['items']:
                    registration.items.add(barter_item)

                registration.save()

                # email confirmation to student
                course.email_student(
                    course.studentconfirmation, registration)

                # render thank you template
                view_templates = branch_templates(
                    branch, 'course_registered.html', 'base.html')
                return render_to_response(
                    view_templates.template.name, {
                        'registration': registration,
                        'templates': view_templates
                    },
                    context_instance=RequestContext(request),
                    mimetype="application/json"
                )

            # in case saving the registration failed
            # (see comment above the try block),
            # add an error to the registration form
            except IntegrityError:

                # restore data
                student.fullname = original_student.fullname
                student.phone = original_student.phone
                student.save()

                # display error
                registration_form._errors['items'] = \
                    registration_form.error_class(
                        [_('You are already registered to this class')])

    else:
        student_form = StudentForm(prefix="student")
        registration_form = RegistrationForm(course=course, prefix="item")

    # return content as either json or html depending on request type
    if request.is_ajax():
        view_templates = branch_templates(
            branch, 'course_register.html', 'base_ajax.html')
        popup_container_class = ''
        mimetype = "application/json"
    else:
        view_templates = branch_templates(
            branch, 'course_register.html', 'base.html')
        popup_container_class = 'visible'
        mimetype = "text/html"

    return render_to_response(view_templates.template.name, {
        'branch': branch,
        'course': course,
        'open_seat_percentage': open_seat_percentage,
        'seats_left': seats_left,
        'registration_form': registration_form,
        'student_form': student_form,
        'templates': view_templates,
        'popup_container_class': popup_container_class
    }, context_instance=RequestContext(request), mimetype=mimetype)


def course_calendar(request, course_slug=None, branch_slug=None):
    """Display an ical for with a single course."""
    course = get_object_or_404(
        Course, slug=course_slug, branch__slug=branch_slug)

    calendar = export.build_calendar_for_courses([course], course.branch.domain)
    return HttpResponse(calendar.to_ical(), content_type="text/calendar")


def teacher_info(request, branch_slug=None):
    """
    display a content page with information for prospective teachers.
    This page leads to the class submission form page.
    """
    branch = get_object_or_404(Branch, slug=branch_slug)

    view_templates = branch_templates(
        branch, 'teacher-info.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'branch': branch,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def course_list_past(request, branch_slug=None):
    """display a list of past classes for the current branch."""

    branch = get_object_or_404(Branch, slug=branch_slug)

    view_templates = branch_templates(
        branch, 'course_list_past.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'branch': branch,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def course_add(request, branch_slug=None):
    """
    """
    branch = get_object_or_404(Branch, slug=branch_slug)

    if request.method == 'POST':
        BarterItemFormSet = formset_factory(
            BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(data=request.POST, prefix="item", branch=branch)
        course_form = CourseForm(request.POST, prefix="course")
        teacher_form = TeacherForm(request.POST, prefix="teacher")
        time_form = TimeSelectionForm(
            data=request.POST,
            prefix="time",
        )
        time_form.fields['time'].queryset = Time.objects.filter(branch=branch)

        if barter_item_formset.is_valid() \
                and course_form.is_valid() \
                and teacher_form.is_valid() \
                and time_form.is_valid():
            # process teacher
            teacher = teacher_form.save(commit=False)
            teacher_data = teacher_form.cleaned_data

            # create a slug for the teacher object
            teacher_data['slug'] = unique_slugify(Teacher, teacher.fullname)

            # check if the submitting teacher already exists in the system
            # we determine an existing teacher by their email
            teacher = Teacher.objects.filter(email=teacher.email)

            # if this is an existing teacher,
            # update the field with the data from the form
            if teacher.exists():
                teacher = teacher[0]
                teacher.fullname = teacher_form.cleaned_data['fullname']
                teacher.bio = teacher_form.cleaned_data['bio']
                teacher.website = teacher_form.cleaned_data['website']
                teacher.phone = teacher_form.cleaned_data['phone']
            else:
                teacher = Person.objects.create_user(**teacher_data)

            teacher.is_teacher = True

            # save teacher
            teacher.save()

            # add a teacher-branch relationship to the current branch
            teacher.branches.add(branch)

            # process course
            course = course_form.save(commit=False)
            course_data = course_form.cleaned_data

            # create a slug for the course object
            course_data['slug'] = unique_slugify(Course, course.title)

            # add the teacher as a foreign key
            course_data['teacher'] = teacher

            # course branch
            course_data['branch'] = branch

            # course status
            course_data['status'] = 'pending'

            # save time
            selected_time = time_form.cleaned_data['time']
            course_data['start_time'] = selected_time.start_time
            course_data['end_time'] = selected_time.end_time

            if selected_time.venue is not None:
                course_data['venue'] = selected_time.venue
            else:
                try:
                    course_data['venue'] = branch.venue_set.all()[0]
                except IndexError:
                    pass

            # save course
            course = Course(**course_data)
            course.save()

            # save barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data

                # check if the submitted barter item
                # already exists in the system.
                # we determine an existing barter item by its title
                barter_item, barter_item_created = BarterItem.objects.get_or_create(
                    title=barter_item_form_data['title'],
                    course=course,
                    defaults=barter_item_form_data
                )
                barter_item.save()

            # send confirmation email to teacher
            course.email_teacher(course.teacherconfirmation)

            # delete the selected time slot
            Time.objects.get(pk=selected_time.pk).delete()

            # redirect to thank you page
            return HttpResponseRedirect(reverse_lazy(
                course_submitted,
                kwargs={
                    'course_slug': course.slug,
                    'branch_slug': branch.slug
                })
            )

    else:
        BarterItemFormSet = formset_factory(
            BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(prefix="item", branch=branch)
        course_form = CourseForm(prefix="course")
        teacher_form = TeacherForm(prefix="teacher")
        time_form = TimeSelectionForm(prefix="time")
        time_form.fields['time'].queryset = Time.objects.filter(branch=branch)

    view_templates = branch_templates(
        branch, 'course_submit.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'branch': branch,
        'barter_item_formset': barter_item_formset,
        'course_form': course_form,
        'teacher_form': teacher_form,
        'time_form': time_form,
        'templates': view_templates
    }, context_instance=RequestContext(request))


#@login_required
def course_edit(request, course_slug=None, branch_slug=None):
    """
    """
    course = get_object_or_404(Course, slug=course_slug)
    branch = get_object_or_404(Branch, slug=branch_slug)

    if request.method == 'POST':
        BarterItemFormSet = formset_factory(
            BarterItemForm, extra=5, formset=BaseBarterItemFormSet)
        barter_item_formset = BarterItemFormSet(data=request.POST, prefix="item", branch=branch)
        course_form = CourseForm(
            request.POST, prefix="course", instance=course)
        teacher_form = TeacherForm(
            request.POST, prefix="teacher", instance=course.teacher)

        if barter_item_formset.is_valid() \
                and course_form.is_valid() \
                and teacher_form.is_valid():
            # save teacher
            teacher = teacher_form.save(commit=False)
            teacher.slug = unique_slugify(Teacher, teacher.fullname)
            teacher.save()

            # save course
            course = course_form.save(commit=False)
            course.slug = unique_slugify(Course, course.title)
            course.save()

            # remove all barter item relationships before saving them again
            for item in course.barteritem_set.all():
                item.delete()

            # save updated barter items
            for barter_item_form in barter_item_formset:
                barter_item_form_data = barter_item_form.cleaned_data
                barter_item, created = BarterItem.objects.get_or_create(
                    title=barter_item_form_data['title'],
                    course=course,
                    defaults=barter_item_form_data
                )
                barter_item.save()
            return HttpResponseRedirect(reverse_lazy(
                course_submitted,
                kwargs={
                    'branch_slug': branch.slug,
                    'course_slug': course.slug
                })
            )

    else:
        initial_item_data = []
        for item in course.barteritem_set.all():
            initial_item_data.append({'title': item.title, })

        BarterItemFormSet = formset_factory(
            BarterItemForm, extra=0, formset=BaseBarterItemFormSet,)
        barter_item_formset = BarterItemFormSet(
            prefix="item", initial=initial_item_data, branch=branch)
        course_form = CourseForm(
            prefix="course",
            instance=course
        )
        teacher_form = TeacherForm(
            prefix="teacher",
            instance=course.teacher
        )

    view_templates = branch_templates(
        branch, 'course_submit.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'barter_item_formset': barter_item_formset,
        'course_form': course_form,
        'teacher_form': teacher_form,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def course_submitted(request, course_slug=None, branch_slug=None):
    """
    loaded after a successful submission of the course form.
    """

    course = get_object_or_404(Course, slug=course_slug)
    branch = get_object_or_404(Branch, slug=branch_slug)

    view_templates = branch_templates(
        branch, 'course_submitted.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'course': course,
        'templates': view_templates
    }, context_instance=RequestContext(request))

#@login_required
def course_unregister(request, branch_slug=None, course_slug=None, student_slug=None):
    """
    """
    registration = get_object_or_404(
        Registration, student__slug=student_slug, course__slug=course_slug)
    branch = get_object_or_404(Branch, slug=branch_slug)

    if request.method == 'POST':
        registration.registration_status = 'unregistered'
        registration.save()
        return HttpResponseRedirect(reverse_lazy(
            course_list,
            kwargs={'branch_slug': branch_slug, })
        )

    view_templates = branch_templates(
        branch, 'course_unregister.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'registration': registration,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def course_feedback(request, branch_slug=None, course_slug=None, feedback_type='student'):
    """
    """
    # don't display form unless course is approved
    course = get_object_or_404(
        Course, slug=course_slug, status='approved')
    branch = get_object_or_404(Branch, slug=branch_slug)

    # don't display form unless the scheduled class took place
    if course.is_past is False:
        raise Http404

    if request.method == 'POST' and course.is_past:
        form = FeedbackForm(data=request.POST)

        if form.is_valid():

            # save feedback
            feedback = form.save(commit=False)
            feedback.feedback_type = feedback_type
            feedback.course = course
            feedback.save()

            # redirect to thank you page
            return HttpResponseRedirect(reverse_lazy(
                course_list,
                kwargs={'branch_slug': branch_slug, })
            )

    else:
        form = FeedbackForm()

    view_templates = branch_templates(
        branch, 'course_feedback.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'form': form,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def branch_page(request, url, branch_slug=None):
    """
    this is copied from django.contrib.flatpages.views only in order to
    query the BranchPage table instead of FlatPage.
    """
    branch = get_object_or_404(Branch, slug=branch_slug)

    try:
        page = get_object_or_404(
            Page, url__exact=url, branch__pk=branch.pk, is_active=True)
    except Http404:
        if url.endswith('/'):
            url = url[:-1]
            page = get_object_or_404(
                Page,
                url__exact=url,
                branch__pk=branch.pk,
                is_active=True
            )
        else:
            raise

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    page.title = mark_safe(page.title)
    page.content = mark_safe(page.content)

    view_templates = branch_templates(
        branch, 'page_detail.html', 'subpage.html')

    return render_to_response(view_templates.template.name, {
        'page': page,
        'templates': view_templates
    }, context_instance=RequestContext(request))


def branch_calendar(request, branch_slug=None):
    """Display a calendar of events for a branch in iCalendar format.
    """
    branch = get_object_or_404(Branch, slug=branch_slug)
    courses = branch.course_set.public().approved()
    calendar = export.build_calendar_for_courses(courses, branch.domain)
    return HttpResponse(calendar.to_ical(), content_type="text/calendar")


def start_a_tradeschool(request):
    branches = Branch.objects.public()
    pages = FlatPage.objects.all()

    if request.method == 'POST':
        branch_form = BranchForm(request.POST, prefix="branch")
        organizer_form = OrganizerForm(request.POST, prefix="organizer")

        if branch_form.is_valid() and organizer_form.is_valid():

            try:
                # save branch
                branch = branch_form.save(commit=False)
                branch_data = branch_form.cleaned_data

                # create a title from the city field
                branch_data['title'] = branch_data['city']

                # create a slug for the organizer object
                branch_data['slug'] = unique_slugify(
                    Branch, branch_data['title'])

                branch_data['is_active'] = False
                branch_data['branch_status'] = 'pending'

                # save branch
                branch = Branch(**branch_data)
                branch.save()

                # save organizer
                organizer = organizer_form.save(commit=False)
                organizer_data = organizer_form.cleaned_data

                # create a slug for the organizer object
                organizer_data['slug'] = unique_slugify(
                    Organizer, organizer.fullname)

                organizer_data['username'] = organizer.fullname
                organizer_data['is_active'] = True
                organizer_data['is_staff'] = True

                # save organizer
                organizer = Organizer(**organizer_data)
                organizer.default_branch = branch
                organizer.save()

                # add an organizer-branch relationship to the current branch
                organizer.branches.add(branch)
                organizer.branches_organized.add(branch)
                organizer.groups.add(Group.objects.get(name='translators'))

                return HttpResponseRedirect(reverse_lazy(
                    branch_submitted,
                    kwargs={
                        'slug': branch.slug,
                    })
                )
            # in case saving the branch failed
            # (see comment above the try block),
            # add an error to the branch form
            except IntegrityError:
                # display error
                branch_form._errors['city'] = \
                    branch_form.error_class(
                        [_('This Trade School already exists')])

    else:
        branch_form = BranchForm(prefix="branch")
        organizer_form = OrganizerForm(prefix="organizer")

    return render_to_response('hub/start_a_tradeschool.html', {
        'branches': branches,
        'pages': pages,
        'branch_form': branch_form,
        'organizer_form': organizer_form,
    }, context_instance=RequestContext(request))


def branch_submitted(request, slug=None):
    """
    loaded after a successful submission of the start a tradeschool form.
    """
    branch = get_object_or_404(Branch, slug=slug, branch_status='pending')

    return render_to_response('hub/branch_submitted.html', {
        'branch': branch,
        'organizer': branch.organizers.all()[0]
    }, context_instance=RequestContext(request))


def story(request):
    """
    """
    exchanges = Registration.objects.annotate(Count('items')).filter(
        registration_status='registered',
        course__status='approved',
        items__count__gt=0).order_by('?')[:10]

    branches = Branch.objects.public().filter().order_by('created')

    for b in branches:
        b.course_count = b.course_set.all().filter(status='approved').count()
        b.student_count = b.person_set.all().filter(is_student=True, courses_taken_count__gt=0).count()
        b.teacher_count = b.person_set.all().filter(is_teacher=True).count()

    total_people_count = Person.objects.filter(is_active=True).count()

    return render_to_response('hub/story.html', {
        'exchanges': exchanges,
        'branches': branches,
        'total_people_count': total_people_count
    }, context_instance=RequestContext(request))


def switch_default_branch(request):

    organizer_id = request.GET.get('organizer_id', None)
    organizer = get_object_or_404(Person, pk=organizer_id)

    default_branch_id = request.GET.get('default_branch', None)
    default_branch = get_object_or_404(Branch, pk=default_branch_id)

    redirect_url = request.GET.get('redirect_to', None)

    if request.method == 'GET':
        form = DefaultBranchForm(organizer, redirect_url, data=request.GET)

        if form.is_valid():

            # save organizer
            organizer.default_branch = default_branch
            organizer.save()

    return HttpResponseRedirect(redirect_url)


def redirect_to_admin(request, branch_slug=None):
    get_object_or_404(Branch, slug=branch_slug)
    return HttpResponseRedirect('/admin/')
