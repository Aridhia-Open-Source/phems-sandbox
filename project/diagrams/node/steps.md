## Initial asset definition
- Researcher raises a PR with a new asset definition.
- Once merged, ArgoCD syncs the change to the CodeServer, which updates Dagster’s available definitions.

## Launching a run
- Researcher raises a PR with run parameters.
- After merge, ArgoCD notifies Dagster to launch the run.

## Run execution
- Dagster creates a Kubernetes worker job.
- Steps are queued in Celery via RabbitMQ.
- Worker pods consume tasks, execute ops, and persist results in Postgres and MinIO.
- Dagster handles post-run events.

## Publication approval
- Dagster notifies the Data Controller of pending publication.
- After approval, the Publication Sensor triggers a publication job.
- Dagster publishes the asset to external storage and the Researcher is notified.