#!/bin/bash
python manage.py makemigrations && python manage.py migrate && python manage.py makemigrations api && python manage.py migrate api
python3 manage.py runserver 0.0.0.0:8000
