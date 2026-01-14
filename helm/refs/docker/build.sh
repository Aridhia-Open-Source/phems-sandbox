#! /usr/bin/env bash

set -e

TARGET_DIR=$1
IMAGE_TAG="v1"
IMAGE_NAME="dagster-pipes-$TARGET_DIR"

cd "docker/$TARGET_DIR"
echo $PWD
# build and tag the docker image
echo "Building image: $IMAGE_NAME:$IMAGE_TAG"
docker build -t $IMAGE_NAME:$IMAGE_TAG .
docker image tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest

# export the image into microk8s
echo "Exporting image: $IMAGE_NAME:$IMAGE_TAG"
docker save $IMAGE_NAME:$IMAGE_TAG | microk8s ctr image import -
