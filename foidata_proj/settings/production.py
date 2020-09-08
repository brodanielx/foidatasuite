from decouple import config

from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    config('RS_DJANGO01'),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}