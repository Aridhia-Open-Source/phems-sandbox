#!/usr/bin/env bash

set -e
alias kubectl='microk8s kubectl -n dagster'

mode=${1:-apply}
# apply namespace
kubectl "$mode" -f k8s/base/namespace.yaml
# apply configmaps
kubectl "$mode" -f k8s/base/configmaps
# apply secrets
kubectl "$mode" -f k8s/base/secrets
# apply persistent volumes
kubectl "$mode" -f k8s/base/volumes
# apply deployment deployments
kubectl "$mode" -f k8s/base/deployments
# apply deployment services
kubectl "$mode" -f k8s/base/services
# apply ingresses
kubectl "$mode" -f k8s/base/ingress

