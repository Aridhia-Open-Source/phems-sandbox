import dagster as dg

from app.definitions.examples import example_job


example_complex_asset_job = dg.define_asset_job(
    name="example_complex_asset_job",
    selection=dg.AssetSelection.keys("example_complex_asset").upstream(),
)

asset_jobs = [
    example_complex_asset_job,
    example_job
]
