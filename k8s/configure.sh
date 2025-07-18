#!/usr/bin/env bash

# mount the configmap to the dagster instance
kubectl create configmap dagster-instance \
    --from-file=dagster.yaml=k8s/base/configmaps/dagster.yaml \
    --namespace=dagster \
    --dry-run=client -o yaml > k8s/base/configmaps/dagster-instance.yaml

