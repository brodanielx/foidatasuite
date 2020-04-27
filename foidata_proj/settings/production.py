from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'ip-address', 'www.your-website.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}