import os

from kombu import Queue

broker_url = f"py{os.environ['DAGSTER_CELERY_BROKER_URL']}"
result_backend = os.environ['DAGSTER_CELERY_BACKEND_URL']
task_create_missing_queues = True
task_default_queue = "code"

task_queues = [
    Queue(
        name='code',
        durable=True,
        max_priority=10,
        # passive=True,
    ),
]
