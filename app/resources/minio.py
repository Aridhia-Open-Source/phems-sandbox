import os

from dagster_aws.s3 import S3PickleIOManager, S3Resource


MINIO_RESOURCE = S3Resource(
    endpoint_url=os.environ['DAGSTER_MINIO_ENDPOINT'],
    aws_access_key_id=os.environ['DAGSTER_MINIO_ACCESS_KEY'],
    aws_secret_access_key=os.environ['DAGSTER_MINIO_SECRET_KEY'],
    region_name='us-east-1',
    verify=False,
)

MINIO_MANAGER = S3PickleIOManager(
    s3_resource=MINIO_RESOURCE,
    s3_bucket=os.environ['DAGSTER_MINIO_BUCKET'],
    s3_prefix=os.environ['DAGSTER_MINIO_IO_PREFIX'],
)
