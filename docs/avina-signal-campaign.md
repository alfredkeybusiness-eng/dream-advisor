# Avina Signal Campaign — Retirement & Transition Leads (CA/TX/FL)

Built via the Avina MCP (`https://api.avina.io/mcp`) in the `Dailysolutions` Avina
workspace, for financial-advisor / annuity retirement-planning outreach.

## Mission

Capture named, outreach-ready prospects who are currently tied to a **dated,
verifiable** retirement, pension/account-decision, employment-transition, or
business-transition event — not general news or anonymous organizational
updates. Every lead requires: named person + role + employer + location +
supporting evidence + a public professional contact path.

Target states: **California, Texas, Florida**
Target profession groups: **education, healthcare/nursing, physicians &
medical-practice owners, fire-service, public/government employees,
small-to-medium business owners**
Lookback: last 30 days, expand to 90 if thin.

## What's live in Avina

### 1 combined signal
- **Retirement Transition Prospects** — single cross-segment signal covering
  all 6 profession groups across all 3 states. Created first as a proof of
  concept; monitoring is currently **off** in favor of the 18 segmented
  signals below (they map 1:1 to the original campaign spec and are easier to
  budget/report on individually).

### 18 segmented signals (state × profession group)

| Segment | Avina signal name |
|---|---|
| ca-education-signals | California Education Retirement Signals |
| ca-healthcare-signals | California Healthcare Staff Changes |
| ca-physician-signals | California Practice Transitions |
| ca-fire-service-signals | California Fire Retirements |
| ca-public-employee-signals | California Government Retirement Signals |
| ca-business-owner-signals | California Owner Transfers |
| tx-education-signals | Texas School Retirement Contacts |
| tx-healthcare-signals | Texas Healthcare Personnel Events |
| tx-physician-signals | Texas Practice Transitions |
| tx-fire-service-signals | Texas Fire Retirement Events |
| tx-public-employee-signals | Texas Government Retirement Signals |
| tx-business-owner-signals | Texas Owner Transfer Events |
| fl-education-signals | Florida Educator Exit Events |
| fl-healthcare-signals | Florida Healthcare Exit Contacts |
| fl-physician-signals | Florida Medical Exit Events |
| fl-fire-service-signals | Florida Fire Retirement Events |
| fl-public-employee-signals | Florida Government Retirement Events |
| fl-business-owner-signals | Florida Owner Transfer Events |

Each signal (`custom_ai_alert` type) requires, before a match counts:
- Named individual with confirmed title, employer, and state
- A dated event in one of: retirement exit, pension/account decision
  (403(b)/401(k)/DROP/COLA), employment transition (layoff/closure/
  restructuring), business transition (sale/succession/buyout/merger)
- Identity confirmed across a primary source **and** a supporting source
  (staff directory, official bio, LinkedIn, licensing record, press release)
- A public professional contact path (staff/business email, phone, LinkedIn,
  or contact page)

All 18 were created as **free, no-cost drafts** — creating a signal doesn't
spend credits; only `request_more_leads` (generation) does.

### Persona / contact targeting

