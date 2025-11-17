#!/usr/bin/env bash
set -e

NAMESPACE="code"
BASEPATH="k8s/base"


k8s() {
  microk8s kubectl -n "$NAMESPACE" "$@"
}

# apply
microk8s kubectl apply -f "$BASEPATH/namespace.yaml" || true
k8s apply -f "$BASEPATH/roles"
k8s apply -f "$BASEPATH/configmaps"
k8s apply -f "$BASEPATH/secrets"
k8s apply -f "$BASEPATH/volumes"
k8s apply -f "$BASEPATH/deployments"
k8s apply -f "$BASEPATH/services"
