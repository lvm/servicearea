# pylint: skip-file
import os
from .common import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "hello")
DEBUG = False
ENV_NAME = "Production"
MEDIA_ROOT = "/app/media/"
STATIC_ROOT = "/app/static/"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "moz_"
    }
}
