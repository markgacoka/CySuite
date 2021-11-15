import os
import datetime
import django_heroku
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# MODE
DEBUG = bool(int(os.environ.get("DEBUG", 0)))
ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'cyauth.Account'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'cyauth.backends.CaseInsensitiveModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'main',
    'cyauth',
    'api',
    'storages',
    'django_celery_results',
    'celery_progress',
    'rest_framework',
    'rest_framework.authtoken',
]

SITE_ID = int(os.environ.get('SITE_ID'))
LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_SIGNUP_FORM_CLASS = 'cyauth.forms.RegistrationForm'
ACCOUNT_ADAPTER = "cysuite.adapter.MyLoginAccountAdapter"
SOCIALACCOUNT_ADAPTER = "cysuite.adapter.MySocialAccountAdapter"
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'oauth2',
    },
    'google':
        { 'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': { 'access_type': 'online' }
    },
    'twitter': {},
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'cysuite.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_tags':'main.template_tags.custom_tags'
            },
        },
    },
]

if DEBUG:
    ALLOWED_HOSTS = ['*',]
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('ENGINE'),
            'HOST': 'localhost',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
else:
    ALLOWED_HOSTS_ENV = os.environ.get('DJANGO_ALLOWED_HOSTS')
    if ALLOWED_HOSTS_ENV:
        ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(','))
    
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('ENGINE'),
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

WSGI_APPLICATION = 'cysuite.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'templates/static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

if DEBUG:
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    REDIS_URL = "redis://{host}:{port}/1".format(
        host=os.getenv('CELERY_BROKER_URL', 'localhost'),
        port=os.getenv('REDIS_PORT', '6379')
    )
else:
    CELERY_BROKER_URL = os.environ.get('REDISTOGO_URL')
    CELERY_RESULT_BACKEND = os.environ.get('REDISTOGO_URL')
    REDIS_URL = "redis://{host}:{port}/1".format(
        host=os.getenv('REDISTOGO_URL', 'localhost'),
        port=os.getenv('REDIS_PORT', '6379')
    )

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = os.environ.get('CELERY_TASK_SERIALIZER', 'json')
CELERY_RESULT_SERIALIZER = os.environ.get('CELERY_RESULT_SERIALIZER', 'json')
CELERY_TASK_TRACK_STARTED= bool(int(os.environ.get('CELERY_TASK_TRACK_STARTED', 1)))
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'Africa/Nairobi')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}

# STATIC_LOCATION = 'static'
MEDIA_LOCATION = 'media'
# STATIC_URL = 'https://%s/%s/' % (os.environ.get('AWS_S3_CUSTOM_DOMAIN'), STATIC_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (os.environ.get('AWS_S3_CUSTOM_DOMAIN'), MEDIA_LOCATION)
DEFAULT_FILE_STORAGE = 'cysuite.s3utils.MediaStorage'
# STATICFILES_STORAGE = 'cysuite.s3utils.StaticStorage'
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL')
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_PRELOAD_METADATA = bool(int(os.environ.get("AWS_PRELOAD_METADATA", 1)))
AWS_QUERYSTRING_AUTH = bool(int(os.environ.get("AWS_QUERYSTRING_AUTH", 0)))

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

django_heroku.settings(locals())

                                         
