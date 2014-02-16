# Django settings for ts project.
import os
import sys
from django.utils.translation import ugettext_lazy as _

ADMINS = (
    ('Or Zubalsky', 'juviley@gmail.com'),
)

MANAGERS = ADMINS

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

PROJECT_DIR = os.path.dirname(__file__) + '/..'

sys.path.append(os.path.dirname(PROJECT_DIR))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))
sys.path.append(os.path.join(PROJECT_DIR, 'libs'))

ROOT_URLCONF = 'ts.urls'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = ''

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static/'),
    os.path.join(PROJECT_DIR, 'apps', 'branches'),
    os.path.join(
        PROJECT_DIR,
        '..',
        'parts',
        'django-admin-enhancer',
        'admin_enhancer',
        'static'
    )
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #('django.template.loaders.cached.Loader', (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
    #)),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'tradeschool.context_processors.branch',
    'tradeschool.context_processors.google_analytics'
)

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tradeschool.middleware.BranchMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

BASE_BRANCH_TEMPLATE_DIR    = PROJECT_DIR + '/apps/tradeschool/templates/branches_base'
DEFAULT_BRANCH_TEMPLATE_DIR = PROJECT_DIR + '/apps/tradeschool/templates/branches_default'
BRANCH_TEMPLATE_DIR         = PROJECT_DIR + '/apps/branches/'

TEMPLATE_DIRS = (
    # Put strings here, like '/home/html/django_templates' or 'C:/www/django/templates'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BRANCH_TEMPLATE_DIR,
    DEFAULT_BRANCH_TEMPLATE_DIR,
    BASE_BRANCH_TEMPLATE_DIR,
    PROJECT_DIR + '/apps/tradeschool/templates',
    PROJECT_DIR + '/templates',
    PROJECT_DIR + '/../parts/django-admin-enhancer/admin_enhancer/templates/',
)


FIXTURE_DIRS = (
    PROJECT_DIR + '/apps/tradeschool/fixtures',
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

ADMIN_MEDIA_PREFIX = '/admin/media/'
LOGIN_URL = '/admin'
INTERNAL_IPS = ('127.0.0.1',)
#BRANCH_FILES = MEDIA_ROOT + '/branches_files'

AUTH_USER_MODEL = 'tradeschool.Person'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'rosetta-grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.redirects',
    'django.contrib.flatpages',
    'flatpages_tinymce',
    'django_ace',
    'templatesadmin',
    'south',              # intelligent schema and data migrations
    'pytz',               # python timezone library
    'dajaxice',           # django ajax app
    'rosetta',            # django admin translation interface
    'admin_enhancer',
    #'debug_toolbar',
    #'tastypie',
    #'django_mailer',     # handle outgoing email queue
    'tradeschool',        # tradeschool branch app
    # 'branches',         # holding all branch-specific files (templates, css, js)
    #'migration',         # tradeschool (zend framework php version) db schema migration

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'dajaxice': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'table,spellchecker,paste,searchreplace',
    'theme': 'advanced',
}


GRAPPELLI_ADMIN_TITLE = _('Trade School Admin')
GRAPPELLI_INDEX_DASHBOARD = 'ts.dashboard.CustomIndexDashboard'

TEMPLATESADMIN_GROUP = 'translators'
TEMPLATESADMIN_TEMPLATE_DIRS = (
    BRANCH_TEMPLATE_DIR,
)

DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d %I:%M %p',      # '2006-10-25 2:30PM'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
)

TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
    '%I:%M %p'       # '2:30PM'
)

# You can find more languages that Django supports
# at http://www.i18nguy.com/unicode/language-identifiers.html

ROSETTA_MESSAGES_PER_PAGE = 100
LANGUAGES = (
    ('en', 'English'),
    ('es_es', 'Spanish (Spain)'),
    ('es_mx', 'Spanish (Mexico)'),
    ('es_us', 'Spanish (US)'),
    ('es_ar', 'Spanish (Argentina)'),
    ('es_cl', 'Spanish (Chile)'),
    ('es_ec', 'Spanish (Ecuador)'),
    ('es_pr', 'Spanish (Puerto Rico)'),
    ('es_ve', 'Spanish (Venezuela)'),
    ('de_de', 'German'),
    ('ms_sg', 'Malay'),
    ('zh_sg', 'Chinese (Singapore)'),
    ('it_it', 'Italian'),
    ('tl', 'Tagalog'),
    ('fr-FR', 'French'),
    ('nl_nl', 'Dutch'),
    ('th', 'Thai'),
    ('pt_br', 'Portuguese'),
    ('el_gr', 'Greek'),
    ('ru_ru', 'Russian'),
    ('zh_cn', 'Chinese (China)'),
    ('vi', 'Vietnamese'),
    ('ta_sg', 'Tamil (Singapore)')
)
