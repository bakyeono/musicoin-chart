#!/bin/bash
source venv.sh
workon musicoin
uwsgi --ini uwsgi.ini
deactivate
