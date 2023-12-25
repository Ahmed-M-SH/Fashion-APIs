from .base import *

ALLOWED_HOSTS = ['127.0.0.1', 'ymall-ye.com', '*']


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'USER': 'nq7testdb_user',
    #     'NAME': 'nq7testdb',
    #     'HOST': 'dpg-cgsu938rddlfvban4fng-a.oregon-postgres.render.com',
    #     'PORT': '5432',
    #     'PASSWORD': 'vPukjyPmO68lGcpsDnYmi2IpAiKe62tr',
    #     'TEST': {
    #         'NAME': 'mytestdatabase',
    #     },
    # },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'USER': 'postgres',
    #     'NAME': 'QAEnvironment',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     'PASSWORD': '',
    #     'TEST': {
    #         'NAME': 'mytestdatabase',
    #     },
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':BASE_DIR / 'db.sqlite3',
    }
}

# Media Files

MEDIA_URL = 'media/'
MEDIAFILES_DIRS = [
    BASE_DIR / "../media",
]
MEDIA_ROOT = BASE_DIR / '../media'
