init-docker-env:
	cp docker-compose.override.yml.dist docker-compose.override.yml

code-quality:
	yapf -i -r -p ./**/*.py
	pylama

test:
	coverage run --source=. -m pytest
