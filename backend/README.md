# Backend

FastAPI service backing the Signal Desk dashboard (Signal Pipeline, Campaign
Metrics, Research Queue, Scout Status, Email Outreach, Calendar/Meetings).

## Local dev

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

No setup needed for local dev: with no `DATABASE_URL` set, it falls back to
a local SQLite file (`dev.db`, git-ignored) and seeds itself on first
startup from `../db/seed/leads_seed.ndjson` plus the static signal/scout
registries in `app/seed.py`.

## Production (Render)

Deployed via the root `render.yaml` Blueprint. Render sets `DATABASE_URL` to
the provisioned Postgres instance automatically — same code path, no
SQLite/Postgres branching needed beyond the URL normalization in `app/db.py`.

## Endpoints

| Route | Backs |
|---|---|
| `GET /api/campaign-metrics` | Campaign Metrics |
| `GET /api/signals` | Signal Pipeline |
| `GET /api/leads` (`?needs_review=true`) | Research Queue |
| `POST /api/leads` | Upsert a lead by `lead_id` — the daily-lead-rotation task or any other source pushes here |
| `GET /api/scout-status` | Scout Status |
| `GET /api/outreach` | Email Outreach (currently always `{"configured": false, "sequences": []}` — no Avina automation built yet) |
| `GET /api/meetings` | Calendar/Meetings (currently always empty — no outreach is live yet) |

## Data model

`app/models.py` mirrors `db/schema.md` at the repo root (the SuperDB lead
schema) — keep both in sync if either changes. `app/seed.py`'s `SEGMENTS`
list mirrors
`.prime/agent/skills/daily-lead-rotation/src/daily_lead_rotation/segments.py`
for the same reason.

Postgres here is the **production** store for the deployed dashboard;
the local SuperDB lake (`db/`) is the working store used during
interactive/agent-driven lead generation. Nothing currently syncs the two
automatically — `POST /api/leads` is the intended bridge once the daily
rotation task is wired to push here too.
