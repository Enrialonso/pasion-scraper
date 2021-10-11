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
	# docker run --rm -it --entrypoint "/bin/bash" --name pasion-bot -v $(path_db):/app/db pasion-bot -c "python get_categories_and_cities.py"
	# docker run --rm -it --entrypoint "/bin/bash" --name pasion-bot -e COUNT_WORKERS=$(count_workers) -e TEST_SCRIPT=$(test_script) -v $(path_db):/app/db pasion-bot -c "python get_ads_id.py"
	docker run --rm -it --entrypoint "/bin/bash" --name pasion-bot -e COUNT_WORKERS=$(count_workers) -v $(path_db):/app/db pasion-bot -c "python get_ads_data.py"

build-and-run:
	# make recreate-db
	make build-image
	make run-bot path_db=$(path_db) count_workers=$(count_workers) test_script=$(test_script)

delete-all-images:
	docker rmi -f $(docker images -a -q)