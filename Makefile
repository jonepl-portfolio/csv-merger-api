ifndef DOCKER_USERNAME
  ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
  endif

  ifndef DOCKER_USERNAME
    $(error DOCKER_USERNAME is not set. Please set it in the environment or in the .env file)
  endif
endif

docker-image:
	docker build -t $(DOCKER_USERNAME)/csv-merger:latest .
	docker image prune -f

start-container:
	docker-compose up -d

destroy-container:
	docker-compose down

start:
	python ./app/api.py
	# flask --app app/api.py run -p 8080

ignore-skip-test:
	export IGNORE_SKIP=True

run-skip-test:
	pytest -k "skip" && unset IGNORE_SKIP

test: 
	python -m pytest -s --cov --cov-fail-under=90 --cov-report=html
	# venv/bin/flask run --no-debugger