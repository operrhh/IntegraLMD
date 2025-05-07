from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = []

# Database
ENGINE = 'django.db.backends.oracle'

OCI_HOST = config('DB_DEFAULT_HOST')
OCI_PORT = config('DB_DEFAULT_PORT')
OCI_SERVICE_NAME = config('DB_DEFAULT_NAME')
OCI_USER = config('DB_DEFAULT_USER')
OCI_PASSWORD = config('DB_DEFAULT_PASSWORD')

PEOPLE_HOST = config('DB_PEOPLE_SOFT_HOST')
PEOPLE_PORT = config('DB_PEOPLE_SOFT_PORT')
PEOPLE_SERVICE_NAME = config('DB_PEOPLE_SOFT_NAME')
PEOPLE_USER = config('DB_PEOPLE_SOFT_USER')
PEOPLE_PASSWORD = config('DB_PEOPLE_SOFT_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },    
    'peoplesoft': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': PEOPLE_SERVICE_NAME,
        'USER': PEOPLE_USER,
        'PASSWORD': PEOPLE_PASSWORD,
        'HOST': PEOPLE_HOST,
        'PORT': PEOPLE_PORT
    }
}

AWS_ACCESS_KEY_ID = config('BK_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('BK_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('BK_AWS_BUCKET_NAME')

STATIC_URL = 'static/'