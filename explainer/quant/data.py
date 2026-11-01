"""Market data for *Quant, Built*: fetched from free public sources, cached, checksummed, resumable.

Every dataset is downloaded once into ``.cache/quant_data/`` (git-ignored), piece by piece: a monthly file, an hour of
trades.  Each piece is written atomically (``.tmp`` then rename), so an interrupted fetch resumes where it stopped
and never leaves half a file.  The SHA-256 of every raw piece is recorded in ``videos/quant/data/manifest.json``
(committed) the first time it is fetched; later fetches, on this machine or another, are checked against it, so
every render sees the same numbers.  A mismatch stops with an error (the source changed its history); set
``EXPLAINER_DATA_REFRESH=1`` to accept and re-record.

Sources (all free; see videos/quant/SYLLABUS.md, "Data"):

* :func:`binance_klines`: Binance's public archive (data.binance.vision), monthly candle files, which Binance
  publishes with their own SHA-256 (checked too);
* :func:`deribit_trades`: every option trade on Deribit in an hour (history.deribit.com), with each trade's
  price, mark price, implied volatility and the index price at that moment;
* :func:`deribit_dvol`: Deribit's DVOL index (a 30-day implied volatility, computed like the VIX), hourly;
* :func:`ken_french_daily`: Kenneth French's daily US market factor since 1926.

    python -m explainer.quant.data            # fetch everything the series uses so far (resumes)
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import threading
import time
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".cache" / "quant_data"
MANIFEST = ROOT / "videos" / "quant" / "data" / "manifest.json"
_LOCK = threading.Lock()
UA = {"User-Agent": "explainer-videos/quant (education; github.com/sir-teo/explainer-videos)"}


# ---------------------------------------------------------------------------
# Plumbing: atomic files, retries, the manifest
# ---------------------------------------------------------------------------
def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _get(url: str, retries: int = 5, timeout: int = 90) -> bytes:
    err = None
    for k in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network errors, 5xx, rate limits: back off and retry
            err = e
            time.sleep(min(2 ** k, 30))
    raise RuntimeError(f"failed to fetch {url}: {err}")


def _get_json(url: str) -> dict:
    return json.loads(_get(url))


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def _check(key: str, raw: bytes, source: str) -> None:
    """Record ``raw``'s hash under ``key`` the first time; afterwards insist on it."""
    h = _sha(raw)
    with _LOCK:
        m = _manifest()
        old = m.get(key)
        if old and old["sha256"] != h and not os.environ.get("EXPLAINER_DATA_REFRESH"):
            raise RuntimeError(f"{key}: the source's data changed (sha256 {h[:12]} != recorded {old['sha256'][:12]}); "
                               f"set EXPLAINER_DATA_REFRESH=1 to accept it")
        if not old or old["sha256"] != h:
            m[key] = {"sha256": h, "bytes": len(raw), "source": source}
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            tmp = MANIFEST.with_suffix(".tmp")
            tmp.write_text(json.dumps(dict(sorted(m.items())), indent=1) + "\n")
            tmp.replace(MANIFEST)


def _cached(key: str, path: Path, fetch, source: str) -> bytes:
    """The bytes of a raw piece: from the cache, or fetched (and recorded or checked against the manifest)."""
    if path.exists():
        raw = path.read_bytes()
    else:
        raw = fetch()
        _atomic_write(path, raw)
    _check(key, raw, source)
    return raw


def _ms(d: datetime) -> int:
    return int(d.replace(tzinfo=timezone.utc).timestamp() * 1000)


def _months(start: str, end: str):
    y, m = map(int, start.split("-"))
    y1, m1 = map(int, end.split("-"))
    while (y, m) <= (y1, m1):
        yield f"{y:04d}-{m:02d}"
        y, m = (y + (m == 12), m % 12 + 1)


