import os

from dagster_aws.s3 import S3PickleIOManager, S3Resource


class MinioManager:
    def __init__(self):
        self.bucket_name = os.environ['DAGSTER_MINIO_BUCKET']
        self.prefix_path = os.environ['DAGSTER_MINIO_IO_PREFIX']
        self.access_key = os.environ['DAGSTER_MINIO_ACCESS_KEY']
        self.secret_key = os.environ['DAGSTER_MINIO_SECRET_KEY']
        self.endpoint_url = os.environ['DAGSTER_MINIO_ENDPOINT']
        self.region_name = os.environ.get('DAGSTER_MINIO_REGION', 'us-east-1')

        self.resource = S3Resource(
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
            verify=False,
        )

        self.io_manager = S3PickleIOManager(
            s3_resource=self.resource,
            s3_bucket=self.bucket_name,
            s3_prefix=self.prefix_path,
        )

    def setup(self):
        # hacky but it works for PoC
        self._create_bucket_if_not_exists(self.bucket_name)
        self._create_bucket_if_not_exists(os.environ['DAGSTER_MLFLOW_ARTIFACT_BUCKET'])
        return self

    def _create_bucket_if_not_exists(self, name: str) -> bool:
        if self._head_bucket(name):
            print(f"Bucket {name} already exists")
            return False

        client = self.resource.get_client()
        client.create_bucket(Bucket=name)
        print(f"Created bucket: {name}")
        return True

    def _head_bucket(self, name: str) -> bool:
        client = self.resource.get_client()
        try:
            client.head_bucket(Bucket=name)
            return True
        except client.exceptions.BotocoreError:
            return False
