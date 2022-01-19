IMAGE_NAME=health_app
IMAGE_TAG=v1
FULL_IMAGE_NAME=${IMAGE_NAME}:${IMAGE_TAG}
FULL_IMAGE_NAME_TEST=${IMAGE_NAME}:test

.PHONY: build,test

build: docker-compose.yaml
	docker-compose up --build

test: ./tests
	docker build --target test . -t ${FULL_IMAGE_NAME_TEST}
	docker run --env-file ./.env ${FULL_IMAGE_NAME_TEST}