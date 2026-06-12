# AGENTS.md

Cross-tool instructions for AI coding agents (Codex, Cursor, Gemini CLI,
Windsurf, Continue, etc.). Claude Code reads `CLAUDE.md`, which imports this
file — see `CLAUDE.md`.

## What this repo is

A Python scraper (`ff_calendar_toolkit`) that pulls the Forex Factory economic
calendar into structured CSV/JSON and fires rule-based pre-event alerts.

A GitHub Actions workflow (`.github/workflows/scrape.yml`, cron `0 * * * *`)
re-scrapes **every hour** and commits the refreshed data back to `main`.

**Do not hand-edit any file under `news/`.** It is machine-generated and will be
overwritten on the next run. To change output, edit the scraper / `config.yaml`.

## Published data feed

| File | Role |
| --- | --- |
| `news/calendar.json` | Canonical consolidated feed, refreshed hourly. **Consume this.** |
| `news/calendar.csv`  | Same rows, flat CSV (confirm path; CSV is emitted when `output_format: both`). |
| `calendar.schema.json` | JSON Schema (draft 2020-12) for `news/calendar.json`. |
| `datapackage.json` | Frictionless Data Package describing both resources. |
| `news/last_run/`, `news/monthly/`, `news/history/` | Internal storage tiers, not the public contract. |

### Stable raw URL (read this, do not re-scrape Forex Factory)

```
https://raw.githubusercontent.com/joor0x/forex-factory-agent-feed/main/news/calendar.json
```

`raw.githubusercontent.com` is CDN-cached ~5 min — fine for an hourly feed.
Scraping Forex Factory directly is rate-limited and against their ToS; always
prefer this URL.

## Schema — read before parsing

`news/calendar.json` is a JSON array of event objects:

```json
{
  "time": "10:30",
  "timezone": "Asia/Karachi",
  "currency": "USD",
  "impact": "red",
  "impact_level": "high",
  "event": "Core CPI m/m",
  "detail": "https://www.forexfactory.com/calendar?month=June#detail=148363",
  "actual": "0.2%",
  "forecast": null,
  "previous": null,
  "day": "Wed",
  "date": "10/06/2026",
  "datetime_utc": "2026-06-10T05:30:00Z",
  "scraped_at": "2026-06-12T08:12:37.721712+00:00"
}
```

Gotchas an agent **will** get wrong without this section:

- `time` + `date` are in **`Asia/Karachi` (UTC+5)** — the value of the
  `timezone` field — NOT UTC and NOT the consumer's local time.
- `date` is **`dd/mm/yyyy`** (`10/06/2026` = 10 June, not 6 October). Not ISO.
- `time` is `HH:MM` (24h) **or** a literal string like `"All Day"` or `"Tentative"`. Handle the non-timed cases explicitly.
- `impact` is a **colour code** (`red`, `orange`, `yellow`, `gray`).
- `impact_level` is a **semantic level**: `high` = red, `medium` = orange,
  `low` = yellow, `holiday` = gray. Use this for filtering instead of parsing colors.
- `actual` is a string (e.g. `"4.2%"`, `"172K"`) and is `""` when the figure has not been released yet.
- `forecast` / `previous` are strings when present, and `null` (not `""`) when absent.
- `datetime_utc` is a single **ISO-8601 UTC timestamp** (e.g. `"2026-06-10T05:30:00Z"`). It is `null` for non-timed events like "All Day" or "Tentative". **Consume this directly** to avoid timezone math!
- `scraped_at` is the ISO-8601 / UTC snapshot freshness timestamp.
- The `news/calendar.json` schema differs from the field table in `README.md`
  (which is stale). This file and `calendar.schema.json` are authoritative.

## How agents should use the feed

- Fetch the raw URL above; validate against `calendar.schema.json` if unsure.
- "What's coming up": filter `impact_level == "high"`, and use the `datetime_utc` value directly.
- Check `scraped_at` to know how fresh the snapshot is before acting on it.

## Feed improvements (implemented in schema version 2)

We implemented key readability improvements:
- A single `datetime_utc` ISO-8601 field per event.
- `null` emitted instead of `""` for missing `forecast`/`previous` in JSON.
- A semantic `impact_level` (`high`/`medium`/`low`/`holiday`) alongside the colour.

## Repo conventions

- Python, package layout under `ff_calendar_toolkit/`, CLI via
  `python -m ff_calendar_toolkit.cli <cmd>`.
- Config precedence: CLI flags > env vars > `config.yaml` > defaults.
- Secrets live in `.env` (see `.env.example`), never commit them.
- Tests in `tests/`; run them before changing scraper/parsing logic.
