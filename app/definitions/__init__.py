import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor

from app.definitions import examples
from app.resources import MINIO_MANAGER


defs = dg.Definitions(
    assets=dg.load_assets_from_modules([examples]),
    executor=celery_k8s_job_executor,
    resources={"s3": MINIO_MANAGER},
    jobs=[examples.example_job],
)
