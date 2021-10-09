SHELL=/bin/bash
.ONESHELL:

create-environment:
	virtualenv .venv
	source .venv/bin/activate
	pip install -r requirements-local.txt

format-code:
	black .

recreate-db:
	source .venv/bin/activate
	rm -fr db/db.sqlite
	cd models
	python models.py
	deactivate

build-image:
	docker build --pull --rm -t pasion-bot "."

run-bot:
	docker run --rm -it --entrypoint "/bin/bash" -v $(path_db)/db:/app/db pasion-bot -c "python get_categories_and_cities.py"
	docker run --rm -it --entrypoint "/bin/bash" -v $(path_db)/db:/app/db pasion-bot -c "python get_ads_id.py"

build-and-run:
	make recreate-db
	make build-image
	make run-bot path_db=$(path_db)

delete-all-images:
	docker rmi -f $(docker images -a -q)