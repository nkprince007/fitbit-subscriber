"""
Django settings for subscriber project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from ast import literal_eval
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6764jv$-2^or2(7#p^r#nsq3icnts61*=qbb2967*3g6fgsmi8'

# SECURITY WARNING: don't run with debug turned on in production!
HEROKU = literal_eval(os.environ.get('IS_HEROKU_DEPLOYMENT', 'False'))
DEBUG = literal_eval(os.environ.get('DJANGO_DEBUG', 'True'))
if HEROKU:
    DEBUG = False


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '.ngrok.io',
    '.herokuapp.com',
    os.environ.get('HOST_IP'),
]


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'bootstrap',
    'fontawesome',
    'fitbit_auth.apps.FitbitAuthConfig',
    'fitbit_data.apps.FitbitDataConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'subscriber.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'subscriber.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if HEROKU or os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME', 'fitbit-subscriber-db'),
            'USER': os.environ.get('DB_USER', 'fitbit-subscriber'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'fitbit-subscriber'),
            'HOST': os.environ.get('DB_ADDRESS', '127.0.0.1'),
            'PORT': os.environ.get('DB_PORT', 5432)
        }
    }


# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public'),
]


# django-cors-headers configuration
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = True


# Fitbit OAuth Configuration

FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID', '22CD9P')
FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET',
                                      '393ccc92f9217f7fe17a0f6f56a48b44')
FITBIT_SUBSCRIBER_VERIFICATION_CODE = os.environ.get(
    'FITBIT_SUBSCRIBER_VERIFICATION_CODE',
    'fdaaebbd1ac8697d7aa750011c7c6a07e88ca14ea2950588c2bbcb0fbb22137d')


# Redis in-memory database
# https://stream-framework.readthedocs.io/en/latest/settings.html

REDIS_ADDRESS = os.environ.get('REDIS_ADDRESS', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
REDIS_DATABASE = os.environ.get('REDIS_DATABASE', 0)


# Configuring celery task queue
# http://docs.celeryproject.org/en/latest/

if DEBUG:
    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
else:
    BROKER_URL = (f'redis://{REDIS_ADDRESS}:{REDIS_PORT}' if not HEROKU
                  else os.environ.get('HEROKU_REDIS_WHITE_URL'))
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
