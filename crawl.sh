#!/bin/sh
workon musicoin
python manage.py crawl
deactivate
