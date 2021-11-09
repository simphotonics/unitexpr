
PROJECT_NAME=unitexpr

.PHONY: clean
clean:

			rm -rf .pytest_cache
			rm -rf src/$(PROJECT_NAME)/__pycache__
			rm -rf dist/*
			rm -rf src/*.egg-info

build:
			pip install --upgrade build
			python3 -m build

compile:
			python src/$(PROJECT_NAME)/setup.py build_ext --inplace


site:
			cp -r README.md src
			cp -r CHANGELOG.md src
			portray as_html

init:
	    pip install -r requirements.txt
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
