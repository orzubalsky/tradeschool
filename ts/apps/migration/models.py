# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db.models import *
from tradeschool.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.encoding import smart_text
from tradeschool.utils import unique_slugify as slugify


class MigrationBase(Model):
    class Meta:
        abstract = True
    pass



class BranchPagesManager(Manager):
    def migrate(self, data, branch_slug=None):
    
        do_save = True
        if branch_slug is not None:
            do_save = False
            old_branchpage_row = BranchPages.objects.get(pk=int(data['id']))
            try:
                branch = Branch.objects.get(pk=old_branchpage_row.branch_id)
                if branch.slug == branch_slug:
                    do_save = True
            except Branch.DoesNotExist:
                pass
        
        print "     saving: %s" % do_save            
        
        if do_save == True:
            branch_page = Page.objects.filter(url=data['url'])
    
            try:
                branch = Branch.objects.get(pk=int(data['branch_id']))
            
                if branch_page.exists() == False:   
                    branch_page = Page(
                            pk          = data['id'], 
                            branch      = branch,
                            title       = data['title'], 
                            content     = data['content'], 
                            url         = data['url'], 
                            is_active   = data['status'], 
                            created     = timezone.make_aware(data['timestamp'], timezone.utc),
                            updated     = timezone.make_aware(data['timestamp'], timezone.utc),                
                        )
                    branch_page.save()
        
                    print "     saved Page: [%s]" % branch_page            
                else:
                    branch_page = Page.objects.get(url=data['url'])
                    print "     found Page: [%s]" % branch_page   
            except Branch.DoesNotExist:
                pass     


