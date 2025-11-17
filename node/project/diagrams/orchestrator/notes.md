
# Diagram 3: Federated Orchestrator

This design establishes a hub-and-spoke model where Dagster at the orchestrator level coordinates distributed
training to federated nodes and MLflow manages global model lifecycle.

## Orchestrator Git Repos and ArgoCD
- Define orchestrator-level pipelines and code.
- Synced into the orchestrator's CodeServer by ArgoCD.

## Dagster Orchestrator
- **CodeServer**: serves orchestrator and federated definitions.
- **Daemon**: runs orchestrator schedules and sensors.
- **Webserver**: provides UI and GraphQL API.
- **Workers (Pods)**: execute orchestration and federated coordination tasks.

## Orchestrator and Federated Learning Resources
- **Postgres**: stores run metadata, execution history, schedules, and sensor state.
- **RabbitMQ**: message broker for Celery; queues orchestration tasks submitted by the daemon and distributes them to worker pods.
- **Minio**: stores pipeline artifacts, intermediates, and results produced by workers.

## MLflow Integration
- **Tracking Server**: aggregates metrics and logs from federated nodes.
- **Model Registry**: stores global models, publishes them to consumers, and redistributes updates to nodes.

## Federated workflow
- Federated Nodes contribute model updates and logs to the orchestrator.
- Orchestrator aggregates results, manages lineage, and publishes updated global models back to the nodes and external consumers.
