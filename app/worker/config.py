from kombu import Queue

broker_url = 'pyamqp://rabbit:rabbit@rabbitmq:5672/dagster'
result_backend = 'db+postgresql://postgres_user:postgres_password@postgres/postgres_db'

task_queues = [
    Queue(
        name='dagster',
        queue_type='classic',
        passive=True,
        durable=True,
        max_priority=10,
    ),
]

task_create_missing_queues = False
# task_default_queue = 'dagster'
# task_default_exchange = 'dagster'
# task_default_routing_key = 'dagster'
