run:
	poetry run python resume-metadata-enricher
up: build
	docker compose up --force-recreate --rm
push: build
	docker compose push
build: export
	docker compose build
export:
	poetry export -f requirements.txt --output requirements.txt
