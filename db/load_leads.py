#!/usr/bin/env python3
"""Load lead records (NDJSON, one record per line) into the SuperDB 'leads'
pool.

Usage:
    python3 db/load_leads.py path/to/records.ndjson [--pool leads] [--url http://localhost:9867]

The target service must already be running (see db/serve.sh). This is a
thin wrapper around superdb.Client.load() -- install the client with:
    pip3 install "git+https://github.com/brimdata/superdb-python"
"""
import argparse
import sys

import superdb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ndjson_path", help="Path to an NDJSON file (one JSON object per line)")
    parser.add_argument("--pool", default="leads", help="Target pool name (default: leads)")
    parser.add_argument("--url", default=None, help="SuperDB service URL (default: $SUPER_DB or http://localhost:9867)")
    parser.add_argument("--message", default="load_leads.py ingest", help="Commit message")
    args = parser.parse_args()

    client = superdb.Client(args.url) if args.url else superdb.Client()

    with open(args.ndjson_path, "rb") as f:
        data = f.read()

    line_count = data.count(b"\n") or 1
    client.load(args.pool, data, commit_body=args.message, mime_type="application/json")
    print(f"Loaded ~{line_count} record(s) from {args.ndjson_path} into pool '{args.pool}'.", file=sys.stderr)


if __name__ == "__main__":
    main()
