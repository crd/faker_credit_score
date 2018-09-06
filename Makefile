help:
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make setup       create virtual environment and install dependencies"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

setup:
	pip install pipenv
	pipenv install --dev --three

activate:
	pipenv shell

test:
	pipenv run coverage run -m unittest tests/*

coverage:
	pipenv run coveralls

.PHONY: help activate test
