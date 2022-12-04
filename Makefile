VERSION ?= $(shell cat VERSION)
APP=sample

.PHONY: help setup  setupdev unittest clean
.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: venv/touchfile ## install dependencies

venv/touchfile: requirements.txt ## install a virtual env and app requirements
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile

setupdev: venv/touchfile.dev ## install dev dependencies

venv/touchfile.dev: requirements-dev.txt ## install dev dependencies
	. venv/bin/activate; pip install -Ur requirements-dev.txt
	touch venv/touchfile.dev

tests:  ## run all component tests
	@start=$$(date +%s); \
    echo $@ start: $$start > test.log 	
	- make lint; echo "lint:" [$$?] $$(date +%s) >> test.log
	- make unittest; echo "unittest:" [$$?] $$(date +%s) >> test.log
	- make coverage; echo "coverage:" [$$?] $$(date +%s)  >> test.log
	- make demo
	@end=$$(date +%s); \
    echo $@ stop: $$end >> test.log
	cat test.log

docs: setupdev ## create/update documentation
	@echo "==== $@ ===="
	. venv/bin/activate; export PYTHONPATH='./polly'; python -m pdoc polly -o docs/generated

unittest: setup setupdev ## run unitest
	@echo "==== $@ ===="
	. venv/bin/activate; cd polly; python -m pytest -rA ..
	
demo: setup ## run demo from source
	python3 main.py


build: setup Dockerfile ## build docker image
	docker build -t polly .

run: build ## run dockerize image (read from stdin)
	docker run -i polly

package: setup ## create a python package under dist folder
	. venv/bin/activate; python setup.py sdist

tar: setup ## create a tar package (needs GIT repo)
	git archive --format=tar.gz -o polly.tar.gz HEAD -v 

clean:
	# clean up
	rm -rf venv

