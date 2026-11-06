"""Precompute everything numerical in Part 37 of *Computer Science, Built* ("Networks II: Reliable Conversation").

    python -m videos.cs.cs37.compute              # everything missing
    python -m videos.cs.cs37.compute --force job

Results are cached in ``.cache/cs37/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/net/`` (rdt, tcp, cc, app); tests in tests/test_cs37_transport.py.

Items:
    udp         ten thousand datagrams across a channel like IP's: how many are lost, duplicated, reordered
    rdt         stop-and-wait and the alternating-bit protocol: correct on a FIFO channel under loss, wrong once
                packets reorder; utilization, measured against (L/R) / (RTT + L/R)
    windows     Go-Back-N and Selective Repeat: utilization against window, with and without loss; the sequence-space
                bound, tested at its edge
    handshake   round trips before the first byte; SYN cookies; TIME_WAIT; the receive window as a throughput cap
    rtt         RTT samples from a shared bottleneck; RFC 793's timer against Jacobson and Karels's; spurious timeouts
    collapse    1986 in miniature: fixed windows and timers against Jacobson's TCP as the offered load grows
    chiujain    two users and a binary signal: AIMD, AIAD, MIAD and MIMD trajectories in the phase plane
    sawtooth    one Reno flow's window; throughput against loss, measured beside Mathis's formula; RTT unfairness
    buffers     bufferbloat: buffer sizes against utilization and delay; RED and CoDel; Appenzeller's BDP / sqrt(n)
    modern      CUBIC and BBR beside Reno: windows, throughput, queues; Kleinrock's operating point; Vegas beside Reno
    num         Kelly's network utility maximization by dual ascent on two topologies, against max-min fairness
    dns         a resolver's caching on a day of lookups; Kaminsky's odds, without and with source-port randomization
    web         a page of 41 objects over HTTP/1.1, HTTP/2 and QUIC at rising loss; handshakes in round trips
    cdn         Zipf's law fitted on the novels' words; an LRU cache on the words as requests, against Che's formula
    job         the novels fetched from Frankfurt over our TCP on a lossy link (Reno, CUBIC, BBR); ledger row 14
    frontier    starvation: delay-based flows beside each other with non-congestive jitter (Arun, Alizadeh and
                Balakrishnan, 2022)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import random
import re
from collections import Counter

from explainer.ai.cache import Cache

CACHE = Cache("cs37")
load = CACHE.load

RTT = 0.108                       # San Francisco to Frankfurt, as Part 36's ping measured it
MBPS = 100.0


def _t(trace, every=1):
    return [[round(a, 4), round(b, 3)] for a, b in trace[::every]]


# ---- reliability from scratch ------------------------------------------------------------------------------------
def compute_udp() -> dict:
    from explainer.cs.net.rdt import Channel
    ch = Channel(delay=0.054, rate=10_000, loss=0.01, dup=0.002, reorder=0.03, jitter=0.002, seed=37)
    arr = []
    for i in range(10_000):
        for a in ch.arrivals(i / 10_000):
            arr.append((a, i))
    arr.sort()
    got = [i for _, i in arr]
    c = Counter(got)
    lost = sum(1 for i in range(10_000) if i not in c)
    dup = sum(v - 1 for v in c.values() if v > 1)
    seen_max, late = -1, 0
    for i in got:
        if i < seen_max:
            late += 1
        seen_max = max(seen_max, i)
    first = got[:40]
    return {"sent": 10_000, "arrived": len(got), "lost": lost, "duplicated": dup, "out_of_order": late,
            "first": first, "udp_header": 8, "tcp_header": 20}


def compute_rdt() -> dict:
    from explainer.cs.net import rdt
    # a short demonstration on a slow line, for the sequence diagram
    demo = rdt.run("stop-and-wait", 6, seq_bits=1, channel=rdt.Channel(delay=0.05, rate=100, loss=0.25, seed=3))
    fifo = [rdt.run("stop-and-wait", 500, seq_bits=1, channel=rdt.Channel(loss=0.1, seed=s))["correct"]
            for s in range(20)]
    reo = []
    for s in range(20):
        r = rdt.run("stop-and-wait", 500, seq_bits=1, channel=rdt.Channel(loss=0.1, reorder=0.2, seed=s))
        d = r["delivered"]
        bad = next((k for k, v in enumerate(d) if v != k), len(d))
        reo.append({"correct": r["correct"], "first_error": bad, "wrong": d[bad] if bad < len(d) else None})
    # utilization of stop-and-wait: lab channel, then the Atlantic at 1 Gb/s
    util = []
    for rate in (100, 1000, 10_000):
        r = rdt.run("stop-and-wait", 400, channel=rdt.Channel(delay=0.05, rate=rate))
        util.append({"rate": rate, "measured": r["utilization"], "formula": rdt.utilization(1 / rate, 0.1)})
    L_R = 1500 * 8 / 1e9
    return {"fifo_correct": sum(fifo), "reorder_correct": sum(x["correct"] for x in reo), "trials": 20,
            "reorder_example": next(x for x in reo if not x["correct"]), "util": util,
            "atlantic": {"L_over_R": L_R, "rtt": RTT, "util": rdt.utilization(L_R, RTT),
                         "mbps": rdt.utilization(L_R, RTT) * 1000},
            "demo": {"sent": demo["sent"], "retx": demo["retransmissions"], "delivered": demo["delivered"]}}


def compute_windows() -> dict:
    from explainer.cs.net import rdt
    rows = []
    for W in (1, 2, 4, 8, 16, 32, 64, 128):
        row = {"W": W, "formula": rdt.utilization(0.001, 0.1, W)}
        for p in ("go-back-n", "selective-repeat"):
            for loss in (0.0, 0.02):
                r = rdt.run(p if W > 1 else "stop-and-wait", 2000, window=W,
                            channel=rdt.Channel(delay=0.05, rate=1000, loss=loss, seed=W))
                assert r["correct"]
                row[f"{p}_{loss}"] = r["utilization"]
                row[f"{p}_{loss}_retx"] = r["retransmissions"]
        rows.append(row)
    edge = []
    for p, W, bits in (("go-back-n", 7, 3), ("go-back-n", 8, 3), ("selective-repeat", 4, 3),
                       ("selective-repeat", 5, 3)):
        ok = [rdt.run(p, 1500, window=W, seq_bits=bits, channel=rdt.Channel(loss=0.1, seed=s))["correct"]
              for s in range(10)]
        edge.append({"protocol": p, "W": W, "bits": bits, "space": 2 ** bits, "correct": sum(ok), "trials": 10})
    return {"rows": rows, "edge": edge, "rtt": 0.1, "L_over_R": 0.001}


def compute_handshake() -> dict:
    # round trips before the first byte of a response, on the 108 ms path
    setups = [("TCP + TLS 1.2", 3), ("TCP + TLS 1.3", 2), ("QUIC (TLS 1.3 inside)", 1), ("QUIC 0-RTT resumption", 0)]
    rows = [{"name": n, "rtts": k, "first_byte_ms": (k + 1) * RTT * 1000} for n, k in setups]
    # a SYN cookie, built the way Linux does: 5 bits of time, 3 bits of MSS index, 24 bits of keyed hash
    key = b"server secret, rotated"
    four = ("203.0.113.7", 51544, "10.4.0.2", 443)
    t = 1_731_000_000 // 64 % 32
    mss_table = [536, 1300, 1440, 1460]
    mss_i = 3
    msg = f"{four}|{t}".encode()
    h = int.from_bytes(hmac.new(key, msg, hashlib.sha256).digest()[:3], "big")
    client_isn = 0x5EED1234
    cookie = ((t << 27) | (mss_i << 24) | h)
    isn = (cookie + client_isn) % 2 ** 32
    # flow control: the receive window caps throughput at window / RTT
    caps = [{"window": w, "mbps": w * 8 / RTT / 1e6} for w in (65_535, 1 << 20, 16 << 20)]
    bdp = MBPS * 1e6 * RTT / 8
    # TIME_WAIT: 2 MSL
    ports = 65535 - 32768 + 1
    return {"rows": rows, "rtt_ms": RTT * 1000, "cookie": {"t": t, "mss": mss_table[mss_i], "hash": h,
            "value": cookie, "isn": isn, "hex": f"{isn:08x}"}, "caps": caps, "bdp_bytes": bdp,
            "time_wait": {"msl": 30, "wait": 60, "ports": ports, "per_second": ports / 60}}


def compute_rtt() -> dict:
    from explainer.cs.net.tcp import Flow, dumbbell
    flows = [Flow("reno", rtt=RTT)] + [Flow("reno", rtt=RTT * (0.5 + 0.25 * i), start=2 + 3 * i) for i in range(5)]
    r = dumbbell(flows, mbps=20, duration=40, buffer=400, seed=4)
    samples = r["flows"][0]["rtts"]
    xs = [s for _, s in samples]
    out = {"samples": [[round(a, 3), round(b, 4)] for a, b in samples]}
    # RFC 793: SRTT = a SRTT + (1 - a) R, RTO = beta SRTT
    for beta in (1.3, 2.0):
        srtt, rto, spur, tr = xs[0], None, 0, []
        for x in xs[1:]:
            rto = beta * srtt
            spur += x > rto
            srtt = 0.875 * srtt + 0.125 * x
            tr.append(rto)
        out[f"rfc793_{beta}"] = {"spurious": spur, "trace": [round(v, 4) for v in tr], "mean": sum(tr) / len(tr)}
    srtt, var, spur, tr = xs[0], xs[0] / 2, 0, []
    for x in xs[1:]:
        rto = srtt + 4 * var
        spur += x > rto
        var = 0.75 * var + 0.25 * abs(srtt - x)
        srtt = 0.875 * srtt + 0.125 * x
        tr.append(rto)
    out["jacobson"] = {"spurious": spur, "trace": [round(v, 4) for v in tr], "mean": sum(tr) / len(tr)}
    out["mean_rtt"] = sum(xs) / len(xs)
    out["n"] = len(xs) - 1
    out["min"], out["max"] = min(xs), max(xs)
    return out


# ---- congestion ----------------------------------------------------------------------------------------------------
def compute_collapse() -> dict:
    from explainer.cs.net.tcp import MSS, Flow, dumbbell
    rows = []
    pipe = 2e6 / (1500 * 8) * 0.1
    for w in (2, 4, 6, 8, 12, 16, 24, 32, 48):
        row = {"window": w, "offered": 4 * w}
        for cc in ("fixed", "reno"):
            r = dumbbell([Flow(cc, rtt=0.1, window=w, start=0.01 * i) for i in range(4)], mbps=2, duration=60,
                         buffer=30)
            row[cc] = sum(f["delivered"] for f in r["flows"]) * MSS * 8 / 60 / 1e6
            row[cc + "_retx"] = sum(f["retransmits"] for f in r["flows"])
            row[cc + "_util"] = r["utilization"]
        rows.append(row)
    return {"rows": rows, "mbps": 2, "flows": 4, "pipe": pipe, "buffer": 30, "rto": 0.2,
            "history": {"before_bps": 32_000, "after_bps": 40, "year": 1986}}


def compute_chiujain() -> dict:
    from explainer.cs.net import cc
    out = {}
    for rule in ("AIMD", "AIAD", "MIAD", "MIMD"):
        r = cc.chiu_jain(rule, x0=(0.1, 0.6), steps=120, a=0.03, b=0.5, m=1.15)
        out[rule] = {"trajectory": [[round(a, 4), round(b, 4)] for a, b in r["trajectory"]],
                     "fairness": r["fairness"], "efficiency": r["efficiency"]}
    return out


def compute_sawtooth() -> dict:
    from explainer.cs.net.tcp import Flow, dumbbell, mathis
    one = dumbbell([Flow("reno", rtt=0.1)], mbps=10, duration=60, buffer=None)
    trace = one["flows"][0]["trace"]
    rows = []
    for p in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2):
        dur = 400 if p < 5e-4 else 200
        r = dumbbell([Flow("reno", rtt=0.1)], mbps=200, buffer=20_000, loss=p, duration=dur, warmup=40, seed=7)
        rows.append({"p": p, "measured": r["flows"][0]["mbps"], "mathis": mathis(0.1, p)})
    unfair = []
    for r2 in (0.02, 0.05, 0.1, 0.2):
        r = dumbbell([Flow("reno", rtt=0.02), Flow("reno", rtt=r2)], mbps=20, duration=120, buffer=None, warmup=20)
        a, b = (f["mbps"] for f in r["flows"])
        unfair.append({"rtt2": r2, "short": a, "long": b, "ratio": a / b})
    return {"trace": _t(trace), "bdp": one["bdp"], "buffer": one["buffer"], "utilization": one["utilization"],
            "mbps": one["flows"][0]["mbps"], "queue": _t(one["queue"]), "mathis": rows, "unfair": unfair}


def compute_buffers() -> dict:
    from explainer.cs.net.tcp import Flow, dumbbell
    rows = []
    rate = 10e6 / 12000
    for mult in (0.1, 0.25, 0.5, 1, 2, 4, 8):
        r = dumbbell([Flow("reno", rtt=0.1)], mbps=10, duration=60, buffer=max(2, int(round(83.3 * mult))),
                     warmup=10)
        q = [x for t, x in r["queue"] if t > 10]
        rows.append({"mult": mult, "util": r["utilization"], "queue_ms": sum(q) / len(q) / rate * 1000,
                     "rtt_ms": 100 + sum(q) / len(q) / rate * 1000})
    deep = {}
    for qd in ("droptail", "red", "codel"):
        r = dumbbell([Flow("reno", rtt=0.1), Flow("cubic", rtt=0.1, start=1)], mbps=10, duration=60, buffer=1000,
                     qdisc=qd, warmup=10)
        q = [x for t, x in r["queue"] if t > 10]
        deep[qd] = {"util": r["utilization"], "queue_ms": sum(q) / len(q) / rate * 1000,
                    "p99_ms": sorted(q)[int(0.99 * len(q))] / rate * 1000, "drops": r["drops"],
                    "queue": _t(r["queue"], 2)}
    app = []
    for n in (1, 4, 16, 64):
        bdp = 100e6 / 12000 * 0.1
        for label, B in (("BDP", bdp), ("BDP/sqrt(n)", bdp / math.sqrt(n))):
            r = dumbbell([Flow("reno", rtt=0.1 * (0.8 + 0.4 * random.Random(i).random()), start=0.05 * i)
                          for i in range(n)], mbps=100, buffer=max(4, int(B)), duration=40, warmup=10, seed=n)
            app.append({"n": n, "rule": label, "buffer": int(B), "util": r["utilization"]})
    return {"rows": rows, "deep": deep, "appenzeller": app}


def compute_modern() -> dict:
    from explainer.cs.net.tcp import Flow, dumbbell
    rate = MBPS * 1e6 / 12000
    solo = {}
    for cc in ("reno", "cubic", "bbr"):
        r = dumbbell([Flow(cc, rtt=RTT)], mbps=MBPS, buffer=int(rate * RTT), duration=60, warmup=10)
        q = [x for t, x in r["queue"] if t > 10]
        f = r["flows"][0]
        solo[cc] = {"mbps": f["mbps"], "trace": _t(f["trace"], 4), "queue_ms": sum(q) / len(q) / rate * 1000,
                    "retx": f["retransmits"], "queue": _t(r["queue"], 4)}
    lossy = {}
    for cc in ("reno", "cubic", "bbr"):
        r = dumbbell([Flow(cc, rtt=RTT)], mbps=MBPS, buffer=int(rate * RTT), duration=60, loss=1e-3, warmup=10)
        lossy[cc] = r["flows"][0]["mbps"]
    mixed = []
    for mult in (0.25, 1, 4):
        r = dumbbell([Flow("bbr", rtt=RTT), Flow("cubic", rtt=RTT, start=0.5)], mbps=50,
                     buffer=int(50e6 / 12000 * RTT * mult), duration=90, warmup=20)
        mixed.append({"mult": mult, "bbr": r["flows"][0]["mbps"], "cubic": r["flows"][1]["mbps"]})
    vegas = dumbbell([Flow("vegas", rtt=0.1)], mbps=10, duration=40, buffer=400, warmup=10)
    q = [x for t, x in vegas["queue"] if t > 10]
    vr = dumbbell([Flow("vegas", rtt=0.1), Flow("reno", rtt=0.1)], mbps=10, duration=60, buffer=400, warmup=10)
    # Kleinrock: delivery rate and RTT against inflight, on the 100 Mb/s path
    bdp = rate * RTT
    kl = [{"inflight": x, "rate": min(x / bdp, 1) * MBPS, "rtt_ms": max(RTT, x / rate) * 1000}
          for x in [bdp * k / 8 for k in range(1, 25)]]
    return {"solo": solo, "lossy": lossy, "mixed": mixed, "bdp": bdp,
            "vegas": {"mbps": vegas["flows"][0]["mbps"], "queue_pkts": sum(q) / len(q),
                      "with_reno": [f["mbps"] for f in vr["flows"]]}, "kleinrock": kl}


def compute_num() -> dict:
    from explainer.cs.net import cc
    routes = {"long": ["L1", "L2"], "a": ["L1"], "b": ["L2"]}
    caps = {"L1": 1.0, "L2": 1.0}
    n = cc.num_dual(routes, caps, step=0.05, iters=3000)
    mm = cc.max_min(routes, caps)
    hist = [{"iter": h["iter"], "x": h["x"], "p": h["p"]} for h in n["history"][:40]]
    park = {"long": ["L1", "L2", "L3"], "a": ["L1"], "b": ["L2"], "c": ["L3"]}
    pcaps = {"L1": 1.0, "L2": 1.0, "L3": 1.0}
    n3 = cc.num_dual(park, pcaps, step=0.05, iters=4000)
    mm3 = cc.max_min(park, pcaps)
    tot = lambda x: sum(x.values())  # noqa: E731
    return {"two": {"x": n["x"], "p": n["p"], "maxmin": mm, "history": hist, "util": n["utility"],
                    "util_maxmin": sum(math.log(v) for v in mm.values()), "total": tot(n["x"]),
                    "total_maxmin": tot(mm)},
            "three": {"x": n3["x"], "p": n3["p"], "maxmin": mm3, "total": tot(n3["x"]), "total_maxmin": tot(mm3)}}


# ---- above transport ---------------------------------------------------------------------------------------------
def compute_dns() -> dict:
    from explainer.cs.net import app
    rng = random.Random(37)
    names = [f"site{k}.{('com', 'org', 'net', 'de', 'jp')[k % 5]}" for k in range(2000)]
    w = [1 / (k + 1) for k in range(2000)]
    zones = {nm: (f"10.{k // 250}.{k % 250}.1", rng.choice((60, 300, 3600, 86400))) for k, nm in enumerate(names)}
    res = app.Resolver(zones)
    hits = trips = 0
    times = sorted(rng.uniform(0, 86400) for _ in range(50_000))
    for t in times:
        nm = rng.choices(names, w)[0]
        _, k, hit = res.resolve(nm, t)
        hits += hit
        trips += k
    odds = []
    for port_bits, label in ((0, "fixed port"), (16, "random port")):
        for races in (1, 100, 10_000):
            odds.append({"ports": label, "races": races, "p": app.kaminsky_odds(16, port_bits, 100, races)})
    # expected races to success, and the time at ten races a second
    exp = {lbl: 1 / app.kaminsky_odds(16, pb, 100, 1) for pb, lbl in ((0, "fixed port"), (16, "random port"))}
    return {"lookups": len(times), "hits": hits, "hit_rate": hits / len(times), "trips": trips,
            "trips_per_lookup": trips / len(times), "odds": odds, "expected_races": exp,
            "expected_seconds": {k: v / 10 for k, v in exp.items()}}


def compute_web() -> dict:
    from explainer.cs.net import app
    objs = [30] + [8] * 40                       # an HTML page of 30 packets and forty 8-packet resources
    rows = []
    for loss in (0.0, 0.01, 0.02, 0.05):
        row = {"loss": loss}
        for mode in ("http1", "http2", "quic"):
            rng = random.Random(int(loss * 1000) + 1)
            runs = [app.page_load(objs, loss, RTT, 2000, mode, rng) for _ in range(200)]
            row[mode] = sum(r["mean_object"] for r in runs) / len(runs) * 1000
            row[mode + "_page"] = sum(r["page"] for r in runs) / len(runs) * 1000
        rows.append(row)
    return {"rows": rows, "objects": len(objs), "packets": sum(objs), "rtt_ms": RTT * 1000, "rate_pps": 2000}


def _words():
    from videos.cs.cs31.compute import _full_text
    return re.findall(rb"[a-z]+", _full_text().lower())


def compute_cdn() -> dict:
    from explainer.cs.net import app
    words = _words()
    c = Counter(words)
    counts = sorted(c.values(), reverse=True)
    s = app.zipf_fit(counts)
    total = len(words)
    probs = [v / total for v in counts]
    rows = []
    reqs = words[:2_000_000]
    for size in (10, 100, 1000, 10_000):
        rows.append({"size": size, "lru": app.lru_hit_rate(reqs, size), "che": app.che(probs, size),
                     "ideal": sum(counts[:size]) / total})
    pts = [[r, counts[r - 1]] for r in sorted({int(round(10 ** (k / 8))) for k in range(0, 41)}) if r <= len(counts)]
    return {"words": total, "distinct": len(c), "s": s, "rank_counts": pts, "top": c.most_common(8) and
            [[w.decode(), n] for w, n in c.most_common(8)], "rows": rows, "requests": len(reqs)}


def compute_job() -> dict:
    from explainer.cs.net.tcp import MSS, Flow, dumbbell
    from videos.cs.cs31.compute import _full_text
    size = len(_full_text())
    rate = MBPS * 1e6 / 12000
    out = {"bytes": size, "packets": math.ceil(size / MSS), "rtt": RTT, "mbps": MBPS, "loss": 1e-3,
           "floor": size * 1500 / 1460 * 8 / (MBPS * 1e6) + 1.5 * RTT}
    for cc in ("reno", "cubic", "bbr"):
        r = dumbbell([Flow(cc, rtt=RTT, size=size)], mbps=MBPS, buffer=int(rate * RTT), loss=1e-3, duration=300,
                     seed=14)
        f = r["flows"][0]
        done = f["done"] + 1.5 * RTT              # the handshake and the request
        out[cc] = {"seconds": done, "retx": f["retransmits"], "round_trips": done / RTT, "drops": r["drops"],
                   "trace": _t(f["trace"], max(1, len(f["trace"]) // 400)), "mbps": size * 8 / done / 1e6}
    for cc in ("reno", "cubic", "bbr"):
        r = dumbbell([Flow(cc, rtt=RTT, size=size)], mbps=MBPS, buffer=int(rate * RTT), loss=0.0, duration=300,
                     seed=14)
        out[cc]["clean_seconds"] = r["flows"][0]["done"] + 1.5 * RTT
    led = json.loads((Cache("cs35").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 37]
    row34 = next(r for r in led if r["part"] == 34)
    fetch = out["cubic"]["seconds"]
    led.append({"part": 37, "label": r"fetched over our TCP, \ then counted", "seconds": fetch + row34["seconds"],
                "fetch_seconds": fetch, "count_seconds": row34["seconds"], "bbr_fetch_seconds": out["bbr"]["seconds"],
                "reno_fetch_seconds": out["reno"]["seconds"]})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    out["ledger"] = led
    out["count_seconds"] = row34["seconds"]
    return out


def compute_frontier() -> dict:
    from explainer.cs.net.tcp import Flow, dumbbell
    rows = []
    for cc, js in (("vegas", (0.0, 0.005, 0.01, 0.02, 0.04)), ("bbr", (0.0, 0.02, 0.04)), ("reno", (0.0, 0.02, 0.04))):
        for j in js:
            r = dumbbell([Flow(cc, rtt=0.04), Flow(cc, rtt=0.04, jitter=j)], mbps=20, duration=60, buffer=500,
                         warmup=10)
            a, b = (f["mbps"] for f in r["flows"])
            rows.append({"cc": cc, "jitter_ms": j * 1000, "steady": a, "jittery": b})
    return {"rows": rows, "mbps": 20, "rtt_ms": 40}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
