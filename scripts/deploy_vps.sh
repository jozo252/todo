#!/usr/bin/env bash
set -e
git pull origin main
. .venv/bin/activate || python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
systemctl --user restart flask-app || true
echo "Deployed."
