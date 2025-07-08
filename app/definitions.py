import dagster as dg
from dagster_celery.executor import celery_executor
from app import assets

# Configure Celery executor
celery_executor_configured = celery_executor.configured({
    "broker": "pyamqp://rabbit:rabbit@rabbitmq:5672/dagster",
    "backend": "db+postgresql://postgres_user:postgres_password@postgres/postgres_db",
    "include": ["app.definitions"]
})

# Load assets
all_assets = dg.load_assets_from_modules([assets])


# Pull the asset into a job manually
@dg.job(executor_def=celery_executor_configured)
def processed_data_job():
    assets.processed_data_1()
    assets.processed_data_2()
    assets.processed_data_3()


defs = dg.Definitions(
    assets=all_assets,
    jobs=[processed_data_job],
)
