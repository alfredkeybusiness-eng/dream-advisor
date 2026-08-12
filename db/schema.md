# `leads` pool schema

SuperDB doesn't require a rigid predeclared schema, but every ingestion
script should aim to produce records with this shape so queries across
sources stay consistent. Unknown/inapplicable fields may be omitted (SuperDB
handles heterogeneity natively) — this is the target shape, not a hard
constraint enforced by the database.

| Field | Type | Notes |
|---|---|---|
| `lead_id` | string | Stable id, prefixed by source: `avina-<row_id>`, `vibe-<prospect_id>`, `clay-<contact_id>` |
| `full_name` | string | |
| `job_title` | string | |
| `target_profession_group` | string | One of `education`, `nursing`, `physician`, `fire_service`, `public_employee`, `business_owner` |
| `employer_name` | string | |
| `city` | string | |
| `county` | string | optional |
| `state` | string | Two-letter state code (`CA`, `TX`, `FL`, ...) |
| `country` | string | Default `"United States"` |
| `signal_category` | string | `retirement_exit`, `pension_or_account_decision`, `employment_transition`, `business_transition` |
| `signal_headline` | string | |
| `signal_summary` | string | |
| `signal_date` | string | ISO date the event happened/was announced, when known |
| `source_url` | string | Primary source for the signal |
| `connected_urls` | array\<string\> | Supporting/corroborating source URLs |
| `campaign_segment` | string | e.g. `tx-fire-service-signals` — matches the Avina signal naming from `docs/avina-signal-campaign.md` |
| `signal_score` | int | Preserve the source's own score; never invent one |
| `public_email` / `public_phone` | string | optional, when a real public contact path is known |
| `avina_signal_group_id` / `avina_row_id` | string/int | present for Avina-sourced rows, for traceability back to `query_signals` |
| `discovered_at` | string | ISO timestamp when the record was captured into this database |

## Example query patterns

```sql
-- everything in Texas
from leads | where state == 'TX'

-- counts by state and profession group
from leads | count() by state, target_profession_group | sort count desc

-- most recent signals first
from leads | sort signal_date desc | limit 20

-- only fire-service retirements
from leads
| where target_profession_group == 'fire_service' and signal_category == 'retirement_exit'
```
