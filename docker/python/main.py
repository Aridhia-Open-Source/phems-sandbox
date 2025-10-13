#!/usr/bin/env python3

import os
import sys
import json

MNT_BASE_PATH = "/mnt/dagster/artifacts"


def main():
    argv = sys.argv[1:]
    print(f"argv: {argv}")
    write_results()
    return 0


def write_results():
    task_id = os.environ['TASK_ID']
    output_dir = f"{MNT_BASE_PATH}/{task_id}"
    os.makedirs(output_dir, exist_ok=True)

    for n in range(1, 5):
        filepath = f"{output_dir}/result_{n}.json"
        print("Creating file:", filepath)
        with open(filepath, 'w') as f:
            f.write(json.dumps({"result": {"value": n}}))


if __name__ == "__main__":
    print("Running main.py")
    sys.exit(main())