# ---------------------------------------------------------------------------
# Binance: monthly candles
# ---------------------------------------------------------------------------
def binance_klines(symbol="BTCUSDT", interval="1h", start="2021-01", end="2025-12", market="spot") -> dict:
    """Candles from Binance's public archive: ``time`` (UTC seconds, the candle's open), ``open``, ``high``,
    ``low``, ``close``, ``volume`` (base asset), ``trades``.  Each monthly file is checked against Binance's own
    published SHA-256 and against the manifest."""
    base = f"https://data.binance.vision/data/{market}/monthly/klines/{symbol}/{interval}"
    cols = []
    for ym in _months(start, end):
        name = f"{symbol}-{interval}-{ym}.zip"
        path = DATA / "binance" / market / symbol / interval / name
        url = f"{base}/{name}"

        def fetch(url=url, name=name):
            raw = _get(url)
            want = _get(url + ".CHECKSUM").decode().split()[0]
            if _sha(raw) != want:
                raise RuntimeError(f"{name}: sha256 does not match Binance's published checksum")
            return raw

        raw = _cached(f"binance/{market}/{symbol}/{interval}/{ym}", path, fetch, url)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            text = z.read(z.namelist()[0]).decode()
        rows = [r.split(",") for r in text.strip().splitlines() if r and r[0].isdigit()]
        a = np.array([[float(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5]), float(r[8])]
                      for r in rows])
        # Binance switched its spot archive from milliseconds to microseconds on 2025-01-01
        a[:, 0] = np.where(a[:, 0] > 1e14, a[:, 0] / 1e6, a[:, 0] / 1e3)
        cols.append(a)
    a = np.concatenate(cols)
    a = a[np.argsort(a[:, 0], kind="stable")]
    return {"time": a[:, 0], "open": a[:, 1], "high": a[:, 2], "low": a[:, 3], "close": a[:, 4],
            "volume": a[:, 5], "trades": a[:, 6]}


# ---------------------------------------------------------------------------
# Deribit: option trades by the hour, DVOL
# ---------------------------------------------------------------------------
DERIBIT_HISTORY = "https://history.deribit.com/api/v2/public"
DERIBIT = "https://www.deribit.com/api/v2/public"
_TRADE_FIELDS = ("timestamp", "trade_id", "instrument_name", "price", "mark_price", "iv", "index_price",
                 "direction", "amount")


def _deribit_hour(currency: str, kind: str, t0: int) -> list[dict]:
    t1 = t0 + 3_600_000 - 1
    out, seen, start = [], set(), t0
    while True:
        q = urllib.parse.urlencode({"currency": currency, "kind": kind, "start_timestamp": start,
                                    "end_timestamp": t1, "count": 1000, "sorting": "asc"})
        res = _get_json(f"{DERIBIT_HISTORY}/get_last_trades_by_currency_and_time?{q}")["result"]
        new = [t for t in res["trades"] if t["trade_id"] not in seen]
        for t in new:
            seen.add(t["trade_id"])
            out.append({k: t.get(k) for k in _TRADE_FIELDS})
        if not res.get("has_more") or not res["trades"]:
            break
        last = res["trades"][-1]["timestamp"]
        if last == start and not new:  # more than a page in one millisecond: step past it
            last += 1
        start = last
    out.sort(key=lambda t: (t["timestamp"], t["trade_id"]))
    return out


def deribit_trades(day: str, hours=range(24), currency="BTC", kind="option") -> list[dict]:
    """Every ``kind`` trade on Deribit in the given UTC hours of ``day`` (YYYY-MM-DD), oldest first.  Each hour is
    fetched (all pages) and cached on its own, so an interrupted day resumes at the next missing hour."""
    d0 = datetime.strptime(day, "%Y-%m-%d")
    trades = []
    for h in hours:
        t0 = _ms(d0 + timedelta(hours=h))
        path = DATA / "deribit" / "trades" / currency / kind / day / f"{h:02d}.json.gz"
        src = f"{DERIBIT_HISTORY}/get_last_trades_by_currency_and_time?currency={currency}&kind={kind}"

        def fetch(t0=t0):
            body = json.dumps(_deribit_hour(currency, kind, t0), separators=(",", ":")).encode()
            return gzip.compress(body, mtime=0)

        raw = _cached(f"deribit/trades/{currency}/{kind}/{day}/{h:02d}", path, fetch, src)
        trades.extend(json.loads(gzip.decompress(raw)))
    return trades


