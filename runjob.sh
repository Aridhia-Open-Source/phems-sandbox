#!/usr/bin/env bash

JOB_NAME=$1
REPO_NAME="__repository__"
REPO_LOCATION_NAME="app"
GRAPHQL_URL="http://localhost:3000/graphql"

RESPONSE=$(curl -X POST "$GRAPHQL_URL" \
  -H "Content-Type: application/json" \
  -d "$(cat <<EOF
{
  "query": "mutation LaunchRun(\$executionParams: ExecutionParams!) { launchRun(executionParams: \$executionParams) { __typename ... on LaunchRunSuccess { run { runId } } ... on PythonError { message, stack } } }",
  "variables": {
    "executionParams": {
      "selector": {
        "jobName": "${JOB_NAME}",
        "repositoryName": "${REPO_NAME}",
        "repositoryLocationName": "${REPO_LOCATION_NAME}"
      },
      "mode": "default",
      "runConfigData": {}
    }
  }
}
EOF
)")

echo $RESPONSE | jq
RUN_ID=$(echo "$RESPONSE" | jq -r '.data.launchRun.run.runId')

if [[ "$RUN_ID" == "null" || -z "$RUN_ID" ]]; then
  echo "Failed to launch run. Response:"
  echo "$RESPONSE" | jq
  exit 1
fi

echo ""
echo "Queued run with ID: $RUN_ID."
echo "You can view the run at: http://localhost:3000/runs/$RUN_ID"


echo ""
echo "Awaiting run completion..."

while true; do
  STATUS=$(curl -s -X POST "$GRAPHQL_URL" \
    -H "Content-Type: application/json" \
    -d "$(cat <<EOF
{
  "query": "query { runOrError(runId: \\"${RUN_ID}\\") { __typename ... on Run { status } ... on PythonError { message } } }"
}
EOF
)" | jq -r '.data.runOrError.status')

  echo "status: $STATUS"

  if [[ "$STATUS" == "SUCCESS" || "$STATUS" == "FAILURE" ]]; then
    echo "status: $STATUS"
    break
  fi

  sleep 1
done