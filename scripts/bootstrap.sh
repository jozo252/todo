#!/usr/bin/env bash      initialize the installation !!!!!!!!!!
set -e
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cp -n .env.example .env || true
pre-commit install || true
FLASK_APP=wsgi.py flask db init || true
FLASK_APP=wsgi.py flask db migrate -m "init" || true
FLASK_APP=wsgi.py flask db upgrade
echo "Bootstrap done."


