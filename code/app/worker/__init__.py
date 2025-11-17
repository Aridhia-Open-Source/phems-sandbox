from dagster_celery.tasks import create_task
from dagster_celery_k8s.app import app

app.config_from_object('app.worker.config')
execute_plan = create_task(app)

if __name__ == '__main__':
    app.worker_main()


__all__ = (
    'app',
)
