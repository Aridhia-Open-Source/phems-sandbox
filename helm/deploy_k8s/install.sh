#!/usr/bin/env bash
set -e

helm upgrade --install dagster dagster/dagster -f values.yaml
