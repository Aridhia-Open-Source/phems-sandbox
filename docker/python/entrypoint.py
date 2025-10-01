#!/usr/bin/env python3

import sys
import subprocess

from dagster_pipes import open_dagster_pipes


def entrypoint():
    with open_dagster_pipes() as _pipes: # NOQA
        argv = sys.argv[1:]
        print(f"argv: {argv}")

        try:
            result = subprocess.run(argv, check=True)
            return result.returncode
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running subprocess: {e}")
            return e.returncode


def materialize(result, pipes, argv):
    pipes.report_asset_materialization(
            metadata={
                'exit_code': {
                    'raw_value': result.returncode, 'type': 'int',
                },
                'argv': {
                    'raw_value': ' '.join(argv), 'type': 'string',
                },
            },
        )


if __name__ == "__main__":
    print("Running entrypoint.py")
    sys.exit(entrypoint())
