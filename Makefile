
PROJECT_NAME=unitexpr

.PHONY: clean
clean:

			rm -rf .pytest_cache
			rm -rf src/$(PROJECT_NAME)/__pycache__
			rm -rf dist/*
			rm -rf src/*.egg-info
			rm -rf site

build:
			pip install --upgrade build
			python3 -m build

compile:
			python src/$(PROJECT_NAME)/setup.py build_ext --inplace


site:
			portray as_html

init:
			if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
			if [ -f requirements_dev.txt ]; then pip install -r requirements_dev.txt; fi
			pip install -e .

lint:
			pylint -f colorized src/$(PROJECT_NAME)

publish-test:
			pip install --upgrade twine
			python3 -m twine upload --repository testpypi dist/*

publish:
			pip install --upgrade twine
			python3 -m twine upload --repository pypi dist/*

test:
		  pytest -rP tests
