#!/usr/bin/env python3

from dagster_pipes import k8s_subprocess

if __name__ == "__main__":
    with k8s_subprocess.run(
        command=["Rscript", "/app/script.R"],
    ) as pipe:
        for event in pipe.events():
            # These events come from stdout of the R process
            print(f"Pipes event: {event}")

        result = pipe.get_materialize_result()
        print("Final outputs:", result.metadata)