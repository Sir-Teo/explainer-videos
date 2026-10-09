"""Precompute every piece of real footage in the trading-system video.

    python -m videos.trading.compute                   # everything missing
    python -m videos.trading.compute bench geo         # specific items
    python -m videos.trading.compute --force mm        # recompute

Big inputs and intermediates live in ``.cache/trading/`` (one day of Nasdaq TotalView-ITCH is 11.6 GB
compressed); the small results that scenes read are written to ``videos/trading/data/<name>.json`` and
committed, so the video renders offline exactly as published (and so numbers measured on this machine stay
the numbers the narration states).  Scenes call ``load(name)`` and never parse the feed themselves.

Market data: Nasdaq TotalView-ITCH 5.0, Wednesday December 10, 2025 (file S121025-v50 on emi.nasdaq.com),
the day of a Federal Reserve rate decision.
    itch        download the day and scan it once with native/itch_scan.c (counts, rates, histograms,
                per-stock message files for SPY IVV VOO QQQ NVDA AAPL TSLA)
    day         message counts by type, the per-second profile of the day, peak rates, the 2:00 pm burst
    messages    real Add / Execute / Delete messages of NVDA, byte for byte, decoded
    book        real NVDA order-book snapshots with every order in its queue; a short replay of real messages
    bookbench   the whole day of SPY through a plain Python book and through native/book.c
    race        reaction times after executions and order lifetimes (from the scan); SPY / IVV / VOO
                return correlation as a function of the time scale
    signal      order-book imbalance vs the next mid-price move, and how fast the signal decays
    mm          a market-making backtest with virtual orders queued behind the real ones; latency sweep
This machine (native/bench.c):
    bench       load latency vs working set (4 KiB vs 2 MiB pages), a system call, core-to-core, kernel
                UDP, a ring buffer, false sharing, branch prediction, OS jitter on a pinned core
Geography:
    geo         data-center coordinates (OpenStreetMap), great-circle distances, map outlines (Natural Earth)
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import time
import urllib.request
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

from .itch import CACHE, CLOSE_NS, ITCH_DIR, NS, OPEN_NS

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NATIVE = HERE / "native"
BIN = CACHE / "bin"
RAW = CACHE / "raw"
ITCH_FILE = "S121025-v50.txt.gz"
ITCH_URL = "https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/" + ITCH_FILE
ITCH_BYTES = 11_557_662_295
SYMBOLS = ["SPY", "IVV", "VOO", "QQQ", "NVDA", "AAPL", "TSLA"]
DATE = "2025-12-10"


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
_loaded: dict = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = DATA / f"{name}.json"
        if not p.exists():
            raise FileNotFoundError(f"{p} missing: run `python -m videos.trading.compute {name}`")
        _loaded[name] = json.loads(p.read_text())
    return _loaded[name]


def save(name: str, obj: dict) -> None:
    DATA.mkdir(exist_ok=True)

    def clean(x):
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [clean(v) for v in x]
        if isinstance(x, np.ndarray):
            return clean(x.tolist())
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating, float)):
            return float(f"{float(x):.6g}")
        return x

    (DATA / f"{name}.json").write_text(json.dumps(clean(obj), separators=(",", ":")))
    print(f"  wrote data/{name}.json ({(DATA / f'{name}.json').stat().st_size / 1e3:.0f} kB)")


def build(prog: str) -> Path:
    BIN.mkdir(parents=True, exist_ok=True)
    src, exe = NATIVE / f"{prog}.c", BIN / prog
    if not exe.exists() or exe.stat().st_mtime < src.stat().st_mtime:
        flags = ["-O3"] if prog == "itch_scan" else ["-O2"]
        subprocess.run(["gcc", *flags, "-march=native", "-pthread", "-o", str(exe), str(src), "-lm"], check=True)
    return exe


def log_bins(per_decade: int, n: int) -> np.ndarray:
    """Lower edges (ns) of the log bins used by the native programs."""
    return 10 ** (np.arange(n) / per_decade)


# ---------------------------------------------------------------------------
# itch: download + one native pass over the day
# ---------------------------------------------------------------------------
def do_itch():
    RAW.mkdir(parents=True, exist_ok=True)
    gz = RAW / ITCH_FILE
    if not gz.exists() or gz.stat().st_size != ITCH_BYTES:
        print(f"  downloading {ITCH_URL} (11.6 GB) ...")
        subprocess.run(["curl", "-sS", "--retry", "5", "-C", "-", "-o", str(gz), ITCH_URL], check=True)
    assert gz.stat().st_size == ITCH_BYTES
    exe = build("itch_scan")
    ITCH_DIR.mkdir(parents=True, exist_ok=True)
    t = time.time()
    gzip = subprocess.Popen(["gzip", "-dc", str(gz)], stdout=subprocess.PIPE)
    subprocess.run([str(exe), str(ITCH_DIR), *SYMBOLS], stdin=gzip.stdout, check=True)
    gzip.wait()
    print(f"  scanned in {time.time() - t:.0f} s")


# ---------------------------------------------------------------------------
# bench: this machine
# ---------------------------------------------------------------------------
def do_bench():
    exe = build("bench")
    out = {}
    for mode in ["syscall", "falseshare", "branch", "spsc", "pingpong", "jitter", "chase"]:
        t = time.time()
        r = subprocess.run([str(exe), mode], check=True, capture_output=True, text=True).stdout
        out[mode] = json.loads(r)
        print(f"  {mode}: {time.time() - t:.0f} s")
    cpu = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
    info = {}
    for line in cpu.splitlines():
        k, _, v = line.partition(":")
        if k.strip() in ("Model name", "L1d cache", "L2 cache", "L3 cache", "CPU(s)", "Hypervisor vendor"):
            info[k.strip()] = v.strip()
    out["cpu"] = info
    j = out["jitter"]
    gaps, at = np.array(j["gap_ns"], float), np.array(j["at_ns"], float)
    out["jitter"]["summary"] = {
        "events": len(gaps), "lost_fraction": float(gaps.sum() / (j["seconds"] * 1e9)),
        "max_gap_ns": float(gaps.max()) if len(gaps) else 0.0,
        "over_10us": int((gaps > 1e4).sum()), "over_100us": int((gaps > 1e5).sum()),
    }
    # keep the jitter arrays small: every gap over 1 us, plus a thinned sample of the rest
    keep = (gaps > 1000) | (np.arange(len(gaps)) % 20 == 0)
    out["jitter"]["gap_ns"], out["jitter"]["at_ns"] = gaps[keep].tolist(), at[keep].tolist()
    save("bench", out)


# ---------------------------------------------------------------------------
# geo: where the matching engines are
# ---------------------------------------------------------------------------
SITES = {
    # name: (label, lat, lon, address); coordinates from OpenStreetMap's Nominatim for the street address
    "aurora": ("CME Group (Aurora, IL)", 41.7980454, -88.2435528, "2905 Diehl Road, Aurora, IL (CyrusOne Aurora I)"),
    "carteret": ("Nasdaq (Carteret, NJ)", 40.5845104, -74.2433378, "1400 Federal Boulevard, Carteret, NJ (Equinix NY11)"),
    "mahwah": ("NYSE (Mahwah, NJ)", 41.0801838, -74.1532413, "1700 MacArthur Boulevard, Mahwah, NJ"),
    "secaucus": ("Equinix NY4 (Secaucus, NJ)", 40.7764281, -74.0697759, "755 Secaucus Road, Secaucus, NJ"),
    "cermak": ("350 E. Cermak (Chicago)", 41.8537537, -87.6183798, "350 East Cermak Road, Chicago, IL"),
}
C_KM_PER_MS = 299.792458
N_FIBER = 1.468  # group index of standard single-mode fiber at 1550 nm (Corning SMF-28: 1.4682)
NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
STATES = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
BOX = (-90.5, -71.5, 38.6, 44.6)  # lon0, lon1, lat0, lat1


def great_circle_km(a, b, r=6371.0088) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def great_circle_path(a, b, n=64):
    def vec(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        return np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
    p, q = vec(*a), vec(*b)
    w = math.acos(float(np.clip(p @ q, -1, 1)))
    pts = []
    for t in np.linspace(0, 1, n):
        v = (math.sin((1 - t) * w) * p + math.sin(t * w) * q) / math.sin(w)
        pts.append([math.degrees(math.atan2(v[1], v[0])), math.degrees(math.asin(v[2]))])
    return pts


def _clip_ring(ring, box, step=1):
    """Sutherland-Hodgman: the part of a polygon inside the map rectangle (None if nothing is left)."""
    lon0, lon1, lat0, lat1 = box
    pts = [(float(x), float(y)) for x, y in ring[::step]]
    edges = [(lambda p: p[0] >= lon0, lambda a, b: _cut_x(a, b, lon0)), (lambda p: p[0] <= lon1, lambda a, b: _cut_x(a, b, lon1)),
             (lambda p: p[1] >= lat0, lambda a, b: _cut_y(a, b, lat0)), (lambda p: p[1] <= lat1, lambda a, b: _cut_y(a, b, lat1))]
    for inside, cut in edges:
        if not pts:
            return None
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
        pts = out
    return [[round(x, 3), round(y, 3)] for x, y in pts] if len(pts) >= 3 else None


def _cut_x(a, b, x):
    t = (x - a[0]) / (b[0] - a[0])
    return (x, a[1] + t * (b[1] - a[1]))


def _cut_y(a, b, y):
    t = (y - a[1]) / (b[1] - a[1])
    return (a[0] + t * (b[0] - a[0]), y)


def do_geo():
    cache = CACHE / "geo"
    cache.mkdir(parents=True, exist_ok=True)

    def get(url, name):
        p = cache / name
        if not p.exists():
            urllib.request.urlretrieve(url, p)
        return json.loads(p.read_text())

    states = get(STATES, "us-states.json")
    lakes = get(NE + "ne_50m_lakes.geojson", "ne_50m_lakes.geojson")
    land = get(NE + "ne_50m_land.geojson", "ne_50m_land.geojson")
    out_land = []
    for f in land["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        out_land += [r for poly in polys if (r := _clip_ring(poly[0], BOX))]
    keep_states = ["Illinois", "Indiana", "Ohio", "Pennsylvania", "New Jersey", "New York", "Michigan", "Wisconsin",
                   "West Virginia", "Maryland", "Delaware", "Kentucky", "Connecticut", "Iowa", "Missouri", "Virginia",
                   "Massachusetts", "Vermont", "Rhode Island", "New Hampshire"]
    out_states = {}
    for f in states["features"]:
        name = f["properties"]["name"]
        if name not in keep_states:
            continue
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        rings = [r for poly in polys if (r := _clip_ring(poly[0], BOX))]
        out_states[name] = rings
    out_lakes = {}
    for f in lakes["features"]:
        name = f["properties"].get("name")
        if name in ("Lake Michigan", "Lake Erie", "Lake Huron", "Lake Ontario", "Lake Saint Clair"):
            g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            out_lakes[name] = [r for poly in polys if (r := _clip_ring(poly[0], BOX, 2))]
    sites = {k: {"label": v[0], "lat": v[1], "lon": v[2], "address": v[3]} for k, v in SITES.items()}
    routes = {}
    for dst in ("carteret", "mahwah", "secaucus"):
        a = (SITES["aurora"][1], SITES["aurora"][2])
        b = (SITES[dst][1], SITES[dst][2])
        km = great_circle_km(a, b)
        routes[dst] = {"km": km, "vacuum_ms": km / C_KM_PER_MS, "fiber_straight_ms": km * N_FIBER / C_KM_PER_MS,
                       "path": great_circle_path(a, b)}
    save("geo", {"box": BOX, "land": out_land, "states": out_states, "lakes": out_lakes, "sites": sites, "routes": routes,
                 "c_km_per_ms": C_KM_PER_MS, "n_fiber": N_FIBER})
    for k, r in routes.items():
        print(f"  Aurora -> {k}: {r['km']:.1f} km, vacuum {r['vacuum_ms']:.3f} ms, straight fiber {r['fiber_straight_ms']:.3f} ms")


# ---------------------------------------------------------------------------
# day: the shape of the day, from the scan
# ---------------------------------------------------------------------------
def scan_summary() -> dict:
    p = ITCH_DIR / "summary.json"
    if not p.exists():
        raise FileNotFoundError("run `python -m videos.trading.compute itch` first")
    return json.loads(p.read_text())


def do_day():
    s = scan_summary()
    per_ms = np.fromfile(ITCH_DIR / "per_ms.u32", dtype="<u4")
    per_ms_b = np.fromfile(ITCH_DIR / "per_ms_bytes.u32", dtype="<u4")
    per_s = per_ms.reshape(-1, 1000).sum(1)
    per_s_b = per_ms_b.reshape(-1, 1000).astype(np.int64).sum(1)
    sec0, sec1 = 4 * 3600, 20 * 3600
    rth = slice(OPEN_NS // NS, CLOSE_NS // NS)
    rth_ms = per_ms[OPEN_NS // 1_000_000:CLOSE_NS // 1_000_000]
    bursts = {}
    for name in ("093000", "140000", "160000"):
        us = np.fromfile(ITCH_DIR / f"burst_{name}.u32", dtype="<u4")  # [t - 100 ms, t + 400 ms) per microsecond
        t0 = int(name[:2]) * 3600 + int(name[2:4]) * 60
        bursts[name] = {
            "t0_s": t0, "pre_us": 100_000,
            "per_100us": us.reshape(-1, 100).sum(1),  # 5,000 bins
            "first_10ms_per_10us": us[100_000:110_000].reshape(-1, 10).sum(1),
            "first_1ms_per_us": us[100_000:101_000],
            "baseline_per_ms": float(us[:100_000].sum() / 100),
            "max_per_ms_after": float(us[100_000:].reshape(-1, 1000).sum(1).max()),
        }
        # the first microsecond at or after t0 with a message, and how many arrive in the next 100 us, 1 ms
        after = us[100_000:]
        nz = np.nonzero(after)[0]
        bursts[name]["first_us_after"] = int(nz[0]) if len(nz) else -1
    # messages per minute over the regular session, and the one-second view around 14:00
    around_2pm = per_ms[(14 * 3600 - 2) * 1000:(14 * 3600 + 3) * 1000]
    out = {
        "date": DATE, "file": ITCH_FILE, "file_bytes": ITCH_BYTES,
        "messages": s["messages"], "bytes": s["bytes"], "messages_rth": s["messages_rth"], "bytes_rth": s["bytes_rth"],
        "symbols": s["symbols"], "count_by_type": s["count_by_type"], "count_by_type_rth": s["count_by_type_rth"],
        "peaks": s["peaks"], "system_events": s["system_events"], "live_orders_peak": s["live_orders_peak"],
        "added_rth": s["added_rth"], "added_rth_traded": s["added_rth_traded"], "fate_rth": s["fate_rth"],
        "deleted_within": s["deleted_within"], "nonmonotonic": s["nonmonotonic"],
        "per_s": per_s[sec0:sec1], "per_s_t0": sec0,
        "per_s_bytes_max": int(per_s_b.max()), "per_ms_bytes_max": int(per_ms_b.max()),
        "per_ms_bytes_max_at_ms": int(per_ms_b.argmax()),
        "rth_ms_mean": float(rth_ms.mean()), "rth_ms_median": float(np.median(rth_ms)),
        "rth_s_mean": float(per_s[rth].mean()), "rth_s_max": int(per_s[rth].max()),
        "rth_s_max_at": int(np.argmax(per_s[rth]) + OPEN_NS // NS),
        "around_2pm_per_ms": around_2pm, "around_2pm_t0_ms": (14 * 3600 - 2) * 1000,
        "bursts": bursts,
    }
    save("day", out)
    print(f"  {s['messages']:,} messages, {s['bytes'] / 1e9:.1f} GB; peak per ms {s['peaks'][3]['max']}")


# ---------------------------------------------------------------------------
# windows: every message around 2:00 pm, by type; the busiest microsecond of the day
# ---------------------------------------------------------------------------
def do_windows():
    import collections
    import csv

    csv_path = ITCH_DIR / "windows.csv"
    t2 = 14 * 3600 * NS
    nflx = (38317 * NS + 273_000_000, 38317 * NS + 274_000_000)
    if not csv_path.exists():
        exe = build("itch_window")
        gzip = subprocess.Popen(["gzip", "-dc", str(RAW / ITCH_FILE)], stdout=subprocess.PIPE)
        subprocess.run([str(exe), str(csv_path), str(nflx[0]), str(nflx[1]), str(t2 - 2 * NS), str(t2 + 3 * NS)],
                       stdin=gzip.stdout, check=True)
        gzip.kill()
    bins = collections.defaultdict(collections.Counter)
    syms = collections.defaultdict(set)
    burst = collections.Counter()
    burst_syms = collections.Counter()
    burst_ts = collections.Counter()
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            ts = int(r["ts_ns"])
            if t2 - 2 * NS <= ts < t2 + 3 * NS:
                k = (ts - t2) // 100_000_000  # 100 ms bins, -20 .. 29
                bins[k][r["type"]] += 1
                syms[k].add(r["symbol"])
            elif nflx[0] <= ts < nflx[1]:
                burst[r["type"]] += 1
                burst_syms[r["symbol"]] += 1
                burst_ts[ts] += 1
    ks = list(range(-20, 30))
    top_ts, top_n = burst_ts.most_common(1)[0]
    out = {
        "bins_100ms": ks,
        "by_type": {t: [bins[k][t] for k in ks] for t in "ADUEXFPC"},
        "total": [sum(bins[k].values()) for k in ks],
        "symbols": [len(syms[k]) for k in ks],
        "burst": {"ts": top_ts, "same_ns": top_n, "types": dict(burst), "symbol": burst_syms.most_common(1)[0][0],
                  "symbol_count": burst_syms.most_common(1)[0][1]},
    }
    save("windows", out)
    k5 = ks.index(-5)
    print(f"  13:59:59.5: {out['total'][k5]} messages, {out['by_type']['D'][k5]} deletes, {out['symbols'][k5]} symbols;"
          f" burst {top_n} messages at one ns in {out['burst']['symbol']}")


# ---------------------------------------------------------------------------
# messages: real bytes
# ---------------------------------------------------------------------------
def do_messages():
    from .itch import clock, decode, raw_messages

    msgs = raw_messages("NVDA")
    picks = {}
    for m in msgs:
        t = chr(m[0])
        if t in ("A", "E", "D", "X", "U") and t not in picks:
            d = decode(m)
            if t == "A" and d["shares"] < 100:
                continue
            picks[t] = {"hex": m.hex(), "fields": d, "clock": clock(d["timestamp"])}
        if len(picks) == 5:
            break
    # the stream around the first pick: types and timestamps of 40 consecutive messages
    first_ts = [decode(m)["timestamp"] for m in msgs[:2000] if chr(m[0]) in "AEDXU"]
    seq = []
    for m in msgs[:60]:
        seq.append({"type": chr(m[0]), "len": len(m), "ts": int.from_bytes(m[5:11], "big")})
    head = (ITCH_DIR / "head.bin").read_bytes()[:400]
    save("messages", {"picks": picks, "seq": seq, "head_hex": head.hex(), "nvda_first_2000_span_ns": first_ts[-1] - first_ts[0]})
    for t, p in picks.items():
        print(f"  {t} {p['clock']} {p['hex']}")


# ---------------------------------------------------------------------------
# book: real NVDA queues
# ---------------------------------------------------------------------------
def do_book():
    from .itch import Book, clock, iter_rows, records

    recs = records("NVDA")
    targets = [10 * 3600 * NS + 30 * 60 * NS, 13 * 3600 * NS + 59 * 60 * NS + 59 * NS, 14 * 3600 * NS + 1 * NS]
    book = Book()
    snaps, replay, k = [], None, 0
    spreads, last_t, tw_spread, tw_total = [], None, 0.0, 0.0
    REPLAY_N = 80
    for i, ts, typ, ref, ref2, shares, price, side in iter_rows(recs):
        r = {"type": typ, "ref": ref, "ref2": ref2, "shares": shares, "price": price, "side": side}
        if replay is not None and len(replay["msgs"]) < REPLAY_N and typ in (65, 70, 69, 67, 88, 68, 85):
            # record where in its queue the order is, before applying
            o = book.orders.get(ref)
            pos = None
            if o is not None:
                lv = book.levels[o[0]][o[1]]
                pos = list(lv.keys()).index(ref)
            replay["msgs"].append({"ts": ts, "type": chr(typ), "ref": ref, "shares": shares,
                                   "price": price // 100 if typ in (65, 70, 85) else (o[1] if o else None),
                                   "side": chr(side) if typ in (65, 70) else (chr(o[0]) if o else None), "pos": pos})
        book.apply(r)
        if OPEN_NS <= ts < CLOSE_NS and book.bid and book.ask:
            if last_t is not None:
                dt = ts - last_t
                tw_spread += dt * (cur_spread)
                tw_total += dt
            cur_spread = book.ask - book.bid
            last_t = ts
        if k < len(targets) and ts >= targets[k]:
            bids, asks = book.ladder(10)
            snaps.append({"t": targets[k], "clock": clock(targets[k], 3), "bids": bids, "asks": asks,
                          "n_orders": len(book.orders)})
            if k == 0:
                replay = {"t0": ts, "start_bids": bids, "start_asks": asks, "msgs": []}
            k += 1
    save("book", {"symbol": "NVDA", "snapshots": snaps, "replay": replay,
                  "tw_spread_cents": tw_spread / tw_total if tw_total else None})
    print(f"  {len(snaps)} snapshots; time-weighted spread {tw_spread / tw_total:.3f} cents")


# ---------------------------------------------------------------------------
# bookbench: plain Python vs the native book, on the whole day of SPY
# ---------------------------------------------------------------------------
def do_bookbench():
    from .itch import Book, iter_rows, records

    exe = build("book")
    native = json.loads(subprocess.run([str(exe), str(ITCH_DIR / "sym_SPY.bin")], check=True, capture_output=True,
                                       text=True).stdout)
    recs = records("SPY")
    book = Book()
    rows = list(iter_rows(recs))  # materialize first: time the book, not the file
    t = time.perf_counter_ns()
    for i, ts, typ, ref, ref2, shares, price, side in rows:
        book.apply({"type": typ, "ref": ref, "ref2": ref2, "shares": shares, "price": price, "side": side})
    dt = time.perf_counter_ns() - t
    py = {"ns_per_message": dt / len(rows), "total_s": dt / 1e9, "end_bid": book.bid, "end_ask": book.ask}
    # both books must agree at the end of the day (empty: no bid, no ask)
    assert (py["end_bid"] if py["end_bid"] is not None else -1) == native["end_best_bid_cents"]
    assert (py["end_ask"] if py["end_ask"] is not None else 262144) == native["end_best_ask_cents"]
    save("bookbench", {"symbol": "SPY", "messages": len(rows), "python": py, "native": native})
    print(f"  python {py['ns_per_message']:.0f} ns/msg; native {native['variants']}")


# ---------------------------------------------------------------------------
# race: how fast the market reacts, and how quickly correlations appear
# ---------------------------------------------------------------------------
def bbo_series(sym: str, t0=OPEN_NS, t1=CLOSE_NS):
    """(ts, bid, ask, bid_size, ask_size) at every message that changes the top of the book, regular hours."""
    from .itch import Book, iter_rows, records

    book = Book()
    out, last = [], None
    for i, ts, typ, ref, ref2, shares, price, side in iter_rows(records(sym)):
        book.apply({"type": typ, "ref": ref, "ref2": ref2, "shares": shares, "price": price, "side": side})
        if ts < t0:
            continue
        if ts >= t1:
            break
        b, a = book.bid, book.ask
        if b is None or a is None:
            continue
        cur = (b, a, book.depth(66, b), book.depth(83, a))
        if cur != last:
            out.append((ts, *cur))
            last = cur
    return np.array(out, dtype=np.int64)


def bbo_cached(sym: str) -> np.ndarray:
    p = CACHE / f"bbo_{sym}.npy"
    if not p.exists():
        t = time.time()
        np.save(p, bbo_series(sym))
        print(f"  BBO series for {sym}: {time.time() - t:.0f} s")
    return np.load(p)


def sample_mid(bbo: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Mid-price (cents) in effect at each grid time (last change at or before it)."""
    idx = np.searchsorted(bbo[:, 0], grid, side="right") - 1
    mid = (bbo[:, 1] + bbo[:, 2]) / 2.0
    return mid[np.clip(idx, 0, None)]


