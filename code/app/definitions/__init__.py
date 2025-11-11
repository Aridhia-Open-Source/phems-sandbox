import dagster as dg
from dagster_k8s import PipesK8sClient
from dagster_celery_k8s import celery_k8s_job_executor

from app.definitions import jobs, pipes, examples
from app.resources.minio import MinioManager

minio = MinioManager().setup()

defs = dg.Definitions(
    jobs=jobs.asset_jobs,
    assets=dg.load_assets_from_modules([pipes, examples]),
    executor=celery_k8s_job_executor,
    resources={
        "io_manager": minio.io_manager,
        "k8s_pipes_client": PipesK8sClient(poll_interval=5.0),
    },
)
