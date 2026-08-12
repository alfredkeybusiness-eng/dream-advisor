# Frontend

`public/index.html` is a **functional placeholder** — it fetches every
backend endpoint and dumps the raw JSON, so `render.yaml`'s static site has
something real to deploy. It is not the intended UI.

**Design reference**: a full mockup of the intended dashboard (Signal
Pipeline, Campaign Metrics, Research Queue, Scout Status, Email Outreach,
Calendar/Meetings), built from this campaign's real data, was published as
a Claude artifact — ask in the session that built it for the link, or
regenerate from the same brief (dark/light "Signal Desk" theme: warm ink
paper background, gold/amber accent, status pills for pipeline/scout state,
serif display + system sans + tabular-nums mono for data).

## Replacing the placeholder

Once the real frontend build (OpenCode) lands here:

1. Update `render.yaml`'s frontend service: `buildCommand`,
   `staticPublishPath`, and `rootDir` to match the real build tool's output
   directory.
2. Point it at the backend via the `API_BASE_URL` env var Render already
   injects from `dream-advisor-backend`'s `hostport` (see `render.yaml`) —
   `public/config.js`'s `window.DREAM_ADVISOR_API` pattern is one way to
   consume it without a build step; a real bundler can inject it at build
   time instead.
3. Delete this placeholder `public/` content.
