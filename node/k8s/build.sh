#!/usr/bin/env bash

set -e

IMAGE_NAME="phems-dagster"

# kubernetes not picking up changes with the same tag
# so we get the latest tag and increments by 1, i.e v1 -> v2 (default to v1)
TAG_VERSION=$(docker images $IMAGE_NAME --format '{{.Tag}}' \
  | grep '^v' \
  | sort -V \
  | tail -n 1 \
  | sed 's/^v//' \
  | awk '{print "v" $1+1}'
); TAG_VERSION=${TAG_VERSION:-v1}

# build and tag the docker image
echo "Building image: $IMAGE_NAME:$TAG_VERSION"
docker build -t $IMAGE_NAME:$TAG_VERSION .
docker image tag $IMAGE_NAME:$TAG_VERSION $IMAGE_NAME:latest

# export the image into microk8s
echo "Exporting image: $IMAGE_NAME:$TAG_VERSION"
docker save $IMAGE_NAME:$TAG_VERSION | microk8s ctr image import -

# update the k8s yaml files with the new tag version
find k8s/base \
  -type f \
  -exec sed \
  -i -E "s|($IMAGE_NAME:)[^ ]+|\1$TAG_VERSION|g" {} +
