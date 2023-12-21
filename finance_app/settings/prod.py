import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['finance-app2-7c8c5a43727c.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config()
}
