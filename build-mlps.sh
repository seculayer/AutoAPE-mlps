#!/bin/bash

VERSION="3.0.0"

REGISTRY_URL="registry.seculayer.com:31500"

# docker build
DOCKER_BUILDKIT=1 docker build -t $REGISTRY_URL/ape/automl-mlps:$VERSION .
docker push $REGISTRY_URL/ape/automl-mlps:$VERSION
