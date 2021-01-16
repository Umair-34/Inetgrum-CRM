import os

from django.contrib import messages
from django.contrib.messages import constants as message_constants
from os.path import join

DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = BASE_DIR

SECRET_KEY = 'ABC1234' #TODO Changeme

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Asia/Kolkata"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "landingRegister:dashboard"
LOGOUT_REDIRECT_URL = "login"



SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 5
SESSION_SECURITY_EXPIRE_AFTER = 12

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "project.wsgi.application"

ASGI_APPLICATION = 'project.routing.application'

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    "todo",
    'django_chatter',
    "landingRegister",
    "django_extensions",
    'rest_framework',
    'channels',
)



# chatenn

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

MESSAGES_TO_LOAD = 15


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "core.routing.channel_routing",
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
# chat

# Static files and uploads

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "project", "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Uploaded media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Without this, uploaded files > 4MB end up with perm 0600, unreadable by web server process
FILE_UPLOAD_PERMISSIONS = 0o644

# ######################
# Override in local.py :
# ######################

# SECRET_KEY = os.environ['SECRET_KEY']
# SECRET_KEY = 'lksdf98wrhkjs88dsf8-324ksdm'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "project", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Your stuff: custom template context processors go here
            ]
        },
    }
]


# Override CSS class for the ERROR tag level to match Bootstrap class name
MESSAGE_TAGS = {message_constants.ERROR: "danger"}

# Override in local.py
# DATABASES = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.environ['DB_NAME'],
        # 'USER': os.environ['DB_USER'],
        # 'PASSWORD': os.environ['DB_PASS'],
        # 'HOST': os.environ['DB_HOST'],
        # 'PORT': '5432',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER='integrum.official@gmail.com'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FORM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD='tpuhygklredbitia'


# kdpycaaslwavodbo
# Todo-specific settings
# TODO_STAFF_ONLY = False
# TODO_DEFAULT_LIST_ID = None
# TODO_DEFAULT_ASSIGNEE = None
# TODO_PUBLIC_SUBMIT_REDIRECT = '/'
# TODO_ALLOW_FILE_ATTACHMENTS = True
# TODO_LIMIT_FILE_ATTACHMENTS = [".jpg", ".gif", ".png", ".csv", ".pdf"]
