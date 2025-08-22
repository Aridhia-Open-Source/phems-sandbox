#!/usr/bin/env bash

set -e

IMAGE_NAME="phems-dagster"

# kubernetes not picking up changes with the same tag
# so we get the latest tag and increments by 1, i.e v1 -> v2 (default to v1)
export TAG_VERSION=$(docker images $IMAGE_NAME --format '{{.Tag}}' \
  | grep '^v' \
  | sort -V \
  | tail -n 1 \
  | sed 's/^v//' \
  | awk '{print "v" $1+1}'
)
export TAG_VERSION=${TAG_VERSION:-v1}

echo "Building image $IMAGE_NAME:$TAG_VERSION"
docker build -t $IMAGE_NAME:$TAG_VERSION .
docker image tag $IMAGE_NAME:$TAG_VERSION $IMAGE_NAME:latest
docker save $IMAGE_NAME:$TAG_VERSION | microk8s ctr image import -