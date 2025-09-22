#!/usr/bin/env bash

set -e

echo "forwarding kubernetes ports..."
kubectl port-forward -n dagster svc/dagit 3000 & \
kubectl port-forward -n dagster svc/flower 5555 & \
kubectl port-forward -n dagster svc/codeserver 4000 & \
kubectl port-forward -n dagster svc/postgres 5432 & \
kubectl port-forward -n dagster svc/rabbitmq 5672 & \
kubectl port-forward -n dagster svc/rabbitmq 15672 & \
kubectl port-forward -n dagster svc/minio 9000 & \
kubectl port-forward -n dagster svc/mlflow 5000 & \
kubectl port-forward -n dagster svc/pgadmin 3001:80
