"""Daily lead-rotation task: pick the next un-generated Avina segment signal
(see segments.py), generate its leads, and load the normalized results into
the local SuperDB `leads` pool (see db/ at the repo root).

Requires, in the running Prime Agent session:
  - the `avina` skill logged in (`/login` -> MCP Connections -> avina)
  - a `super db serve` instance reachable at LEADS_DB_URL (default
    http://localhost:9867) -- see db/serve.sh at the repo root
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from datetime import datetime, timezone

import superdb

import avina

from .segments import LEADS_PER_RUN, SEGMENTS, WORKSPACE

_MD_LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^\s)]+)\)")
_BARE_URL_RE = re.compile(r"(?<!\()https?://[^\s)\]]+")


def _extract_urls(text: str) -> list[str]:
    urls = _MD_LINK_RE.findall(text or "")
    urls += _BARE_URL_RE.findall(text or "")
    seen: list[str] = []
    for u in urls:
        if u not in seen:
            seen.append(u)
    return seen


async def _segment_has_leads(signal_id: str) -> bool:
    result = await avina.query_signals(
        filters=[{"field": "signal_group_id", "op": "=", "value": signal_id}],
        limit=1,
        workspace=WORKSPACE,
    )
    return bool(result.get("results"))


def _normalize(row: dict, segment) -> dict:
    account = row.get("account") or {}
    urls = _extract_urls(row.get("content", ""))
    return {
        "lead_id": f"avina-{row['id']}",
        # NOT extracted automatically: freeform text (header/content) can name
        # multiple people (a retiree and their successor, e.g.) and a wrong
        # regex/name guess would silently mislabel the record. Leave for a
        # manual or LLM review pass rather than fabricate.
        "full_name": None,
        "job_title": None,
        "target_profession_group": segment.target_profession_group,
        "employer_name": account.get("name"),
        "state": segment.state,
        "country": "United States",
        "signal_category": None,  # not a structured Avina field; infer on review
        "signal_headline": row.get("header"),
        "signal_summary": row.get("content"),
        "signal_date": row.get("trigger_date"),
        "source_url": urls[0] if urls else None,
        "connected_urls": urls[1:],
        "campaign_segment": segment.campaign_segment,
        "signal_score": row.get("score"),
        "avina_signal_group_id": segment.signal_id,
        "avina_row_id": row.get("id"),
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "needs_review": True,
    }


async def run(dry_run: bool = False, poll_seconds: int = 15, max_polls: int = 40) -> str:
    """Run one rotation step: generate leads for the next un-run segment and
    load them into the local SuperDB `leads` pool.

    Args:
        dry_run: pick the segment and report it, but don't call
            request_more_leads or write to the database.
        poll_seconds: delay between signal_generation_status polls.
        max_polls: give up waiting after this many polls (generation keeps
            running server-side; a later run will pick up the results).
    """
    next_segment = None
    for segment in SEGMENTS:
        if not await _segment_has_leads(segment.signal_id):
            next_segment = segment
            break

    if next_segment is None:
        return "Rotation complete: all 18 segments have at least one lead batch. Nothing to do."

    if dry_run:
        return f"Would generate leads for {next_segment.campaign_segment} ({next_segment.signal_id})."

    await avina.request_more_leads(
        signal_id=next_segment.signal_id, count=LEADS_PER_RUN, workspace=WORKSPACE
    )

    for _ in range(max_polls):
        status = await avina.signal_generation_status(
            signal_id=next_segment.signal_id, workspace=WORKSPACE
        )
        if not status.get("generation_in_progress"):
            break
        await asyncio.sleep(poll_seconds)

    result = await avina.query_signals(
        filters=[{"field": "signal_group_id", "op": "=", "value": next_segment.signal_id}],
        includes=["account", "contacts"],
        limit=100,
        workspace=WORKSPACE,
    )
    rows = result.get("results", [])
    records = [_normalize(row, next_segment) for row in rows]

    if records:
        db_url = os.environ.get("LEADS_DB_URL", "http://localhost:9867")
        client = superdb.Client(db_url)
        ndjson = "\n".join(json.dumps(r) for r in records)
        client.load(
            "leads",
            ndjson.encode("utf-8"),
            commit_body=f"daily-lead-rotation: {next_segment.campaign_segment}",
            mime_type="application/json",
        )

    return (
        f"Generated and loaded {len(records)} lead(s) for {next_segment.campaign_segment} "
        f"into the leads pool. needs_review=true on every row (full_name/job_title/"
        f"signal_category weren't auto-extracted from freeform text)."
    )
