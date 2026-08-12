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
