#!/usr/bin/env bash

set -e

echo "forwarding kubernetes ports..."

# kill any existing port-forward processes
pkill -f "kubectl port-forward"

kubectl port-forward -n code svc/codeserver 4001
