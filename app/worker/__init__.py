from celery import Celery

from dagster_celery.tasks import create_task

app = Celery('dagster-celery')
app.config_from_object('app.worker.config')
execute_plan = create_task(app)


if __name__ == '__main__':
    app.worker_main()


__all__ = (
    'app',
)