def do_race():
    react = np.fromfile(ITCH_DIR / "reaction.u64", dtype="<u8").reshape(6, 200)
    gaps = np.fromfile(ITCH_DIR / "gaps.u64", dtype="<u8")
    life = np.fromfile(ITCH_DIR / "lifetimes.u64", dtype="<u8").reshape(4, 160)
    s = scan_summary()
    # S&P 500 ETFs on Nasdaq's book: correlation of mid-price returns at many time scales
    t0, t1 = OPEN_NS + 5 * 60 * NS, CLOSE_NS - 5 * 60 * NS
    bbo = {k: bbo_cached(k) for k in ("SPY", "IVV", "VOO")}
    scales_ms = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 30000, 60000]
    corr = {"SPY_IVV": [], "SPY_VOO": [], "IVV_VOO": []}
    for dms in scales_ms:
        step = int(dms * 1e6)
        grid = np.arange(t0, t1, step, dtype=np.int64)
        r = {}
        for k, b in bbo.items():
            m = sample_mid(b, grid)
            r[k] = np.diff(np.log(m))
        for pair in corr:
            a, c = pair.split("_")
            x, y = r[a], r[c]
            ok = (x != 0) | (y != 0)
            corr[pair].append(float(np.corrcoef(x[ok], y[ok])[0, 1]) if ok.sum() > 10 else 0.0)
    # one minute and one second of the three mid-prices, for the zoom
    def window(a, b):
        out = {}
        for k, v in bbo.items():
            m = (v[:, 0] >= a) & (v[:, 0] < b)
            first = np.searchsorted(v[:, 0], a, side="right") - 1
            sel = np.r_[first, np.nonzero(m)[0]]
            out[k] = {"t": (v[sel, 0] - a), "mid": (v[sel, 1] + v[sel, 2]) / 2}
        return out
    day_grid = np.arange(OPEN_NS, CLOSE_NS, 60 * NS, dtype=np.int64)
    day = {k: sample_mid(v, day_grid) for k, v in bbo.items()}
    wz = 11 * 3600 * NS
    save("race", {
        "reaction_bins_ns": log_bins(20, 201), "reaction": react, "reaction_kinds": ["add", "delete", "cancel", "replace",
                                                                                     "any", "same_side_cancel_or_delete"],
        "gaps": gaps, "lifetime_bins_ns": log_bins(10, 161), "lifetimes": life,
        "lifetime_kinds": ["deleted", "fully_executed", "replaced", "first_partial_cancel"],
        "added_rth": s["added_rth"], "added_rth_traded": s["added_rth_traded"], "fate_rth": s["fate_rth"],
        "deleted_within": s["deleted_within"],
        "corr_scales_ms": scales_ms, "corr": corr,
        "day_mid": day, "day_t0_ns": OPEN_NS, "minute": window(wz, wz + 60 * NS), "second": window(wz, wz + NS),
        "zoom_t0_ns": wz,
    })


