---
name: spendly-ui
description: Generate UI components, pages, and partials for the Spendly personal expense tracker (Flask + Jinja2 + vanilla CSS, no frameworks). Use this skill whenever the user asks to build, design, scaffold, or modify any Spendly UI — dashboards, KPI cards, transaction tables, budget views, AI chat surfaces, forms, empty states, or full pages. Trigger this even if the user just says "add a page to spendly", "make a transactions view", "design a dashboard for spendly", or references files like base.html, style.css, or templates/. Do NOT use React, Tailwind, Bootstrap, or any framework — Spendly is strictly Flask/Jinja2/vanilla CSS/vanilla JS.
---

# Spendly UI

Generate UI for the Spendly Flask app. Spendly is a personal expense tracker built incrementally as a student project. The codebase is Flask + Jinja2 + vanilla CSS + vanilla JS — **no frameworks, ever**.

## When this skill applies

- Building any new template, partial, or page for Spendly
- Adding a UI feature (dashboard, transactions list, budget tracker, AI chat, etc.)
- Restyling or extending existing Spendly pages
- Creating reusable Jinja macros (KPI cards, transaction rows, progress bars)
- Wiring per-page CSS or vanilla JS

If the user is working on Spendly and the request touches a `.html`, `.css`, or `templates/` path — this skill applies.

## Hard rules — never violate

1. **No frameworks.** No React, Vue, Tailwind, Bootstrap, Material UI, jQuery. Vanilla HTML/CSS/JS only.
2. **No CDN UI libs.** No Bootstrap CSS, no Font Awesome, no Tailwind Play CDN. Inline SVG for icons; system fonts only unless the user opts in to a Google Font.
3. **All pages extend `base.html`.** Use `{% extends "base.html" %}` with `{% block content %}`, `{% block head %}` (per-page CSS), `{% block scripts %}` (per-page JS).
4. **Global CSS lives in `static/css/style.css`.** Page-specific CSS goes in its own file (e.g., `static/css/dashboard.css`) and is loaded via `{% block head %}`. Never inline `<style>` blocks in templates.
5. **Use the design tokens.** Reference CSS variables from `style.css` (see "Design system" below). Don't hardcode colors, spacing, or radii in page CSS — extend the system.
6. **Vanilla JS only**, scoped in `{% block scripts %}`. Shared JS goes in `static/js/main.js`.
7. **Routes are defined in `app.py`.** When proposing a new page, also state which route renders it and what context variables it needs.

## Project layout (memorize this)

```
spendly/
├── app.py                  # All Flask routes
├── database/db.py          # SQLite stubs (get_db, init_db, seed_db)
├── templates/
│   ├── base.html           # Shared navbar + footer + blocks
│   ├── landing.html        # Public landing page
│   ├── login.html, register.html
│   ├── terms.html, privacy.html
│   └── ... (add new pages here)
└── static/
    ├── css/
    │   ├── style.css       # Global tokens + shared styles
    │   ├── landing.css     # Page-specific
    │   └── ... (one CSS file per page that needs it)
    └── js/
        └── main.js         # Shared JS (currently empty)
```

App runs on `http://127.0.0.1:5001` via `python3 app.py`.

## Design system (Spendly-native)

These are **the** Spendly tokens. Establish them in `style.css` if not already present, and reference them everywhere else. Do not deviate.

### Color palette

```css
:root {
  /* Brand */
  --accent: #1a472a;          /* Deep Spendly green — primary brand */
  --accent-bright: #2ebd76;   /* Brighter green — hero/CTA highlights */
  --accent-soft: #e8f5ee;     /* Tinted background for accent surfaces */

  /* Neutrals */
  --bg: #fafaf7;              /* Page background — warm off-white */
  --surface: #ffffff;         /* Cards, modals */
  --surface-2: #f4f4ef;       /* Sunken surfaces, table stripes */
  --border: #e5e5e0;
  --text: #1a1a1a;
  --text-muted: #6b6b6b;
  --text-subtle: #9a9a9a;

  /* Semantic — financial */
  --income: #2ebd76;          /* Positive amounts, income */
  --expense: #d94e4e;         /* Negative amounts, expenses */
  --warning: #e0a93a;         /* Over-budget, alerts */
  --info: #4a7fb8;            /* Neutral informational */

  /* Elevation */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 2px 8px rgba(0,0,0,0.06);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
}

[data-theme="dark"] {
  --bg: #0f1410;
  --surface: #1a201c;
  --surface-2: #232a26;
  --border: #2e3631;
  --text: #f0f0ec;
  --text-muted: #a8a8a4;
  --text-subtle: #6e6e6a;
  --accent-soft: #1f3328;
}
```

### Spacing scale (4px base)

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;
}
```

Use these tokens — never raw px values for spacing.

### Typography

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;

  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 22px;
  --text-2xl: 28px;
  --text-3xl: 36px;

  --leading-tight: 1.2;
  --leading-normal: 1.5;
}
```

