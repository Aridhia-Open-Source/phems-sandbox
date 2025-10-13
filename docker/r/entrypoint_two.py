#!/usr/bin/env python3
import subprocess
import json
from typing import TextIO, cast
from dagster_pipes import open_dagster_pipes

if __name__ == "__main__":
    with open_dagster_pipes() as pipes:
        process = subprocess.Popen(
            ["Rscript", "/app/script.R"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        if process.stdout is None:
            raise RuntimeError("Failed to capture R stdout")

        for line in cast(TextIO, process.stdout):
            line = line.rstrip()
            try:
                # Try to parse as JSON (structured Pipes event)
                event = json.loads(line)
                if isinstance(event, dict) and "event" in event:
                    # Forward the raw line as-is so Dagster sees the event
                    print(line, flush=True)
                    continue
            except Exception:
                pass

            # Fallback: treat as plain log
            pipes.log(line, level="INFO")

        retcode = process.wait()
        if retcode != 0:
            pipes.report_failure(f"R process exited with code {retcode}")
        else:
            pipes.report_success()
