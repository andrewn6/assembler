##########
# Building
##########

build-docker-prod:
	docker build .
build-docker-dev:
	docker build -f dev.Dockerfile .
build-docker-dev-lint:
	docker build -f dev.lint.Dockerfile .

############
# Formatting
############

format:
	black .

#########
# Linting
#########

lint-black:
	black --check --diff .
lint-pylint:
	pylint --errors-only PROJECT_NAME tests
lint-poetry:
	poetry check
lint-hadolint:
	hadolint Dockerfile
	hadolint dev.Dockerfile
	hadolint dev.lint.Dockerfile
lint-in-docker:
	docker build -f dev.lint.Dockerfile -t mattgleich/PROJECT_NAME:lint .
	docker run mattgleich/PROJECT_NAME:lint

#########
# Testing
#########

test-pytest:
	cd tests
	pytest -vv
	cd ..
test-in-docker:
	docker build -f dev.Dockerfile -t mattgleich/PROJECT_NAME:test .
	docker run mattgleich/PROJECT_NAME:test

##########
# Grouping
##########

# Testing
local-test: test-pytest
docker-test: test-in-docker
# Linting
local-lint: lint-black lint-pylint lint-hadolint
docker-lint: lint-in-docker
# Build
local-build: build-docker-prod build-docker-dev build-docker-dev-lint
