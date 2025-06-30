import dagster as dg
from dagster_celery import celery_executor

from app import assets

# Load asset(s)
all_assets = dg.load_assets_from_modules([assets])

# Define a job that targets the asset
processed_data_job = dg.define_asset_job(
    name="processed_data_job",
    selection=["processed_data"],
    executor_def=celery_executor
)

# Register both assets and job
defs = dg.Definitions(
    assets=all_assets,
    jobs=[processed_data_job],
)
