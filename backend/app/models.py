from sqlalchemy import JSON, Boolean, Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from .db import Base


class Lead(Base):
    """Mirrors db/schema.md at the repo root -- keep both in sync."""

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    target_profession_group = Column(String, nullable=True, index=True)
    employer_name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    county = Column(String, nullable=True)
    state = Column(String, nullable=True, index=True)
    country = Column(String, nullable=True, default="United States")
    signal_category = Column(String, nullable=True)
    signal_headline = Column(String, nullable=True)
    signal_summary = Column(String, nullable=True)
    signal_date = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    connected_urls = Column(JSON, nullable=True, default=list)
    campaign_segment = Column(String, nullable=True, index=True)
    signal_score = Column(Integer, nullable=True)
    public_email = Column(String, nullable=True)
    public_phone = Column(String, nullable=True)
    avina_signal_group_id = Column(String, nullable=True)
    avina_row_id = Column(Integer, nullable=True)
    needs_review = Column(Boolean, nullable=False, default=True)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())


class SignalDef(Base):
    """The 19 Avina signal definitions (1 combined + 18 segments). Seeded
    statically from docs/avina-signal-campaign.md; `last_lead_count` /
    `status` get updated by whatever process runs the rotation
    (see .prime/agent/skills/daily-lead-rotation)."""

    __tablename__ = "signal_defs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_segment = Column(String, unique=True, nullable=False)
    avina_signal_id = Column(String, nullable=False)
    state = Column(String, nullable=True)
    target_profession_group = Column(String, nullable=True)
    status = Column(String, nullable=False, default="queued")  # queued | generating | done | paused
    last_lead_count = Column(Integer, nullable=False, default=0)
    last_run_at = Column(DateTime(timezone=True), nullable=True)


class ScoutSource(Base):
    """Status of each lead-generation source/tool (Avina, Vibe Prospecting,
    Clay, ...) -- backs the "Scout Status" dashboard panel."""

    __tablename__ = "scout_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    detail = Column(String, nullable=True)
    status = Column(String, nullable=False, default="idle")  # good | warning | critical | idle
    status_label = Column(String, nullable=True)
