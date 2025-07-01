import dagster as dg
import dagster_celery

from app import assets

# Load asset(s)
all_assets = dg.load_assets_from_modules([assets])
executor_def = dagster_celery.celery_executor.configured({
    "broker": "pyamqp://rabbit:rabbit@rabbitmq:5672//",
    "backend": "db+postgresql://postgres_user:postgres_password@postgres/postgres_db",
})

# Define a job that targets the asset
processed_data_job = dg.define_asset_job(
    name="processed_data_job",
    selection=["processed_data"],
    executor_def=executor_def
)

# Register both assets and job
defs = dg.Definitions(
    assets=all_assets,
    jobs=[processed_data_job],
)
