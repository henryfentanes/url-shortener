#!/bin/sh
export DEBUG=True
python manage.py migrate
python manage.py runserver
