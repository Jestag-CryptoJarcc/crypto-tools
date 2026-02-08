import os
import json
import re
import html
from datetime import datetime, timezone
import time
import requests
import feedparser

HOLDINGS_PATH = "holdings.json"
TOP_COINS_CACHE = "top_coins_cache.json"
NEWS_CACHE = "news_cache.json"
MY_COINS_CACHE = "my_coins_cache.json"
COINGECKO_LIST_CACHE = "coingecko_list_cache.json"
SUGGESTIONS_PATH = "suggestions.json"

SESSION = requests.Session()
_CACHE = {}


def _cached(key, ttl_seconds, value_fn):
    now = time.time()
    hit = _CACHE.get(key)
    if hit and (now - hit["ts"] < ttl_seconds):
        return hit["value"]
    value = value_fn()
    _CACHE[key] = {"ts": now, "value": value}
    return value


def load_holdings():
    if os.path.exists(HOLDINGS_PATH):
        try:
            with open(HOLDINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_holdings(items):
    with open(HOLDINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def load_suggestions():
    if os.path.exists(SUGGESTIONS_PATH):
        try:
            with open(SUGGESTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def add_suggestion(email, message):
    items = load_suggestions()
    items.append(
        {
            "email": email,
            "message": message,
            "created": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "status": "new",
        }
    )
    with open(SUGGESTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    return items


def update_suggestion_status(index, status):
    items = load_suggestions()
    if 0 <= index < len(items):
        items[index]["status"] = status
        with open(SUGGESTIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    return items


def delete_suggestion(index):
    items = load_suggestions()
    if 0 <= index < len(items):
        items.pop(index)
        with open(SUGGESTIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    return items


def get_cache_snapshot():
    snapshot = {}
    now = time.time()
    for key, value in _CACHE.items():
        age = int(now - value["ts"])
        snapshot[key] = f"{age}s ago"
    return snapshot


def get_btc_data():
    def _fetch():
        headers = {"User-Agent": "JestagCryptoTools/1.0"}
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        params = {
            "localization": "false",
            "tickers": "false",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "true",
            "market_data": "true",
        }
        try:
            resp = SESSION.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            data = None

        if data:
            market = data.get("market_data", {})
            spark = market.get("sparkline_7d", {}).get("price", [])
            image = data.get("image", {})
            prices = market.get("current_price", {})
            return {
                "name": data.get("name", "Bitcoin"),
                "symbol": data.get("symbol", "btc").upper(),
                "image": image.get("small"),
                "price_usd": prices.get("usd"),
                "price_eur": prices.get("eur"),
                "prices": {
                    "usd": prices.get("usd"),
                    "eur": prices.get("eur"),
                    "gbp": prices.get("gbp"),
                    "aud": prices.get("aud"),
                    "cad": prices.get("cad"),
                    "jpy": prices.get("jpy"),
                    "cny": prices.get("cny"),
                    "inr": prices.get("inr"),
                    "krw": prices.get("krw"),
                },
                "change_24h": market.get("price_change_percentage_24h"),
                "volume_24h": market.get("total_volume", {}).get("usd"),
                "market_cap": market.get("market_cap", {}).get("usd"),
                "sparkline": spark[-60:] if len(spark) > 60 else spark,
                "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            }

        fallback_url = "https://api.coingecko.com/api/v3/simple/price"
        fallback_params = {
            "ids": "bitcoin",
            "vs_currencies": "usd,eur",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true",
        }
        try:
            resp = SESSION.get(fallback_url, params=fallback_params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("bitcoin", {})
            return {
                "name": "Bitcoin",
                "symbol": "BTC",
                "image": None,
                "price_usd": data.get("usd"),
                "price_eur": data.get("eur"),
                "prices": {
                    "usd": data.get("usd"),
                    "eur": data.get("eur"),
                    "gbp": data.get("gbp"),
                    "aud": data.get("aud"),
                    "cad": data.get("cad"),
                    "jpy": data.get("jpy"),
                    "cny": data.get("cny"),
                    "inr": data.get("inr"),
                    "krw": data.get("krw"),
                },
                "change_24h": data.get("usd_24h_change"),
                "volume_24h": data.get("usd_24h_vol"),
                "market_cap": data.get("usd_market_cap"),
                "sparkline": [],
                "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            }
        except Exception:
            return None

    return _cached("btc", 15, _fetch)


def get_top_coins(limit=15):
    def _fetch():
        headers = {"User-Agent": "JestagCryptoTools/1.0"}
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 30,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        }
        try:
            resp = SESSION.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            items = resp.json()
        except Exception:
            items = None

        if items:
            results = []
            for item in items[:limit]:
                results.append(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "symbol": (item.get("symbol") or "").upper(),
                        "image": item.get("image"),
                        "price_usd": item.get("current_price"),
                        "change_24h": item.get("price_change_percentage_24h"),
                        "change_7d": item.get("price_change_percentage_7d_in_currency"),
                        "volume_24h": item.get("total_volume"),
                        "market_cap": item.get("market_cap"),
                        "rank": item.get("market_cap_rank"),
                    }
                )
            try:
                with open(TOP_COINS_CACHE, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            except OSError:
                pass
            return results
        return None

    items = _cached(f"top_{limit}", 30, _fetch)
    if items:
        return items

    if os.path.exists(TOP_COINS_CACHE):
        try:
            with open(TOP_COINS_CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, list) and cached:
                return cached
        except (OSError, json.JSONDecodeError):
            pass

    btc = get_btc_data()
    return [btc] if btc else []


def search_coins(query, limit=6):
    query = (query or "").strip()
    if not query:
        return []
    cache_key = f"search:{query.lower()}:{limit}"
    hit = _CACHE.get(cache_key)
    if hit and (time.time() - hit["ts"] < 10):
        return hit["value"]
    headers = {"User-Agent": "JestagCryptoTools/1.0"}
    q_lower = query.lower()
    alias_map = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "bnb": "binancecoin",
        "xrp": "ripple",
        "doge": "dogecoin",
        "matic": "polygon-ecosystem-token",
        "pol": "polygon-ecosystem-token",
        "usdt": "tether",
        "usdc": "usd-coin",
    }
    search_url = "https://api.coingecko.com/api/v3/search"
    ids = []
    try:
        resp = SESSION.get(search_url, params={"query": query}, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        coins = data.get("coins", [])[:limit]
        ids = [c.get("id") for c in coins if c.get("id")]
    except Exception:
        ids = []

    if not ids and q_lower in alias_map:
        ids = [alias_map[q_lower]]

    if not ids:
        ids = _search_coin_list_cache(query, limit=limit)
        if not ids:
            return []

    markets_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(ids),
        "order": "market_cap_desc",
        "per_page": len(ids),
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h,7d",
    }
    try:
        resp = SESSION.get(markets_url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        items = resp.json()
    except Exception:
        items = _search_cache_by_ids(ids)
        if not items:
            return []

    results = []
    for item in items:
        results.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "symbol": (item.get("symbol") or "").upper(),
                "image": item.get("image"),
                "price_usd": item.get("current_price") if item.get("current_price") is not None else item.get("price_usd"),
                "change_24h": item.get("price_change_percentage_24h") if item.get("price_change_percentage_24h") is not None else item.get("change_24h"),
                "change_7d": item.get("price_change_percentage_7d_in_currency") if item.get("price_change_percentage_7d_in_currency") is not None else item.get("change_7d"),
                "volume_24h": item.get("total_volume") if item.get("total_volume") is not None else item.get("volume_24h"),
                "market_cap": item.get("market_cap"),
                "rank": item.get("market_cap_rank") if item.get("market_cap_rank") is not None else item.get("rank"),
            }
        )
    _CACHE[cache_key] = {"ts": time.time(), "value": results}
    return results


def _search_coin_list_cache(query, limit=6):
    query = query.lower()
    now = int(time.time())
    coins = []
    if os.path.exists(COINGECKO_LIST_CACHE):
        try:
            with open(COINGECKO_LIST_CACHE, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, dict):
                updated = int(payload.get("updated", 0))
                if now - updated < 24 * 60 * 60:
                    coins = payload.get("coins", [])
        except (OSError, json.JSONDecodeError, ValueError):
            coins = []

    if not coins:
        try:
            resp = SESSION.get("https://api.coingecko.com/api/v3/coins/list", headers={"User-Agent": "JestagCryptoTools/1.0"}, timeout=10)
            resp.raise_for_status()
            coins = resp.json()
            with open(COINGECKO_LIST_CACHE, "w", encoding="utf-8") as f:
                json.dump({"updated": now, "coins": coins}, f)
        except Exception:
            return []

    matches = []
    for c in coins:
        name = (c.get("name") or "").lower()
        sym = (c.get("symbol") or "").lower()
        if query in name or query == sym or sym.startswith(query):
            if c.get("id"):
                matches.append(c.get("id"))
        if len(matches) >= limit:
            break
    return matches


def _search_cache_by_ids(ids):
    results = []
    for path in (TOP_COINS_CACHE, MY_COINS_CACHE):
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if not isinstance(cached, list):
                continue
            cmap = {c.get("id"): c for c in cached if c.get("id")}
            for cid in ids:
                if cid in cmap and cmap[cid] not in results:
                    results.append(cmap[cid])
        except (OSError, json.JSONDecodeError):
            pass
    return results


def get_fear_greed():
    def _fetch():
        url = "https://api.alternative.me/fng/"
        try:
            resp = SESSION.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            item = data.get("data", [{}])[0]
            return {
                "value": int(item.get("value", 0)),
                "classification": item.get("value_classification", ""),
            }
        except Exception:
            return None

    return _cached("fear_greed", 300, _fetch)


def market_mood(change_24h):
    if change_24h is None:
        return "Unknown"
    if change_24h >= 5:
        return "Hype"
    if change_24h >= 1:
        return "Positive"
    if change_24h <= -5:
        return "Fear"
    if change_24h <= -1:
        return "Caution"
    return "Calm"


def get_my_coins():
    headers = {"User-Agent": "JestagCryptoTools/1.0"}
    pool_id = "9FepPyQDMBvj4bcLrfCUhK9pyLk8WoTDNkvgSCR86aWp"
    url = f"https://api.geckoterminal.com/api/v2/networks/solana/pools/{pool_id}"
    nestex_url = "https://trade.nestex.one/api/cg/tickers"
    params = {"include": "base_token,quote_token"}
    results = []
    hit = _CACHE.get("my_coins")
    if hit and (time.time() - hit["ts"] < 30):
        return hit["value"]

    def _store(value):
        _CACHE["my_coins"] = {"ts": time.time(), "value": value}
        return value

    def load_smlo_from_cache():
        if os.path.exists(MY_COINS_CACHE):
            try:
                with open(MY_COINS_CACHE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if isinstance(cached, list):
                    return next((c for c in cached if c.get("id") == "smlo"), None)
            except (OSError, json.JSONDecodeError):
                return None
        return None

    try:
        # SMLO from GeckoTerminal pool + Nestex volume (kept first)
        resp = SESSION.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        pool_attr = data.get("data", {}).get("attributes", {})
        relationships = data.get("data", {}).get("relationships", {})
        included = data.get("included", [])
        base_id = relationships.get("base_token", {}).get("data", {}).get("id")
        base_token = next((item for item in included if item.get("type") == "token" and item.get("id") == base_id), {})
        base_attr = base_token.get("attributes", {})

        nestex_volume = 0.0
        try:
            nestex = SESSION.get(nestex_url, headers=headers, timeout=10).json()
            for item in nestex:
                if item.get("ticker_id") == "SMLO_USDT":
                    nestex_volume = float(item.get("target_volume") or 0)
                    break
        except Exception:
            nestex_volume = 0.0

        smlo_entry = {
            "id": "smlo",
            "name": base_attr.get("name") or "Smellow",
            "symbol": (base_attr.get("symbol") or "SMLO").upper(),
            "image": base_attr.get("image_url"),
            "price_usd": float(pool_attr.get("base_token_price_usd") or 0),
            "change_24h": float(pool_attr.get("price_change_percentage", {}).get("h24") or 0),
            "change_7d": float(pool_attr.get("price_change_percentage", {}).get("d7") or 0),
            "volume_24h": float(pool_attr.get("volume_usd", {}).get("h24") or 0) + nestex_volume,
            "market_cap": float(pool_attr.get("fdv_usd") or 0),
            "rank": None,
        }
        results.append(smlo_entry)

        # Core coins from CoinGecko (ordered)
        core_order = [
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
        cg_url = "https://api.coingecko.com/api/v3/coins/markets"
        cg_params = {
            "vs_currency": "usd",
            "ids": ",".join(core_order),
            "order": "market_cap_desc",
            "per_page": len(core_order),
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        }
        cg_resp = SESSION.get(cg_url, params=cg_params, headers=headers, timeout=10)
        cg_resp.raise_for_status()
        cg_data = {item.get("id"): item for item in cg_resp.json()}
        missing = []
        for coin_id in core_order:
            item = cg_data.get(coin_id)
            if not item:
                missing.append(coin_id)
                continue
            results.append(
                {
                    "id": coin_id,
                    "name": item.get("name"),
                    "symbol": (item.get("symbol") or "").upper(),
                    "image": item.get("image"),
                    "price_usd": float(item.get("current_price") or 0),
                    "change_24h": float(item.get("price_change_percentage_24h") or 0),
                    "change_7d": float(item.get("price_change_percentage_7d_in_currency") or 0),
                    "volume_24h": float(item.get("total_volume") or 0),
                    "market_cap": float(item.get("market_cap") or 0),
                    "rank": item.get("market_cap_rank"),
                }
            )

        # Fallback: fetch missing coins one-by-one
        if missing:
            for coin_id in missing:
                try:
                    one_params = {
                        "vs_currency": "usd",
                        "ids": coin_id,
                        "order": "market_cap_desc",
                        "per_page": 1,
                        "page": 1,
                        "sparkline": "false",
                        "price_change_percentage": "24h,7d",
                    }
                    one_resp = SESSION.get(cg_url, params=one_params, headers=headers, timeout=10)
                    one_resp.raise_for_status()
                    one = one_resp.json()
                    if not one:
                        continue
                    item = one[0]
                    results.append(
                        {
                            "id": coin_id,
                            "name": item.get("name"),
                            "symbol": (item.get("symbol") or "").upper(),
                            "image": item.get("image"),
                            "price_usd": float(item.get("current_price") or 0),
                            "change_24h": float(item.get("price_change_percentage_24h") or 0),
                            "change_7d": float(item.get("price_change_percentage_7d_in_currency") or 0),
                            "volume_24h": float(item.get("total_volume") or 0),
                            "market_cap": float(item.get("market_cap") or 0),
                            "rank": item.get("market_cap_rank"),
                        }
                    )
                except Exception:
                    pass

        if results:
            order = ["smlo", "bitcoin", "solana", "polygon-ecosystem-token", "dogecoin", "litecoin", "binancecoin", "mantle", "nano", "banano", "atto"]
            rmap = {c.get("id"): c for c in results}
            results = [rmap[i] for i in order if i in rmap] + [c for c in results if c.get("id") not in order]
            if "smlo" not in rmap:
                cached_smlo = load_smlo_from_cache()
                if cached_smlo:
                    results = [cached_smlo] + results
            try:
                with open(MY_COINS_CACHE, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            except OSError:
                pass
            return _store(results)
    except Exception:
        pass

    if os.path.exists(MY_COINS_CACHE):
        try:
            with open(MY_COINS_CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, list) and cached:
                order = ["smlo", "bitcoin", "solana", "polygon-ecosystem-token", "dogecoin", "litecoin", "binancecoin", "mantle", "nano", "banano", "atto"]
                cmap = {c.get("id"): c for c in cached}
                cached = [cmap[i] for i in order if i in cmap] + [c for c in cached if c.get("id") not in order]
                return _store(cached)
        except (OSError, json.JSONDecodeError):
            pass

    return _store([])


def get_crypto_news(limit=10):
    hit = _CACHE.get("news")
    if hit and (time.time() - hit["ts"] < 3600):
        return hit["value"]

    def _store(value):
        _CACHE["news"] = {"ts": time.time(), "value": value}
        return value

    def clean_text(text):
        if not text:
            return ""
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    feeds = [
        ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("Cointelegraph", "https://cointelegraph.com/rss"),
        ("The Block", "https://www.theblock.co/rss.xml"),
        ("Reddit r/CryptoCurrency", "https://www.reddit.com/r/CryptoCurrency/.rss"),
        ("Reddit r/Bitcoin", "https://www.reddit.com/r/Bitcoin/.rss"),
    ]
    results = []
    try:
        for source, feed_url in feeds:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:limit]:
                image_url = None
                media_thumb = entry.get("media_thumbnail")
                media_content = entry.get("media_content")
                if media_thumb and isinstance(media_thumb, list):
                    image_url = media_thumb[0].get("url")
                if not image_url and media_content and isinstance(media_content, list):
                    image_url = media_content[0].get("url")

                published_struct = entry.get("published_parsed") or entry.get("updated_parsed")
                if published_struct:
                    published_ts = int(time.mktime(published_struct))
                    published_str = datetime.fromtimestamp(published_ts, tz=timezone.utc).strftime(
                        "%Y-%m-%d %H:%M UTC"
                    )
                else:
                    published_ts = None
                    published_str = "Unknown time"
                summary_raw = entry.get("summary") or entry.get("description")
                if not summary_raw:
                    content = entry.get("content")
                    if isinstance(content, list) and content:
                        summary_raw = content[0].get("value")
                summary = clean_text(summary_raw)
                results.append(
                    {
                        "title": entry.get("title", "Untitled"),
                        "source": source,
                        "summary": summary or "Summary unavailable.",
                        "image": image_url,
                        "url": entry.get("link"),
                        "published_ts": published_ts,
                        "published_str": published_str,
                    }
                )
        if results:
            cutoff = int(time.time()) - (7 * 24 * 60 * 60)
            results = [r for r in results if r.get("published_ts") and r["published_ts"] >= cutoff]
            results.sort(key=lambda r: r["published_ts"], reverse=True)
            results = results[:limit]
            try:
                with open(NEWS_CACHE, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            except OSError:
                pass
            return _store(results)
    except Exception:
        pass

    if os.path.exists(NEWS_CACHE):
        try:
            with open(NEWS_CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if isinstance(cached, list) and cached:
                cutoff = int(time.time()) - (7 * 24 * 60 * 60)
                cached = [r for r in cached if r.get("published_ts") and r["published_ts"] >= cutoff]
                cached.sort(key=lambda r: r["published_ts"], reverse=True)
                for item in cached:
                    if not item.get("summary"):
                        item["summary"] = "Summary unavailable."
                return _store(cached[:limit])
        except (OSError, json.JSONDecodeError):
            pass

    return _store([
        {
            "title": "Crypto news feed will appear here once data loads.",
            "source": "CoinDesk",
            "summary": "",
            "image": None,
            "url": None,
            "published_ts": None,
            "published_str": "Unknown time",
        }
    ])
