#!/bin/sh
source venv.sh
workon musicoin
python manage.py crawl
deactivate
