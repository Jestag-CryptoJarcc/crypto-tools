import json
import os
from flask import Blueprint, render_template
from crypto_data import get_btc_data, get_my_coins, load_holdings, MY_COINS_CACHE

personal_bp = Blueprint("personal", __name__)


@personal_bp.route("/my")
def personal():
    btc = get_btc_data()
    my_coins = get_my_coins()
    if not my_coins and os.path.exists(MY_COINS_CACHE):
        try:
            with open(MY_COINS_CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, list) and cached:
                my_coins = cached
        except (OSError, json.JSONDecodeError):
            pass
    if my_coins:
        order = [
            "smlo",
            "bitcoin",
            "solana",
            "polygon-ecosystem-token",
            "dogecoin",
            "litecoin",
            "binancecoin",
            "mantle",
            "nano",
            "banano",
            "atto",
        ]
        my_map = {coin.get("id"): coin for coin in my_coins}
        my_coins = [my_map[i] for i in order if i in my_map] + [c for c in my_coins if c.get("id") not in order]
    holdings = load_holdings()
    return render_template(
        "personal.html",
        btc=btc,
        my_coins=my_coins,
        holdings=holdings,
        active="personal",
    )
