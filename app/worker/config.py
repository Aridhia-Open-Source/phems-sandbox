import os

from kombu import Queue

broker_url = f"py{os.environ['DAGSTER_CELERY_BROKER_URL']}"
result_backend = os.environ['DAGSTER_CELERY_BACKEND_URL']

task_queues = [
    Queue(
        name='dagster',
        queue_type='classic',
        passive=True,
        durable=True,
        max_priority=10,
    ),
]
