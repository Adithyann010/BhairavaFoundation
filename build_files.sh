#!/bin/bash
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py migrate --noinput
python3 populate_db.py
python3 manage.py collectstatic --noinput --clear
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/ 2>/dev/null || true
