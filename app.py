import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("register.html")

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    password = request.form["password"]

    if not name:
        return render_template("register.html", error="Name is required.", name=name, email=email)
    if "@" not in email or "." not in email.split("@")[-1]:
        return render_template("register.html", error="Please enter a valid email address.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    password_hash = generate_password_hash(password)

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"].strip()
    password = request.form["password"]

    conn = get_db()
    user = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.", email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": session["user_name"],
        "initials": "".join(w[0].upper() for w in session["user_name"].split()[:2]),
        "email": "demo@spendly.com",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": 356.24,
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "2026-04-13", "description": "Lunch out",        "category": "Food",          "amount": 18.75},
        {"date": "2026-04-11", "description": "New shoes",        "category": "Shopping",      "amount": 89.99},
        {"date": "2026-04-09", "description": "Cinema tickets",   "category": "Entertainment", "amount": 25.00},
        {"date": "2026-04-07", "description": "Pharmacy",         "category": "Health",        "amount": 35.00},
        {"date": "2026-04-05", "description": "Electricity bill", "category": "Bills",         "amount": 120.00},
        {"date": "2026-04-03", "description": "Bus pass top-up",  "category": "Transport",     "amount": 15.00},
        {"date": "2026-04-01", "description": "Grocery run",      "category": "Food",          "amount": 42.50},
        {"date": "2026-04-13", "description": "Miscellaneous",    "category": "Other",         "amount": 10.00},
    ]
    categories = [
        {"name": "Bills",         "total": 120.00, "percentage": 33.7},
        {"name": "Shopping",      "total":  89.99, "percentage": 25.3},
        {"name": "Food",          "total":  61.25, "percentage": 17.2},
        {"name": "Health",        "total":  35.00, "percentage":  9.8},
        {"name": "Entertainment", "total":  25.00, "percentage":  7.0},
        {"name": "Transport",     "total":  15.00, "percentage":  4.2},
        {"name": "Other",         "total":  10.00, "percentage":  2.8},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