class BranchPages(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField()
    title           = CharField(max_length=765)
    url             = CharField(max_length=765)
    content         = TextField()
    status          = IntegerField()
    timestamp       = DateTimeField()
    
    objects = BranchPagesManager()
    
    class Meta:
        db_table = u'branch_pages'
                
                
class BranchPhotosManager(Manager):
    def migrate(self, data, branch_slug=None):

        do_save = True
        if branch_slug is not None:
            do_save = False
            old_branchphoto_row = BranchPhotos.objects.get(pk=int(data['id']))
            try:
                branch = Branch.objects.get(pk=old_branchphoto_row.branch_id)
                if branch.slug == branch_slug:
                    do_save = True
            except Branch.DoesNotExist:
                pass
        
        print "     saving: %s" % do_save            
        
        if do_save == True:
            branch_photo = Photo.objects.filter(filename=data['filename'])
            try:
                branch = Branch.objects.get(pk=int(data['branch_id']))                

                if branch_photo.exists() == False:   
                    branch_photo = Photo(
                            pk          = data['id'], 
                            branch      = branch,
                            filename    = data['filename'], 
                            created     = timezone.make_aware(data['timestamp'], timezone.utc),
                            updated     = timezone.make_aware(data['timestamp'], timezone.utc),                
                        )
                    branch_photo.save()

                    print "     saved Photo: [%s]" % branch_photo            
                else:
                    branch_photo = Photo.objects.get(filename=data['filename'])
                    print "     found Photo: [%s]" % branch_photo   
            except Branch.DoesNotExist:
                pass                
                
                
class BranchPhotos(MigrationBase):
    id                  = IntegerField(primary_key=True)
    branch_id           = IntegerField()
    filename            = CharField(max_length=765)
    filename_original   = CharField(max_length=765)
    status              = IntegerField()
    timestamp           = DateTimeField()
    
    objects = BranchPhotosManager()
    
    class Meta:
        db_table = u'branch_photos'

class BranchSeasons(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField()
    title           = CharField(max_length=765)
    status          = IntegerField()
    unix_start_time = BigIntegerField()
    unix_end_time   = BigIntegerField()
    class Meta:
        db_table = u'branch_seasons'

class BranchesManager(Manager):
    def migrate(self, data, branch_slug=None):
                
        site_data = {
                'domain' : 'http://tradeschool.coop',
                'name'   : 'tradeschool everywhere'
            }
        site, created = Site.objects.get_or_create(domain='http://tradeschool.coop', defaults=site_data)            
        site.save()
        
        utc = timezone.utc
        
        branch = Branch.objects.filter(pk=int(data['id']))

        do_save = True
        if branch_slug is not None:
            do_save = False
            if data['url'] == branch_slug:
                do_save = True
        print "     saving: %s" % do_save

        if do_save == True:          
            if branch.exists() == False:                  

                branch = Branch(
                        pk                     = int(data['id']), 
                        title                  = data['title'], 
                        phone                  = data['phone'], 
                        city                   = data['city'], 
                        state                  = data['state'], 
                        country                = data['country'], 
                        branch_status          = 'in_session',
                        slug                   = data['url'].lower(), 
                        email                  = data['email'].lower(),  
                        created                = timezone.make_aware(data['timestamp'], timezone.utc),
                        updated                = timezone.make_aware(data['timestamp'], timezone.utc),
                        intro_copy             = data['header'],
                        footer_copy            = data['footer'],
                        timezone               = data['timezone'],
                        language               = 'en',                
                        site                   = site,     
                    )
                branch.save()

                print "     saved Branch: [%s]" % branch            
            else:
                branch = Branch.objects.get(pk=int(data['id']))
                print "     found Branch: [%s]" % branch            

  

class Branches(MigrationBase):
    id          = IntegerField(primary_key=True)
    title       = CharField(max_length=765)
    url         = CharField(max_length=765)
    email       = CharField(max_length=765)
    timezone    = CharField(max_length=765)
    phone       = CharField(max_length=765)
    city        = CharField(max_length=765)
    state       = CharField(max_length=765, blank=True)
    country     = CharField(max_length=765)
    timestamp   = DateTimeField()
    header      = TextField(blank=True, null=True)
    footer      = TextField(blank=True, null=True)
        
    objects = BranchesManager()
    
    class Meta:
        db_table = u'branches'     

class ClassCategories(MigrationBase):
    id          = IntegerField(primary_key=True)
    title       = CharField(max_length=765)
    color       = CharField(max_length=21)
    timestamp   = DateTimeField()
    class Meta:
        db_table = u'class_categories'

class ClassNotifications(MigrationBase):
    id          = IntegerField(primary_key=True)
    class_id    = IntegerField()
    type        = IntegerField()
    status      = IntegerField()
    send_on     = BigIntegerField(null=True, blank=True)
    subject     = CharField(max_length=765)
    content     = TextField()
    class Meta:
        db_table = u'class_notifications'

class ClassesManager(Manager):
    def migrate(self, data, branch_slug=None):
        # find teacher object according to old join classes
        if TeachersXClasses.objects.filter(class_id=int(data['id'])).exists():
            old_join_row = TeachersXClasses.objects.get(class_id=int(data['id']))
            
            do_save = True
            if branch_slug is not None:
                do_save = False
                try:
                    old_class_row = Classes.objects.get(pk=old_join_row.class_id)
                    try:
                        venue = Venue.objects.get(pk=old_class_row.venue_id)
                        try:
                            branch = Branch.objects.get(pk=venue.branch_id)
                            if branch.slug == branch_slug:
                                do_save = True
                        except Branch.DoesNotExist:
                            pass
                    except Venue.DoesNotExist:
                        pass
                except Classes.DoesNotExist:
                    pass            
            
            print "     saving: %s" % do_save            

            if do_save == True:            
                old_teacher_row = Teachers.objects.get(pk=old_join_row.teacher_id)

                teacher = Person.objects.get(email=old_teacher_row.email.lower())
            
                # use django slugify to generate a slug
                slug = slugify(Course, data['title'])

                # clean weird character (remaining UTF-8 data)
                description = data['description'].replace(u"Â ", "")

                # fake a default category value
                if data['category_id'] == None:
                    category = 0
                else:
                    category = data['category_id']
            
                color = '#cc3333'
                if category == 0:
                    color = '#cc3333'
                elif category == 1:
                    color = '#e26521'
                elif category == 2:
                    color = '#dda51e'
                elif category == 3:
                    color = '#74ac23'
                elif category == 4:
                    color = '#2da57c'
                elif category == 5:
                    color = '#2d9ac2'
                elif category == 6:
                    color = '#8a54bb'                                                               

                # create course first
                course = Course.objects.filter(title=data['title'])
                                
                if course.exists() == False: 
                    course = Course(
                                pk           = int(data['id']), 
                                title        = data['title'], 
                                teacher      = teacher, 
                                max_students = int(data['max_students']), 
                                description  = description, 
                                slug         = slug, 
                                created      = timezone.make_aware(data['timestamp'], timezone.utc),
                                updated      = timezone.make_aware(data['timestamp'], timezone.utc),
                        )
                    course.save()
            
                    print "     saved Course: [%s]" % course
                else:
                    course = Course.objects.get(title=data['title'])
                    print "     found Course: [%s]" % course
            
            
                # get venue object for the Schedule venue foreign key field, and for the branch's timezone
                if Venue.objects.filter(pk=data['venue_id']).exists():
                    venue = Venue.objects.get(pk=data['venue_id'])
                    print "         in venue: [%s]" % venue
                    branch = Branch.objects.get(pk=venue.branch.id)
                    print "         in branch: [%s]" % branch
                
                    # save branch to teacher
                    course.teacher.branches.add(branch)
                    course.teacher.save()
                
                    # save branch to course
                    course.save()
                
                    # convert the old unix time values (a bigint) to a timezone-aware datetime object
                    from django.utils.dateparse import parse_datetime    
                    import datetime
                    start_time_naive = parse_datetime(datetime.datetime.fromtimestamp(int(data['unix_start_time'])).strftime('%Y-%m-%d %H:%M:%S'))
                    end_time_naive = parse_datetime(datetime.datetime.fromtimestamp(int(data['unix_end_time'])).strftime('%Y-%m-%d %H:%M:%S'))
                    import pytz
                    localized_start_time = pytz.timezone(branch.timezone).localize(start_time_naive, is_dst=None)
                    localized_end_time = pytz.timezone(branch.timezone).localize(end_time_naive, is_dst=None)
    
                    utc = pytz.timezone('UTC')
                    normalized_start_time = utc.normalize(localized_start_time.astimezone(utc))
                    normalized_end_time   = utc.normalize(localized_end_time.astimezone(utc))    
                
                    aware_start_time = timezone.make_aware(start_time_naive, utc)
                    aware_end_time   = timezone.make_aware(end_time_naive, utc)
                                
                    print "         schedule start time: [%s]" % aware_start_time
                    print "         schedule end time: [%s]" % aware_end_time
                                
                    # now create the schedule
                    schedule = Schedule.objects.filter(course=course)

            
                    # use django slugify to generate a slug
                    slug = slugify(Schedule, course.title)
                    
                    if data['status'] == 0:
                        schedule_status = 'pending'
                    elif data['status'] == 1:
                        schedule_status = 'contacted'
                    elif data['status'] == 2:
                        schedule_status = 'updated'
                    elif data['status'] == 3:
                        schedule_status = 'approved'
                    elif data['status'] == 4:
                        schedule_status = 'rejected'
                    else:
                        schedule_status = 'pending'

                    if schedule.exists() == False:

                        schedule = Schedule(
                                venue                  = venue, 
                                course                 = course, 
                                branch                 = branch,
                                slug                   = slug,
                                color                  = color,
                                schedule_status        = schedule_status,
                                start_time             = aware_start_time, 
                                end_time               = aware_end_time, 
                                created                = timezone.make_aware(data['timestamp'], timezone.utc),                             
                            )
                        schedule.save()


                    else:
                        schedule = Schedule.objects.get(course=course)  
                        schedule.slug = slug
                        schedule.save()
                        #print "             found Schedule: [%s]" % schedule.course.title
                   
                    # create the related barter items, and add them to the schedule item
                    if ClassesXItems.objects.filter(class_id=int(data['id'])).exists():
                        item_old_join_rows = ClassesXItems.objects.filter(class_id=int(data['id']))
                        for item_old_join_row in item_old_join_rows:
                            if Items.objects.filter(pk=item_old_join_row.item_id).exists():
                                item = Items.objects.get(pk=item_old_join_row.item_id)
                            
                                barter_item = BarterItem.objects.filter(pk=item.id)
                                if barter_item.exists() == False:                            
                                    barter_item = BarterItem(
                                            pk          = item.id, 
                                            title       = item.title, 
                                            schedule    = schedule,
                                            created     = timezone.make_aware(data['timestamp'], timezone.utc),
                                        )
                                    barter_item.save()
                            
                                    #print "                 saved BarterItem: [%s]" % barter_item.title
                                else:
                                    barter_item = BarterItem.objects.get(pk=item.id)
                                    barter_item.schedule = schedule
                                    barter_item.save()
                                    #print "                 found BarterItem: [%s]" % barter_item.title
                            
                        #for item in schedule.barteritem_set.all():
                            #print "                          schedule item: [%s]" % item.title
                    
                
class Classes(MigrationBase):
    id              = IntegerField(primary_key=True)
    venue_id        = IntegerField()
    category_id     = IntegerField(null=True, blank=True)
    title           = CharField(max_length=765)
    description     = TextField()
    max_students    = IntegerField()
    status          = IntegerField()
    hash            = CharField(max_length=96)
    timestamp       = DateTimeField()
    unix_start_time = BigIntegerField()
    unix_end_time   = BigIntegerField()
    
    objects = ClassesManager()
    
    class Meta:
        db_table = u'classes'

class ClassesXItems(MigrationBase):
    id              = IntegerField(primary_key=True)
    class_id        = IntegerField()
    item_id         = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'classes_x_items'


class FeedbacksManager(Manager):
    def migrate(self, data, branch_slug=None):

        do_save = True
        if branch_slug is not None:
            do_save = False
            old_feedback_row = Feedbacks.objects.get(pk=int(data['id']))
            try:
                old_class_row = Classes.objects.get(pk=old_feedback_row.class_id)
                try:
                    venue = Venue.objects.get(pk=old_class_row.venue_id)
                    try:
                        branch = Branch.objects.get(pk=venue.branch_id)
                        if branch.slug == branch_slug:
                            do_save = True
                    except Branch.DoesNotExist:
                        pass
                except Venue.DoesNotExist:
                    pass
            except Classes.DoesNotExist:
                pass            
        
        print "     saving: %s" % do_save            
        
        if do_save == True:
            try:
                schedule = Schedule.objects.get(course__id=data['class_id'])
            
                feedback = Feedback.objects.filter(content=data['content'], schedule=schedule)

                if feedback.exists() == False:   
                
                    feedback_type = 'student'
                    if data['type'] == 1:
                        feedback_type = 'teacher'
                
                    feedback = Feedback(
                            pk            = int(data['id']), 
                            schedule      = schedule,
                            feedback_type = feedback_type,
                            content       = data['content'],
                            created       = timezone.make_aware(data['timestamp'], timezone.utc),
                            updated       = timezone.make_aware(data['timestamp'], timezone.utc),                
                        )
                    feedback.save()

                    print "     saved Feedback: [%s]" % feedback            
                else:
                    feedback = Feedback.objects.get(content=data['content'], schedule=schedule)
                    print "     found Feedback: [%s]" % feedback   
            except Schedule.DoesNotExist:
                pass                


class Feedbacks(MigrationBase):
    id              = IntegerField(primary_key=True)
    class_id        = IntegerField()
    type            = IntegerField()
    author_id       = IntegerField()
    content         = TextField()
    timestamp       = DateTimeField()
    
    objects = FeedbacksManager()
    
    class Meta:
        db_table = u'feedbacks'

class Items(MigrationBase):
    id              = IntegerField(primary_key=True)
    title           = CharField(max_length=765)
    requested       = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'items'

class Mailinglist(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField(null=True, blank=True)
    email           = CharField(max_length=765)
    hash            = CharField(max_length=96)
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'mailinglist'

class Notifications(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField()
    type            = IntegerField()
    status          = IntegerField()
    cron            = IntegerField()
    hour_interval   = IntegerField(null=True, blank=True)
    day_interval    = IntegerField(null=True, blank=True)
    subject         = CharField(max_length=765)
    content         = TextField()
    class Meta:
        db_table = u'notifications'

class NotificationsDefaults(MigrationBase):
    id                      = IntegerField(primary_key=True)
    type                    = IntegerField()
    status                  = IntegerField()
    cron                    = IntegerField()
    hour_interval_default   = IntegerField(null=True, blank=True)
    day_interval_default    = IntegerField(null=True, blank=True)
    subject                 = CharField(max_length=765)
    content                 = TextField()
    class Meta:
        db_table = u'notifications_defaults'

class StudentsManager(Manager):
    def migrate(self, data, branch_slug=None):
        
        do_save = True
        if branch_slug is not None:
            do_save = False
            if StudentsXClasses.objects.filter(student_id=int(data['id'])).exists():
                class_old_join_rows = StudentsXClasses.objects.filter(student_id=int(data['id']))
                for class_old_join_row in class_old_join_rows:
                    try:
                        old_class_row = Classes.objects.get(pk=class_old_join_row.class_id)
                        try:
                            venue = Venue.objects.get(pk=old_class_row.venue_id)
                            try:
                                branch = Branch.objects.get(pk=venue.branch_id)
                                if branch.slug == branch_slug:
                                    do_save = True
                            except Branch.DoesNotExist:
                                pass
                        except Venue.DoesNotExist:
                            pass
                    except Classes.DoesNotExist:
                        pass            
        
        print "     saving: %s" % do_save            
        
        if do_save == True:
            # auto generate slug field
            slug = slugify(Person, data['fullname'])

            # we're not copyig the id, to not clash with migrated teachers, 
            # as both are represented with the Person model
            student = Person.objects.filter(email=data['email'].lower())
            if student.exists() == False:
                student = Person.objects.create_user(
                        fullname    = data['fullname'], 
                        email       = data['email'].lower(),
                        phone       = data['phone'], 
                        slug        = slug, 
                        created     = timezone.make_aware(data['timestamp'], timezone.utc),
                        updated     = timezone.make_aware(data['timestamp'], timezone.utc)
                    )
                student.save()
                print "     saved Person: [%s]" % student
            else:
                student = Person.objects.get(email=data['email'].lower())
                print "     found Person: [%s]" % student
            
            # create student registrations
            if StudentsXClasses.objects.filter(student_id=int(data['id'])).exists():
                class_old_join_rows = StudentsXClasses.objects.filter(student_id=int(data['id']))
                for class_old_join_row in class_old_join_rows:
                    class_old_row = Classes.objects.get(pk=class_old_join_row.class_id)
                    try:
                        schedule = Schedule.objects.get(course__title=class_old_row.title)
                        print "         found Schedule: [%s]" % schedule
                
                        registration = Registration.objects.filter(schedule=schedule, student=student)
                        status = 'registered'
                        if class_old_join_row.status == 1:
                            status = 'unregistered'
                    
                        if registration.exists() == False:
                            registration = Registration(schedule=schedule, student=student, registration_status=status, created=data['timestamp']) 
                            registration.save()
                            #print "         saved Registration: [%s]" % registration
                        else:
                            registration = Registration.objects.get(schedule=schedule, student=student)
                            registration.registration_status = status
                            registration.save()
                            #print "         found Registration: [%s]" % registration
                    
                        # save branch id in student Person object
                        branch = registration.schedule.branch
                        #print "             found Branch: [%s]" % branch
                
                        student.branches.add(branch)
                        student.save()                
                    except Schedule.DoesNotExist:
                        pass

                # create student items
                if StudentsXItems.objects.filter(student_id=int(data['id'])).exists():
                    item_old_join_rows = StudentsXItems.objects.filter(student_id=int(data['id']))
                    #print "             found row: [%s]" % item_old_join_rows
                
                    for item_old_join_row in item_old_join_rows:
                    
                        try:                    
                            barter_item = BarterItem.objects.get(pk=item_old_join_row.item_id)
                            registration.items.add(barter_item)
                            registration.save()
                        except BarterItem.DoesNotExist:
                            pass
    
class Students(MigrationBase):
    id              = IntegerField(primary_key=True)
    fullname        = CharField(max_length=765, blank=True)
    email           = CharField(max_length=765)
    phone           = CharField(max_length=60)
    hash            = CharField(max_length=96)
    timestamp       = DateTimeField()
    
    objects = StudentsManager()
    
    class Meta:
        db_table = u'students'

class StudentsXClasses(MigrationBase):
    id              = IntegerField(primary_key=True)
    student_id      = IntegerField()
    class_id        = IntegerField()
    status          = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'students_x_classes'

class StudentsXItems(MigrationBase):
    id              = IntegerField(primary_key=True)
    student_id      = IntegerField()
    item_id         = IntegerField()
    class_id        = IntegerField()
    registered      = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'students_x_items'

class TeachersManager(Manager):
    def migrate(self, data, branch_slug=None):        
        do_save = True
        if branch_slug is not None:
            do_save = False
            
            if TeachersXClasses.objects.filter(teacher_id=int(data['id'])).exists():
                class_old_join_rows = TeachersXClasses.objects.filter(teacher_id=int(data['id']))
                for class_old_join_row in class_old_join_rows:
                    try:
                        old_class_row = Classes.objects.get(pk=class_old_join_row.class_id)
                        try:
                            venue = Venue.objects.get(pk=old_class_row.venue_id)
                            try:
                                branch = Branch.objects.get(pk=venue.branch_id)
                                if branch.slug == branch_slug:
                                    do_save = True
                            except Branch.DoesNotExist:
                                pass
                        except Venue.DoesNotExist:
                            pass
                    except Classes.DoesNotExist:
                        pass

        if do_save == True:
            slug = slugify(Person, data['fullname'])            

            try:
                teacher = Person.objects.get(email=data['email'].lower())
                print "     found Person: [%s]" % teacher
            except Person.DoesNotExist:
                teacher = Person.objects.create_user(
                        pk          = int(data['id']),
                        fullname    = data['fullname'], 
                        email       = data['email'].lower(), 
                        phone       = data['phone'],
                        bio         = data['bio'],
                        website     = data['website'],
                        slug        = slug,
                        created     = timezone.make_aware(data['timestamp'], timezone.utc),
                        updated     = timezone.make_aware(data['timestamp'], timezone.utc),
                    )
                teacher.save()
                print "     saved Person: [%s]" % teacher
            
        
class Teachers(MigrationBase):
    id              = IntegerField(primary_key=True)
    fullname        = CharField(max_length=765)
    email           = CharField(max_length=765)
    bio             = TextField()
    phone           = CharField(max_length=60)
    website         = CharField(max_length=765, blank=True)
    status          = IntegerField()
    hash            = CharField(max_length=96)
    timestamp       = DateTimeField()
    
    objects = TeachersManager()
    
    class Meta:
        db_table = u'teachers'

class TeachersXClasses(MigrationBase):
    id              = IntegerField(primary_key=True)
    teacher_id      = IntegerField()
    class_id        = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'teachers_x_classes'



class UsersManager(Manager):
    def migrate(self, data, branch_slug=None):

        do_save = True
        if branch_slug is not None:
            do_save = False
            try:
                branch = Branch.objects.get(pk=data['branch_id'])
                if branch.slug == branch_slug:
                    do_save = True
            except Branch.DoesNotExist:
                pass

        print "     saving: %s" % do_save        

        if do_save == True:
            pk = int(data['id']) + 10000            
            slug = unique_slugify(Person, data['username'], 'fullname')
            try:
                user = Person.objects.get(username=data['username'], email=data['email'])
                user.is_staff = True
                user.save()
                print "     turned student or teacher into admin: [%s]" % user                            
            except Person.DoesNotExist:
                try:
                    user = Person.objects.get(pk=pk)
                    print "     found User: [%s]" % user                    
                except Person.DoesNotExist:        
                    user = Person.objects.create_user(
                            pk          = pk, 
                            fullname    = data['username'],
                            username    = data['username'],
                            slug        = slug,
                            email       = data['email'].lower(), 
                            is_staff    = True, 
                            created     = timezone.make_aware(data['timestamp'], timezone.utc),
                            updated     = timezone.make_aware(data['timestamp'], timezone.utc),
                        )
                    print "     saved User: [%s]" % user            

            g = Group.objects.get(name='translators') 
            g.person_set.add(user)
        
            try:
                branch = Branch.objects.get(pk=data['branch_id'])
                branch.organizers.add(user)
                user.branches.add(branch)
                user.default_branch = branch
                user.save()
                
            except Branch.DoesNotExist:
                pass
            

class Users(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField()
    username        = CharField(max_length=765)
    email           = CharField(max_length=765)
    password        = CharField(max_length=765)
    hash            = CharField(max_length=96, blank=True)
    status          = IntegerField()
    role            = IntegerField()
    timestamp       = DateTimeField()
    
    objects = UsersManager()
    
    class Meta:
        db_table = u'users'

class VenueRules(MigrationBase):
    id              = IntegerField(primary_key=True)
    venue_id        = IntegerField()
    season_id       = IntegerField()
    day             = CharField(max_length=765)
    start_time      = TextField() # This field type is a guess.
    end_time        = TextField() # This field type is a guess.
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'venue_rules'

class VenueRulesExceptions(MigrationBase):
    id              = IntegerField(primary_key=True)
    rule_id         = IntegerField()
    start_time      = DateTimeField()
    end_time        = DateTimeField()
    type            = IntegerField()
    timestamp       = DateTimeField()
    class Meta:
        db_table = u'venue_rules_exceptions'

class VenueTimes(MigrationBase):
    id              = IntegerField(primary_key=True)
    venue_id        = IntegerField()
    timestamp       = DateTimeField()
    unix_start_time = BigIntegerField()
    unix_end_time   = BigIntegerField()
    class Meta:
        db_table = u'venue_times'

class VenuesManager(Manager):
    def migrate(self, data, branch_slug=None):
        
        if data['color'] is None:
            color = '#000fff'
        else:
            color = data['color']
        
        venue = Venue.objects.filter(pk=data['id'])
        
        do_save = True
        if branch_slug is not None:
            do_save = False
            try:
                branch = Branch.objects.get(pk=data['branch_id'])
                if branch.slug == branch_slug:
                    do_save = True
            except Branch.DoesNotExist:
                pass
        print "     saving: %s" % do_save        
        
        if do_save == True:
            branch = Branch.objects.get(pk=data['branch_id'])
            
            if venue.exists() == False:                        
                venue = Venue(
                        pk          = data['id'], 
                        title       = data['title'], 
                        phone       = data['phone'], 
                        city        = data['city'], 
                        state       = data['state'], 
                        country     = data['country'][:2], 
                        address_1   = data['address_1'], 
                        capacity    = int(data['capacity']), 
                        resources   = data['resources'], 
                        color       = color, 
                        is_active   = data['status'], 
                        created     = timezone.make_aware(data['timestamp'], timezone.utc),
                        updated     = timezone.make_aware(data['timestamp'], timezone.utc),
                        branch      = branch
                    )
                venue.save()   
                print "     saved Venue: [%s]" % venue            
            
            else:
                venue = Venue.objects.get(pk=data['id'])
                print "     found Venue: [%s]" % venue            
             
    
class Venues(MigrationBase):
    id              = IntegerField(primary_key=True)
    branch_id       = IntegerField()
    title           = CharField(max_length=765)
    type            = IntegerField()
    address_1       = CharField(max_length=765)
    address_2       = CharField(max_length=765, blank=True, null=True)
    city            = CharField(max_length=765)
    state           = CharField(max_length=765, blank=True, null=True)
    country         = CharField(max_length=765)
    zipcode         = CharField(max_length=60)
    phone           = CharField(max_length=60, blank=True, null=True)
    capacity        = IntegerField()
    resources       = TextField()
    status          = IntegerField()
    timestamp       = DateTimeField()
    color           = CharField(max_length=21, blank=True, null=True)
    
    objects = VenuesManager()
    
    class Meta:
        db_table = u'venues'
        

