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
* :func:`ken_french_sorts`: his monthly portfolios sorted on a characteristic (accruals, profitability, ...);
* :func:`yahoo_daily`: daily closes of an index from Yahoo Finance's chart API (CSI 500, HSCEI, ...), frozen through a
  date and checksummed like the rest;
* :func:`gsw`, :func:`acm`, :func:`treasury_par`, :func:`treasury_auctions`, :func:`sec_facts`: the
  Fed's fitted Treasury curve, the NY Fed's term premium, Treasury's par yields, every Treasury note
  auction, and a filer's XBRL facts (Part 18).

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
    import fcntl  # several processes record at once: an exclusive file lock around read-modify-write

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    with _LOCK, open(DATA / "manifest.lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        m = _manifest()
        old = m.get(key)
        if old and old["sha256"] != h and not os.environ.get("EXPLAINER_DATA_REFRESH"):
            raise RuntimeError(f"{key}: the source's data changed (sha256 {h[:12]} != recorded {old['sha256'][:12]}); "
                               f"set EXPLAINER_DATA_REFRESH=1 to accept it")
        if not old or old["sha256"] != h:
            m[key] = {"sha256": h, "bytes": len(raw), "source": source}
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            tmp = MANIFEST.with_suffix(f".{os.getpid()}.tmp")
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


YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"


def yahoo_daily(symbol: str, start: str = "2015-01-01", through: str = "2025-11-30") -> dict:
    """Daily closes of ``symbol`` (an index such as 000905.SS for the CSI 500 or ^HSCE for the HSCEI) from Yahoo
    Finance's chart API: ``date`` (YYYYMMDD ints, exchange-local) and ``close``. The window is frozen through
    ``through`` and the extracted closes are checksummed, so a revision upstream stops the render."""
    p0 = int(datetime.fromisoformat(start).replace(tzinfo=timezone.utc).timestamp())
    p1 = int((datetime.fromisoformat(through) + timedelta(days=1)).replace(tzinfo=timezone.utc).timestamp())
    safe = symbol.replace("^", "_").replace(".", "_")
    path = DATA / "yahoo" / f"{safe}_{start}_{through}.json"

    def fetch():
        q = urllib.parse.urlencode({"period1": p0, "period2": p1, "interval": "1d"})
        req = urllib.request.Request(f"{YAHOO}{urllib.parse.quote(symbol)}?{q}",
                                     headers={"User-Agent": "Mozilla/5.0 (education)"})
        err = None
        for k in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    return r.read()
            except Exception as e:
                err = e
                time.sleep(min(2 ** k, 30))
        raise RuntimeError(f"failed to fetch {symbol} from Yahoo: {err}")

    if not path.exists():
        _atomic_write(path, fetch())
    d = json.loads(path.read_text())["chart"]["result"][0]
    off = d["meta"].get("gmtoffset", 0)
    ts = np.asarray(d["timestamp"], float) + off
    close = np.asarray([np.nan if c is None else c for c in d["indicators"]["quote"][0]["close"]], float)
    ymd = np.array([int(datetime.fromtimestamp(t, timezone.utc).strftime("%Y%m%d")) for t in ts])
    ok = np.isfinite(close)
    ymd, close = ymd[ok], close[ok]
    frozen = json.dumps(np.column_stack([ymd, close.round(4)]).tolist(), separators=(",", ":")).encode()
    _check(f"yahoo/{symbol}/{start}_{through}", frozen, f"{YAHOO}{symbol}")
    return {"date": ymd, "close": close}


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


def _kf_monthly(fn: str, key: str, through: str, weighting: str) -> dict:
    """The first (value-weighted) or second (equal-weighted) monthly block of one of Kenneth French's CSV files."""
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
    _check(f"kenfrench/{key}_{weighting}/through_{through}", frozen, f"{KF}/{fn}")
    return {"date": a[:, 0].astype(int), "columns": b["header"], "returns": a[:, 1:]}


def ken_french_sorts(name: str, through: str = "2020-12", weighting: str = "value") -> dict:
    """Monthly returns (decimal) of the portfolios in Kenneth French's ``Portfolios_Formed_on_<name>`` file: ``date``
    (YYYYMM ints), ``columns`` (the file's portfolio names) and ``returns`` (months x portfolios), from the first
    (value-weighted) or second (equal-weighted) monthly block, through ``through``."""
    return _kf_monthly(f"Portfolios_Formed_on_{name}_CSV.zip", name, through, weighting)


def ken_french_industries(n: int = 49, through: str = "2020-12", weighting: str = "value") -> dict:
    """Monthly returns of Kenneth French's ``n`` industry portfolios (5, 10, 12, 17, 30, 38, 48 or 49), as
    :func:`ken_french_sorts`."""
    return _kf_monthly(f"{n}_Industry_Portfolios_CSV.zip", f"industries{n}", through, weighting)


def ken_french_factors_monthly(through: str = "2020-12") -> dict:
    """Monthly Fama-French three factors and the riskless rate (decimal): ``date`` (YYYYMM), ``mkt_rf``, ``smb``, ``hml``,
    ``rf``."""
    k = _kf_monthly("F-F_Research_Data_Factors_CSV.zip", "ff3_monthly", through, "value")
    r = k["returns"]
    return {"date": k["date"], "mkt_rf": r[:, 0], "smb": r[:, 1], "hml": r[:, 2], "rf": r[:, 3]}


CBOE = "https://cdn.cboe.com/api/global/us_indices/daily_prices"


def cboe_index(symbol: str, through: str = "2025-12-31") -> dict:
    """A Cboe index's daily history (``COR3M``, the 3-month implied correlation of the 50 largest S&P 500 members;
    ``COR1M``; ``VIX``...): ``date`` (YYYYMMDD ints) and ``close``.  Cboe extends the file every day, so the
    manifest checks the frozen window through ``through``, as :func:`fred` does."""
    path = DATA / "cboe" / f"{symbol}_History.csv"
    if not path.exists():
        _atomic_write(path, _get(f"{CBOE}/{symbol}_History.csv"))
    rows = []
    for line in path.read_text().strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) < 2 or not parts[-1].strip():
            continue
        m, d, y = parts[0].split("/")
        rows.append((int(y) * 10000 + int(m) * 100 + int(d), float(parts[-1])))
    a = np.array(sorted(rows))
    a = a[a[:, 0] <= int(through.replace("-", ""))]
    frozen = json.dumps(a.round(6).tolist(), separators=(",", ":")).encode()
    _check(f"cboe/{symbol}/through_{through}", frozen, f"{CBOE}/{symbol}_History.csv")
    return {"date": a[:, 0].astype(int), "close": a[:, 1]}


