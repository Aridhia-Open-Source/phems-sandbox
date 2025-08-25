import time

import dagster as dg


@dg.asset
def example_1():
    time.sleep(1)
    print("Step 1")
    return {"result": 1}


@dg.asset
def example_2():
    time.sleep(1)
    print("Step 2")
    return {"result": 2}


@dg.asset
def example_3():
    time.sleep(1)
    print("Step 3")
    return {"result": 3}
