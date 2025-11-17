#!/usr/bin/env bash

# kill any existing port-forward processes
pkill -f "kubectl port-forward"

set -e

echo "forwarding kubernetes ports..."

kubectl port-forward -n code svc/codeserver 4001
