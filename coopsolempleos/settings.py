# Django settings for coopsolempleos project.
#encoding:utf-8

# Identificando la ruta del proyecto
import os
PATH_PROJECT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EXTJS4_DEBUG = DEBUG

#SIMPLE_AUTOCOMPLETE_MODELS = ('',)
#SIMPLE_AUTOCOMPLETE = {'Universidad': {'max_items': 10}}
#ROOT_URLCONF = 'simple_autocomplete.urls'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Jimbert Castillo M.', 'jcastillo@coopsol.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'coopsolempleos',                      # Or path to database file if using sqlite3.
        'USER': 'ce',                      # Not used with sqlite3.
        'PASSWORD': 'ce.++',                  # Not used with sqlite3.
        'HOST': '192.168.0.2',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Lima'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-PE'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PATH_PROJECT, 'carga')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
if DEBUG:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = 'http://www.coopsolempleos.com/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://www.coopsolempleos.com/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PATH_PROJECT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7)1_ixspd((n0v=x@w!5hl4zjry)nl_-p+ijn+%s-7bp50h=9i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'coopsolempleos.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'coopsolempleos.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PATH_PROJECT, 'templates'),
    #'C:/Python27/Lib/site-packages/django_debug_toolbar-0.9.4-py2.7.egg/debug_toolbar/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'main',
    'ubigeo',
    'emailusernames',
    #'captcha',
    #'extjs4',
    'django_facebook',
    #'open_facebook'
    'djcelery',
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
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.grupocoopsol.com'
EMAIL_HOST_USER = 'jcastillo@coopsol.com'
EMAIL_HOST_PASSWORD = 'abc123.'
EMAIL_PORT = 25

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'emailusernames.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

RECAPTCHA_PUBLIC_KEY = '6LcdcNwSAAAAAHg6fMHjoQ0tZKbJ0a-pUzJjGxxH'
RECAPTCHA_PRIVATE_KEY = '6LcdcNwSAAAAAP2ATB3n_LYW0pBDVt2fzIVdxriI'

#TWITTER_CONSUMER_KEY = 'CN53sBLpSBVXQ77k6FB74g'
#TWITTER_CONSUMER_SECRET = 'alR2AL7KBBmkwgFl51VA8mCINoYGVHLTMYKsfmX218'

FACEBOOK_APP_ID = '595394750488938'
FACEBOOK_APP_SECRET = 'dc480e4e1286147e3e51c39c66888629'

FACEBOOK_STORE_LIKES = True
FACEBOOK_STORE_FRIENDS = True
FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/postulante'

import djcelery
djcelery.setup_loader()

# use celery for storing friends and likes
FACEBOOK_CELERY_STORE = True
# use celery for extending tokens
FACEBOOK_CELERY_TOKEN_EXTEND = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django_facebook.context_processors.facebook',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'main.globals.globals',
    "django.core.context_processors.request",
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# debug_toolbar settings
#if DEBUG:
#    INTERNAL_IPS = ('127.0.0.1',)
#    MIDDLEWARE_CLASSES += (
#        'debug_toolbar.middleware.DebugToolbarMiddleware',
#    )
#
#    INSTALLED_APPS += (
#        'debug_toolbar',
#    )
#
#    DEBUG_TOOLBAR_PANELS = (
#        'debug_toolbar.panels.version.VersionDebugPanel',
#        'debug_toolbar.panels.timer.TimerDebugPanel',
#        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#        'debug_toolbar.panels.headers.HeaderDebugPanel',
#        #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
#        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#        'debug_toolbar.panels.sql.SQLDebugPanel',
#        'debug_toolbar.panels.template.TemplateDebugPanel',
#        'debug_toolbar.panels.cache.CacheDebugPanel',
#        'debug_toolbar.panels.signals.SignalDebugPanel',
#        'debug_toolbar.panels.logger.LoggingPanel',
#    )

#    DEBUG_TOOLBAR_CONFIG = {
#        'INTERCEPT_REDIRECTS': False,
#    }