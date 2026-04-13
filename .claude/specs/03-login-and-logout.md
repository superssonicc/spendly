# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate with Spendly. This step upgrades the existing stub `GET /login` route to handle `POST` submissions, verifies the user's password against the stored hash, stores the user's id and name in a server-side Flask session on success, and redirects to the dashboard (placeholder for now). The `/logout` stub route is also wired to clear the session and redirect back to the landing page. Together these two routes form the authentication boundary that all future protected pages will rely on.

## Depends on
- Step 01 — Database Setup (`get_db()`, `users` table must exist)
- Step 02 — Registration (users must exist in the database to log in)

## Routes
- `GET /login` — render login form — public (already exists as stub, needs POST added)
- `POST /login` — validate credentials, set session, redirect — public
- `GET /logout` — clear session, redirect to `/` — public (stub already exists, needs implementation)

## Database changes
No database changes. Reads from the existing `users` table using the `email` column to look up the user.

## Templates
- **Modify:** `templates/login.html` — add `method="POST"` action to the form; display `{{ error }}` message on failed login; repopulate the `email` field on error

## Files to change
- `app.py` — add `POST` to `/login` route; implement `/logout`; add `session` to Flask import; add `check_password_hash` to werkzeug import; set `app.secret_key`

## Files to create
No new files.

## New dependencies
No new dependencies. (`werkzeug.security.check_password_hash` is already installed with Flask/Werkzeug.)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any session usage — use a hard-coded development string for now (e.g. `"dev-secret-change-in-prod"`)
- Store only `session["user_id"]` and `session["user_name"]` — never store the password or hash in the session
- On bad email or wrong password show a generic error `"Invalid email or password."` — do not reveal which field is wrong
- On success redirect to `url_for('landing')` for now (dashboard does not exist yet)
- `/logout` must call `session.clear()` then redirect to `url_for('landing')`
- Email lookup must use a parameterised `SELECT … WHERE email = ?` query

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting the correct email and password for the seed user (`demo@spendly.com` / `demo123`) redirects to `/`
- [ ] After login, `session["user_id"]` and `session["user_name"]` are set (verifiable via Flask debug or a `print` in the route)
- [ ] Submitting a non-existent email re-renders the form with `"Invalid email or password."` and does not expose which field failed
- [ ] Submitting the correct email but wrong password re-renders the form with the same generic error
- [ ] Email field is repopulated after a failed login attempt
- [ ] Visiting `/logout` clears the session and redirects to the landing page
- [ ] After logout, `session.get("user_id")` returns `None`
- [ ] App starts without errors (`python3 app.py`)
