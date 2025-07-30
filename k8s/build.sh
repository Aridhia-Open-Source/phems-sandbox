#!/usr/bin/env bash

# build docker image and import to microk8s
docker build -t phems-dagster .
docker save phems-dagster > phems-dagster.tar
microk8s ctr image import phems-dagster.tar
