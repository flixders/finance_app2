from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-bo_)lsqe1rdr*tv+7f6+5^b@s3uv66c-#**+ouob^!(1*3c17c'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finance_app_11',
        'USER': 'postgres',
        'PASSWORD': 'new_password',
        'HOST': 'localhost',  # or your specific host
        'PORT': '',           # if using a non-default port
    }
}
