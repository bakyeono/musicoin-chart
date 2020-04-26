#!/bin/bash
source venv.sh
workon musicow
uwsgi --ini uwsgi.ini
deactivate
