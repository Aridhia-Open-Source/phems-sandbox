import time

import dagster as dg


@dg.asset
def processed_data_1():
    time.sleep(1)
    print("Processing Data 1")
    return "Data 1"


@dg.asset
def processed_data_2():
    time.sleep(1)
    print("Processing Data 2")
    return "Data 2"


@dg.asset
def processed_data_3():
    time.sleep(1)
    print("Processing Data 3")
    return "Data 3"
