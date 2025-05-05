from .base import *
from decouple import config
from oracledb import makedsn

DEBUG = False

ALLOWED_HOSTS = ['integralmd.ccu.cl','192.168.0.107','0.0.0.0','127.0.0.1','localhost','web', '168.138.71.27', '129.151.110.152','10.85.4.72']

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

# Uso de las variables de entorno en settings.py
AWS_ACCESS_KEY_ID = config('BK_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('BK_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('BK_AWS_BUCKET_NAME')

STATIC_URL = 'static/'
