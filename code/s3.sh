
#!/usr/bin/env bash

set -euo pipefail

unset AWS_DEFAULT_PROFILE
export AWS_BUCKET_NAME="phems-bucket"
export AWS_ACCESS_KEY_ID="minio"
export AWS_SECRET_ACCESS_KEY="miniosecret"
export AWS_ENDPOINT_URL="http://localhost:9000"

echo "Listing S3 bucket contents at s3://$AWS_BUCKET_NAME/artifacts/ ..."

# list s3 objects and group with file counts per directory prefix
aws s3 ls "s3://$AWS_BUCKET_NAME/artifacts/" \
    --endpoint-url "$AWS_ENDPOINT_URL" \
    --recursive
    # awk '
    # {
    #     # Extract directory prefix (up to the last slash)
    #     match($4, /^(artifacts\/[^\/]+)/, m)
    #     if (m[1] != "") {
    #         prefix = m[1]
    #         count[prefix]++
    #         # Store timestamp and size of last file for display (arbitrary choice)
    #         ts[prefix]=$1" "$2
    #         size[prefix]=$3
    #     }
    # }
    # END {
    #     for (p in count) {
    #         printf "%s %12d %s (%d files)\n", ts[p], size[p], p, count[p]
    #     }
    # }' | sort

# echo "Removing all objects from S3 bucket at s3://$AWS_BUCKET_NAME/artifacts/ ...""
# aws s3 rm s3://$AWS_BUCKET_NAME/artifacts/ \
#     --endpoint-url "$AWS_ENDPOINT_URL" \p
#     --recursive
