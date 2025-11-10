#!/usr/bin/env bash

set -e
export K8MODE=${1:-apply}
export BASEPATH='k8s/base'
export NAMESPACE='code'
alias kubectl="microk8s kubectl -n ${NAMESPACE}"

# apply roles
kubectl $K8MODE -f $BASEPATH/roles
# apply namespace
kubectl $K8MODE -f $BASEPATH/namespace.yaml
# apply configmaps
kubectl $K8MODE -f $BASEPATH/configmaps
# apply secrets
kubectl $K8MODE -f $BASEPATH/secrets
# apply persistent volumes
kubectl $K8MODE -f $BASEPATH/volumes
# apply deployment deployments
kubectl $K8MODE -f $BASEPATH/deployments
# apply deployment services
kubectl $K8MODE -f $BASEPATH/services
# apply ingresses
kubectl $K8MODE -f $BASEPATH/ingress
kubectl scale deployment mlflow --replicas=0
