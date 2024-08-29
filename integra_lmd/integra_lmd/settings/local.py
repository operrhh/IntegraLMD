import os
from .base import *
from decouple import config
from cx_Oracle import makedsn

# prueba SECURITY WARNING: don't run with debug turned on in production!
# Debug no puede ser True en produccion
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

ENGINE = 'django.db.backends.oracle'

# Leer variables de entorno
DEFAULT_HOST = config('DB_DEFAULT_HOST')
DEFAULT_PORT = config('DB_DEFAULT_PORT')
DEFAULT_SERVICE_NAME = config('DB_DEFAULT_NAME')
DEFAULT_USER = config('DB_DEFAULT_USER')
DEFAULT_PASSWORD = config('DB_DEFAULT_PASSWORD')

PEOPLE_HOST = config('DB_PEOPLE_SOFT_HOST')
PEOPLE_PORT = config('DB_PEOPLE_SOFT_PORT')
PEOPLE_SERVICE_NAME = config('DB_PEOPLE_SOFT_NAME')
PEOPLE_USER = config('DB_PEOPLE_SOFT_USER')
PEOPLE_PASSWORD = config('DB_PEOPLE_SOFT_PASSWORD')

OCI_DSN = makedsn(DEFAULT_HOST, DEFAULT_PORT, service_name=DEFAULT_SERVICE_NAME)
PEOPLE_DSN = makedsn(PEOPLE_HOST, PEOPLE_PORT, service_name=PEOPLE_SERVICE_NAME)


DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': OCI_DSN,
        'USER': DEFAULT_USER,
        'PASSWORD': DEFAULT_PASSWORD,
    },
   'peoplesoft': {
       'ENGINE': ENGINE,
       'NAME': PEOPLE_DSN,
       'USER': PEOPLE_USER,
       'PASSWORD': PEOPLE_PASSWORD,
   }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
