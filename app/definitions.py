import os

import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor
from dagster_aws.s3 import S3PickleIOManager, S3Resource
from app.assets import examples


minio_manager = S3PickleIOManager(
    s3_resource=S3Resource(
        endpoint_url=os.environ['DAGSTER_MINIO_ENDPOINT'],
        aws_access_key_id=os.environ['DAGSTER_MINIO_ACCESS_KEY'],
        aws_secret_access_key=os.environ['DAGSTER_MINIO_SECRET_KEY'],
        region_name='us-east-1',
        verify=False,
    ),
    s3_bucket=os.environ['DAGSTER_MINIO_BUCKET'],
    s3_prefix=os.environ['DAGSTER_MINIO_IO_PREFIX'],
)


@dg.job
def example_job():
    examples.example_1()
    examples.example_2()
    examples.example_3()


defs = dg.Definitions(
    assets=dg.load_assets_from_modules([examples]),
    executor=celery_k8s_job_executor,
    resources={"s3": minio_manager},
    jobs=[example_job],

)
