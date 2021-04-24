.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT: help

SHELL := /bin/bash

# These variables can be passed from the command line when invoking make.
PREFIX		= /usr/local

GITHUB_USER = ReliaQualAssociates
TOKEN		= $(shell echo $(GITHUB_TOKEN))
REPO		= ramstk

SRCFILE		= src/ramstk/
TESTFILE	= tests/
TESTOPTS	= -x -c ./pyproject.toml --cache-clear
VIRTENV		= .venv
ROOT 		= $(shell git rev-parse --show-toplevel)
WORKBRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
COVDIR		= .reports/coverage/html

# Shell commands:
PYTHON		= $(shell which python)
PY			= $(shell which python -V | cut -d ' ' -f2)
COPY 		= cp -v
MKDIR 		= mkdir -pv
RM			= rm -fv
RMDIR		= rm -fvr
SED			= sed
GIT			= $(shell which git)

BLACK		= $(shell which black)
CHKMANI		= $(shell which check-manifest)
DOCFORMATTER	= $(shell which docformatter)
ISORT       = $(shell which isort)
MYPY		= $(shell which mypy)
POETRY		= $(shell which poetry)
PYCODESTYLE	= $(shell which pycodestyle)
PYDOCSTYLE	= $(shell which pydocstyle)
PYLINT		= $(shell which pylint)
PYROMA		= $(shell which pyroma)
RADON		= $(shell which radon)
RSTCHECK	= $(shell which rstcheck)
TWINE		= $(shell which twine)

# Data files.
LAYOUTS		= $(shell ls ./data/layouts)
ICONS16		= $(shell ls ./data/icons/16x16)
ICONS32		= $(shell ls ./data/icons/32x32)

# Argument lists for tools.
DOCFORMATTER_ARGS	= --in-place
ISORT_ARGS	= --settings-file ./pyproject.toml --atomic
MYPY_ARGS	= --config-file ./setup.cfg
PYCODESTYLE_ARGS	= --count --config=./setup.cfg
PYDOCSTYLE_ARGS	= --count --config=./setup.cfg
PYLINT_ARGS	= -j0 --rcfile=./pyproject.toml

help:
	@echo "You can use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "Targets related to managing RAMSTK dependencies:"
	@echo "	requirements				create/update the poetry.lock file."
	@echo "	depends					install the packages found in the poetry.lock file into the current (virtual) environment."
	@echo "	upgrade					update the poetry.lock file with the latest package versions available."
	@echo "Targets related to testing RAMSTK:"
	@echo "	test.unit				run all tests decorated with the 'unit' marker."
	@echo "	test.calc				run all tests decorated with the 'calculation' marker."
	@echo "	test.integration			run all tests decorated with the 'integration' marker."
	@echo "	test					run the complete RAMSTK test suite without coverage."
	@echo "	test-all				run the complete RAMSTK test suite on every Python version using tox. <FUTURE>"
	@echo "	coverage				run the complete RAMSTK test suite with coverage."
	@echo "Targets related to static code checking tools (good for IDE integration):"
	@echo "	format SRCFILE=<file>			format using black, isort, and docformatter.  Helpful to keymap in IDE or editor."
	@echo "	stylecheck SRCFILE=<file>		check using pycodestyle and pydocstyle.  Helpful to keymap in IDE or editor."
	@echo "	typecheck SRCFILE=<file>		check using mypy.  Helpful to keymap in IDE or editor."
	@echo "	lint SRCFILE=<file>			lint using pylint.  Helpful to keymap in IDE or editor."
	@echo "						If passing a directory, all files will be recusively checked."
	@echo "	maintain SRCFILE=<file>			check maintainability using mccabe and radon.  Helpful to keymap in IDE or editor."
	@echo "						Pass wildcard (*) at end of FILE=<file> path to analyze all files in directory."
	@echo "Targets related to documentation:"
	@echo "	docs					build API and user documentation."
	@echo "Other targets:"
	@echo "	clean					removes all build, test, coverage, and Python artifacts."
	@echo "	install 				install RAMSTK in the current (virtualenv) environment."
	@echo "	uninstall 				remove RAMSTK from the current (virtualenv) environment."
	@echo "	dist					build source and wheel packages."
	@echo "	release					package and upload a release to PyPi."
	@echo ""
	@echo "The following variables are recognized by this Makefile.  They can be changed in this file or passed on the command line."
	@echo ""
	@echo "	GITHUB_USER				set the name of the Github user.  Defaults to $(GITHUB_USER)"
	@echo "	TOKEN					set the Github API token to use.  Defaults to environment variable GITHUB_TOKEN"
	@echo "	REPO					set the name of the GitHub repository to generate the change log from.  Defaults to $(REPO)"
	@echo "	SRCFILE					set the file or directory to static code check.  Defaults to $(SRCFILE)"
	@echo "	TESTOPTS				set additional options to pass to py.test/pytest.  Defaults to $(TESTOPTS)"
	@echo "	TESTFILE				set the file or directory to test.  Defaults to $(TESTFILE)"
	@echo "	VIRTENV					set the name of the virtual environment to create/use.  Defaults to $(VIRTENV)."
	@echo "	COVDIR					set the output directory for the html coverage report.  Defaults to $(COVDIR)."

