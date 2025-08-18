#!/usr/bin/env bash

set -e
MODE=${1:-apply}
export NAMESPACE='dagster'
alias kubectl="microk8s kubectl -n ${NAMESPACE}"

# apply namespace
kubectl $MODE -f k8s/base/namespace.yaml
# apply configmaps
kubectl $MODE -f k8s/base/configmaps
# apply secrets
kubectl $MODE -f k8s/base/secrets
# apply persistent volumes
kubectl $MODE -f k8s/base/volumes
# apply deployment deployments
kubectl $MODE -f k8s/base/deployments
# apply deployment services
kubectl $MODE -f k8s/base/services
# apply ingresses
kubectl $MODE -f k8s/base/ingress
