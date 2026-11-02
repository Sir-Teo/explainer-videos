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
* :func:`ken_french_daily`: Kenneth French's daily US market factor since 1926;
* :func:`ken_french_size_daily`: his daily value-weighted size-decile portfolios since 1926;
* :func:`binance_funding`: the funding rate of a Binance USD-margined perpetual future, every eight hours;
* :func:`fred`: a daily or weekly series from FRED (St. Louis Fed), frozen through a date;
* :func:`shiller`: Robert Shiller's monthly US stock market data since 1871 (price, dividends, earnings, CPI, CAPE);
* :func:`ken_french_sorts`: his monthly portfolios sorted on a characteristic (accruals, profitability, ...).

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


def ken_french_size_daily(through: str = "2025-12-31") -> dict:
    """Daily value-weighted returns (decimal) of the ten NYSE-breakpoint size deciles, smallest first: ``date``
    (YYYYMMDD ints) and ``deciles`` (days x 10), through ``through``; checked like :func:`ken_french_daily`."""
    name = "Portfolios_Formed_on_ME_daily_CSV.zip"
    path = DATA / "kenfrench" / name
    if not path.exists():
        _atomic_write(path, _get(f"{KF}/{name}"))
    with zipfile.ZipFile(path) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    rows, started = [], False
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if parts[0].isdigit() and len(parts[0]) == 8:
            started = True
            rows.append([int(parts[0])] + [float(x) / 100 for x in parts[-10:]])
        elif started:  # the first block is value-weighted; the equal-weighted block follows
            break
    a = np.array(rows)
    a = a[a[:, 0] <= int(through.replace("-", ""))]
    frozen = json.dumps(a.round(8).tolist(), separators=(",", ":")).encode()
    _check(f"kenfrench/size_deciles_daily/through_{through}", frozen, f"{KF}/{name}")
    return {"date": a[:, 0].astype(int), "deciles": a[:, 1:]}


def binance_funding(symbol="BTCUSDT", start="2020-01", end="2020-12") -> dict:
    """Funding of a Binance USD-margined perpetual: ``time`` (UTC seconds of each settlement, every 8 hours) and
    ``rate`` (paid by longs to shorts when positive, as a fraction of the position's value).  Monthly files from the
    public archive, checked against Binance's published SHA-256 and the manifest."""
    base = f"https://data.binance.vision/data/futures/um/monthly/fundingRate/{symbol}"
    t, r = [], []
    for ym in _months(start, end):
        name = f"{symbol}-fundingRate-{ym}.zip"
        path = DATA / "binance" / "futures" / "um" / "fundingRate" / symbol / name
        url = f"{base}/{name}"

        def fetch(url=url, name=name):
            raw = _get(url)
            want = _get(url + ".CHECKSUM").decode().split()[0]
            if _sha(raw) != want:
                raise RuntimeError(f"{name}: sha256 does not match Binance's published checksum")
            return raw

        raw = _cached(f"binance/futures/um/fundingRate/{symbol}/{ym}", path, fetch, url)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            text = z.read(z.namelist()[0]).decode()
        for row in text.strip().splitlines():
            parts = row.split(",")
            if parts[0].isdigit():
                t.append(float(parts[0]) / 1e3)
                r.append(float(parts[2]))
    o = np.argsort(t, kind="stable")
    return {"time": np.array(t)[o], "rate": np.array(r)[o]}


FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def fred(series: str, start: str = "2015-01-01", through: str = "2025-12-31") -> dict:
    """A FRED series as ``date`` (YYYYMMDD ints) and ``value`` (as published: percent for rates, millions of dollars
    for balances), missing days dropped.  FRED revises some series, so the manifest checks the frozen window."""
    path = DATA / "fred" / f"{series}.csv"
    if path.exists():
        first = path.read_text().splitlines()[1].split(",")[0].replace("-", "")
        if int(first) > int(start.replace("-", "")) and int(first) > 19000101:
            path.unlink()  # cached from a later start: fetch the whole history once (cached windows stay checked)
    if not path.exists():
        _atomic_write(path, _get(f"{FRED}?id={series}&cosd=1900-01-01&coed=2025-12-31"))
    rows = []
    for line in path.read_text().strip().splitlines()[1:]:
        d, v = line.split(",")[:2]
        if v.strip() in ("", "."):
            continue
        rows.append((int(d.replace("-", "")), float(v)))
    a = np.array(rows)
    m = (a[:, 0] >= int(start.replace("-", ""))) & (a[:, 0] <= int(through.replace("-", "")))
    a = a[m]
    frozen = json.dumps(a.round(6).tolist(), separators=(",", ":")).encode()
    _check(f"fred/{series}/{start}_{through}", frozen, f"{FRED}?id={series}")
    return {"date": a[:, 0].astype(int), "value": a[:, 1]}


