# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
python3 app.py
```

Runs on http://127.0.0.1:5001 with Flask debug mode enabled.

## Running tests

```bash
pytest
# single test file
pytest tests/test_foo.py
```

## Architecture

This is a Flask app for personal expense tracking, built incrementally as a student project. The codebase is partially stubbed — several features are marked "coming in Step N" and are not yet implemented.

**Request flow:** `app.py` defines all routes → renders Jinja2 templates that extend `templates/base.html` → `static/css/style.css` provides global styles.

**Templates:**
- `base.html` — shared navbar, footer (links to `/terms`, `/privacy`), and script blocks. All pages extend this.
- `landing.html` — public landing page. Has its own `static/css/landing.css` for the hero section and mock UI. Includes a vanilla-JS YouTube modal triggered by "See how it works".
- `login.html`, `register.html` — auth forms (backend not yet implemented).
- `terms.html`, `privacy.html` — static legal pages using `.terms-page` / `.terms-inner` CSS classes from `style.css`.

**CSS split:** `style.css` holds all global styles (variables, navbar, footer, auth, terms). `landing.css` is landing-page-only and is loaded via `{% block head %}`. Hero accent color is `#2ebd76` (overrides the global `--accent: #1a472a`).

**Database:** `database/db.py` is a stub — students implement `get_db()`, `init_db()`, and `seed_db()` using SQLite. Not yet wired into any routes.

**No JS framework** — vanilla JS only. Per-page scripts go in `{% block scripts %}`. Shared JS goes in `static/js/main.js` (currently empty).

**Unimplemented routes** (stubs in `app.py`): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.
