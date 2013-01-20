LOCAL_SETTINGS = True
from django.conf import settings
from settings import *

SITE_ID = 2

# define environment
STAGE_NAME = 'PROD' # either PROD or DEV

# debugging changes according to environment configuration
if STAGE_NAME == 'DEV':
    DEBUG = True
else :
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                         # Or path to database file if using sqlite3.
        'USER': '',                         # Not used with sqlite3.
        'PASSWORD': '',                     # Not used with sqlite3.
        'HOST': '',                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                         # Set to empty string for default. Not used with sqlite3.
    }
}
 
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_URL = 'http://127.0.0.1:8000/media/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

MAILER_USE_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#MAILER_USE_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST =
# EMAIL_PORT =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_USE_TLS =


CACHES = {
    'default' : dict(
        BACKEND = 'johnny.backends.filebased.FileBasedCache',
        LOCATION = PROJECT_DIR + '/tmp/django_cache',
        JOHNNY_CACHE = True,
    )
}
# CACHES = {
#     'default' : dict(
#         BACKEND = 'johnny.backends.memcached.MemcachedCache',
#         LOCATION = ['127.0.0.1:11211'],
#         JOHNNY_CACHE = True,
#     )
# }
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_ts'