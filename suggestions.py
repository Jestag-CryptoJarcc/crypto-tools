from flask import Blueprint, render_template, request
from crypto_data import add_suggestion

suggestions_bp = Blueprint("suggestions", __name__)


@suggestions_bp.route("/suggestions", methods=["GET", "POST"])
def suggestions():
    success = False
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if email and message:
            add_suggestion(email, message)
            success = True
    return render_template(
        "suggestions.html",
        success=success,
        active="suggestions",
        page_title="Suggestions & Contact",
    )
