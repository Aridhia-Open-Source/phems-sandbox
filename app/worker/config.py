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