**Financial numbers** always use `font-variant-numeric: tabular-nums;` so digits align in tables.

### Radii & borders

```css
:root {
  --radius-sm: 6px;
  --radius-md: 8px;     /* default for buttons, inputs */
  --radius-lg: 12px;    /* default for cards */
  --radius-xl: 20px;    /* hero sections */
  --radius-full: 999px; /* pills, avatars */
}
```

### Motion

```css
:root {
  --transition-fast: 120ms ease;
  --transition-base: 200ms ease;
}
```

Hover/focus states should use `var(--transition-base)`. Respect `@media (prefers-reduced-motion: reduce)`.

## Component patterns

When asked for a component, follow these blueprints. Keep markup semantic (`<section>`, `<article>`, `<nav>`, `<button>`, real headings).

### Page scaffold

Every new page starts here:

```jinja
{% extends "base.html" %}

{% block title %}Dashboard · Spendly{% endblock %}

{% block head %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
{% endblock %}

{% block content %}
<main class="page page-dashboard">
  <header class="page-header">
    <h1>Dashboard</h1>
    <p class="page-subtitle">Your money at a glance.</p>
  </header>

  {# sections here #}
</main>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/dashboard.js') }}" defer></script>
{% endblock %}
```

Always state the matching `app.py` route alongside the template. Example:

```python
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", kpis=..., transactions=...)
```

### KPI card

```html
<article class="kpi-card">
  <span class="kpi-label">Income this month</span>
  <span class="kpi-value kpi-value--positive">$4,250.00</span>
  <span class="kpi-delta kpi-delta--up">▲ 12.4% vs last month</span>
</article>
```

CSS conventions: BEM-ish (`.block__elem--mod`), grouped in the page CSS.

### Transaction row

Used inside `<table class="txn-table">` or as flex rows. Always tabular-nums for amounts. Negative amounts use `--expense`, positive use `--income`. Category is a small pill.

### Budget progress

A horizontal bar with label, amount-spent / budget, and a `<progress>` element or styled div. When over budget, swap the bar color to `--warning` and show an inline alert.

### AI chat

Two bubble variants: `.chat-msg--user` (right-aligned, accent background) and `.chat-msg--ai` (left-aligned, neutral surface). AI insight cards (`.insight-card`) include a "Why?" disclosure that expands an explanation panel. Never invent data — wire to context vars passed from `app.py`.

### Empty states

Every list/table needs an empty state: an inline SVG illustration (simple, single-color stroke), a short headline, one supporting line, and a primary action. Don't ship a list view without one.

### Forms

Native HTML controls. Inputs get `.input`, labels stack above. Show validation inline below the field with `.field-error`. Use `aria-invalid` and `aria-describedby`.

## Workflow when responding

When the user asks for a Spendly UI piece:

1. **Identify the artifact type:** full page, partial/macro, or component-only? If unclear, ask once.
2. **Confirm the route + data shape** if creating a page. Propose the `app.py` route and required context variables before writing the template.
3. **Check `style.css` for existing tokens.** If the user shares it, reuse what's there. If not, propose additions to `style.css` separately from the page CSS.
4. **Output structure:** show files in order — `app.py` route snippet → `templates/<name>.html` → `static/css/<name>.css` (page-specific) → `static/css/style.css` additions (if any) → `static/js/<name>.js` (if needed).
5. **Use accessible, semantic HTML.** Real buttons (not divs), labeled inputs, alt text on images, proper heading hierarchy.
6. **Mobile-first CSS.** Default styles target mobile; use `@media (min-width: 768px)` and `@media (min-width: 1024px)` to scale up.
7. **Include an empty state** for any list/table. Include a loading state for any async-loaded data.
8. **Keep it simple.** This is a student project. Prefer clarity over cleverness. No bundlers, no build step.

## What NOT to do

- ❌ Don't reach for `<script src="https://cdn.tailwindcss.com">` or any CDN framework.
- ❌ Don't write inline `style="..."` attributes (one or two for dynamic widths like progress bars is OK).
- ❌ Don't introduce a JS framework, build tool, or package.json change.
- ❌ Don't hardcode colors like `#1a472a` in page CSS — use `var(--accent)`.
- ❌ Don't create a new top-level directory. Stick to `templates/` and `static/{css,js}/`.
- ❌ Don't assume features exist. If the user asks to wire up "the existing transactions API", ask — the codebase has stubs marked "coming in Step N".

## References

For deeper guidance, see:
- `references/components.md` — fuller markup blueprints for KPI cards, transaction tables, budget bars, AI chat, empty states
- `references/style-css-starter.md` — a complete `style.css` you can drop in if the project has none yet
- `references/base-html-starter.md` — a `base.html` template if needed