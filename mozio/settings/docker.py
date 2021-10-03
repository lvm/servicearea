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
