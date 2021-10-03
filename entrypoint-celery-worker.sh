#!/bin/sh

celery worker --loglevel=info --app=mozio -Q mozio
