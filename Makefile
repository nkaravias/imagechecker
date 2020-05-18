clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {} 

clean-build:
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

lint:
	flake8 --exclude=tests

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python imagechecker/main.py
