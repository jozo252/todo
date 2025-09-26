PY=python
PIP=pip

init:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install -r requirements-dev.txt
	@echo "Created venv and installed deps."

run:
	FLASK_APP=wsgi.py FLASK_ENV=development flask run

migrate-init:
	FLASK_APP=wsgi.py flask db init

migrate:
	FLASK_APP=wsgi.py flask db migrate -m "auto"

upgrade:
	FLASK_APP=wsgi.py flask db upgrade

fmt:
	. .venv/bin/activate && black .
	. .venv/bin/activate && ruff --fix .

lint:
	. .venv/bin/activate && ruff .

test:
	. .venv/bin/activate && pytest -q

gunicorn:
	. .venv/bin/activate && gunicorn -c gunicorn.conf.py wsgi:app