def deribit_dvol(start="2021-04", end="2025-12", currency="BTC", resolution=3600) -> dict:
    """Deribit's DVOL (30-day implied volatility index, in vol points) at ``resolution`` seconds: ``time`` (UTC
    seconds) and ``open``/``high``/``low``/``close``.  Cached month by month (the current month is never cached)."""
    now = datetime.now(timezone.utc)
    rows = []
    for ym in _months(start, end):
        y, m = map(int, ym.split("-"))
        a = datetime(y, m, 1)
        b = datetime(y + (m == 12), m % 12 + 1, 1)
        if b.replace(tzinfo=timezone.utc) > now:
            raise ValueError(f"DVOL month {ym} is not over yet; freeze on a past month")
        path = DATA / "deribit" / "dvol" / currency / str(resolution) / f"{ym}.json.gz"

        def fetch(a=a, b=b):
            pts, t = [], _ms(a)
            end_ms = _ms(b) - 1
            while t <= end_ms:
                chunk_end = min(t + 900 * resolution * 1000, end_ms)
                q = urllib.parse.urlencode({"currency": currency, "start_timestamp": t, "end_timestamp": chunk_end,
                                            "resolution": resolution})
                pts += _get_json(f"{DERIBIT}/get_volatility_index_data?{q}")["result"]["data"]
                t = chunk_end + 1
            pts = sorted({p[0]: p for p in pts}.values())
            return gzip.compress(json.dumps(pts, separators=(",", ":")).encode(), mtime=0)

        raw = _cached(f"deribit/dvol/{currency}/{resolution}/{ym}", path, fetch,
                      f"{DERIBIT}/get_volatility_index_data?currency={currency}&resolution={resolution}")
        rows += json.loads(gzip.decompress(raw))
    a = np.array(sorted({r[0]: r for r in rows}.values()), float)
    return {"time": a[:, 0] / 1e3, "open": a[:, 1], "high": a[:, 2], "low": a[:, 3], "close": a[:, 4]}


# ---------------------------------------------------------------------------
# Kenneth French: the daily US market since 1926
# ---------------------------------------------------------------------------
KF = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp"


def ken_french_daily(through: str = "2025-12-31") -> dict:
    """Daily Fama–French factors (decimal returns): ``date`` (YYYYMMDD ints), ``mkt`` (the market's total return,
    Mkt-RF + RF), ``mkt_rf``, ``smb``, ``hml``, ``rf``, through ``through``.  The library revises recent months, so
    the manifest checks the *frozen subset*, not the downloaded file: the raw zip is cached once and reused."""
    path = DATA / "kenfrench" / "F-F_Research_Data_Factors_daily_CSV.zip"
    if not path.exists():
        _atomic_write(path, _get(f"{KF}/F-F_Research_Data_Factors_daily_CSV.zip"))
    with zipfile.ZipFile(path) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    rows = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 5 and parts[0].isdigit() and len(parts[0]) == 8:
            rows.append([int(parts[0])] + [float(x) / 100 for x in parts[1:]])
    a = np.array(rows)
    a = a[a[:, 0] <= int(through.replace("-", ""))]
    frozen = json.dumps(a.round(8).tolist(), separators=(",", ":")).encode()
    _check(f"kenfrench/daily_factors/through_{through}", frozen, f"{KF}/F-F_Research_Data_Factors_daily_CSV.zip")
    return {"date": a[:, 0].astype(int), "mkt_rf": a[:, 1], "smb": a[:, 2], "hml": a[:, 3], "rf": a[:, 4],
            "mkt": a[:, 1] + a[:, 4]}


# ---------------------------------------------------------------------------
# What the series has used so far: ``python -m explainer.quant.data`` fetches all of it
# ---------------------------------------------------------------------------
def fetch_all() -> None:
    from explainer.quant.house import surface

    t = time.time()
    for day in surface.DAYS:
        n = len(deribit_trades(day, hours=surface.HOURS))
        print(f"  deribit option trades {day}: {n}", flush=True)
    d = deribit_dvol(*surface.DVOL_RANGE)
    print(f"  deribit DVOL: {len(d['time'])} hours", flush=True)
    k = binance_klines("BTCUSDT", "1h", *surface.SPOT_RANGE)
    print(f"  binance BTCUSDT 1h: {len(k['time'])} candles", flush=True)
    kf = ken_french_daily()
    print(f"  Ken French daily: {len(kf['date'])} days", flush=True)
    print(f"  all data ready in {time.time() - t:.0f}s")


if __name__ == "__main__":
    fetch_all()
