# CLAUDE.md

Claude Code does not read `AGENTS.md` natively (as of mid-2026), so this file
imports it. Keep the shared, tool-agnostic content in `AGENTS.md`; keep only
Claude-specific notes here.

@AGENTS.md

## Claude-specific notes

- The public contract is `news/calendar.json`. **Never hand-edit anything under
  `news/`** — it is regenerated hourly by GitHub Actions and your edit will be
  overwritten and committed away.
- When asked about "the calendar data", read the stable raw URL or the local
  `news/calendar.json`; do not scrape forexfactory.com.
- Before changing parsing/scraping, run the test suite in `tests/` and validate
  output against `calendar.schema.json`.
- If you add or remove an event field, update `calendar.schema.json`,
  `datapackage.json`, the schema block in `AGENTS.md`, and bump
  `schema_version` — all four, or the contract drifts.

<!--
  Alternative to this import file: symlink so both tools read one file.
    ln -s AGENTS.md CLAUDE.md
  (On Windows, enable Developer Mode or use `git config core.symlinks true`.)
-->
