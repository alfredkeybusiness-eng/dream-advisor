# Retirement Intelligence site

Public-facing Cloudflare Worker + D1 site — phase 1 of the event-driven
retirement-intelligence architecture (publishing side only; no contact/PII
data lives here or ever should — see `docs/architecture.md`).

Live routes:

| Route | Renders |
|---|---|
| `/` | Homepage: hero, "Today's Retirement Intelligence" cards, category pills, state grid |
| `/article/:slug` | Full article: What Happened / Why It Matters / Who May Be Affected / What To Do / Source |
| `/category/:slug` | Signals filtered by category |
| `/:state-retirement-updates` | e.g. `/texas-retirement-updates` — signals filtered by state |
| `/api/signals` | Raw JSON of published signals |

## Data

Real Cloudflare D1 database, already provisioned:

- Name: `dream-advisor-retirement-intel`
- UUID: `224e2d9b-d743-45d8-b052-095455266a57`
- Table: `retirement_signals` (schema in `schema.sql`)

Currently seeded with **9 real articles**, derived from Avina's first
signal batch (see `docs/avina-signal-campaign.md`) and rewritten as public
retirement news — no personal contact info, only facts already published
elsewhere with sources preserved. This is deliberately a **content-only**
table: contact/enrichment/outreach data belongs in a separate store per
`docs/architecture.md` and must never be joined into what this Worker
serves publicly.

## Dashboard API (for the frontend build)

Separate from the public content routes above — this is the contract for
the internal dashboard (Signal Pipeline, Campaign Metrics, Research Queue,
Scout Status, Email Outreach, Calendar/Meetings; matches the reference
mockup published earlier as a Claude artifact). Backed by `leads`,
`signal_defs`, and `scout_sources` — separate tables from
`retirement_signals`, deliberately: those hold contact/campaign data, this
table holds public article content, and the public site routes never touch
the former.

CORS is wide open (`*`) for now — no auth exists yet; tighten before this
carries anything beyond this campaign's own read-mostly data.

| Route | Returns |
|---|---|
| `GET /api/campaign-metrics` | `{leads_captured, signals_configured, contact_ready, flagged_for_review, leads_by_state, leads_by_profession_group}` |
| `GET /api/pipeline` | Array of the 19 Avina signal defs: `{campaign_segment, avina_signal_id, state, target_profession_group, status, last_lead_count, last_run_at}` |
| `GET /api/leads` (`?needs_review=true\|false`) | Array of leads (Research Queue) |
| `POST /api/leads` | Upsert a lead by `lead_id` (JSON body, same shape as a lead row) — the daily-lead-rotation task or any other source pushes here |
| `GET /api/scout-status` | Array of `{name, detail, status, status_label}` |
| `GET /api/outreach` | `{configured: false, sequences: []}` — no Avina automation built yet |
| `GET /api/meetings` | `{meetings: []}` — no outreach is live yet |

Real data live right now: 9 leads, 19 signal defs, 5 scout sources — same
numbers as the reference dashboard mockup.

## Local dev

```bash
cd site
npm install
npx wrangler d1 execute dream-advisor-retirement-intel --local --file=schema.sql
npx wrangler dev --local   # http://localhost:8787, local D1 copy (not the real data)
```

To develop against the real seeded data instead of an empty local copy,
add `--remote` to the dev command (requires being logged in via
`wrangler login` or `CLOUDFLARE_API_TOKEN`).

## Deployment

No deploy credentials exist in the environment that built this — two ways
to actually ship it:

1. **CI (recommended)**: `.github/workflows/deploy-site.yml` deploys on
   every push to `main` that touches `site/`. Requires two repo secrets
   (Settings → Secrets and variables → Actions):
   - `CLOUDFLARE_API_TOKEN` — a token with Workers Scripts:Edit + D1:Edit
   - `CLOUDFLARE_ACCOUNT_ID`
2. **Manual**: `cd site && npx wrangler login && npx wrangler deploy`

Until one of those runs, this Worker exists as real, tested code and a
real, seeded D1 database — but isn't live on a public URL yet.

## What's NOT built yet

This is phase 1 (publishing) only, per the phased plan agreed in
`docs/architecture.md`:

- The event bus (`signal.discovered` → verify → classify → store →
  publish) — signals here were inserted by hand from the existing Avina
  batch, not by an automated pipeline yet.
- Org pages (`/schools/...`, `/companies/...`), dynamic visual/social-card
  generation, and the contact/enrichment/email-validation/outreach
  pipeline are all future phases.
- Yutori as a second discovery source — no connector exists in this
  environment yet.
