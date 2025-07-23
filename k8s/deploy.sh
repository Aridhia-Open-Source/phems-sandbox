#!/usr/bin/env bash
set -e

# setup microk8s and kubectl
echo "Setting up microk8s"
alias kubectl='microk8s kubectl'
microk8s enable dns
microk8s enable storage
microk8s enable ingress
echo "----------------------------------"

# build and import docker image
echo "Building and importing Docker image..."
docker build -t phems-dagster .
# docker save phems-dagster > phems-dagster.tar
# microk8s ctr image import phems-dagster.tar
echo "----------------------------------"


# initialize kubernetes deployment
echo "Initializing Kubernetes deployment..."
## create namespace
kubectl apply -f k8s/base/namespace.yaml
## apply configmaps and secrets
kubectl apply -f k8s/base/configmaps/
kubectl apply -f k8s/base/secrets/
## apply persistent volumes
kubectl apply -f k8s/base/volumes
## deploy infrastructure components:
kubectl apply -f k8s/base/deployments/postgres-deployment.yaml
kubectl apply -f k8s/base/deployments/rabbitmq-deployment.yaml
kubectl apply -f k8s/base/deployments/minio-deployment.yaml
## deploy dagster components:
kubectl apply -f k8s/base/deployments/dagit-deployment.yaml
kubectl apply -f k8s/base/deployments/daemon-deployment.yaml
kubectl apply -f k8s/base/deployments/codeserver-deployment.yaml
kubectl apply -f k8s/base/deployments/flower-deployment.yaml
## apply services
kubectl apply -f k8s/base/services/
## apply ingresses
# kubectl apply -f k8s/base/ingress/
echo "----------------------------------"

# # verify kubernetes deployment
# echo "Verifying Kubernetes deployment..."
# ## verify pods
# kubectl get pods -n dagster
# ## verify services
# kubectl get services -n dagster
# ## verify ingress
# kubectl get ingress -n dagster
# ## port-forward to access dagit
# kubectl port-forward svc/dagit 3000:3000 -n dagster