SHILLER = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"


def shiller(through: str = "2020-12") -> dict:
    """Robert Shiller's monthly data (the "Data" sheet of ie_data.xls): ``t`` (fractional year), ``price`` (S&P
    composite, monthly average of daily closes), ``div`` and ``earn`` (twelve-month totals, nominal), ``cpi``,
    ``gs10`` (10-year Treasury yield, percent) and ``cape`` (the cyclically adjusted P/E), through ``through``.  Shiller
    revises recent months, so the manifest checks the frozen window."""
    import xlrd

    path = DATA / "shiller" / "ie_data.xls"
    if not path.exists():
        _atomic_write(path, _get(SHILLER))
    sh = xlrd.open_workbook(str(path)).sheet_by_name("Data")
    rows = []
    for i in range(sh.nrows):
        r = sh.row_values(i)
        if not isinstance(r[0], float):
            continue
        y = int(r[0])
        m = int(round((r[0] - y) * 100))
        if not (1 <= m <= 12):
            continue

        def num(x):
            return float(x) if isinstance(x, float) else np.nan

        rows.append([y + (m - 1) / 12, num(r[1]), num(r[2]), num(r[3]), num(r[4]), num(r[6]), num(r[12])])
    a = np.array(rows)
    y1, m1 = map(int, through.split("-"))
    a = a[a[:, 0] <= y1 + (m1 - 1) / 12 + 1e-6]
    frozen = json.dumps(np.nan_to_num(a, nan=-1).round(6).tolist(), separators=(",", ":")).encode()
    _check(f"shiller/ie_data/through_{through}", frozen, SHILLER)
    return {"t": a[:, 0], "price": a[:, 1], "div": a[:, 2], "earn": a[:, 3], "cpi": a[:, 4], "gs10": a[:, 5],
            "cape": a[:, 6]}


def ken_french_sorts(name: str, through: str = "2020-12", weighting: str = "value") -> dict:
    """Monthly returns (decimal) of the portfolios in Kenneth French's ``Portfolios_Formed_on_<name>`` file: ``date``
    (YYYYMM ints), ``columns`` (the file's portfolio names) and ``returns`` (months x portfolios), from the first
    (value-weighted) or second (equal-weighted) monthly block, through ``through``."""
    fn = f"Portfolios_Formed_on_{name}_CSV.zip"
    path = DATA / "kenfrench" / fn
    if not path.exists():
        _atomic_write(path, _get(f"{KF}/{fn}"))
    with zipfile.ZipFile(path) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    blocks, cur, header = [], None, None
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if parts[0] == "" and len(parts) > 2 and cur is None:
            header = parts[1:]
            continue
        if parts[0].isdigit() and len(parts[0]) == 6:
            if cur is None:
                cur = {"header": header, "rows": []}
            cur["rows"].append([int(parts[0])] + [float(x) for x in parts[1:]])
        elif cur is not None:
            blocks.append(cur)
            cur = None
    if cur is not None:
        blocks.append(cur)
    b = blocks[0 if weighting == "value" else 1]
    a = np.array(b["rows"])
    a = a[a[:, 0] <= int(through.replace("-", ""))]
    a[:, 1:] = np.where(a[:, 1:] <= -99.99, np.nan, a[:, 1:] / 100)
    frozen = json.dumps(np.nan_to_num(a, nan=-1).round(8).tolist(), separators=(",", ":")).encode()
    _check(f"kenfrench/{name}_{weighting}/through_{through}", frozen, f"{KF}/{fn}")
    return {"date": a[:, 0].astype(int), "columns": b["header"], "returns": a[:, 1:]}


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
    sz = ken_french_size_daily()
    print(f"  Ken French size deciles, daily: {len(sz['date'])} days", flush=True)
    b = binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    print(f"  binance BTCUSDT 1d: {len(b['time'])} days (from its first listing)", flush=True)
    print(f"  all data ready in {time.time() - t:.0f}s")


if __name__ == "__main__":
    fetch_all()
