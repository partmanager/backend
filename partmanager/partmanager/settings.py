"""
Django settings for partmanager project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Celery settings
#CELERY_BROKER_URL = 'amqp://guest:guest@localhost'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
#CELERY_TASK_SERIALIZER = 'json'

# Celery Configuration Options
#CELERY_TIMEZONE = "Australia/Tasmania"
#CELERY_TASK_TRACK_STARTED = True
#CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6!uh6dqr$25b0vs1k0!$p_^3mitiopdk6vbemqoje3egumr8#g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'django_filters',
    'django_celery_results',
    "corsheaders",

    'inventory.apps.InventoryConfig',
    'invoices.apps.InvoicesConfig',
    'distributors.apps.DistributorsConfig',
    'symbolandfootprint.apps.SymbolandfootprintConfig',
    'manufacturers.apps.ManufacturersConfig',
    'partcatalog.apps.PartcatalogConfig',
    'projects.apps.ProjectsConfig',
    'packages.apps.PackagesConfig',
    'partdb_git.apps.PartDBConfig',
    'celery_progress'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )

    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 15,
    # 'PAGE_SIZE_QUERY_PARAM': 'page_size'
}

ROOT_URLCONF = 'partmanager.urls'


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

WSGI_APPLICATION = 'partmanager.wsgi.application'

# DATE_INPUT_FORMATS = ('%Y/%m/%d')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '',
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/shelftracker/debug.log",
        },
        "distributors-file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/shelftracker/debug-distributors.log",
        },
        "inventory-file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/shelftracker/debug-inventory.log",
        },
        "invoices-file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/shelftracker/debug-invoices.log",
        },
        "partcatalog-file": {
            "class": "logging.FileHandler",
            "filename": "/var/log/shelftracker/debug-partcatalog.log",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "distributors": {
            "level": "DEBUG",
            "handlers": ["file", 'distributors-file'],
            "propagate": False,
        },
        "partcatalog": {
            "level": "DEBUG",
            "handlers": ["file", 'partcatalog-file'],
            "propagate": False,
        },
        "inventory": {
            "level": "DEBUG",
            "handlers": ["file", "inventory-file"],
            "propagate": False,
        },
        "invoices": {
            "level": "DEBUG",
            "handlers": ["file", "invoices-file"],
            "propagate": False,
        },
    },
}


CORS_ALLOW_ALL_ORIGINS = True

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

MEDIA_ROOT = '/var/media'
MEDIA_URL = '/media/'

DISTRIBUTORS_CREDENTIALS_FILE = '/etc/partmanager/distributors.json'

PARTSDB_CONFIG = {
    "directory": "/var/partsdb/",
    "repositories": {
        "partsdb-official": {
            "url": "https://github.com/partmanager/partsdb.git",
            "branch": "main"
        }
    }
}