# ---------------------------------------------------------------------------
# signal: order-book imbalance predicts the next move of the mid-price
# ---------------------------------------------------------------------------
def do_signal():
    out = {}
    for sym in ("NVDA", "SPY"):
        b = bbo_cached(sym)
        ts, bid, ask, qb, qa = b.T
        one_tick = (ask - bid) == 1
        mid = (bid + ask) / 2.0
        imb = qb / np.maximum(qb + qa, 1)
        # next mid change after each state (only states with a one-cent spread)
        chg = np.nonzero(np.diff(mid))[0] + 1  # indices where the mid changed
        nxt = np.searchsorted(chg, np.arange(len(mid)), side="right")
        valid = nxt < len(chg)
        up = np.zeros(len(mid), bool)
        up[valid] = mid[chg[nxt[valid]]] > mid[np.arange(len(mid))[valid]]
        sel = one_tick & valid
        edges = np.linspace(0, 1, 21)
        k = np.clip(np.digitize(imb[sel], edges) - 1, 0, 19)
        p_up = [float(up[sel][k == i].mean()) if (k == i).sum() > 50 else None for i in range(20)]
        n_bin = [int((k == i).sum()) for i in range(20)]
        # how fast it decays: correlation of (imbalance - 1/2) with the mid change over horizon h, sampled each 100 ms
        grid = np.arange(OPEN_NS + 5 * 60 * NS, CLOSE_NS - 6 * 60 * NS, 100_000_000, dtype=np.int64)
        idx = np.searchsorted(ts, grid, side="right") - 1
        i0 = imb[idx] - 0.5
        hs_ms = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 30000, 60000, 300000]
        rho = []
        for h in hs_ms:
            j = np.searchsorted(ts, grid + int(h * 1e6), side="right") - 1
            d = mid[j] - mid[idx]
            rho.append(float(np.corrcoef(i0, d)[0, 1]))
        out[sym] = {"edges": edges, "p_up": p_up, "n": n_bin, "horizons_ms": hs_ms, "corr": rho,
                    "one_tick_share": float(one_tick.mean()), "states": int(len(b))}
        print(f"  {sym}: P(up) from {p_up[1]} to {p_up[-2]}; corr at 10ms {rho[3]:.3f}")
    save("signal", out)


