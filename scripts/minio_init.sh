#!/usr/bin/env bash
set -euo pipefail

MC_BIN="${MC_BIN:-mc}"
MINIO_ALIAS="beamlocal"
MINIO_ENDPOINT="${MINIO_ENDPOINT:-http://localhost:9000}"
MINIO_ACCESS_KEY="${MINIO_ACCESS_KEY:-beamadmin}"
MINIO_SECRET_KEY="${MINIO_SECRET_KEY:-beamadmin12345}"
BUCKET="beam-images"

"$MC_BIN" alias set "$MINIO_ALIAS" "$MINIO_ENDPOINT" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"
"$MC_BIN" mb -p "$MINIO_ALIAS/$BUCKET" || true
"$MC_BIN" anonymous set download "$MINIO_ALIAS/$BUCKET"

echo "OK: bucket $BUCKET is ready and public (read-only)."
echo "Upload images as: $MINIO_ENDPOINT/$BUCKET/m100.jpg (etc.)"
