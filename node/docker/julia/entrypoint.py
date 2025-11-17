#!/usr/bin/env python3

import sys
import subprocess
import logging
import time


from dagster_pipes import open_dagster_pipes


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def entrypoint():
    with open_dagster_pipes() as _:
        # argv = sys.argv[1:]
        logger.info("[CHILD][PYTHON][INFO] - hello world")
        logger.error("[CHILD][PYTHON][ERROR] - goodbye world")
        time.sleep(5)

        result = subprocess.run([
            "julia",
            "--project=/project",
            "/project/src/main.jl",
        ], check=True)
        return result.returncode


if __name__ == "__main__":
    print("Running entrypoint.py")
    sys.exit(entrypoint())
