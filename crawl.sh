#!/bin/bash
WORK_PATH=/home/bakyeono/musicoin
cd $WORK_PATH
source venv.sh
workon musicoin
python manage.py crawl
deactivate
