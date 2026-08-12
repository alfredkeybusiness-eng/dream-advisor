const STATE_NAMES = {
  CA: "California",
  TX: "Texas",
  FL: "Florida",
  NV: "Nevada",
  AZ: "Arizona",
};

const STATE_BADGE_COLOR = {
  CA: "#a855c9",
  TX: "#3b82f6",
  FL: "#f59e0b",
  NV: "#10b981",
  AZ: "#ef4444",
};

const IMPACT_COLOR = { High: "#f97066", Medium: "#f5b942", Low: "#7dd3a8" };

const CATEGORIES = [
  "Pension Updates",
  "Teacher Retirement",
  "Public Employee Retirement",
  "Medicare",
  "Social Security",
  "403(b)",
  "Retirement Deadlines",
  "Employer Benefits",
  "Executive Retirement",
  "Business Succession",
  "Market & Retirement",
];

function escapeHtml(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

function layout({ title, description, body }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<meta name="description" content="${escapeHtml(description)}">
<style>
  :root {
    --bg: #0a0f1c;
    --surface: #111a2e;
    --surface-2: #17233d;
    --border: #24304d;
    --ink: #eef2fb;
    --ink-muted: #9aa8c7;
    --ink-faint: #6b7897;
    --accent: #3b82f6;
    --accent-ink: #dbe8ff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.5;
  }
  a { color: inherit; text-decoration: none; }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px; }
  header.site {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 0; border-bottom: 1px solid var(--border);
  }
  header.site .brand { font-weight: 700; font-size: 16px; letter-spacing: -0.01em; }
  header.site nav a { font-size: 13px; color: var(--ink-muted); margin-left: 20px; }
  header.site nav a:hover { color: var(--ink); }

  .hero {
    background: radial-gradient(ellipse at top, #16223f 0%, var(--bg) 70%);
    padding: 64px 0 48px;
    text-align: center;
    border-bottom: 1px solid var(--border);
  }
  .hero h1 { font-size: 34px; margin: 0 0 14px; text-wrap: balance; letter-spacing: -0.01em; }
  .hero p.sub { color: var(--ink-muted); font-size: 15px; max-width: 46ch; margin: 0 auto 26px; }
  .cta-row { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
  .btn {
    display: inline-block; padding: 11px 20px; border-radius: 8px; font-size: 13.5px; font-weight: 600;
  }
  .btn.primary { background: var(--accent); color: #fff; }
  .btn.secondary { background: var(--surface-2); color: var(--ink); border: 1px solid var(--border); }

  section { padding: 40px 0; }
  section h2 { font-size: 18px; margin: 0 0 18px; }
  .eyebrow { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-faint); margin-bottom: 4px; }

  .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
  .card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
    padding: 18px; display: flex; flex-direction: column; gap: 8px;
  }
  .badge {
    display: inline-flex; align-items: center; font-size: 10.5px; font-weight: 700;
    letter-spacing: 0.04em; padding: 3px 9px; border-radius: 999px; color: #0a0f1c;
    align-self: flex-start;
  }
  .card h3 { font-size: 15px; margin: 4px 0 2px; line-height: 1.35; text-wrap: balance; }
  .card .meta { font-size: 11.5px; color: var(--ink-faint); }
  .card .affected { font-size: 12.5px; color: var(--ink-muted); }
  .card .affected b { color: var(--ink); font-weight: 600; }
  .card .impact { font-size: 12px; font-weight: 700; }
  .card .read { font-size: 12.5px; color: var(--accent); font-weight: 600; margin-top: auto; }

  .pill-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .pill {
    font-size: 12.5px; padding: 7px 13px; border-radius: 999px;
    background: var(--surface-2); border: 1px solid var(--border); color: var(--ink-muted);
  }
  .pill:hover { color: var(--ink); border-color: var(--accent); }

  .state-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }
  .state-grid a { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 12px 14px; font-size: 13px; }
  .state-grid a:hover { border-color: var(--accent); }

  article.detail { padding: 40px 0 70px; }
  article.detail h1 { font-size: 26px; margin: 6px 0 10px; text-wrap: balance; }
  article.detail .meta { color: var(--ink-faint); font-size: 12.5px; margin-bottom: 24px; }
  article.detail h2 { font-size: 14px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink-faint); margin: 26px 0 8px; }
  article.detail p { font-size: 15px; color: var(--ink); margin: 0; }
  article.detail .affected-list { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
  article.detail .affected-list span { background: var(--surface-2); border: 1px solid var(--border); border-radius: 999px; padding: 5px 12px; font-size: 12.5px; }
  article.detail .source { margin-top: 30px; padding-top: 20px; border-top: 1px solid var(--border); font-size: 13px; }
  article.detail .source a { color: var(--accent); }

  footer.site { border-top: 1px solid var(--border); padding: 26px 0; font-size: 12px; color: var(--ink-faint); text-align: center; }

  .empty { color: var(--ink-faint); font-size: 13.5px; padding: 20px 0; }
</style>
</head>
<body>
  <div class="wrap">
    <header class="site">
      <a class="brand" href="/">Retirement Intelligence</a>
      <nav>
        <a href="/#today">Today's Updates</a>
        <a href="/#categories">Categories</a>
        <a href="/#states">States</a>
      </nav>
    </header>
  </div>
  ${body}
  <footer class="site">dream-advisor &middot; retirement intelligence, sourced and verified &middot; not financial advice</footer>
</body>
</html>`;
}

function card(row) {
  const stateColor = STATE_BADGE_COLOR[row.state] || "#3b82f6";
  const impactColor = IMPACT_COLOR[row.impact] || IMPACT_COLOR.Medium;
  let affected = [];
  try {
    affected = JSON.parse(row.who_may_be_affected || "[]");
  } catch {
    affected = [];
  }
  return `<a class="card" href="/article/${escapeHtml(row.slug)}">
    <span class="badge" style="background:${stateColor}">${escapeHtml(row.state || row.category)}</span>
    <h3>${escapeHtml(row.title)}</h3>
    <div class="meta">Updated: ${escapeHtml(row.published_at)}</div>
    <div class="affected"><b>Who may be affected:</b> ${escapeHtml((affected[0]) || row.category)}</div>
    <div class="impact" style="color:${impactColor}">Impact: ${escapeHtml(row.impact)}</div>
    <div class="read">Read Update &rarr;</div>
  </a>`;
}

export function renderHome(rows) {
  const cards = rows.length
    ? rows.map(card).join("\n")
    : `<div class="empty">No verified signals published yet.</div>`;

  const states = Object.keys(STATE_NAMES)
    .map((code) => `<a href="/${code.toLowerCase()}-retirement-updates">${STATE_NAMES[code]}<br><span style="color:var(--ink-faint);font-size:11.5px;">retirement updates</span></a>`)
    .join("\n");

  const categories = CATEGORIES.map(
    (c) => `<a class="pill" href="/category/${encodeURIComponent(c.toLowerCase().replace(/[^a-z0-9]+/g, "-"))}">${escapeHtml(c)}</a>`
  ).join("\n");

  const body = `
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">Retirement Intelligence</div>
      <h1>Retirement Changes Are Happening Every Day.</h1>
      <p class="sub">Understand what changed, who may be affected, and what you should consider next.</p>
      <div class="cta-row">
        <a class="btn primary" href="/get-clarification">Get Retirement Clarification</a>
        <a class="btn secondary" href="#today">View Today's Updates</a>
      </div>
    </div>
  </section>
  <div class="wrap">
    <section id="today">
      <h2>Today's Retirement Intelligence</h2>
      <div class="card-grid">${cards}</div>
    </section>
    <section id="categories">
      <h2>Browse by Category</h2>
      <div class="pill-row">${categories}</div>
    </section>
    <section id="states">
      <h2>State Intelligence Pages</h2>
      <div class="state-grid">${states}</div>
    </section>
  </div>`;

  return layout({
    title: "Retirement Intelligence That Keeps You Ahead",
    description: "Verified retirement, pension, and benefit signals for CA, TX, FL and beyond — updated as they happen.",
    body,
  });
}

export function renderCategory(categorySlug, categoryName, rows) {
  const cards = rows.length
    ? rows.map(card).join("\n")
    : `<div class="empty">No verified signals in this category yet.</div>`;
  const body = `<div class="wrap"><section>
    <div class="eyebrow">Category</div>
    <h2 style="font-size:24px;">${escapeHtml(categoryName)}</h2>
    <div class="card-grid">${cards}</div>
  </section></div>`;
  return layout({
    title: `${categoryName} — Retirement Intelligence`,
    description: `Verified ${categoryName.toLowerCase()} signals.`,
    body,
  });
}

export function renderState(stateCode, rows) {
  const name = STATE_NAMES[stateCode] || stateCode;
  const cards = rows.length
    ? rows.map(card).join("\n")
    : `<div class="empty">No verified ${escapeHtml(name)} signals yet.</div>`;
  const body = `<div class="wrap"><section>
    <div class="eyebrow">State Intelligence</div>
    <h2 style="font-size:24px;">${escapeHtml(name)} Retirement Updates</h2>
    <div class="card-grid">${cards}</div>
  </section></div>`;
  return layout({
    title: `${name} Retirement Updates`,
    description: `Latest verified retirement, pension, and benefit signals affecting ${name}.`,
    body,
  });
}

export function renderArticle(row) {
  if (!row) {
    return layout({
      title: "Not found",
      description: "",
      body: `<div class="wrap"><div class="empty">That update wasn't found.</div></div>`,
    });
  }
  let affected = [];
  try {
    affected = JSON.parse(row.who_may_be_affected || "[]");
  } catch {
    affected = [];
  }
  const impactColor = IMPACT_COLOR[row.impact] || IMPACT_COLOR.Medium;
  const body = `<div class="wrap"><article class="detail">
    <div class="eyebrow">${escapeHtml(row.category)} &middot; ${escapeHtml(row.state || "")}</div>
    <h1>${escapeHtml(row.title)}</h1>
    <div class="meta">Published ${escapeHtml(row.published_at)} &middot; <span style="color:${impactColor}">Impact: ${escapeHtml(row.impact)}</span></div>

    <h2>What Happened</h2>
    <p>${escapeHtml(row.what_happened)}</p>

    <h2>Why It Matters</h2>
    <p>${escapeHtml(row.why_it_matters)}</p>

    <h2>Who May Be Affected</h2>
    <div class="affected-list">${affected.map((a) => `<span>${escapeHtml(a)}</span>`).join("")}</div>

    <h2>What To Do</h2>
    <p>${escapeHtml(row.what_to_do)}</p>

    <div class="source">Source: <a href="${escapeHtml(row.source_url)}" rel="noopener nofollow">${escapeHtml(row.source_domain || row.source_url)}</a></div>
  </article></div>`;
  return layout({ title: row.title, description: row.what_happened, body });
}

export { CATEGORIES, STATE_NAMES };
