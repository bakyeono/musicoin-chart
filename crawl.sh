#!/bin/bash
WORK_PATH=/home/bakyeono/musicow
cd $WORK_PATH
source venv.sh
workon musicow
python manage.py crawl
deactivate