.PHONY: all test clean

# Targets for cleaning up after yourself.
clean: clean-build clean-docs clean-pyc clean-test		## removes all build, test, coverage, and Python artifacts

clean-build:	## remove build artifacts
	@echo -e "\n\t\033[1;37;43mCleaning up old build artifacts ...\033[0m\n"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(shell find . -name '*.egg-info' -exec rm -fr '{}' +)
	$(shell find . -name '*.egg' -exec rm -fr '{}' +)

clean-docs:
	cd docs; rm -fr _build/html/*

clean-pyc:		## remove Python file artifacts
	$(shell find . -name '*.pyc' -exec rm -f {} +)
	$(shell find . -name '*.pyo' -exec rm -f {} +)
	$(shell find . -name '*~' -exec rm -f {} +)
	$(shell find . -name '__pycache__' -exec rm -fr {} +)

clean-test:	clean-pyc	## remove test and coverage artifacts
	@echo -e "\n\t\033[1;37;43mCleaning up old test run artifacts ...\033[0m\n"
	rm -fr .tox/
	rm -fr .reports/coverage
	rm -fr .pytest_cache

# Targets for managing RAMSTK dependencies.
requirements:
	$(POETRY) lock

depends:
	pip install -U wheel
	$(POETRY) install --no-root

upgrade:
	pip install -U wheel
	$(POETRY) install --remove-untracked
	$(POETRY) update

# Targets to install and uninstall RAMSTK.
install: clean-build clean-pyc
	@echo -e "\n\t\033[1;37;42mInstalling RAMSTK to $(PREFIX) ...\033[0m\n"
	pip install . --prefix=$(PREFIX)
	${MKDIR} "$(PREFIX)/share/RAMSTK"
	${MKDIR} "$(PREFIX)/share/RAMSTK/layouts"
	${MKDIR} "$(PREFIX)/share/RAMSTK/icons/16x16"
	${MKDIR} "$(PREFIX)/share/RAMSTK/icons/32x32"
	${MKDIR} "$(PREFIX)/share/RAMSTK/logs"
	${MKDIR} "$(PREFIX)/share/doc/ramstk"
	${MKDIR} "$(PREFIX)/share/applications"
	${MKDIR} "$(PREFIX)/share/pixmaps"
	${COPY} "./data/RAMSTK.desktop" "$(PREFIX)/share/applications"
	${COPY} "./data/icons/RAMSTK.png" "$(PREFIX)/share/pixmaps"
	${COPY} "./README.md" "$(PREFIX)/share/doc/ramstk"
	for file in ${LAYOUTS} ; do \
		${COPY} "./data/layouts/$$file" "$(PREFIX)/share/RAMSTK/layouts/" ; \
	done
	for icon in ${ICONS16} ; do \
		${COPY} "./data/icons/16x16/$$icon" "$(PREFIX)/share/RAMSTK/icons/16x16/" ; \
	done
	for icon in ${ICONS32} ; do \
		${COPY} "./data/icons/32x32/$$icon" "$(PREFIX)/share/RAMSTK/icons/32x32/" ; \
	done
	${COPY} "./data/sqlite_common_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/postgres_common_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/sqlite_program_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/postgres_program_db.sql" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/Site.toml" "$(PREFIX)/share/RAMSTK/"
	${COPY} "./data/RAMSTK.toml" "$(PREFIX)/share/RAMSTK/"

uninstall:
	@echo -e "\n\t\033[1;31;47mUninstalling RAMSTK :( ...\033[0m\n"
	pip uninstall -y ramstk
	${RMDIR} "$(PREFIX)/share/RAMSTK/"
	${RM} "$(PREFIX)/share/pixmaps/RAMSTK.png"
	${RM} "$(PREFIX)/share/applications/RAMSTK.desktop"

# Targets for testing.
test.unit: clean-test
	@echo -e "\n\t\033[1;37;1:43mRunning RAMSTK unit tests without coverage ...\033[0m\n"
	py.test $(TESTOPTS) -m unit $(TESTFILE)

test.calc: clean-test
	py.test $(TESTOPTS) -m calculation $(TESTFILE)

test.integration: clean-test
	@echo -e "\n\t\033[1;37;1;43mRunning RAMSTK integration tests without coverage ...\033[0m\n"
	py.test $(TESTOPTS) -m integration $(TESTFILE)

test.gui: clean-test
	py.test $(TESTOPTS) -m gui $(TESTFILE)

test: clean-test
	@echo -e "\n\t\033[1;37;1;45mRunning RAMSTK test suite without coverage ...\033[0m\n"
	py.test $(TESTOPTS) $(TESTFILE)

test-all:
	$(info "TODO: Need to add tox support for this target to work.")

coverage: clean-test
	@echo -e "\n\t\033[1;37;42mRunning RAMSTK test suite with coverage ...\033[0m\n"
	py.test $(TESTOPTS) $(TESTFILE)

# This target is for use with IDE integration.
format:
	@echo -e "\n\t\033[1;32mAutoformatting $(SRCFILE) ...\033[0m\n"
	$(BLACK) $(BLACK_ARGS) $(SRCFILE)
	$(ISORT) $(ISORT_ARGS) $(SRCFILE)
	$(DOCFORMATTER) $(DOCFORMATTER_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
stylecheck:
	@echo -e "\n\t\033[1;32mStyle checking $(SRCFILE) ...\033[0m\n"
	$(PYCODESTYLE) $(PYCODESTYLE_ARGS) $(SRCFILE)
	$(PYDOCSTYLE) $(PYDOCSTYLE_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
typecheck:
	@echo -e "\n\t\033[1;32mType checking $(SRCFILE) ...\033[0m\n"
	$(MYPY) $(MYPY_ARGS) $(SRCFILE)

# This target is for use with IDE integration.
maintain:
	@echo -e "\n\t\033[1;32mChecking maintainability of $(SRCFILE) ...\033[0m\n"
	$(PY) -m mccabe -m 10 $(SRCFILE)
	$(RADON) mi -s $(SRCFILE)
	$(RADON) hal $(SRCFILE)
	$(RADON) cc -s $(SRCFILE)

# This target is for use with IDE integration.
security:
	$(info Security linting $(SRCFILE)...)
	bandit --ini .bandit -c .bandit.conf -b .bandit.baseline -r $(SRCFILE)

# This target is for use with IDE integration.
lint:
	@echo -e "\n\t\033[1;32mLinting $(SRCFILE) ...\033[0m\n"
	$(PYLINT) $(PYLINT_ARGS) $(SRCFILE)

dupcheck:
	$(info Checking for duplicate code ...)
	$(PYLINT) --disable=all --enable=duplicate-code src/ramstk

# Targets for managing RAMSTK documentation.
lintdocs:
	$(info Linting documentation ...)
	$(RSTCHECK) -r docs/api docs/user

apidocs:
	sphinx-apidoc -f -o docs/api src/ramstk

docs: clean-docs
	$(info Building documentation ...)
	cd docs; $(MAKE) html -e

# Targets for creating and publishing RAMSTK packages.
packchk:
	$(PYROMA) .

build: clean
	@echo -e "\n\t\033[33;47mCreating source distribution and wheel ...\033[0m\n"
	$(POETRY) build

release: packchk build
	@echo -e "\n\t\033[33;47mBuilding and uploading artifacts to PyPi ...\033[0m\n"
	$(POETRY) publish
