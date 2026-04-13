# Spec: Registration

## Overview
Implement user registration so visitors can create a Spendly account. This step wires the existing `register.html` form (which already renders correctly) to a `POST /register` route that validates input, hashes the password, inserts the new user into the `users` table, and redirects to the login page on success. It is the first route to touch the database and establishes the pattern all future authenticated routes will follow.

## Depends on
- Step 01 — Database Setup (users table, `get_db()`, `init_db()`, `seed_db()` must be complete)

## Routes
- `GET /register` — render registration form — public (already exists, needs no change)
- `POST /register` — process form submission, insert user, redirect — public

## Database changes
No new tables or columns. Uses the existing `users` table:
- `name` TEXT NOT NULL
- `email` TEXT NOT NULL UNIQUE
- `password_hash` TEXT NOT NULL
- `created_at` TEXT DEFAULT (datetime('now'))

## Templates
- **Modify:** `templates/register.html` — form already targets `POST /register`; add `{{ name }}` and `{{ email }}` value re-population on validation error so the user does not have to retype

## Files to change
- `app.py` — add `POST` method to `/register` route, import `request`, `redirect`, `url_for`, `session` from Flask; import `generate_password_hash` from `werkzeug.security`
- `templates/register.html` — repopulate `name` and `email` fields on error

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side: name not empty, valid email format (basic check), password minimum 8 characters
- On duplicate email, re-render the form with `error="An account with that email already exists."` and re-populate name/email fields
- On success, redirect to `url_for('login')` — do NOT log the user in automatically (login is Step 3)
- Use `conn.execute` with parameterised `?` placeholders; always `commit()` and `close()` the connection

## Definition of done
- [ ] `GET /register` still renders the form without errors
- [ ] Submitting valid name/email/password inserts a row in `users` with a hashed password (verifiable via SQLite browser or `python3 -c "from database.db import get_db; ..."`)
- [ ] After successful registration, the browser redirects to `/login`
- [ ] Submitting a duplicate email re-renders the form with an error message and does not insert a second row
- [ ] Submitting an empty name, invalid email, or password shorter than 8 characters re-renders the form with an appropriate error message
- [ ] Name and email fields are repopulated after a validation error
- [ ] Password is never stored in plain text — `password_hash` column contains a werkzeug hash string
- [ ] App starts without errors (`python3 app.py`)
