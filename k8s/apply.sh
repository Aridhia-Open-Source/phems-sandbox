#!/usr/bin/env bash

set -e
alias kubectl='microk8s kubectl'

# apply namespace
kubectl apply -f k8s/base/namespace.yaml
# apply configmaps
kubectl apply -f k8s/base/configmaps
# apply secrets
kubectl apply -f k8s/base/secrets
# apply persistent volumes
kubectl apply -f k8s/base/volumes
# apply deployment deployments
kubectl apply -f k8s/base/deployments
# apply deployment services
kubectl apply -f k8s/base/services
# apply ingresses
kubectl apply -f k8s/base/ingress

