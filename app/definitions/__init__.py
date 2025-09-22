import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor

from app.definitions import jobs, schedules, examples, hackernews, wine_quality
from app.resources.minio import MinioManager

minio = MinioManager().setup()

defs = dg.Definitions(
    jobs=jobs.asset_jobs,
    schedules=schedules.asset_schedules,
    assets=dg.load_assets_from_modules([examples, hackernews, wine_quality]),
    executor=celery_k8s_job_executor,
    resources={"io_manager": minio.io_manager},
)
