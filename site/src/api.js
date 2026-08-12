// JSON API for the dashboard (Signal Pipeline, Campaign Metrics, Research
// Queue, Scout Status, Email Outreach, Calendar/Meetings) -- this is the
// contract the frontend build (OpenCode) consumes. Content-only routes
// (site homepage, /article/:slug, etc.) live in index.js + render.js and
// never touch these tables' contact fields.

function json(data, init = {}) {
  return Response.json(data, {
    ...init,
    headers: { "access-control-allow-origin": "*", ...(init.headers || {}) },
  });
}

function parseJsonArray(s) {
  try {
    return JSON.parse(s || "[]");
  } catch {
    return [];
  }
}

function leadOut(r) {
  return {
    lead_id: r.lead_id,
    full_name: r.full_name,
    job_title: r.job_title,
    employer_name: r.employer_name,
    city: r.city,
    state: r.state,
    target_profession_group: r.target_profession_group,
    signal_category: r.signal_category,
    signal_headline: r.signal_headline,
    signal_summary: r.signal_summary,
    signal_date: r.signal_date,
    source_url: r.source_url,
    connected_urls: parseJsonArray(r.connected_urls),
    campaign_segment: r.campaign_segment,
    signal_score: r.signal_score,
    public_email: r.public_email,
    public_phone: r.public_phone,
    needs_review: !!r.needs_review,
  };
}

export async function campaignMetrics(db) {
  const { results: leads } = await db.prepare(`SELECT * FROM leads`).all();
  const { results: signals } = await db.prepare(`SELECT count(*) AS n FROM signal_defs`).all();

  const byState = {};
  const byGroup = {};
  let contactReady = 0;
  let flagged = 0;
  for (const l of leads) {
    if (l.state) byState[l.state] = (byState[l.state] || 0) + 1;
    if (l.target_profession_group) byGroup[l.target_profession_group] = (byGroup[l.target_profession_group] || 0) + 1;
    if (l.public_email || l.public_phone) contactReady++;
    if (l.needs_review) flagged++;
  }

  return json({
    leads_captured: leads.length,
    signals_configured: signals[0]?.n ?? 0,
    contact_ready: contactReady,
    flagged_for_review: flagged,
    leads_by_state: byState,
    leads_by_profession_group: byGroup,
  });
}

export async function signalPipeline(db) {
  const { results } = await db
    .prepare(`SELECT * FROM signal_defs ORDER BY state IS NULL, state, campaign_segment`)
    .all();
  return json(
    results.map((r) => ({
      campaign_segment: r.campaign_segment,
      avina_signal_id: r.avina_signal_id,
      state: r.state,
      target_profession_group: r.target_profession_group,
      status: r.status,
      last_lead_count: r.last_lead_count,
      last_run_at: r.last_run_at,
    }))
  );
}

export async function researchQueue(db, url) {
  const needsReview = url.searchParams.get("needs_review");
  let q = `SELECT * FROM leads`;
  const binds = [];
  if (needsReview !== null) {
    q += ` WHERE needs_review = ?`;
    binds.push(needsReview === "true" ? 1 : 0);
  }
  q += ` ORDER BY signal_date DESC`;
  const { results } = await db.prepare(q).bind(...binds).all();
  return json(results.map(leadOut));
}

export async function upsertLead(db, request) {
  const body = await request.json();
  if (!body.lead_id) {
    return json({ error: "lead_id is required" }, { status: 400 });
  }
  const cols = [
    "lead_id", "full_name", "job_title", "target_profession_group", "employer_name",
    "city", "county", "state", "country", "signal_category", "signal_headline",
    "signal_summary", "signal_date", "source_url", "connected_urls", "campaign_segment",
    "signal_score", "public_email", "public_phone", "avina_signal_group_id",
    "avina_row_id", "needs_review", "discovered_at",
  ];
  const values = cols.map((c) => {
    if (c === "connected_urls") return JSON.stringify(body.connected_urls || []);
    if (c === "needs_review") return body.needs_review === false ? 0 : 1;
    if (c === "country") return body.country ?? "United States";
    return body[c] ?? null;
  });
  const placeholders = cols.map(() => "?").join(",");
  const updateClause = cols.filter((c) => c !== "lead_id").map((c) => `${c} = excluded.${c}`).join(", ");
  await db
    .prepare(
      `INSERT INTO leads (${cols.join(",")}) VALUES (${placeholders})
       ON CONFLICT(lead_id) DO UPDATE SET ${updateClause}`
    )
    .bind(...values)
    .run();
  return json({ ok: true });
}

export async function scoutStatus(db) {
  const { results } = await db.prepare(`SELECT * FROM scout_sources ORDER BY id`).all();
  return json(
    results.map((r) => ({ name: r.name, detail: r.detail, status: r.status, status_label: r.status_label }))
  );
}

export async function emailOutreach() {
  // No Avina automation/sequence built yet -- see docs/architecture.md.
  return json({ configured: false, sequences: [] });
}

export async function meetings() {
  // No outreach is live yet, so nothing has been booked.
  return json({ meetings: [] });
}
