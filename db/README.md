# Lead database (SuperDB)

Local canonical store for every lead extracted from Avina, Vibe Prospecting,
Clay, or any future source — one place to hold and query the campaign's
targeted-lead records, independent of any single source platform.

Built on [SuperDB](https://superdb.org/) (`brimdata/super`), queried with
[SuperSQL](https://superdb.org/super-sql/intro), accessed from Python via the
[`superdb-python`](https://github.com/brimdata/superdb-python) client.

## Setup

```bash
# CLI (Go, builds the `super` binary)
GOBIN=/usr/local/bin go install github.com/brimdata/super/cmd/super@main

# Python client
pip3 install "git+https://github.com/brimdata/superdb-python"
```

## Layout

- `data/lake/` — the actual lake storage (git-ignored; binary/local only).
  Recreate it with `./db/serve.sh init` if missing.
- `db/schema.md` — the `leads` pool record shape.
- `db/seed/leads_seed.ndjson` — 9 real leads pulled from the Avina
  `Retirement Transition Prospects` signal (public officials' publicly
  reported retirements — see `docs/avina-signal-campaign.md`), used both as
  a working example and as the current real content of the pool.
- `db/load_leads.py` — load an NDJSON file of lead records into the `leads`
  pool via the Python client (`superdb.Client`).
- `db/serve.sh` — init the lake (if needed) and start `super db serve` on
  `localhost:9867`.

## Quickstart

```bash
./db/serve.sh init      # only needed once, or after deleting data/lake
./db/serve.sh serve &   # starts the service on localhost:9867

# load the seed data (idempotent-ish: re-running adds a new commit)
python3 db/load_leads.py db/seed/leads_seed.ndjson

# query
super db -db file://$(pwd)/data/lake -f table \
  -c "from leads | values {full_name, employer_name, state, signal_category} | sort state"
```

Or from Python:

```python
import superdb
c = superdb.Client('http://localhost:9867')
for row in c.query("from leads | where state == 'TX'"):
    print(row)
```

## Why SuperDB here

Every lead source (Avina's `custom_ai_alert` output, Vibe Prospecting rows,
Clay enrichment) returns a slightly different, semi-structured shape.
SuperDB's whole design point is ingesting eclectic JSON without forcing a
rigid schema up front, while still supporting real SQL-style queries
(filter, group, join) once the data is in — which fits a lead pipeline
pulling from several APIs better than a rigid relational table would.
