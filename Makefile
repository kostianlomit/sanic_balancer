# WARNING! Use TABS, not spaces for tabbing in Makefile!

# variables -------
PREFIX := user
APP_NAME := sanic_balancer
# !FIXME WE MUST NOT USE 'latest' AS VALID VERSION 'NUMBER'
APP_VERSION := latest
IMAGE_FOLDER := /var/tmp
DOCKER_FILE := Dockerfile
BUILD_PATH := ./
# variables end ---


.PHONY: container
container:
	@echo "Building $(APP_NAME):$(APP_VERSION) container…"
	@docker build -t $(APP_NAME):$(APP_VERSION) -f $(DOCKER_FILE) $(BUILD_PATH) && \
	echo "Done"
