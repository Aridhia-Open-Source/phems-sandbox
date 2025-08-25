# Notes

## Infrastructure

### Postgres
- Stores Dagster's metadata (runs, schedules, sensors, assets, logs).
- Celery result backend (so workers can record task results).

### MinIO
- S3-compatible object storage.
- Used by Dagster to persist intermediate values, run artifacts, or asset materializations (instead of local disk).

### RabbitMQ

- Message broker for Celery.
- Dagster submits tasks here, workers consume them from the queue.

### Services

### Daemon
- Runs background processes such as sensors, schedules and jobs
- Submits jobs and workflows to the Celery queue via RabbitMQ.

### webserver
- rich web ui
- dagster api

### Workers

#### Run worker

The run worker is still responsible for traversing the execution plan.

#### Step Worker
The step worker is responsible for executing a single step, writing the structured events to the database.
The Celery worker polls for the step worker completion.