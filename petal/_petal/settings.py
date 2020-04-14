"""
Django settings for petal project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from os import environ, path, makedirs

# Connect to Neo4j Database
from neomodel import config
from neomodel import db

config.DATABASE_URL = "bolt://neo4j:testing@139.88.179.199:7667"
db.set_connection('bolt://neo4j:testing@139.88.179.199:7667')

ELASTIC_SEARCH_HOST = 'localhost:9200'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wtfbk4yoq5lj2%d_-f#l=6msc8)1+&(de2b!5)1d_a@n8$=+8l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['139.88.179.199', '0.0.0.0', '127.0.0.1']

# Application definition

INSTALLED_APPS = [

    # Petal
    'home.apps.HomeConfig',
    'bird.apps.BirdConfig',
    'api.apps.ApiConfig',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_api_key',
    'rest_auth',

    # Third Party
    'django_neomodel',
    'neomodel',
    'allauth',
    'allauth.account',
    'six',
]

# django-allauth config
SITE_ID = 1

LOGIN_REDIRECT_URL = 'petalhome'
ACCOUNT_LOGOUT_REDIRECT = 'petalhome'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# have Django output any emails to the command line console instead.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '_petal.urls'

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
        },
    },
]

WEB_ADDRESS = "https://petal.local"


WSGI_APPLICATION = '_petal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'kunle',
        'PASSWORD': 'testing',
        'HOST': '139.88.179.199',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_ALWAYS_EAGER = False

REMOVE_CLASSES = ["Searchable", "AbstractNode"]

SEARCH_TYPES = [
    ("general", "general"),
]
