#!/bin/sh
set -e

rm celerybeat.pid;
cd /app \
    && ./manage.py migrate --noinput \
    && ./manage.py collectstatic --noinput \
    && ./manage.py runserver 0:8000
