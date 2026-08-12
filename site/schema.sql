CREATE TABLE retirement_signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL,
  signal_type TEXT NOT NULL,
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  what_happened TEXT NOT NULL,
  why_it_matters TEXT NOT NULL,
  who_may_be_affected TEXT NOT NULL,
  what_to_do TEXT NOT NULL,
  source_url TEXT NOT NULL,
  source_domain TEXT,
  organization_name TEXT,
  state TEXT,
  city TEXT,
  sentiment TEXT NOT NULL DEFAULT 'INFORMATIONAL',
  impact TEXT NOT NULL DEFAULT 'Medium',
  event_date TEXT,
  published_at TEXT NOT NULL,
  discovered_at TEXT NOT NULL,
  publication_status TEXT NOT NULL DEFAULT 'PUBLISHED',
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_signals_state ON retirement_signals(state);
CREATE INDEX idx_signals_category ON retirement_signals(category);
CREATE INDEX idx_signals_published ON retirement_signals(published_at);

-- Dashboard tables (Research Queue, Signal Pipeline, Scout Status). These
-- hold campaign/contact data -- deliberately separate tables from
-- retirement_signals (public article content, no PII) even though they
-- share this database. Never join contact fields into anything /api/signals
-- or the public site pages expose.

CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id TEXT UNIQUE NOT NULL,
  full_name TEXT,
  job_title TEXT,
  target_profession_group TEXT,
  employer_name TEXT,
  city TEXT,
  county TEXT,
  state TEXT,
  country TEXT DEFAULT 'United States',
  signal_category TEXT,
  signal_headline TEXT,
  signal_summary TEXT,
  signal_date TEXT,
  source_url TEXT,
  connected_urls TEXT,
  campaign_segment TEXT,
  signal_score INTEGER,
  public_email TEXT,
  public_phone TEXT,
  avina_signal_group_id TEXT,
  avina_row_id INTEGER,
  needs_review INTEGER NOT NULL DEFAULT 1,
  discovered_at TEXT
);

CREATE TABLE signal_defs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  campaign_segment TEXT UNIQUE NOT NULL,
  avina_signal_id TEXT NOT NULL,
  state TEXT,
  target_profession_group TEXT,
  status TEXT NOT NULL DEFAULT 'queued',
  last_lead_count INTEGER NOT NULL DEFAULT 0,
  last_run_at TEXT
);

CREATE TABLE scout_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  detail TEXT,
  status TEXT NOT NULL DEFAULT 'idle',
  status_label TEXT
);
