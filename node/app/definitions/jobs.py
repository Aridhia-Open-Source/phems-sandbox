import dagster as dg
from app.definitions.examples import example_op_job, super_simple_asset_job

DEFAULT_QUEUE = "dagster"


example_complex_asset_job = dg.define_asset_job(
    name='example_complex_asset_job',
    selection=dg.AssetSelection.assets('example_complex_asset').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

hacknews_stories_asset_job = dg.define_asset_job(
    name='hacknews_stories_asset_job',
    selection=dg.AssetSelection.assets('hackernews_stories').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

wine_quality_asset_job = dg.define_asset_job(
    name='wine_quality_asset_job',
    selection=dg.AssetSelection.assets('wine_quality').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

hourly_wine_quality_asset_job = dg.define_asset_job(
    name='hourly_wine_quality_asset_job',
    selection=dg.AssetSelection.assets('wine_quality').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

julia_k8s_pipes_asset_job = dg.define_asset_job(
    name='julia_k8s_pipes_asset_job',
    selection=dg.AssetSelection.assets('julia_k8s_pipes_asset').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

example_logging_asset_job = dg.define_asset_job(
    name='example_logging_asset_job',
    selection=dg.AssetSelection.assets('example_logging_asset').upstream(),
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)

asset_jobs = [
    example_op_job,
    super_simple_asset_job,
    example_complex_asset_job,
    hacknews_stories_asset_job,
    wine_quality_asset_job,
    hourly_wine_quality_asset_job,
    julia_k8s_pipes_asset_job,
    example_logging_asset_job,
]
