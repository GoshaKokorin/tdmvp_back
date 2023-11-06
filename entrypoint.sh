#!/bin/bash
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn tdmvp_back.wsgi:application --bind 0.0.0.0:8000