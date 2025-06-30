from celery import Celery

from dagster_celery.tasks import create_task

app = Celery(
    'dagster',
    broker_url='pyamqp://guest@rabbitmq//',
    backend='db+postgresql://postgres_user:postgres_password@postgres/postgres_db',
    include=['app.definitions'],
    task_serializer='json',
)

execute_plan = create_task(app)

if __name__ == '__main__':
    app.worker_main()
