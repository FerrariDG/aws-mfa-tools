PACKAGE=mfa_tools

all: static-tests

.PHONY: all

style:
		###### Running style analysis ######
		pipenv run flake8 $(PACKAGE)

typecheck:
		###### Running static type analysis ######
		pipenv run mypy $(PACKAGE)

doccheck:
		###### Running documentation analysis ######
		pipenv run pydocstyle -v $(PACKAGE)

static-tests: style typecheck doccheck

publish:
		###### Publish package to Pypi server ######
		pipenv run python setup.py sdist bdist_wheel
		pipenv run twine upload --non-interactive -u ${PYPI_USER} -p ${PYPI_PASS} --repository-url ${PYPI_URL} dist/*
