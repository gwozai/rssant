"""
Django settings for rssant project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
from .env import EnvConfig

ENV_CONFIG = EnvConfig.load()

if ENV_CONFIG.is_celery_process is None:
    IS_CELERY_PROCESS = 'celery' in sys.argv[0]
else:
    IS_CELERY_PROCESS = ENV_CONFIG.is_celery_process

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_CONFIG.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_CONFIG.debug

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'raven.contrib.django.raven_compat',
    'debug_toolbar',
    'django_celery_results',
    'django_celery_beat',
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'rest_auth',
    'rest_auth.registration',
    'rssant_api',
]

MIDDLEWARE = [
    'rssant.middleware.time.TimeMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'rssant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rssant.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_postgrespool2',
        'NAME': ENV_CONFIG.pg_db,
        'USER': ENV_CONFIG.pg_user,
        'PASSWORD': ENV_CONFIG.pg_password,
        'HOST': ENV_CONFIG.pg_host,
        'PORT': ENV_CONFIG.pg_port,
    }
}

# https://github.com/heroku-python/django-postgrespool
DATABASE_POOL_ARGS = {
    'max_overflow': 20,
    'pool_size': 5,
    'recycle': 300
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Sentry, 在celery进程中不要配置django的sentry
if not IS_CELERY_PROCESS:
    RAVEN_CONFIG = {
        'dsn': ENV_CONFIG.sentry_dsn,
    }

# RSSANT

# 每10分钟检查一次更新
RSSANT_CHECK_FEED_SECONDS = 10 * 60


# Celery tasks

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = ENV_CONFIG.redis_url
CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_BEAT_SCHEDULE = {
    'check-feed-every-10-seconds': {
        'task': 'rssant.tasks.check_feed',
        'schedule': 10,
        'kwargs': {'seconds': RSSANT_CHECK_FEED_SECONDS}
    },
    'clean-user-feed-every-10-seconds': {
        'task': 'rssant.tasks.clean_user_feed',
        'schedule': 10,
        'kwargs': {}
    }
}


# Django All Auth
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
SOCIAL_APP_GITHUB = {
    'client_id': ENV_CONFIG.github_client_id,
    'secret': ENV_CONFIG.github_secret,
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
