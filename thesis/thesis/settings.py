# -*- coding: utf-8 -*-
"""
Django settings for thesis project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1_!*!#ewh0qzj_gi59c2o65kb(=35=etn(d0oqv!2)^k)de6g*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [ 'localhost']

# Application definition

INSTALLED_APPS = [
    'funfly',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.sites',
    'social.apps.django_app.default',
    'sass_processor',
    'crispy_forms',
    # 'debug_toolbar',
    'pytz',
    'moderation',
    'el_pagination',
    'rolepermissions',
    'gm2m',
    'haystack',
    'django_social_share',

]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'funfly.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'thesis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/Users/alexandrurustin/Desktop/thesis/thesis/thesis/funfly/templates/funfly'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

WSGI_APPLICATION = 'thesis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',

)

SOCIAL_AUTH_FACEBOOK_KEY = '527379650781936'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd14158368a25f659e4920fb7fb845380'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_location']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email, gender, timezone, location, picture'
}

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email', 'location']

# SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'index'
SOCIAL_AUTH_LOGIN_URL = 'index'

USER_MODEL = 'auth.User'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'funfly.middleware.save_profile',  # <--- set the path to the function
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

ROLEPERMISSIONS_MODULE = 'thesis.roles'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'funfly/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'funfly/static/funfly')
MEDIA_URL = '/'

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'funfly/static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(BASE_DIR, 'funfly/static/funfly/css'),
)


SASS_PRECISION = 8

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'


CRISPY_TEMPLATE_PACK = 'bootstrap3'
DEFAULT_CHARSET = 'utf-8'

# DEBUG_TOOLBAR_PANELS = (
# #   'debug_toolbar.panels.version.VersionDebugPanel',
# #   'debug_toolbar.panels.timer.TimerDebugPanel',
# #   'debug_toolbar.panels.profiling.ProfilingPanel',
# # )

# BROKER_URL = 'amqp://guest@localhost//'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Bucharest'
CELERY_ENABLE_UTC = False

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
