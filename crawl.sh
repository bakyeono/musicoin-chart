#!/bin/bash
source venv.sh
workon musicoin
python manage.py crawl
deactivate
