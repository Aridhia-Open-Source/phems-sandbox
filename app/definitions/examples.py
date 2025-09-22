import time
import random
import dagster as dg


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
def example_complex_asset(example_asset_a: int, example_asset_b: int) -> int:
    print("Example Complex Asset")
    return example_asset_a + example_asset_b


@dg.job
def example_op_job():
    print("Example Job")
    num = random_int()
    result = example_op(num)
    result = example_op(result)
    result = example_op(result)
    print(result)