# ---------------------------------------------------------------------------
# Cboe: VIX futures daily settlements, one CSV per expiry
# ---------------------------------------------------------------------------
CBOE_VX = "https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/VX_{}.csv"


def cboe_vx(expiry: str) -> dict:
    """Daily settlement prices of the VIX future expiring on ``expiry`` (YYYY-MM-DD) from Cboe Futures Exchange's
    public history: ``date`` (YYYYMMDD ints) and ``settle`` (index points), days with no settlement dropped. The parsed
    pairs are checksummed."""
    path = DATA / "cboe" / "vx" / f"VX_{expiry}.csv"
    if not path.exists():
        _atomic_write(path, _get(CBOE_VX.format(expiry)))
    rows = []
    for line in path.read_text().strip().splitlines()[1:]:
        parts = line.split(",")
        try:
            s = float(parts[6])
        except (ValueError, IndexError):
            continue
        if s > 0:
            rows.append((int(parts[0].replace("-", "")), s))
    a = np.array(sorted(rows))
    frozen = json.dumps(a.round(4).tolist(), separators=(",", ":")).encode()
    _check(f"cboe/vx/{expiry}", frozen, CBOE_VX.format(expiry))
    return {"date": a[:, 0].astype(int), "settle": a[:, 1]}


# ---------------------------------------------------------------------------
# Rates (Part 18): the Fed's fitted Treasury curve, the NY Fed's term premium, Treasury's par yields, gilts, EDGAR
# ---------------------------------------------------------------------------
GSW = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"


