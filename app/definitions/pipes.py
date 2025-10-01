import os
import uuid

import dagster as dg
from dagster_k8s import PipesK8sClient
from dagster._core.pipes.client import PipesClientCompletedInvocation

from app.resources.minio import MinioManager

minio = MinioManager()

PVC_NAME = 'artifacts-pvc'
DOCKER_IMAGE = 'dagster-pipes-python:v1'
S3_BASE_PATH = f"s3://{minio.bucket_name}/artifacts"
MNT_BASE_PATH = os.environ['DAGSTER_ARTIFACT_MOUNT_PATH']

BASE_POD_SPEC = {
    "volumes": [
        {
            "name": PVC_NAME,
            "persistentVolumeClaim": {
                "claimName": PVC_NAME
            },
        }
    ],
    "containers": [
        {
            "name": "main",  # dagster convention
            "volumeMounts": [
                {
                    "name": PVC_NAME,
                    "mountPath": MNT_BASE_PATH,
                }
            ],
        }
    ],
}


@dg.asset
def k8s_pipes_asset(context: dg.AssetExecutionContext, k8s_pipes_client: PipesK8sClient):
    task = K8sPipeAsset(k8s_pipes_client, context)
    result = task(image=DOCKER_IMAGE)
    upload_result(context, result)
    return result.output


class K8sPipeAsset:
    def __init__(
            self,
            client: PipesK8sClient,
            context: dg.AssetExecutionContext,
    ):
        self.client = client
        self.context = context

    def __call__(self, image, **kwargs) -> 'K8sPipesResponse':
        return self._run_task(image, **kwargs)

    def _run_task(self, image, env=None, **kwargs) -> 'K8sPipesResponse':
        task_id = str(uuid.uuid4())
        kwargs['env'] = env or {}
        kwargs['env']['TASK_ID'] = task_id
        kwargs.update(image=image, base_pod_spec=BASE_POD_SPEC)

        self._log(task_id, "Task Starting")
        result = self.client.run(context=self.context, **kwargs)
        self._log(task_id, "Task Completed")

        return K8sPipesResponse(task_id, image, result)

    def _log(self, task_id: str, message: str):
        self.context.log.info(f"[K8Pipe:{task_id}] {message}")


class K8sPipesResponse:
    output: dg.Output

    def __init__(self, task_id, image, result: PipesClientCompletedInvocation):
        self.task_id = task_id
        self.result = result
        self.output = dg.Output(
            metadata={'task_id': task_id, 'image': image},
            value={'artifacts': f"{S3_BASE_PATH}/{task_id}"},
        )


def upload_result(context: dg.AssetExecutionContext, result: K8sPipesResponse):
    source_dir = f"{MNT_BASE_PATH}/{result.task_id}"
    target_prefix = f"artifacts/{result.task_id}"
    minio.upload_dir(source_dir=source_dir, target_prefix=target_prefix)
    context.log.info(f"Uploaded {source_dir} to {target_prefix}")