# ---------------------------------------------------------------------------
# mm: a market maker's virtual orders, queued behind the real ones
# ---------------------------------------------------------------------------
class Quote:
    """One virtual resting order.  ``ahead`` holds the real orders that were in the queue when it arrived
    (ref -> shares still ahead); anything arriving later is behind it."""
    __slots__ = ("side", "price", "size", "ahead", "t_live", "ahead0")

    def __init__(self, side, price, size, ahead, t_live):
        self.side, self.price, self.size, self.ahead, self.t_live = side, price, size, ahead, t_live
        self.ahead0 = sum(ahead.values())


class MM:
    """Quote 100 shares at the best bid and the best ask, re-joining whenever the best price moves; optionally
    stand aside on a side whose queue is thin (imbalance below ``theta``); inventory capped at +-``cap``.
    Every action (place, cancel) reaches the exchange ``latency`` ns after the decision."""

    def __init__(self, name, latency, theta=None, size=100, cap=500):
        self.name, self.latency, self.theta, self.size, self.cap = name, latency, theta, size, cap
        self.q = {66: None, 83: None}  # live quotes
        self.want = {66: None, 83: None}  # price we last asked for (None = no quote)
        self.pending = []  # (t_effective, side, price or None)
        self.inv, self.cash = 0, 0
        self.fills = []  # (ts, side, price_cents, qty, ahead_at_join)

    def decide(self, ts, book):
        b, a = book.bid, book.ask
        if b is None or a is None or a <= b:
            targets = {66: None, 83: None}
        else:
            qb, qa = book.depth(66, b), book.depth(83, a)
            imb = qb / (qb + qa)
            targets = {66: b, 83: a}
            if self.theta is not None:
                if imb < self.theta:
                    targets[66] = None
                if 1 - imb < self.theta:
                    targets[83] = None
            if self.inv >= self.cap:
                targets[66] = None
            if self.inv <= -self.cap:
                targets[83] = None
        for side, px in targets.items():
            if px != self.want[side]:
                self.want[side] = px
                self.pending.append((ts + self.latency, side, px))

    def arrive(self, ts, book):
        """Apply actions that reach the exchange by ``ts`` (cancel the old quote, join the back of the new queue)."""
        keep = []
        for t, side, px in self.pending:
            if t > ts:
                keep.append((t, side, px))
                continue
            self.q[side] = None
            if px is not None:
                lv = book.levels[side].get(px, {})
                self.q[side] = Quote(side, px, self.size, dict(lv), t)
        self.pending = keep

    def on_message(self, ts, typ, ref, shares, order):
        """A real message about order ``order`` = [side, price, shares] (looked up before the book applies it)."""
        if order is None:
            return
        side, price = order[0], order[1]
        q = self.q[side]
        if q is None:
            return
        if q.price != price:
            # a trade at a worse price than ours on our side means the incoming order swept through our level
            worse = price < q.price if side == 66 else price > q.price
            if worse and typ in (69, 67):
                self.fill(ts, q, q.size)
            return
        if ref in q.ahead:
            if typ in (69, 67, 88):  # executed or partly canceled: fewer shares ahead
                left = q.ahead[ref] - shares
                if left > 0:
                    q.ahead[ref] = left
                else:
                    del q.ahead[ref]
            elif typ in (68, 85):  # deleted, or replaced (which loses its place)
                del q.ahead[ref]
        elif typ in (69, 67):
            # an order that queued behind us traded: in price-time priority the incoming order reached us first
            q.ahead.clear()
            self.fill(ts, q, min(q.size, shares))

    def fill(self, ts, q, qty):
        side, price = q.side, q.price
        q.size -= qty
        sgn = 1 if side == 66 else -1
        self.inv += sgn * qty
        self.cash -= sgn * qty * price
        self.fills.append((ts, side, price, qty, q.ahead0))
        if q.size == 0:
            self.q[side] = None
            self.want[side] = None  # free to re-quote