def gsw(start: str = "1961-06-14", through: str = "2025-12-31") -> dict:
    """The Federal Reserve's fitted US Treasury curve (Gurkaynak, Sack and Wright 2007), one row a business day:
    ``date`` (YYYYMMDD ints), the Svensson parameters ``beta`` (n, 4: percent) and ``tau`` (n, 2: years; ``beta[:, 3]``
    is 0 and ``tau[:, 1]`` NaN on days fitted with Nelson-Siegel alone), and ``y`` (n, 30): continuously compounded
    zero-coupon yields at 1..30 years, percent, NaN beyond the longest bond of the day.  The Fed refits and extends
    the file daily, so the manifest checks the frozen window."""
    path = DATA / "fed" / "feds200628.csv"
    if not path.exists():
        _atomic_write(path, _get(GSW))
    lines = path.read_text().splitlines()
    i0 = next(i for i, ln in enumerate(lines) if ln.startswith("Date,"))
    head = lines[i0].split(",")
    col = {h: j for j, h in enumerate(head)}
    names = ["BETA0", "BETA1", "BETA2", "BETA3", "TAU1", "TAU2"] + [f"SVENY{k:02d}" for k in range(1, 31)]
    lo, hi = int(start.replace("-", "")), int(through.replace("-", ""))
    rows = []
    for ln in lines[i0 + 1:]:
        f = ln.split(",")
        if len(f) < len(head) or not f[0]:
            continue
        d = int(f[0].replace("-", ""))
        if lo <= d <= hi:
            rows.append([d] + [float(f[col[n]]) if f[col[n]] not in ("NA", "") else np.nan for n in names])
    a = np.array(rows)
    frozen = json.dumps(np.nan_to_num(a, nan=-999).round(6).tolist(), separators=(",", ":")).encode()
    _check(f"fed/gsw/{start}_{through}", frozen, GSW)
    a = a[~np.isnan(a[:, 1])]  # holidays: rows of NA
    return {"date": a[:, 0].astype(int), "beta": a[:, 1:5], "tau": a[:, 5:7], "y": a[:, 7:37]}


ACM = "https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls"


def acm(through: str = "2025-12") -> dict:
    """The NY Fed's Adrian-Crump-Moench (2013) decomposition, monthly: ``date`` (YYYYMMDD, month end), and for 1..10
    years (percent) the fitted yield ``y``, the term premium ``tp`` and the risk-neutral (expected average short
    rate) yield ``rny``; ``y = tp + rny``.  Revised as the model is re-estimated, so the window is frozen."""
    import xlrd

    path = DATA / "nyfed" / "ACMTermPremium.xls"
    if not path.exists():
        _atomic_write(path, _get(ACM))
    sh = xlrd.open_workbook(str(path)).sheet_by_name("ACM Monthly")
    mon = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                       "Dec"], 1)}
    y1, m1 = map(int, through.split("-"))
    rows = []
    for i in range(1, sh.nrows):
        r = sh.row_values(i)
        dd, mm, yy = r[0].split("-")
        d = int(yy) * 10000 + mon[mm] * 100 + int(dd)
        if d // 100 <= y1 * 100 + m1:
            rows.append([d] + [float(x) for x in r[1:31]])
    a = np.array(rows)
    _check(f"nyfed/acm_monthly/through_{through}", json.dumps(a.round(6).tolist(), separators=(",", ":")).encode(),
           ACM)
    return {"date": a[:, 0].astype(int), "y": a[:, 1:11], "tp": a[:, 11:21], "rny": a[:, 21:31]}


TREASURY_PAR = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
                "{year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv")


