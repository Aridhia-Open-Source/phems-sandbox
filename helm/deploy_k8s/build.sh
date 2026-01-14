#!/usr/bin/env bash
set -e

IMAGE_TAG="v3"
IMAGE_NAME="iris-analytics"
DOCKER_REPO_URI="localhost:32000"

# Build the local Docker image
echo "Building image: $IMAGE_NAME:$IMAGE_TAG"
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Tag the image for the MicroK8s registry
echo "Tagging image -> $DOCKER_REPO_URI/$IMAGE_NAME:$IMAGE_TAG"
docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKER_REPO_URI/$IMAGE_NAME:$IMAGE_TAG

# Push into MicroK8s registry
echo "Pushing image -> $DOCKER_REPO_URI/$IMAGE_NAME:$IMAGE_TAG"
docker push $DOCKER_REPO_URI/$IMAGE_NAME:$IMAGE_TAG

# Verify image push
echo "Verifying image in MicroK8s registry..."
