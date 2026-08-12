---
name: daily-lead-rotation
description: Runs one step of the CA/TX/FL retirement-lead campaign rotation across the 18 Avina segment signals -- generates the next un-run segment's leads and loads them into the local SuperDB `leads` pool. Use for the scheduled daily lead-generation task, or when asked to "run the daily rotation" / "generate today's leads".
---

# Daily lead rotation

Replaces the CCR (Claude Code Remote) Routine automation that couldn't carry
the Avina MCP connector into scheduled firings -- this runs inside Prime
Agent's own kernel instead, with its own Avina MCP login, so it isn't
blocked by that limitation.

## One-time setup

1. **Log in to Avina**: `/login` -> MCP Connections -> `avina` (OAuth in the
   browser). See `../avina/SKILL.md`.
2. **Run the local lead database**: from the repo root,
   `./db/serve.sh init` (once) then `./db/serve.sh serve &` (keep it
   running). Defaults to `http://localhost:9867`; override with
   `LEADS_DB_URL` if it runs elsewhere.
3. Start a background Prime Agent session in this repo and give it a name
   (`prime-agent list` shows the id if you skip renaming):
   ```
   cd /path/to/dream-advisor
   prime-agent --mode daemon
   prime-agent rename <id> dream-advisor
   ```
4. Schedule the daily run (adjust the cron time/zone as needed -- this
   example is 15:00 UTC, matching the pacing plan in
   `docs/avina-signal-campaign.md`):
   ```
   prime-agent schedule add dream-advisor "0 15 * * *" -- "/skill:daily-lead-rotation Run the daily rotation step."
   prime-agent schedule list
   ```

## What it does

```python
await daily_lead_rotation()
```

1. Walks the 18 segments in `segments.py` in a fixed order (CA then TX then
   FL, each state's 6 profession groups) and finds the first one with **zero**
   leads generated so far (`avina.query_signals` filtered by
   `signal_group_id`).
2. If all 18 already have leads, reports the rotation complete and does
   nothing further -- **it will not overspend the trial's 200-credit budget**
   by re-running segments.
3. Otherwise calls `avina.request_more_leads(signal_id, count=10)`, polls
   `avina.signal_generation_status` until it finishes (or a poll-count
   ceiling is hit -- generation keeps running server-side either way),
   fetches the new rows via `avina.query_signals`, and loads them into the
   local `leads` SuperDB pool via `db/schema.md`'s shape.

## Known limitation

`full_name`, `job_title`, and `signal_category` are **not** auto-extracted
from Avina's freeform `header`/`content` text -- a regex or naive parse could
silently attribute the wrong person's name when a signal mentions both a
retiree and a successor (this happened with one of the seed leads; see
`docs/avina-signal-campaign.md`). Every loaded row is flagged
`needs_review: true` in the `leads` pool; review and fill those fields in
(by hand, or with a follow-up LLM pass) before using a row for outreach.

## Manual run / dry run

```python
await daily_lead_rotation(dry_run=True)   # report which segment is next, no spend
await daily_lead_rotation()               # generate + load
```

or from a shell: `!daily_lead_rotation --dry-run`
