from flask import Blueprint, request
from crypto_data import get_btc_data, get_fear_greed, get_top_coins, get_my_coins, market_mood, search_coins, get_crypto_news, load_holdings

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/summary")
def api_summary():
    btc = get_btc_data()
    top_coins = get_top_coins()
    my_coins = get_my_coins()
    if my_coins:
        order = ["smlo", "bitcoin", "solana", "polygon-ecosystem-token", "dogecoin", "litecoin", "binancecoin", "mantle", "nano", "banano", "atto"]
        my_map = {coin.get("id"): coin for coin in my_coins}
        my_coins = [my_map[i] for i in order if i in my_map] + [c for c in my_coins if c.get("id") not in order]
    fear_greed = get_fear_greed()
    return {
        "btc": btc,
        "top_coins": top_coins,
        "my_coins": my_coins,
        "fear_greed": fear_greed,
        "mood": market_mood(btc.get("change_24h") if btc else None),
    }


@api_bp.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    results = search_coins(query, limit=6)
    if not results and query:
        q = query.strip().lower()
        fallback = []
        for coin in (get_my_coins() or []) + (get_top_coins() or []):
            name = (coin.get("name") or "").lower()
            sym = (coin.get("symbol") or "").lower()
            if q in name or q == sym or sym.startswith(q):
                fallback.append(coin)
        results = fallback[:6]
    return {"results": results}


@api_bp.route("/api/news")
def api_news():
    items = get_crypto_news(limit=30)
    return {"items": items}


@api_bp.route("/api/personal")
def api_personal():
    return {
        "my_coins": get_my_coins(),
        "holdings": load_holdings(),
    }
