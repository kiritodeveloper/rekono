"""
Django settings for rekono project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from findings.enums import Severity
from processes.enums import StepPriority
from security.crypto import generate_random_value, hash
from targets.enums import TargetType
from tasks.enums import Status, TimeUnit
from tools.enums import FindingType, IntensityRank
from users.enums import Notification

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to save execution outputs
EXECUTION_OUTPUTS = os.path.join(BASE_DIR.parent, 'outputs')
if not os.path.isdir(EXECUTION_OUTPUTS):
    os.mkdir(EXECUTION_OUTPUTS)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = generate_random_value(3000)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_rq',
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',
    'executions',
    'findings',
    'processes',
    'projects',
    'targets',
    'tasks',
    'telegram_bot',
    'tools',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'security.middleware.RekonoMiddleware',
]

ROOT_URLCONF = 'rekono.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'mail', 'templates')
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

WSGI_APPLICATION = 'rekono.wsgi.application'


# API REST

REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': None,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rekono.api.pagination.Pagination',
    'ORDERING_PARAM': 'order',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
        'security.authorization.permissions.ProjectMemberPermission',
        'security.authorization.permissions.ProcessCreatorPermission',
    ]
}

# Documentation

SPECTACULAR_SETTINGS = {
    'TITLE': 'Rekono API Rest',
    'DESCRIPTION': 'Tool to automate recon tasks during pentesting processes',
    'VERSION': '1.0.0',
    'PREPROCESSING_HOOKS': [
        'drf_spectacular.hooks.preprocess_exclude_path_format'
    ],
    'ENUM_NAME_OVERRIDES': {
        'PriorityEnum': StepPriority.choices,
        'StatusEnum': Status.choices,
        'NotificationPreferenceEnum': Notification.choices,
        'SeverityEnum': Severity.choices,
        'TimeUnitEnum': TimeUnit.choices,
        'IntensityEnum': IntensityRank.choices,
        'FindingTypeEnum': FindingType.choices,
        'TargetTypeEnum': TargetType.choices,
    }
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rekono',
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Redis Queue

RQ_QUEUES = {
    'tasks-queue': {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 60       # 1 minute
    },
    'executions-queue': {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 7200     # 2 hours
    },
    'findings-queue': {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 300      # 5 minutes
    }
}


# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = True


# Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_TOKEN_EXPIRATION_HOURS = 24


# Defect-Dojo
DEFECT_DOJO = {
    'HOST': 'http://127.0.0.1:8080',
    'API_KEY': os.getenv('DEFECTDOJO_KEY', ''),
    'AUTO_CREATION': True,
    'REKONO_TAGS': ['rekono'],
    'REKONO_PROD_TYPE_ID': None,
    'REKONO_PROD_TYPE': 'Rekono',
    'REKONO_ENGAGEMENT': 'Rekono'
}


# Tools configuration
TOOLS = {
    'cmseek': {
        'directory': '/usr/share/cmseek'
    }
}


# Authentication

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'security.passwords.PasswordComplexityValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
