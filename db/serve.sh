#!/usr/bin/env bash
# Init and/or serve the local SuperDB lead database.
#
# Usage:
#   ./db/serve.sh init    # create data/lake and the 'leads' pool (once, or after deleting data/lake)
#   ./db/serve.sh serve   # start `super db serve` on localhost:9867 (foreground)
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
LAKE_PATH="$(pwd)/data/lake"
SUPER_DB="file://${LAKE_PATH}"

case "${1:-}" in
  init)
    mkdir -p "$LAKE_PATH"
    super db init "$LAKE_PATH" || true
    super db -db "$SUPER_DB" create leads || echo "(pool 'leads' already exists)"
    ;;
  serve)
    exec super db serve -db "$SUPER_DB" -l localhost:9867
    ;;
  *)
    echo "usage: $0 {init|serve}" >&2
    exit 1
    ;;
esac