def treasury_par(year: int) -> dict:
    """The US Treasury's daily par yield curve (from its quotes of on-the-run securities) for one calendar year:
    ``date`` (YYYYMMDD, oldest first), ``tenor`` (years) and ``y`` (days, tenors: percent, bond-equivalent; NaN where
    not published, e.g. the 20-year before 1993 or the 30-year in 2002-2006).  Past years are final; frozen anyway."""
    path = DATA / "treasury" / f"par_{year}.csv"
    if not path.exists():
        _atomic_write(path, _get(TREASURY_PAR.format(year=year)))
    lines = path.read_text().strip().splitlines()
    head = [h.strip('"') for h in lines[0].split(",")]
    unit = {"Mo": 1 / 12, "Month": 1 / 12, "Yr": 1.0}
    ten = []
    for h in head[1:]:
        n, u = h.split(" ", 1)
        ten.append(float(n) * unit[u.split()[0]])
    rows = []
    for ln in lines[1:]:
        f = ln.split(",")
        m, d, y = f[0].split("/")
        rows.append([int(y) * 10000 + int(m) * 100 + int(d)] + [float(x) if x else np.nan for x in f[1:]])
    a = np.array(sorted(rows))
    order = np.argsort(ten)
    out = {"date": a[:, 0].astype(int), "tenor": np.array(ten)[order], "y": a[:, 1:][:, order]}
    _check(f"treasury/par/{year}", json.dumps(np.nan_to_num(a, nan=-999).round(6).tolist(),
                                               separators=(",", ":")).encode(), TREASURY_PAR.format(year=year))
    return out


SEC_UA = {"User-Agent": "explainer-videos research bot"}  # a client name, no personal contact


