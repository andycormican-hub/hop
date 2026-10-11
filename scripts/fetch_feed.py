#!/usr/bin/env python3
"""Fetch the Binance Web3 RWA token list for BSC and write a trimmed feed file.

Usage:  python3 scripts/fetch_feed.py out/markets.json

Reads BINANCE_WEB3_API_KEY and BINANCE_WEB3_API_SECRET from the environment.
Never prints either value. Read-only: one signed GET, no trading.
If the call fails, the output file is NOT written, so the last good feed stays
in place and the page will mark it stale once it gets old enough.
"""
import base64
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://web3.binance.com"
PATH = "/build/api/v1/dex/market/rwa/tokens?binanceChainId=56"
CHAIN = "56"


def timestamp():
    """UTC time in the format the API expects, e.g. 2026-10-12T15:00:00.123Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def sign(secret, ts, method, path, body=""):
    """HMAC-SHA256 over timestamp + method + path (with query) + body, base64."""
    prehash = ts + method + path + body
    digest = hmac.new(secret.encode(), prehash.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def call(key, secret, path=PATH):
    ts = timestamp()
    req = Request(BASE + path, method="GET")
    req.add_header("X-OC-APIKEY", key)
    req.add_header("X-OC-TIMESTAMP", ts)
    req.add_header("X-OC-SIGN", sign(secret, ts, "GET", path))
    with urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _price(value):
    p = _num(value)
    if p is None:
        return "\u2014"
    return f"{p:.2f}" if p >= 1 else f"{p:.4f}"


def transform(payload, fetched_at):
    """Turn the raw API response into the small feed file the page reads."""
    rows, counts = [], {}
    for t in payload["data"]:
        si = t.get("statusInfo") or {}
        status = si.get("marketStatus") or "unknown"
        counts[status] = counts.get(status, 0) + 1
        rows.append({
            "symbol": t.get("tokenSymbol"),
            "name": t.get("tokenName"),
            "platform": t.get("platformId"),
            "contract": t.get("tokenContractAddress"),
            "price": _price(t.get("tokenPrice")),
            "status": status,
            "open": bool(si.get("openState")),
            "reason": si.get("reasonCode"),
            "next_open": si.get("nextOpenTime"),
            "next_close": si.get("nextCloseTime"),
            "_vol": _num(t.get("volume24H")) or 0.0,
        })
    rows.sort(key=lambda r: r["_vol"], reverse=True)
    for r in rows:
        del r["_vol"]
    return {
        "schema": 1,
        "chain": CHAIN,
        "fetched_at": fetched_at,
        "api_timestamp": payload.get("timestamp"),
        "count": len(rows),
        "status_counts": counts,
        "rows": rows,
    }


def main(argv):
    if len(argv) != 2:
        print("usage: fetch_feed.py OUTPUT.json", file=sys.stderr)
        return 2
    key = os.environ.get("BINANCE_WEB3_API_KEY", "")
    secret = os.environ.get("BINANCE_WEB3_API_SECRET", "")
    if not key or not secret:
        print("Missing BINANCE_WEB3_API_KEY or BINANCE_WEB3_API_SECRET.", file=sys.stderr)
        return 2

    payload, last_err = None, None
    for attempt in range(2):
        try:
            payload = call(key, secret)
            break
        except HTTPError as e:
            last_err = f"HTTP {e.code}"
        except (URLError, TimeoutError, ValueError) as e:
            last_err = type(e).__name__
        time.sleep(3)
    if payload is None:
        print(f"API call failed: {last_err}. Feed not updated.", file=sys.stderr)
        return 1

    if payload.get("code") != 0 or not isinstance(payload.get("data"), list) or not payload["data"]:
        print(f"Unexpected response: code={payload.get('code')!r}, msg={payload.get('msg')!r}. Feed not updated.",
              file=sys.stderr)
        return 1

    feed = transform(payload, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    out = argv[1]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(feed, f, separators=(",", ":"))
    os.replace(tmp, out)
    print(f"Wrote {feed['count']} tokens. Status counts: {feed['status_counts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
