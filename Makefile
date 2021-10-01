SHELL=/bin/bash

create-environment:
	virtualenv -p python3.8 .venv
	pip install -r requirements.txt

format-code:
	black .

recreate-db:
	rm -fr db.sqlite
	.venv/bin/activate
	python get_categories_and_cities.py
	deactivate