Workspace personas drive which contact Avina enriches per alert. The
workspace's leftover demo persona (`Chief Procurement Officer`, `Director of
Procurement`, etc. — unrelated trial defaults) was deleted. Replaced with:

- **Retirement & Transition Prospects** persona — Teacher, Superintendent,
  School Administrator, Registered Nurse, Nurse Manager, Physician, Dentist,
  Practice Owner, Firefighter, Fire Chief, Government Employee, Agency
  Director, Business Owner, Founder, President.

A few signals also carry a per-signal `enrichment_titles` override (e.g.
tx-business-owner-signals, fl-healthcare-signals, fl-business-owner-signals)
when Avina's drafting step scoped the titles more narrowly than the
workspace persona.

## Credit / trial budget

- Trial: 200 signal credits for the period **2026-08-11 → 2026-09-10**.
- `trial_end_date` is **2026-08-18** (7 days from workspace setup) — note this
  is sooner than the 20-day pacing target; the account may need to convert to
  paid before day 8 for the full 20-day plan to complete.
- Plan: ~10 credits/day, one segmented signal generated per day, rotating
  through the 18 segments (~18 days of generation, leaving a small buffer).

## Automation limitation (important)

A daily Routine was attempted to automate the rotation (`request_more_leads`
on the next un-generated segment each day), but this org's Routine/trigger
mechanism **cannot carry the Avina MCP connector into fired sessions** — a
scheduled job would run with no Avina tools and silently do nothing. The
trigger was deleted rather than left broken.

**Until this is resolved**, generating each day's batch requires either:
1. An active conversation turn (ask the assistant to run the next segment), or
2. A Routine created directly from the claude.ai Routines UI, where the Avina
   connector can be attached to the fired session.

## Parallel workstream (not built yet)

A separate prompt ("Vanguard / Lead Force Support") describes a different
B2B trigger-based lead pipeline (funding rounds, exec hires, tech-stack
adoption; HubSpot + PostgreSQL + SMTP routing; cultural-intelligence
tagging) that explicitly must **not** reference Avina signals in its output.
Per user direction, this runs **in parallel** as its own workstream, not
merged into the Avina retirement-lead campaign above. It has not been scoped
or built yet.

## Local lead database (SuperDB)

All extracted leads now land in a local SuperDB database (`db/`, see
`db/README.md`) rather than staying scattered across each source platform's
own UI/API. It currently holds the **9 real leads** produced by the
combined `Retirement Transition Prospects` signal's initial test batch —
named individuals with dated, sourced retirement/transition events:

Linda Hoff (CFO, Stanford Health Care, CA) · Lee Glover (Fire Chief, City of
Frisco, TX) · Raymond Hill (Interim Fire Chief, Fort Worth, TX) · Maria F.
Vazquez (Superintendent, Orange County Public Schools, FL) · Joel G. Baker
(Fire Chief, Austin, TX) · Sharita Herrera (Principal, Killeen ISD, TX) ·
Craig Bessent (Asst. Superintendent, Wylie ISD, TX) · Michael A. Cardona
(Superintendent, San Marcos CISD, TX) · Chris Hughes (Interim Fire Chief,
Daytona Beach, FL — note: the actual retiree of record here is his
predecessor, Dru Driscoll; flagged in the record for verification before
outreach).

See `db/schema.md` for the record shape and `db/seed/leads_seed.ndjson` for
the raw data. Future pulls from Avina (`query_signals`), Vibe Prospecting,
or Clay should be normalized to this schema and loaded via
`db/load_leads.py`.

## Other lead-source tools evaluated (Apollo / Exa / Bright Data / Clay / Vibe Prospecting)

Asked to also use Apollo, Exa, Clay, Bright Data, and Vibe Prospecting for
targeted-lead generation. Actual capability in this session, checked before
spending anything:

| Tool | Status | Usable for lead generation? |
|---|---|---|
| Apollo.io | connected | **No** — only call/conversation-intelligence tools (transcript search, insights, recordings) are exposed here; no people/company search tool exists in this integration. |
| Exa | not connected | **No** — not an installed connector for this org. |
| Bright Data | not connected | **No** — not an installed connector for this org. |
| Clay | connected | **Partial** — real prospecting, but scoped per-company (needs a known domain/LinkedIn URL to search contacts at). Good for enriching/verifying a specific business once named (e.g. from an Avina business-owner lead), not for open-ended "find all X in state Y" discovery. |
| Vibe Prospecting | connected | **Yes**, but **paid** (Explorium credits; packages start at $29.90/900 credits, no free tier). A naive query (`job_level: owner/founder/president` + state only) pulled big-tech founders (Airbnb, Cisco, Google, Databricks, Salesforce) instead of SMB owners, for 10 credits. Corrected with `linkedin_category` (via required `autocomplete` step) + `company_size` + state, validated for 1 credit: matched **Derek Zobrist, Owner, Enovative Mechanical, Los Angeles, CA** — a real small-HVAC-contractor-owner match. 11 credits spent total on validation; user opted to stop there rather than fund a full pull across all industries/states for now.

## Next steps

- Manually (or via a UI-created Routine) run `request_more_leads` on each
  segmented signal per the pacing plan above, then `query_signals` to pull
  results.
- Scope and build the separate Vanguard/Lead Force B2B pipeline when ready.
- Consider whether the Hermes-style source-hierarchy/scoring spec (see prior
  conversation) needs a custom implementation beyond what Avina's
  `custom_ai_alert` natively supports.
