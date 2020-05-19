#include .env
#ifndef TAG
#$(error The TAG variable is missing.)
#endif

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

docker-build:
	docker-compose build

# This will wipe all your stopped containers - Use at your own peril
#docker-clean:
#	@docker system prune --volumes --force

docker-run:
	docker-compose up

k8s-run:
	@make -s docker-build
	kubectl apply -f tests/kubernetes/
	kubectl wait --for=condition=complete job/imagechecker --timeout=60s -n imagechecker-dev
	kubectl logs job/imagechecker -n imagechecker-dev

