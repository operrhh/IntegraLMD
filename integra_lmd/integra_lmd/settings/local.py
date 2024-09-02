from .base import *
from decouple import config
from cx_Oracle import makedsn

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

OCI_DSN = makedsn(OCI_HOST, OCI_PORT, service_name=OCI_SERVICE_NAME)
PEOPLE_DSN = makedsn(PEOPLE_HOST, PEOPLE_PORT, service_name=PEOPLE_SERVICE_NAME)

DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': OCI_DSN,
        'USER': OCI_USER,
        'PASSWORD': OCI_PASSWORD,
    },
    'peoplesoft': {
        'ENGINE': ENGINE,
        'NAME': PEOPLE_DSN,
        'USER': PEOPLE_USER,
        'PASSWORD': PEOPLE_PASSWORD,
    }
}

STATIC_URL = 'static/'
