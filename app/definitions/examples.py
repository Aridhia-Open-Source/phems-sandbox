import time

import dagster as dg


@dg.op
def example_1():
    time.sleep(5)
    print("Step 1")
    return {"result": 1}


@dg.op
def example_2():
    time.sleep(5)
    print("Step 2")
    return {"result": 2}


@dg.op
def example_3():
    time.sleep(5)
    print("Step 3")
    return {"result": 3}


@dg.job
def example_job():
    example_1()
    example_2()
    example_3()
b