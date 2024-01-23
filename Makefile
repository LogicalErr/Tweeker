.PHONY: compose_up activate_venv django_migrate run_django run_backend run_frontend compose_down run
SHELL = /bin/bash


compose_up:
	docker compose up -d

compose_down:
	docker compose down

activate_venv:
	python -m venv venv && . venv/bin/activate

install_requirements:
	pip install -r backend/requirements.txt

django_migrate:
	python backend/manage.py migrate

run_django:
	python backend/manage.py runserver

run_backend:
	make activate_venv && make install_requirements && make django_migrate && make run_django

run_frontend:
	cd frontend/ && npm i && npm run build && serve -s build

run:
	make -j2 run_backend run_frontend
