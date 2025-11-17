#!/usr/bin/env bash

# kill any existing port-forward processes
pkill -f "kubectl port-forward"

set -e

echo "forwarding kubernetes ports..."

# MLFlow Bitnami image unavailable (discontinued)
# kubectl port-forward -n node svc/mlflow 5000 & \
kubectl scale deployment mlflow -n node --replicas=0 & \
kubectl port-forward -n node svc/dagit 3000 & \
kubectl port-forward -n node svc/flower 5555 & \
kubectl port-forward -n node svc/codeserver 4000 & \
kubectl port-forward -n node svc/postgres 5432 & \
kubectl port-forward -n node svc/rabbitmq 5672 & \
kubectl port-forward -n node svc/rabbitmq 15672 & \
kubectl port-forward -n node svc/minio 9000 & \
kubectl port-forward -n node svc/pgadmin 3001:80
