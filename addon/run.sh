#!/bin/sh
set -e

export NAKUPNI_DB="${NAKUPNI_DB:-/data/nakupni.db}"
mkdir -p "$(dirname "$NAKUPNI_DB")"
echo "[nakupni-seznam] DB: $NAKUPNI_DB, port: ${PORT:-8091}"

exec python3 -u /app/app.py
