# -*- coding: utf-8 -*-
'''
Django settings for toolbox project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

import os

#
# Path settings.
#

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJ_DIR)

#
# Security.
#

SECRET_KEY = 'change-me-in-production'

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

DEBUG = False

ALLOWED_HOSTS = [
    '*',
]

#
# Applications and middleware classes.
# https://docs.djangoproject.com/en/1.9/ref/applications/
# https://docs.djangoproject.com/en/1.9/topics/http/middleware/
#

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'compressor',
    'ordertracking',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'toolbox.middleware.LoginRequiredMiddleware'
]


WSGI_APPLICATION = 'toolbox.wsgi.application'


#
# Database settings.
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
#


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators




#
# Internationalization.
# https://docs.djangoproject.com/en/1.9/topics/i18n/
#

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'

USE_I18N = False
USE_L10N = False
USE_TZ   = False

TIME_FORMAT           = 'H:i:s'
DATE_FORMAT           = 'j. M Y'
SHORT_DATE_FORMAT     = 'j.m.y'
DATETIME_FORMAT       = '{} / {}'.format(DATE_FORMAT, TIME_FORMAT)
SHORT_DATETIME_FORMAT = '{} / {}'.format(SHORT_DATE_FORMAT, TIME_FORMAT)

#
# URL settings.
#

ROOT_URLCONF = 'toolbox.urls'

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL         = '/'

LOGIN_REQUIRED_URLS = (
    r'.',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'^/admin/',
    r'^/login/$',
)

#
# Template settings.
# https://docs.djangoproject.com/en/1.9/ref/templates/
#

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJ_DIR, 'templates'),
        ],
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


#
# Static files.
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# http://django-compressor.readthedocs.org/en/latest
#

STATIC_URL       = '/static/'

STATIC_ROOT      = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(PROJ_DIR, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

#
# Crispy forms.
# http://django-crispy-forms.readthedocs.org/en/latest/
#

CRISPY_TEMPLATE_PACK = 'bootstrap3'

#
# Toolbox settings.
#

SHIPPING_URL = 'https://service.post.ch/EasyTrack/submitParcelData.do?formattedParcelCodes={}&from_directentry=True&directSearch=false&p_language=de&VTI-GROUP=1&lang=de&service=ttb'

#
# Load custom settings.
#

try:
    from settings_custom import *
except ImportError:
    pass