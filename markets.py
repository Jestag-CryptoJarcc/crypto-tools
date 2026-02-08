from flask import Blueprint, render_template
from crypto_data import get_btc_data, get_top_coins, get_my_coins

markets_bp = Blueprint("markets", __name__)

WEBSITE_MAP = {
    "bitcoin": "https://bitcoin.org",
    "ethereum": "https://ethereum.org",
    "tether": "https://tether.to",
    "usd-coin": "https://www.circle.com/en/usdc",
    "binancecoin": "https://www.bnbchain.org",
    "solana": "https://solana.com",
    "dogecoin": "https://dogecoin.com",
    "litecoin": "https://litecoin.org",
    "polygon-ecosystem-token": "https://polygon.technology",
    "mantle": "https://www.mantle.xyz",
    "nano": "https://nano.org",
    "banano": "https://banano.cc",
    "xrp": "https://xrpl.org",
    "cardano": "https://cardano.org",
    "avalanche-2": "https://www.avax.network",
    "tron": "https://tron.network",
    "the-open-network": "https://ton.org",
    "polkadot": "https://polkadot.network",
}


@markets_bp.route("/markets")
def markets():
    btc = get_btc_data()
    top = get_top_coins()
    mine = get_my_coins()
    merged = []
    seen = set()
    for coin in mine + top:
        cid = coin.get("id")
        if not cid or cid in seen:
            continue
        seen.add(cid)
        coin["website"] = WEBSITE_MAP.get(cid)
        merged.append(coin)
    return render_template(
        "markets.html",
        btc=btc,
        coins=merged,
        active="markets",
    )
