import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor

from app.definitions import examples, jobs
from app.resources.minio import MinioManager


minio = MinioManager().setup()

defs = dg.Definitions(
    jobs=jobs.asset_jobs,
    assets=dg.load_assets_from_modules([examples]),
    executor=celery_k8s_job_executor,
    resources={"io_manager": minio.io_manager},
)
