## Git Repos and ArgoCD
- Node and code repositories define both pipelines and execution code.
- ArgoCD continuously syncs changes into the FN environment.

## Dagster K8s
- **CodeServer**: serves the node's Dagster definitions.
- **Daemon**: runs sensors and schedules.
- **Webserver**: exposes Dagster UI and GraphQL API.
- **Workers (Pods)**: execute ML ops and tasks.

## Dagster Resources
- **Postgres**: stores run metadata, execution logs, schedules, and states.
- **RabbitMQ**: queues Celery tasks.
- **Minio**: persists artifacts and results.

## Storage integration
- Artifacts in Minio feed into abstract persistent storage, ensuring portability across nodes.