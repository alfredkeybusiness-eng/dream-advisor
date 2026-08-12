"""One-time/idempotent seed data: the 19 Avina signal defs, scout-source
status, and the 9 real leads already captured in db/seed/leads_seed.ndjson.

Run automatically on startup (see main.py) -- every insert checks for an
existing row first, so re-running on redeploy is safe.
"""

import json
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Lead, ScoutSource, SignalDef

# Keep in sync with .prime/agent/skills/daily-lead-rotation/src/daily_lead_rotation/segments.py
SEGMENTS = [
    ("ca-education-signals", "e246145f-f130-4408-a2d8-3b4b908f5892", "CA", "education"),
    ("ca-healthcare-signals", "0c9cf148-640a-40bb-a53c-f4615e277e6a", "CA", "nursing"),
    ("ca-physician-signals", "48da55c9-75a8-4d58-896e-15554c88e6b7", "CA", "physician"),
    ("ca-fire-service-signals", "234c917c-0979-4e7d-bf42-8f73751d8871", "CA", "fire_service"),
    ("ca-public-employee-signals", "5efb1c64-f6e9-4a92-94d3-816a4031470c", "CA", "public_employee"),
    ("ca-business-owner-signals", "02f4e747-4330-478d-9871-d512652a624d", "CA", "business_owner"),
    ("tx-education-signals", "7973a449-49cc-4057-b98a-816b0505a5af", "TX", "education"),
    ("tx-healthcare-signals", "f34d678f-0522-45fb-8d01-83eb719bc34f", "TX", "nursing"),
    ("tx-physician-signals", "6824aaf0-52bf-42f1-a236-c53ad598c805", "TX", "physician"),
    ("tx-fire-service-signals", "12999e1f-afe0-4bf2-a7c2-12d7682936ff", "TX", "fire_service"),
    ("tx-public-employee-signals", "3237082f-ec95-4821-a734-37987bed5b2a", "TX", "public_employee"),
    ("tx-business-owner-signals", "c53bbd6b-8b71-4639-92d8-8e27edf74240", "TX", "business_owner"),
    ("fl-education-signals", "18561e17-96da-415a-a1b2-c61e1fd0b099", "FL", "education"),
    ("fl-healthcare-signals", "eb8600af-6f18-4005-96c5-976e65a00da0", "FL", "nursing"),
    ("fl-physician-signals", "b4f52b4a-8a2f-4beb-88db-38b0d1c7c39d", "FL", "physician"),
    ("fl-fire-service-signals", "c96cdb42-8fd5-46c5-8dfe-bf3537df926b", "FL", "fire_service"),
    ("fl-public-employee-signals", "62afe135-cc06-492e-b95f-92cd4b084628", "FL", "public_employee"),
    ("fl-business-owner-signals", "2cea8478-39ac-4023-bafc-333139f787d6", "FL", "business_owner"),
    ("combined-retirement-transition-prospects", "a5f91c4d-bc31-4aeb-9207-f9582c3664e6", None, None),
]

SCOUT_SOURCES = [
    ("Avina — combined signal", "Retirement Transition Prospects", "idle", "Paused"),
    ("Avina — 18-segment rotation", "Prime Agent daily task", "warning", "Awaiting /login"),
    ("Vibe Prospecting", "business-owner segment, validated", "idle", "Paused — 11 credits used"),
    ("Clay", "per-company enrichment", "idle", "Not started"),
    ("Apollo · Exa · Bright Data", "no usable lead-gen tool in this session", "critical", "Unavailable"),
]

SEED_LEADS_PATH = Path(__file__).resolve().parent.parent.parent / "db" / "seed" / "leads_seed.ndjson"


def run_seed(db: Session) -> None:
    if db.query(SignalDef).count() == 0:
        for campaign_segment, avina_signal_id, state, group in SEGMENTS:
            is_combined = campaign_segment.startswith("combined-")
            db.add(
                SignalDef(
                    campaign_segment=campaign_segment,
                    avina_signal_id=avina_signal_id,
                    state=state,
                    target_profession_group=group,
                    status="done" if is_combined else "queued",
                    last_lead_count=9 if is_combined else 0,
                )
            )

    if db.query(ScoutSource).count() == 0:
        for name, detail, status, status_label in SCOUT_SOURCES:
            db.add(ScoutSource(name=name, detail=detail, status=status, status_label=status_label))

    if db.query(Lead).count() == 0 and SEED_LEADS_PATH.exists():
        with open(SEED_LEADS_PATH) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                db.add(
                    Lead(
                        lead_id=row["lead_id"],
                        full_name=row.get("full_name"),
                        job_title=row.get("job_title"),
                        target_profession_group=row.get("target_profession_group"),
                        employer_name=row.get("employer_name"),
                        city=row.get("city"),
                        county=row.get("county"),
                        state=row.get("state"),
                        country=row.get("country", "United States"),
                        signal_category=row.get("signal_category"),
                        signal_headline=row.get("signal_headline"),
                        signal_summary=row.get("signal_summary"),
                        signal_date=row.get("signal_date"),
                        source_url=row.get("source_url"),
                        connected_urls=row.get("connected_urls", []),
                        campaign_segment=row.get("campaign_segment"),
                        signal_score=row.get("signal_score"),
                        avina_signal_group_id=row.get("avina_signal_group_id"),
                        avina_row_id=row.get("avina_row_id"),
                        needs_review=True,
                    )
                )

    db.commit()
