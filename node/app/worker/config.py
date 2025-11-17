# import os

# from kombu import Queue

# broker_url = f"py{os.environ['DAGSTER_CELERY_BROKER_URL']}"
# result_backend = os.environ['DAGSTER_CELERY_BACKEND_URL']
# task_create_missing_queues = False
# task_default_queue = 'dagster'

# task_queues = [
#     Queue(
#         name='dagster',
#         durable=True,
#         max_priority=10,
#         passive=False,
#     ),
# ]

import os

from kombu import Queue

broker_url = f"py{os.environ['DAGSTER_CELERY_BROKER_URL']}"
result_backend = os.environ['DAGSTER_CELERY_BACKEND_URL']
task_create_missing_queues = False
task_queue_max_priority = 10
task_default_queue = 'dagster'

task_queues = [
    Queue(
        name='dagster',
        durable=True,
        max_priority=10,
        passive=False,
    ),
]
