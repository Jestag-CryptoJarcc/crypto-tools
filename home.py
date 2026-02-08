from flask import Blueprint, render_template
from crypto_data import get_btc_data, get_fear_greed, get_top_coins, get_my_coins, load_holdings, market_mood

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    btc = get_btc_data()
    top_coins = get_top_coins()
    my_coins = get_my_coins()
    if my_coins:
        order = ["smlo", "bitcoin", "solana", "polygon-ecosystem-token", "dogecoin", "litecoin", "binancecoin", "mantle", "nano", "banano", "atto"]
        my_map = {coin.get("id"): coin for coin in my_coins}
        my_coins = [my_map[i] for i in order if i in my_map] + [c for c in my_coins if c.get("id") not in order]
    fear_greed = get_fear_greed()
    holdings = load_holdings()
    return render_template(
        "home.html",
        btc=btc,
        top_coins=top_coins,
        my_coins=my_coins,
        fear_greed=fear_greed,
        holdings=holdings,
        mood=market_mood(btc.get("change_24h") if btc else None),
        active="home",
    )
