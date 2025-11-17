import time
import logging
import random

import dagster as dg
from dagster_celery_k8s import celery_k8s_job_executor

DEFAULT_QUEUE = 'node'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
celery_k8s_executor = celery_k8s_job_executor.configured(
    {"config_source": {"task_default_queue": DEFAULT_QUEUE}}
)


@dg.asset(
    tags={"dagster-celery/queue": DEFAULT_QUEUE}
)
def super_simple_asset() -> int:
    print("Super Simple Asset - START")
    time.sleep(3)
    print("Super Simple Asset - END")
    return 0


@dg.job(
    executor_def=celery_k8s_executor,
    tags={"dagster-celery/queue": DEFAULT_QUEUE},
)
def super_simple_asset_job():
    print("Super Simple Asset Job - START")
    super_simple_asset()
    print("Super Simple Asset Job - END")


@dg.op(
    config_schema={
        "x": dg.Field(int, default_value=1),
        "y": dg.Field(int, default_value=3),
    }
)
def random_int(context) -> int:
    return random.randint(context.op_config["x"], context.op_config["y"])


@dg.op
def example_op(num: int) -> int:
    print("Example Op")
    print(f"Sleeping for {num} seconds...")
    time.sleep(num)
    return num + 1


@dg.graph_asset
def example_asset_a() -> int:
    print("Example Asset A")
    num = random_int()
    result = example_op(num)
    result = example_op(result)
    result = example_op(result)
    return result


@dg.graph_asset
def example_asset_b() -> int:
    print("Example Asset B")
    num = random_int()
    result = example_op(num)
    result = example_op(result)
    result = example_op(result)
    return result


@dg.asset
def example_complex_asset(
    context: dg.AssetExecutionContext,
    example_asset_a: int,
    example_asset_b: int
) -> int:
    context.log.info("Example Complex Asset")
    return example_asset_a + example_asset_b


@dg.job
def example_op_job():
    print("Example Job")
    num = random_int()
    result = example_op(num)
    result = example_op(result)
    result = example_op(result)
    print(result)


@dg.asset
def example_logging_asset(context: dg.AssetExecutionContext) -> int:
    for _ in range(5):
        context.log.info("DAGSTER - INFO: Example Logging Asset")
        context.log.error("DAGSTER - ERROR: Example Logging Asset")
        time.sleep(1)
    return 0
