#!/usr/bin/env bash

set -e

echo "forwarding kubernetes ports..."

kubectl port-forward -n code svc/codeserver 4001
