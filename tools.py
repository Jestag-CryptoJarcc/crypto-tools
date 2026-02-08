from flask import Blueprint, render_template
from crypto_data import get_btc_data, get_fear_greed

tools_bp = Blueprint("tools", __name__)


@tools_bp.route("/tools")
def tools():
    btc = get_btc_data()
    fear_greed = get_fear_greed()
    return render_template(
        "tools.html",
        btc=btc,
        fear_greed=fear_greed,
        active="tools",
    )
