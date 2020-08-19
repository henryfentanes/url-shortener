#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py migrate
gunicorn url-shortener.wsgi -w 2 -b 0.0.0.0:8000 --timeout 900 --chdir=/app --log-level debug --log-file -