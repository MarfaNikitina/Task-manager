
install:
	poetry install

lint:
	poetry run flake8 .

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage xml

migrate:
	poetry run python manage.py migrate

setup:
	cp -n .env.example .env || true
	make install
	make migrate

start:
	poetry run python manage.py runserver 7778

check:
	poetry check

test:
	poetry run python manage.py test
