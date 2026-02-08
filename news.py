from flask import Blueprint, render_template
from datetime import datetime, timedelta, timezone
from crypto_data import get_crypto_news

news_bp = Blueprint("news", __name__)


@news_bp.route("/news")
def news():
    items = get_crypto_news(limit=10)
    now = datetime.now(timezone.utc)
    day_cutoff = now - timedelta(days=1)
    week_cutoff = now - timedelta(days=7)
    daily = []
    weekly = []
    for item in items:
        ts = item.get("published_ts")
        if not ts:
            continue
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        if dt >= day_cutoff:
            daily.append(item)
        elif dt >= week_cutoff:
            weekly.append(item)
    return render_template(
        "news.html",
        daily=daily,
        weekly=weekly,
        active="news",
        page_title="Crypto News",
    )
