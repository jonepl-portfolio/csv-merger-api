docker-image:
	docker build -t $(DOCKER_USERNAME)/csv-merger:latest .
	docker image prune -f

start-container:
	docker-compose up -d

destroy-container:
	docker-compose down

start:
	venv/bin/flask run --no-debugger

ignore-skip-test:
	export IGNORE_SKIP=True

run-skip-test:
	pytest -k "skip" && unset IGNORE_SKIP

test: 
	python -m pytest -s --cov --cov-fail-under=90 --cov-report=html
	# venv/bin/flask run --no-debugger

lint:
	venv/bin/flake8 . --exclude venv --max-line-length 106

format:
	venv/bin/black .