---
name: avina
description: MCP integration for the Avina.io signal/lead platform (query_signals, request_more_leads, list_signals, etc). Use when the daily-lead-rotation skill or the user needs to read or generate leads from the "Dailysolutions" Avina workspace.
---

# Avina MCP integration

Thin `McpIntegration` wrapper around `https://api.avina.io/mcp`. One-time
setup per machine:

```
/login
```

then choose **MCP Connections** → **avina**, complete the OAuth flow in the
browser. `/mcp` shows connection status; `/mcp login avina` / `/mcp logout avina`
also work from the CLI.

Once connected:

```python
import avina

for tool in await avina.list_tools():
    print(tool["name"], "-", tool["description"])

help(avina.query_signals)

rows = await avina.query_signals(
    filters=[{"field": "signal_group_id", "op": "=", "value": "<signal_id>"}],
    limit=25,
)
```

All 19 signal ids for the CA/TX/FL x 6-profession-group retirement/transition
campaign (plus the combined signal) are recorded in
`../daily-lead-rotation/src/daily_lead_rotation/segments.py` and in
`docs/avina-signal-campaign.md` at the repo root — this skill is just the
transport, not the campaign logic.

A call before `/login` raises `rlm.NotEnabled`.