def do_mm():
    from .itch import Book, iter_rows, records

    sym = "NVDA"
    t0, t1 = OPEN_NS + 15 * 60 * NS, CLOSE_NS - 15 * 60 * NS
    lat = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    mms = [MM(f"join_{l}", l) for l in lat] + [MM(f"signal_{l}", l, theta=0.3) for l in lat]
    book = Book()
    t = time.time()
    for i, ts, typ, ref, ref2, shares, price, side in iter_rows(records(sym)):
        r = {"type": typ, "ref": ref, "ref2": ref2, "shares": shares, "price": price, "side": side}
        if ts < t0:
            book.apply(r)
            continue
        if ts >= t1:
            break
        for m in mms:
            if m.pending:
                m.arrive(ts, book)
        order = book.orders.get(ref) if typ in (69, 67, 88, 68, 85) else None
        if order is not None:
            order = list(order)
            for m in mms:
                m.on_message(ts, typ, ref, shares, order)
        b0, a0 = book.bid, book.ask
        book.apply(r)
        for m in mms:
            m.decide(ts, book)
    print(f"  replayed in {time.time() - t:.0f} s")
    bbo = bbo_cached(sym)
    mids = (bbo[:, 1] + bbo[:, 2]) / 2.0

    def mid_at(tt):
        return mids[np.clip(np.searchsorted(bbo[:, 0], tt, side="right") - 1, 0, None)]

    horizons_ms = [0, 1, 10, 100, 1000, 10_000, 60_000]
    end_mid = float(mid_at(np.array([t1]))[0])
    out = {"symbol": sym, "t0": t0, "t1": t1, "latencies_ns": lat, "horizons_ms": horizons_ms, "runs": {}}
    for m in mms:
        f = np.array(m.fills, dtype=np.int64).reshape(-1, 5)
        n = len(f)
        res = {"fills": n, "shares": int(f[:, 3].sum()) if n else 0, "end_inventory": m.inv}
        if n:
            ts, side, px, qty, ahead = f.T
            sgn = np.where(side == 66, 1, -1)
            # per-share edge vs the mid at each horizon: (mid(t+h) - price) * sign, in cents
            edges = []
            for h in horizons_ms:
                mh = mid_at(ts + int(h * 1e6))
                edges.append(float(np.sum((mh - px) * sgn * qty) / qty.sum()))
            res["markout_cents"] = edges
            res["pnl_dollars"] = float((m.cash + m.inv * end_mid) / 100)
            res["pnl_cents_per_share"] = float((m.cash + m.inv * end_mid) / qty.sum())
            res["median_ahead_shares"] = float(np.median(ahead))
            res["mean_ahead_shares"] = float(np.mean(ahead))
            if m.name == "join_10000":
                res["sample"] = f[:400].tolist()
        out["runs"][m.name] = res
        print(f"  {m.name:>16}: {n:6d} fills, pnl/share {res.get('pnl_cents_per_share', 0):+.3f} c, markouts "
              f"{[round(x, 3) for x in res.get('markout_cents', [])]}, ahead {res.get('median_ahead_shares')}")
    save("mm", out)


ITEMS = {
    "itch": do_itch,
    "day": do_day,
    "windows": do_windows,
    "messages": do_messages,
    "book": do_book,
    "bookbench": do_bookbench,
    "race": do_race,
    "signal": do_signal,
    "mm": do_mm,
    "bench": do_bench,
    "geo": do_geo,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("items", nargs="*")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    todo = args.items or list(ITEMS)
    for name in todo:
        done = (ITCH_DIR / "summary.json").exists() if name == "itch" else (DATA / f"{name}.json").exists()
        if done and not args.force and not args.items:
            print(f"[{name}] cached")
            continue
        print(f"[{name}]")
        ITEMS[name]()


if __name__ == "__main__":
    main()
