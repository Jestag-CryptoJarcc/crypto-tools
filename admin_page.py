import os
from flask import Blueprint, render_template, request, redirect, session
from crypto_data import load_holdings, save_holdings, load_suggestions, update_suggestion_status, delete_suggestion, get_cache_snapshot
from site_meta import SITE_CREATED, site_last_updated

admin_bp = Blueprint("admin", __name__)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" not in session:
        if request.method == "POST":
            password = request.form.get("password", "")
            if password and password == ADMIN_PASSWORD:
                session["admin"] = True
                return redirect("/admin")
            return render_template("admin.html", error="Wrong password", active="admin")
        return render_template("admin.html", active="admin")

    holdings = load_holdings()
    suggestions = load_suggestions()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            name = request.form.get("name", "").strip()
            symbol = request.form.get("symbol", "").strip().upper()
            note = request.form.get("note", "").strip()
            if name and symbol:
                holdings.append({"name": name, "symbol": symbol, "note": note})
                save_holdings(holdings)
            return redirect("/admin")
        if action == "delete":
            idx = int(request.form.get("index", "-1"))
            if 0 <= idx < len(holdings):
                holdings.pop(idx)
                save_holdings(holdings)
            return redirect("/admin")
        if action == "suggestion_status":
            idx = int(request.form.get("s_index", "-1"))
            status = request.form.get("status", "new")
            update_suggestion_status(idx, status)
            return redirect("/admin")
        if action == "suggestion_delete":
            idx = int(request.form.get("s_index", "-1"))
            delete_suggestion(idx)
            return redirect("/admin")

    indexed = list(enumerate(suggestions))
    indexed.reverse()
    groups = {
        "new": [(i, s) for i, s in indexed if s.get("status") == "new"],
        "in_progress": [(i, s) for i, s in indexed if s.get("status") == "in_progress"],
        "done": [(i, s) for i, s in indexed if s.get("status") == "done"],
    }
    stats = {
        "holdings": len(holdings),
        "suggestions": len(suggestions),
        "new_suggestions": len([s for s in suggestions if s.get("status") == "new"]),
    }
    cache_snapshot = get_cache_snapshot()

    return render_template(
        "admin.html",
        holdings=holdings,
        suggestions=suggestions,
        suggestion_groups=groups,
        stats=stats,
        cache_snapshot=cache_snapshot,
        site_created=SITE_CREATED,
        site_updated=site_last_updated(),
        logged_in=True,
        active="admin",
    )


@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")
