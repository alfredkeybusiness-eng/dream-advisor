import { renderArticle, renderCategory, renderHome, renderState, CATEGORIES, STATE_NAMES } from "./render.js";

function categorySlug(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-");
}

async function latestSignals(db, limit = 12) {
  const { results } = await db
    .prepare(
      `SELECT * FROM retirement_signals WHERE publication_status = 'PUBLISHED' ORDER BY published_at DESC LIMIT ?`
    )
    .bind(limit)
    .all();
  return results;
}

export default {
  /**
   * @param {Request} request
   * @param {{DB: import('@cloudflare/workers-types').D1Database}} env
   */
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/" || path === "") {
      const rows = await latestSignals(env.DB);
      return new Response(renderHome(rows), {
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }

    const articleMatch = path.match(/^\/article\/([a-z0-9-]+)$/);
    if (articleMatch) {
      const { results } = await env.DB.prepare(
        `SELECT * FROM retirement_signals WHERE slug = ? AND publication_status = 'PUBLISHED' LIMIT 1`
      )
        .bind(articleMatch[1])
        .all();
      return new Response(renderArticle(results[0]), {
        status: results[0] ? 200 : 404,
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }

    const categoryMatch = path.match(/^\/category\/([a-z0-9-]+)$/);
    if (categoryMatch) {
      const slug = categoryMatch[1];
      const categoryName = CATEGORIES.find((c) => categorySlug(c) === slug) || slug;
      const { results } = await env.DB.prepare(
        `SELECT * FROM retirement_signals WHERE category = ? AND publication_status = 'PUBLISHED' ORDER BY published_at DESC`
      )
        .bind(categoryName)
        .all();
      return new Response(renderCategory(slug, categoryName, results), {
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }

    const stateMatch = path.match(/^\/([a-z]+)-retirement-updates$/);
    if (stateMatch) {
      const stateCode = Object.keys(STATE_NAMES).find(
        (code) => STATE_NAMES[code].toLowerCase() === stateMatch[1]
      );
      if (stateCode) {
        const { results } = await env.DB.prepare(
          `SELECT * FROM retirement_signals WHERE state = ? AND publication_status = 'PUBLISHED' ORDER BY published_at DESC`
        )
          .bind(stateCode)
          .all();
        return new Response(renderState(stateCode, results), {
          headers: { "content-type": "text/html; charset=utf-8" },
        });
      }
    }

    if (path === "/api/signals") {
      const rows = await latestSignals(env.DB, 100);
      return Response.json(rows);
    }

    return new Response("Not found", { status: 404 });
  },
};
