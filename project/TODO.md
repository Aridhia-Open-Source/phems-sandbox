# TO DO

## POC
- Dagster Kubernetes Assets
    - Develop solution for executing non-python code in a k8s container through dagster pipes
    - small sidecar script on child container for parsing args and returning result
    - develop dagster asset decorator for managing container and handling params/results
    - develop dagster asset decorator for mlflow to handle params, metrics and model logging
    - persistant storage for artifact caching, might not be needed? (julia can just be pre-compiled I think)

- Federated Learning
    - Develop a dagster orchestrator asset for a federated machine learning model
    - Develop dagster node assets for federated machine learning model
    - Test dagster federated learning by spinning up three dummy nodes stacks and an orchestrator stack

- Tidy up project and document current working state

## MVP

- Architect/Integrate project structure (docs, structure, packaging, etc)
- Convert existing POC kubernetes manifests to helm charts
- Setup devlopment tools and create test scaffolding
- Create ArgoCD deployments for node and orchestrator
- Develop Dagster/ArgoCD git job submission
- Develop publication approval sensor for dagster (s3?)
- Develop docs and sdk for dagster-celery-mlflow-k8s
- Integrate existing API into POC
- Integrate existing authentication with dagster
- Integration and "real world" testing
