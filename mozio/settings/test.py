# pylint: skip-file
import os
from .common import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "hello")
DEBUG = True
ENV_NAME = "Docker"
MEDIA_ROOT = "/tmp/mozio-api-media"
STATIC_ROOT = "/tmp/mozio-api"

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


# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework_gis.schema.GeoFeatureAutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
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
