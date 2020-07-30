code-quality:
	yapf -i -r -p ./**/*.py
	pylama

test:
	coverage run --source=. -m pytest
