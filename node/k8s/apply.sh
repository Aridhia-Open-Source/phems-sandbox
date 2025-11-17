#!/usr/bin/env bash
set -e

NAMESPACE="node"
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

# cleanup
# scale down mlflow if it exists (bitnami image no longer available)
k8s scale deployment mlflow --replicas=0 >/dev/null 2>&1 || true
