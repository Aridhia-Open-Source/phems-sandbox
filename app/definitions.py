from dagster import load_assets_from_modules, define_asset_job, Definitions
from app import assets

# Load asset(s)
all_assets = load_assets_from_modules([assets])

# Define a job that targets the asset
processed_data_job = define_asset_job(
    name="processed_data_job",
    selection=["processed_data"],
)

# Register both assets and job
defs = Definitions(
    assets=all_assets,
    jobs=[processed_data_job],
)
