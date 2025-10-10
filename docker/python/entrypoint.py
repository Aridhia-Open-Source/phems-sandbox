#!/usr/bin/env python3

import sys
# import subprocess
import logging
import time
import os

from dagster_pipes import open_dagster_pipes

PIPES_CONTEXT_VALUE = os.environ.get('DAGSTER_PIPES_CONTEXT')
DAGSTER_PIPES_MESSAGES_ENV_VAR = os.environ.get('DAGSTER_PIPES_MESSAGES_ENV_VAR')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def add_pipes_logging(pipes):
#     handler = logging.StreamHandler(sys.stdout)
#     handler.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     pipes.log.addHandler(handler)


def entrypoint():
    with open_dagster_pipes() as pipes:
        # argv = sys.argv[1:]
        # add_pipes_logging(pipes)
        # for n in range(5):
        # pipes.log.info("hello world")
        # pipes.log.error("goodbye world")

        logger.info("bonjour monde")
        logger.error("au revoir monde")
        time.sleep(5)

        # pipes.log.info(f"argv: {argv}")
        # pipes.log.info(f"DAGSTER_PIPES_CONTEXT: {PIPES_CONTEXT_VALUE}")
        # pipes.log.info(f"DAGSTER_PIPES_MESSAGES_ENV_VAR: {DAGSTER_PIPES_MESSAGES_ENV_VAR}")
        # result = subprocess.run(argv, check=True)
        return 0


if __name__ == "__main__":
    print("Running entrypoint.py")
    sys.exit(entrypoint())