def sec_facts(cik: int, concepts: tuple, filed_through: str = "2025-12-31") -> dict:
    """Selected facts (us-gaap, or ``dei:Name``) from EDGAR's XBRL company facts (data.sec.gov) for ``cik``: for each
    concept, a list of
    {unit, end, val, filed, form}, facts filed through ``filed_through`` only; the extract is checked."""
    path = DATA / "edgar" / f"CIK{cik:010d}.json"
    if not path.exists():
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
        with urllib.request.urlopen(urllib.request.Request(url, headers=SEC_UA), timeout=120) as r:
            _atomic_write(path, r.read())
    raw = json.loads(path.read_text())
    lim = int(filed_through.replace("-", ""))
    out = {}
    for c in concepts:
        tax, name = c.split(":", 1) if ":" in c else ("us-gaap", c)  # e.g. dei:EntityCommonStockSharesOutstanding
        body = raw["facts"].get(tax, {}).get(name, {"units": {}})
        rows = [{"unit": u, "end": x["end"], "val": x["val"], "filed": x["filed"], "form": x.get("form", "")}
                for u, lst in body["units"].items() for x in lst if int(x["filed"].replace("-", "")) <= lim]
        out[c] = sorted(rows, key=lambda q: (q["end"], q["filed"], q["form"], q["unit"]))
    _check(f"edgar/facts/CIK{cik:010d}/{'_'.join(sorted(concepts))[:120]}/through_{filed_through}",
           json.dumps(out, sort_keys=True, separators=(",", ":")).encode(),
           f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    return {"name": raw.get("entityName", ""), "facts": out}



def _sec_get(url: str, retries: int = 5) -> bytes:
    err = None
    for k in range(retries):
        try:
            time.sleep(0.15)  # EDGAR asks for at most ten requests a second
            with urllib.request.urlopen(urllib.request.Request(url, headers=SEC_UA), timeout=120) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(min(2 ** k, 30))
    raise RuntimeError(f"failed to fetch {url}: {err}")


def sec_frame(concept: str, period: str, unit: str = "USD", taxonomy: str = "us-gaap") -> dict:
    """One XBRL concept for every filer in one calendar period from EDGAR's frames API: ``period`` is CY2019 for a
    year's flow, CY2019Q4I for an instant at the year's end (CY2019Q2I for mid-year).  Returns {cik: (val, end,
    accn, name)}; the compact extract is cached and checked (frames gain late filers, so the first fetch is frozen)."""
    path = DATA / "edgar" / "frames" / f"{taxonomy}_{concept}_{unit}_{period}.json"
    url = f"https://data.sec.gov/api/xbrl/frames/{taxonomy}/{concept}/{unit}/{period}.json"
    if not path.exists():
        try:
            raw = json.loads(_sec_get(url))
            rows = sorted([[int(x["cik"]), x["val"], x.get("end", ""), x.get("accn", ""), x.get("entityName", "")]
                           for x in raw.get("data", [])])
        except RuntimeError as e:
            if "404" not in str(e):
                raise
            rows = []  # no filer used the concept in that period
        _atomic_write(path, json.dumps(rows, separators=(",", ":")).encode())
    body = path.read_bytes()
    _check(f"edgar/frames/{taxonomy}/{concept}/{unit}/{period}", body, url)
    return {r[0]: (r[1], r[2], r[3], r[4]) for r in json.loads(body)}


EFTS = "https://efts.sec.gov/LATEST/search-index?q=%22Item%201.03%22&forms=8-K&dateRange=custom&startdt={a}&enddt={b}&from={k}"


def sec_bankruptcy_8k(year: int) -> list:
    """Current reports (8-K) filed in ``year`` that report Item 1.03, Bankruptcy or Receivership, from EDGAR's
    full-text search: [cik, file_date (YYYYMMDD), form, name], one row per filing, sorted; checked."""
    path = DATA / "edgar" / "efts" / f"item103_{year}.json"
    if not path.exists():
        rows, k = {}, 0
        while True:
            d = json.loads(_sec_get(EFTS.format(a=f"{year}-01-01", b=f"{year}-12-31", k=k)))
            hits = d["hits"]["hits"]
            for h in hits:
                src = h["_source"]
                if "1.03" not in (src.get("items") or []):
                    continue
                for c in src.get("ciks", [])[:1]:
                    rows[(int(c), src["adsh"])] = [int(c), int(src["file_date"].replace("-", "")), src.get("form", ""),
                                                   (src.get("display_names") or [""])[0].split("  (")[0]]
            k += len(hits)
            if not hits or k >= d["hits"]["total"]["value"] or k >= 9900:
                break
        _atomic_write(path, json.dumps(sorted(rows.values()), separators=(",", ":")).encode())
    body = path.read_bytes()
    _check(f"edgar/efts/item1.03/{year}", body, EFTS.format(a=f"{year}-01-01", b=f"{year}-12-31", k=0))
    return json.loads(body)

TD = "https://www.treasurydirect.gov/TA_WS/securities/search?type={kind}&format=json"


def treasury_auctions(kind: str = "Note") -> list:
    """Every auction of Treasury ``kind`` ("Note" or "Bond") in TreasuryDirect's record, as dicts with ``cusip``,
    ``coupon`` (percent), ``issue`` and ``maturity`` (YYYYMMDD), ``term`` (e.g. "10-Year"), ``reopening``; auctions
    through 2025 only."""
    path = DATA / "treasury" / f"auctions_{kind}.json"
    if not path.exists():
        _atomic_write(path, _get(TD.format(kind=kind)))
    raw = path.read_bytes()
    out = []
    for r in json.loads(raw):
        try:
            iss = int(r["issueDate"][:10].replace("-", ""))
            mat = int(r["maturityDate"][:10].replace("-", ""))
            cpn = float(r["interestRate"])
        except (KeyError, ValueError):
            continue
        if iss <= 20251231:
            out.append({"cusip": r["cusip"], "coupon": cpn, "issue": iss, "maturity": mat,
                        "term": r.get("securityTerm", ""), "reopening": r.get("reopening", "") == "Yes"})
    out.sort(key=lambda q: (q["issue"], q["cusip"]))
    _check(f"treasurydirect/{kind}/through_2025", json.dumps(out, sort_keys=True, separators=(",", ":")).encode(),
           TD.format(kind=kind))
    return out


BOE = ("https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&Datefrom=01/Jan/{y0}"
       "&Dateto=31/Dec/2025&SeriesCodes={code}&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N")
_MON = {m: i + 1 for i, m in enumerate(("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                        "Dec"))}


def boe(code: str, start_year: int = 1975) -> dict:
    """A Bank of England database series (daily, as published, through 2025) as ``date`` and ``value``: e.g.
    XUDLUSS (spot US dollars per pound, London late afternoon), XUDLDS1/XUDLDS3/XUDLDSY (one-, three- and twelve-month
    forward outright rates, the same quote), IUDSOIA (SONIA)."""
    path = DATA / "boe" / f"{code}_{start_year}.csv"

    def fetch():  # the database sometimes answers with an error page: wait and ask again, politely
        for k in range(6):
            b = _get(BOE.format(y0=start_year, code=code))
            if b.startswith(b"DATE"):
                return b
            time.sleep(5 * (k + 1))
        raise RuntimeError(f"BoE {code}: the database returned an error page, not data")
    raw = _cached(f"boe/{code}/{start_year}_2025", path, fetch, BOE.format(y0=start_year, code=code))
    rows = []
    for line in raw.decode().strip().splitlines()[1:]:
        d, v = line.split(",")[:2]
        if not v.strip():
            continue
        dd, mm, yy = d.split()
        rows.append((int(yy) * 10000 + _MON[mm] * 100 + int(dd), float(v)))
    if not rows:
        raise RuntimeError(f"BoE {code}: no data (is the series code right?)")
    rows.sort()
    a = np.array(rows)
    return {"date": a[:, 0].astype(int), "value": a[:, 1]}


EIA = "https://www.eia.gov/dnav/{kind}/hist_xls/{series}d.xls"


def eia_daily(series: str, kind: str = "pet") -> dict:
    """An EIA daily price history from its spreadsheet (e.g. RCLC1..RCLC4, the NYMEX WTI futures contracts 1-4 at
    Cushing, which EIA published through April 2024; RWTC, the WTI spot; kind "ng" for RNGC1..RNGC4, Henry Hub
    futures). Excel dates become YYYYMMDD."""
    import xlrd

    path = DATA / "eia" / f"{series}d.xls"
    raw = _cached(f"eia/{series}/daily", path, lambda: _get(EIA.format(kind=kind, series=series)),
                  EIA.format(kind=kind, series=series))
    book = xlrd.open_workbook(file_contents=raw)
    sh = book.sheet_by_index(1)
    rows = []
    for i in range(3, sh.nrows):
        d, v = sh.row_values(i)[:2]
        if v in ("", None):
            continue
        y, m, dd, *_ = xlrd.xldate_as_tuple(d, book.datemode)
        rows.append((y * 10000 + m * 100 + dd, float(v)))
    a = np.array(rows)
    return {"date": a[:, 0].astype(int), "value": a[:, 1]}


CFTC_TFF = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"


def cftc_tff(code: str, start: str = "2010-01-01", through: str = "2025-12-31") -> dict:
    """The CFTC's Traders in Financial Futures report (futures only) for one contract market code (e.g. 043602, the
    10-year note; 044601, the 5-year; 042601, the 2-year; 020601, the bond), weekly: open interest and the long and
    short positions of dealers, asset managers, leveraged funds and other reportables, in contracts."""
    import urllib.parse

    q = urllib.parse.urlencode({"$where": f"cftc_contract_market_code='{code}' AND report_date_as_yyyy_mm_dd between "
                                          f"'{start}T00:00:00' and '{through}T00:00:00'",
                                "$order": "report_date_as_yyyy_mm_dd", "$limit": 5000})
    url = f"{CFTC_TFF}?{q}"
    path = DATA / "cftc" / f"tff_{code}_{start}_{through}.json"
    raw = _cached(f"cftc/tff/{code}/{start}_{through}", path, lambda: _get(url), url)
    keys = ["open_interest_all", "dealer_positions_long_all", "dealer_positions_short_all", "asset_mgr_positions_long",
            "asset_mgr_positions_short", "lev_money_positions_long", "lev_money_positions_short"]
    rows = json.loads(raw)
    out = {"date": np.array([int(r["report_date_as_yyyy_mm_dd"][:10].replace("-", "")) for r in rows])}
    for k in keys:
        out[k] = np.array([float(r.get(k, "nan")) for r in rows])
    return out

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
