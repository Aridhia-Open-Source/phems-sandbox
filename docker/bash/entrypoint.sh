#!/usr/bin/env bash

# Generic Dagster Pipes bash wrapper using /mnt/$TASK_ID for logs and results
# Usage: entrypoint.sh <command> [args...]

# -e          : exit if any command returns non-zero
# -u          : treat unset variables as an error
# -o pipefail : fail a pipeline if any command in it fails
set -euo pipefail

if [ -z "${TASK_ID:-}" ]; then
  echo "[pipes-wrapper] ERROR: TASK_ID environment variable is not set"
  exit 1
fi

if [ -z "${DAGSTER_PIPES_OUTPUT:-}" ]; then
  echo "[pipes-wrapper] ERROR: DAGSTER_PIPES_OUTPUT environment variable is not set"
  exit 1
fi

# Workspace for this job under /mnt, shared with parent container
WORKDIR="/mnt/dagster/storage/${TASK_ID}"
mkdir -p "$WORKDIR"

echo "[pipes-wrapper] Using TASK_ID=$TASK_ID"
echo "[pipes-wrapper] Workspace is $WORKDIR"
echo "[pipes-wrapper] Running command: $*"

# Disable automatic exit so we can capture the child exit code manually
set +e

# Run the child command ("$@"):
# - stdout is piped through tee → written to STDOUT_LOG and echoed live to Dagster UI
# - stderr is piped through tee → written to STDERR_LOG and echoed live to Dagster UI
"$@" 2> >(tee "$STDERR_LOG" >&2) | tee "$STDOUT_LOG"

# Capture exit code of the child command (first element of PIPESTATUS array)
EXIT_CODE=${PIPESTATUS[0]}

# Re-enable immediate exit on error
set -e

# === Failure path ===
if [ $EXIT_CODE -ne 0 ]; then
  echo "[pipes-wrapper] Command failed with exit code $EXIT_CODE"

  # Write Pipes OUTPUT JSON indicating failure
  # Includes paths to logs so parent Dagster can inspect or upload them
  cat > "$DAGSTER_PIPES_OUTPUT" <<EOF
{
  "events": [
    {
      "event_type": "OUTPUT",
      "output_name": "result",
      "data": {
        "status": "error",
        "exit_code": $EXIT_CODE,
        "stdout_path": "$STDOUT_LOG",
        "stderr_path": "$STDERR_LOG"
      }
    }
  ]
}
EOF

  echo "[pipes-wrapper] Error reported to Dagster via Pipes output"
  exit 0   # Exit success so Dagster can parse JSON instead of treating as infra failure
fi

# === Success path ===

# If the child did not create a result.json, create an empty JSON file
if [ ! -f "$RESULT_FILE" ]; then
  echo "{}" > "$RESULT_FILE"
fi

# Write Pipes OUTPUT JSON indicating success
cat > "$OUTPUT_FILE" <<EOF
{
  "events": [
    {
      "event_type": "OUTPUT",
      "output_name": "result",
      "data": {
        "status": "ok",
        "result_path": "$RESULT_FILE",
        "stdout_path": "$STDOUT_LOG",
        "stderr_path": "$STDERR_LOG"
      }
    }
  ]
}
EOF

# Print confirmation message
echo "[pipes-wrapper] Pipes output written to $OUTPUT_FILE"
