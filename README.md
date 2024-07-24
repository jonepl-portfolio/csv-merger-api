# CSV Merger API

## Design
<p align="center">
 <img src="./docs/CSV-Merger-API.png" style="display: block; margin: 0 auto">
</p>

<br/>

This Dockerized Python application is used for merging CSVs files into a single document. It utilizes an Nginx web server and gunicorn to send & receive API requests. The docker-compose file is meant to be used within a docker-swarm instance.

## Usage

### Start application locally
```bash
# Create a virtual environment
$ make venv

# Activate virtual environment
$ make venv-activate

# Start application
$ make start

# Deactivate virtual environment
$ make venv-deactivate
```

### Start application via Docker
```bash
# Ensure your .env file is populated with DOCKER_USERNAME the create your docker image 
$ make docker-image

# Run you docker container
$ start-container
```

### Running tests
```bash
# Runs all tests
$ make test
```

# Making Code Changes

* Make sure to update the VERSION before merging