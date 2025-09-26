#!/usr/bin/env bash
set -e
. .venv/bin/activate
exec gunicorn -c gunicorn.conf.py wsgi:app
