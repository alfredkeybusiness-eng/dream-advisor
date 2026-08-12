from collections import Counter
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine, get_db
from .models import Lead, ScoutSource, SignalDef
from .seed import run_seed

Base.metadata.create_all(bind=engine)

app = FastAPI(title="dream-advisor backend")

# The frontend is a separate static site (see render.yaml) on its own
# origin -- wide open for now since there's no auth yet; tighten before
# handling anything beyond this campaign's own read-mostly data.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_on_startup() -> None:
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/campaign-metrics")
def campaign_metrics(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    by_state = Counter(l.state for l in leads if l.state)
    by_group = Counter(l.target_profession_group for l in leads if l.target_profession_group)
    return {
        "leads_captured": len(leads),
        "signals_configured": db.query(SignalDef).count(),
        "contact_ready": sum(1 for l in leads if l.public_email or l.public_phone),
        "flagged_for_review": sum(1 for l in leads if l.needs_review),
        "leads_by_state": dict(by_state),
        "leads_by_profession_group": dict(by_group),
    }


@app.get("/api/signals")
def signal_pipeline(db: Session = Depends(get_db)):
    rows = db.query(SignalDef).order_by(SignalDef.state.is_(None), SignalDef.state, SignalDef.campaign_segment).all()
    return [
        {
            "campaign_segment": r.campaign_segment,
            "avina_signal_id": r.avina_signal_id,
            "state": r.state,
            "target_profession_group": r.target_profession_group,
            "status": r.status,
            "last_lead_count": r.last_lead_count,
            "last_run_at": r.last_run_at.isoformat() if r.last_run_at else None,
        }
        for r in rows
    ]


@app.get("/api/leads")
def research_queue(needs_review: Optional[bool] = None, db: Session = Depends(get_db)):
    q = db.query(Lead)
    if needs_review is not None:
        q = q.filter(Lead.needs_review == needs_review)
    rows = q.order_by(Lead.signal_date.desc()).all()
    return [
        {
            "lead_id": r.lead_id,
            "full_name": r.full_name,
            "job_title": r.job_title,
            "employer_name": r.employer_name,
            "city": r.city,
            "state": r.state,
            "target_profession_group": r.target_profession_group,
            "signal_category": r.signal_category,
            "signal_headline": r.signal_headline,
            "signal_date": r.signal_date,
            "source_url": r.source_url,
            "campaign_segment": r.campaign_segment,
            "signal_score": r.signal_score,
            "public_email": r.public_email,
            "public_phone": r.public_phone,
            "needs_review": r.needs_review,
        }
        for r in rows
    ]


class LeadIn(BaseModel):
    lead_id: str
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    target_profession_group: Optional[str] = None
    employer_name: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "United States"
    signal_category: Optional[str] = None
    signal_headline: Optional[str] = None
    signal_summary: Optional[str] = None
    signal_date: Optional[str] = None
    source_url: Optional[str] = None
    connected_urls: Optional[list[str]] = None
    campaign_segment: Optional[str] = None
    signal_score: Optional[int] = None
    public_email: Optional[str] = None
    public_phone: Optional[str] = None
    avina_signal_group_id: Optional[str] = None
    avina_row_id: Optional[int] = None
    needs_review: bool = True


@app.post("/api/leads")
def upsert_lead(lead: LeadIn, db: Session = Depends(get_db)):
    """Idempotent upsert by lead_id -- the daily-lead-rotation task (or any
    other source) posts here to land rows in Postgres, same shape as
    db/schema.md."""
    existing = db.query(Lead).filter(Lead.lead_id == lead.lead_id).first()
    data = lead.model_dump()
    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
    else:
        db.add(Lead(**data))
    db.commit()
    return {"ok": True}


@app.get("/api/scout-status")
def scout_status(db: Session = Depends(get_db)):
    rows = db.query(ScoutSource).all()
    return [
        {"name": r.name, "detail": r.detail, "status": r.status, "status_label": r.status_label}
        for r in rows
    ]


@app.get("/api/outreach")
def email_outreach():
    # No Avina automation/sequence has been built yet -- see
    # docs/avina-signal-campaign.md. Placeholder shape for the frontend.
    return {"configured": False, "sequences": []}


@app.get("/api/meetings")
def meetings():
    # No outreach is live yet, so nothing has been booked. Placeholder
    # shape for the frontend.
    return {"meetings": []}
