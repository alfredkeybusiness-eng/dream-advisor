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
