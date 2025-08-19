import os

import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor
from dagster_aws.s3 import s3_pickle_io_manager

from app import assets


class Executor:
    celery_k8s = celery_k8s_job_executor.configured({
        "broker": os.environ['DAGSTER_CELERY_BROKER_URL'],
        "backend": os.environ['DAGSTER_CELERY_BACKEND_URL'],
    })


# throws error...
# dagster._core.errors.DagsterInvariantViolationError:
# Resource with key 's3' required by resource with key 'io_manager', but not provided.
class IOManager:
    s3 = s3_pickle_io_manager.configured({
        "s3_bucket": os.environ['DAGSTER_MINIO_BUCKET'],
        "s3_prefix": os.environ['DAGSTER_MINIO_IO_PREFIX'],
        "s3_endpoint_url": os.environ['DAGSTER_MINIO_ENDPOINT'],
        "s3_access_key": os.environ['DAGSTER_MINIO_ACCESS_KEY'],
        "s3_secret_key": os.environ['DAGSTER_MINIO_SECRET_KEY'],
        "s3_secure": False,
    })


# Pull the asset into a job manually
@dg.job(executor_def=Executor.celery_k8s)
def processed_data_job():
    assets.processed_data_1()
    assets.processed_data_2()
    assets.processed_data_3()


defs = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    jobs=[processed_data_job],
    resources={
        "io_manager": IOManager.s3
    }
)
