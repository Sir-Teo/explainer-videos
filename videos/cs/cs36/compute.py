"""Precompute everything numerical in Part 36 of *Computer Science, Built* ("Networks I: Moving Bits").

    python -m videos.cs.cs36.compute              # everything missing
    python -m videos.cs.cs36.compute --force bgp

Results are cached in ``.cache/cs36/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/net/`` (phy, link, mac, bridge, ip, routing, bgp, sim, wireless, dataplane); tests in
tests/test_cs36_net.py.

Items:
    hook        a datagram from Pebble 1 in San Francisco to Pebble 2 in Frankfurt: its headers, byte by byte, and
                its route, measured by ping and traceroute in our simulated internet
    multiplex   circuits against packets: 35 bursty users on a link sized for 10 (binomial, exact)
    layers      the nested headers of one frame, their overhead, and the end-to-end argument in numbers
    phy         Shannon's capacity for three channels; square QAM measured against its formula and against Shannon;
                noisy constellations; fibre round trips and bandwidth-delay products
    link        bit stuffing, an Ethernet frame and its CRC-32, and corrupted frames the CRC catches
    mac         pure and slotted ALOHA against G e^{-2G} and G e^{-G}; CSMA/CD with backoff against Metcalfe and
                Boggs; the hidden terminal with and without RTS/CTS
    bridges     a broadcast storm in a looped LAN, Perlman's spanning tree, and learning
    ipaddr      CIDR, aggregation, NAT, fragmentation; IPv4 against IPv6 address space
    lpm         longest-prefix match on 100,000 prefixes: linear, binary trie, multibit tries
    dv          distance vector: convergence, count-to-infinity, split horizon and poisoned reverse
    ls          link state: flooding costs, Dijkstra, and the transient loops of reconvergence
    bgp         Gao-Rexford routing on a 125-AS internet; an origin and a sub-prefix hijack; RPKI adoption
    sdn         a P4-shaped pipeline processing one packet
    internet    our internet of eight cities: a ping matrix, traceroute, a failure, and packets caught in a loop
    wireless    Rayleigh fading against Gaussian noise; OFDM with and without a cyclic prefix; MIMO capacity
    frontier    a data-plane verifier on our internet's tables; BAD GADGET's endless oscillation
    hol         an input-queued switch: head-of-line blocking against virtual output queues
    ecmp        flows hashed over equal paths in a Clos fabric: imbalance, elephants, and per-packet spraying
    queueing    ping across a loaded link in our internet: delay against utilization, and Pollaczek-Khinchine
"""

from __future__ import annotations

import math
import random
import time

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs36")
load = CACHE.load

CITIES = {"sfo": (37.6, -122.4), "nyc": (40.7, -74.0), "lon": (51.5, -0.1), "ams": (52.4, 4.9),
          "fra": (50.1, 8.7), "par": (48.9, 2.4), "sgp": (1.35, 103.8), "tok": (35.7, 139.7)}
# cable route lengths in km (longer than great circles; approximate)
LINKS = [("sfo", "nyc", 4700), ("nyc", "lon", 5570), ("nyc", "par", 5840), ("lon", "ams", 360), ("lon", "par", 340),
         ("ams", "fra", 360), ("par", "fra", 480), ("fra", "sgp", 11000), ("sgp", "tok", 5300),
         ("tok", "sfo", 8300)]
HOSTS = {"pebble1": ("10.1.0.2/24", "sfo"), "pebble2": ("10.4.0.2/24", "fra"), "pebble3": ("10.7.0.2/24", "tok"),
         "pebble4": ("10.3.0.2/24", "lon")}


def our_internet(seed=1, mbps=10_000):
    from explainer.cs.net.sim import Internet
    n = Internet(seed)
    for c in CITIES:
        n.router(c)
    for a, b, km in LINKS:
        n.link(a, b, mbps, km)
    for h, (addr, gw) in HOSTS.items():
        n.host(h, addr, gw)
    n.converge()
    return n


# ---- the hook --------------------------------------------------------------------------------------------------------
def compute_hook() -> dict:
    from explainer.cs.net import ip as I
    from explainer.cs.net import link as L
    payload = b"Call me Ishmael."
    src, dst = "10.1.0.2", "10.4.0.2"
    udp = I.udp_header(40001, 7, payload, src, dst)
    iph = I.ipv4_header(src, dst, 17, len(udp) + len(payload), ttl=64)
    frame = L.ethernet("02:00:00:00:01:01", "02:00:00:00:00:02", 0x0800, iph + udp + payload)
    n = our_internet()
    ping = n.ping("pebble1", "pebble2")[0]
    trace = n.traceroute("pebble1", "pebble2")
    km = sum(km for a, b, km in LINKS for x, y in zip(ping["path"], ping["path"][1:]) if {a, b} == {x, y})
    return {"payload": payload.decode(), "frame": frame.hex(), "eth": 14, "ip": 20, "udp": 8,
            "payload_len": len(payload), "pad": len(frame) - 4 - 14 - 20 - 8 - len(payload), "fcs": frame[-4:].hex(),
            "ip_checksum": iph[10:12].hex(), "ping_ms": ping["rtt"] * 1000, "path": ping["path"],
            "trace": [{"ttl": h["ttl"], "by": h["by"], "ms": h["rtt"] * 1000} for h in trace],
            "route_km": km, "light_ms": 2 * km * 1000 / 2.04e8 * 1000}


# ---- circuits and packets ----------------------------------------------------------------------------------------
def compute_multiplex() -> dict:
    from math import comb
    users, p, cap = 35, 0.1, 10
    tail = sum(comb(users, k) * p ** k * (1 - p) ** (users - k) for k in range(cap + 1, users + 1))
    rows = []
    for n in (10, 35, 50, 100, 1000):
        # the smallest capacity c (in user rates) such that P(more than c active) < 1e-4
        c = 0
        while sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(c + 1, n + 1)) >= 1e-4:
            c += 1
        rows.append({"users": n, "circuit": n, "packet": c, "mean": n * p})
    return {"users": users, "p": p, "cap": cap, "overflow": tail, "rows": rows}


# ---- layers ---------------------------------------------------------------------------------------------------------
def compute_layers() -> dict:
    rows = []
    for size in (16, 100, 512, 1460):
        rows.append({"payload": size, "wire": max(size + 42 + 4, 64) + 20, "efficiency": size / (max(size + 46, 64) + 20)})
    tcp_rows = [{"payload": s, "efficiency": s / (s + 14 + 20 + 20 + 4 + 20)} for s in (16, 536, 1460)]
    # the end-to-end argument: per-hop checks cannot see corruption inside a router's memory
    p_router = 1e-9          # chance a router's memory or bus corrupts a packet it holds
    hops, packets = 15, 700_000          # about a gigabyte in 1460-byte packets
    ok = (1 - p_router) ** (hops * packets)
    return {"rows": rows, "tcp": tcp_rows, "p_router": p_router, "hops": hops, "packets": packets,
            "file_ok": ok, "file_bad": 1 - ok}


# ---- the physical layer ------------------------------------------------------------------------------------------
def compute_phy() -> dict:
    from explainer.cs.net import phy as P
    rng = np.random.default_rng(0)
    channels = [{"name": "telephone line", "B": 3100, "snr_db": 35},
                {"name": "Wi-Fi, 80 MHz", "B": 80e6, "snr_db": 30},
                {"name": "a 5G carrier, 100 MHz", "B": 100e6, "snr_db": 20}]
    for c in channels:
        c["C"] = P.shannon(c["B"], P.undb(c["snr_db"]))
    qam = []
    for M in (4, 16, 64, 256):
        need = P.snr_needed(M, 1e-6)
        shan = P.db(P.shannon_snr(math.log2(M)))
        meas = []
        for snr in range(4, 36, 2):
            s = P.qam_simulate(M, snr, 200_000, rng)
            meas.append({"snr_db": snr, "ser": s["ser"], "ber": s["ber"], "formula": P.qam_ser(M, snr)})
        qam.append({"M": M, "bits": int(math.log2(M)), "snr_needed": need, "shannon": shan, "gap": need - shan,
                    "curve": meas})
    clouds = {}
    for M, snr in ((16, 24), (16, 14), (64, 24)):
        s = P.qam_simulate(M, snr, 600, rng)
        clouds[f"{M}@{snr}"] = {"pts": s["sample"], "tx": s["sample_tx"], "ser": s["ser"]}
    pts16, lab16 = P.qam(16)
    routes = [("San Francisco to New York", 4700), ("New York to London", 5570), ("London to Singapore", 12000),
              ("around the Earth", 40075 / 2)]
    rtts = [{"name": n, "km": km, "rtt_ms": P.fibre_rtt(km) * 1000} for n, km in routes]
    bdp = [{"rate": r, "rtt_ms": 55, "bytes": P.bdp(r, 0.055)} for r in (1e6, 1e9, 100e9)]
    return {"channels": channels, "qam": qam, "clouds": clouds,
            "points16": [[float(z.real), float(z.imag), int(l)] for z, l in zip(pts16, lab16)],
            "rtts": rtts, "bdp": bdp, "c_fibre": P.C_FIBRE}


# ---- links -----------------------------------------------------------------------------------------------------------
def compute_link() -> dict:
    from explainer.cs.net import link as L
    r = random.Random(2)
    data = [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1]
    st = L.stuff(data)
    trials = [L.crc_trial(k, 100_000, r) for k in ("single", "double", "burst", "random")]
    fr = L.ethernet("02:00:00:00:01:01", "02:00:00:00:00:02", 0x0800, b"Call me Ishmael.")
    return {"data": data, "stuffed": st, "framed": L.frame(data), "trials": trials, "frame": fr.hex(),
            "fcs_ok": L.fcs_ok(fr)}


# ---- sharing the medium ---------------------------------------------------------------------------------------------
def compute_mac() -> dict:
    from explainer.cs.net import mac as M
    r = random.Random(3)
    Gs = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    aloha = [M.aloha(G, 80_000, r) for G in Gs]
    slotted = [M.slotted_aloha(G, 80_000, r) for G in Gs]
    csma = []
    for a in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5):
        b = M.csma_cd(20, a, 40_000, r)
        p = M.csma_cd(20, a, 40_000, r, policy="p")
        csma.append({"a": a, "beb": b["efficiency"], "p": p["efficiency"], "formula": M.metcalfe_boggs(20, a),
                     "kurose": 1 / (1 + 5 * a)})
    hidden = [{"G": G, "plain": M.hidden_terminal(G, 80_000, r)["S"], "rts": M.hidden_terminal(G, 80_000, r, True)["S"],
               "aloha": G * math.exp(-G)} for G in (0.25, 0.5, 1.0, 2.0, 4.0)]
    # Ethernet numbers: 10 Mb/s, 2500 m, 512-bit slot
    eth = {"rate": 10e6, "slot_bits": 512, "slot_us": 51.2, "min_frame": 64, "max_k": 10, "attempts": 16}
    return {"aloha": aloha, "slotted": slotted, "csma": csma, "hidden": hidden, "ethernet": eth}


# ---- bridges ---------------------------------------------------------------------------------------------------------
LAN_LINKS = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 2), (4, 5), (5, 3)]
LAN_HOSTS = {"ana": 1, "ben": 4, "cy": 5, "dee": 2}


def compute_bridges() -> dict:
    from explainer.cs.net import bridge as B
    topo = B.lan(LAN_LINKS, LAN_HOSTS)
    storm = B.flood(topo, 1, limit=20)
    st = B.spanning_tree(topo)
    tree = B.flood(topo, 1, active=st["active"])
    active_links = []
    for a, b in LAN_LINKS:
        pa = next(p for p, v in topo[a].items() if v[0] == "bridge" and v[1] == b)
        pb = next(p for p, v in topo[b].items() if v[0] == "bridge" and v[1] == a)
        active_links.append({"a": a, "b": b, "active": pa in st["active"][a] and pb in st["active"][b]})
    frames = [("ana", "ben"), ("ben", "ana"), ("ana", "ben"), ("cy", "ana"), ("dee", "cy")]
    lr = B.learning(topo, frames, st["active"], LAN_HOSTS)
    return {"storm": storm["per_hop"], "storm_sent": storm["sent"], "tree": tree, "root": st["root"],
            "rounds": st["rounds"], "links": active_links, "blocked": st["blocked_ports"],
            "best": {str(k): list(v) for k, v in st["best"].items()}, "frames": frames, "copies": lr["copies"]}


# ---- IP -------------------------------------------------------------------------------------------------------------
def compute_ipaddr() -> dict:
    from explainer.cs.net import ip as I
    P = I.Prefix.parse
    blocks = [(P("192.168.0.0/24"), "A"), (P("192.168.1.0/24"), "A"), (P("192.168.2.0/24"), "A"),
              (P("192.168.3.0/24"), "A"), (P("192.168.4.0/24"), "B")]
    agg = I.aggregate(blocks)
    nat = I.Nat("203.0.113.7")
    m = [nat.outbound("192.168.1.10", 51000), nat.outbound("192.168.1.11", 51000), nat.outbound("192.168.1.10", 51001)]
    frags = I.fragment(4000, 1500)
    r = random.Random(4)
    rows = I.routing_table(100_000, r)
    agg_big = I.aggregate(rows)
    return {"aggregate_in": [repr(p) for p, _ in blocks], "aggregate_out": sorted(repr(p) for p, _ in agg),
            "nat": [list(x) for x in m], "fragments": frags, "v4": 2 ** 32, "v6": 2 ** 128,
            "v6_per_m2": 2 ** 128 / 5.1e14, "table": len(rows), "table_aggregated": len(agg_big)}


def compute_lpm() -> dict:
    from explainer.cs.net import ip as I
    r = random.Random(5)
    rows = I.routing_table(100_000, r)
    from collections import Counter
    hist = Counter(p.len for p, _ in rows)
    tabs = {"linear": I.LinearTable(), "binary trie": I.BinaryTrie(), "multibit, stride 8": I.MultibitTrie(8),
            "multibit, stride 4": I.MultibitTrie(4)}
    for p, h in rows:
        for t in tabs.values():
            t.insert(p, h)
    addrs = [r.getrandbits(32) for _ in range(500)] + [p.net | (r.getrandbits(32 - p.len) if p.len < 32 else 0)
                                                     for p, _ in r.sample(rows, 500)]
    out = {}
    for name, t in tabs.items():
        steps, answers = 0, []
        sample = addrs if name != "linear" else addrs[:60]
        t0 = time.perf_counter()
        for a in sample:
            answers.append(t.lookup(a))
            steps += t.steps
        dt = (time.perf_counter() - t0) / len(sample)
        out[name] = {"steps": steps / len(sample), "us": dt * 1e6,
                     "nodes": getattr(t, "nodes", len(rows))}
    ref = [tabs["binary trie"].lookup(a) for a in addrs]
    for name in ("multibit, stride 8", "multibit, stride 4"):
        assert [tabs[name].lookup(a) for a in addrs] == ref
    pps = 400e9 / ((64 + 20) * 8)
    return {"prefixes": len(rows), "hist": {str(k): v for k, v in sorted(hist.items())}, "tables": out,
            "pps_400g": pps, "ns_per_packet": 1e9 / pps, "real_table": 1_000_000}


# ---- routing ---------------------------------------------------------------------------------------------------------
LINE = {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}
TRI = {"A": {"B": 1, "C": 1}, "B": {"A": 1, "C": 1}, "C": {"A": 1, "B": 1, "D": 1}, "D": {"C": 1}}


def compute_dv() -> dict:
    from explainer.cs.net import routing as R
    net = {"u": {"v": 2, "x": 1}, "v": {"u": 2, "x": 3, "w": 3}, "x": {"u": 1, "v": 3, "y": 1},
           "w": {"v": 3, "y": 1, "z": 5}, "y": {"x": 1, "w": 1, "z": 2}, "z": {"w": 5, "y": 2}}
    run = R.dv_run(net, infinity=99)
    hist = [{x: {y: list(t[x][y]) for y in t[x]} for x in t} for t in run["history"]]
    line = {}
    for mode in ("plain", "split", "poison"):
        f = R.dv_fail(LINE, "B", "C", mode=mode)
        line[mode] = {"rounds": f["after"]["converged"],
                      "A": [t["A"]["C"][0] for t in f["after"]["history"]],
                      "B": [t["B"]["C"][0] for t in f["after"]["history"]]}
    tri = {}
    for mode in ("plain", "split", "poison"):
        f = R.dv_fail(TRI, "C", "D", mode=mode)
        tri[mode] = {"rounds": f["after"]["converged"],
                     "A": [t["A"]["D"][0] for t in f["after"]["history"]],
                     "B": [t["B"]["D"][0] for t in f["after"]["history"]],
                     "C": [t["C"]["D"][0] for t in f["after"]["history"]]}
    sp = R.spf(net, "u")
    return {"net": net, "rounds": run["converged"], "history": hist, "spf_u": {k: list(v) for k, v in sp.items()},
            "line": line, "tri": tri}


def compute_ls() -> dict:
    from explainer.cs.net import routing as R
    n = our_internet()
    g = n.graph()
    floods = {c: R.ls_flood(g, c) for c in g}
    E = sum(len(v) for v in g.values()) // 2
    ring = {"lon": {"ams": 360, "par": 340}, "ams": {"lon": 360, "fra": 360}, "fra": {"ams": 360, "par": 480},
            "par": {"lon": 340, "fra": 480}}
    rec = R.ls_reconverge(ring, "ams", "fra", {"ams": 0.05, "lon": 0.25, "par": 0.15, "fra": 0.10})
    timeline = [{"t": e["t"], "loops": [[s, d, p] for s, d, p in e["loops"]], "drops": e["drops"]}
                for e in rec["timeline"]]
    return {"nodes": len(g), "edges": E, "flood_sent": floods["lon"]["sent"], "flood_hops": floods["lon"]["max_hops"],
            "lsas_total": sum(f["sent"] for f in floods.values()), "ring": ring, "timeline": timeline}


def compute_bgp() -> dict:
    from explainer.cs.net import bgp as G
    from explainer.cs.net.ip import Prefix, ip
    r = random.Random(8)
    rel, T = G.tiered(r)
    victim, attacker = T["stubs"][0], T["stubs"][57]
    P22, P24 = Prefix.parse("208.65.152.0/22"), Prefix.parse("208.65.153.0/24")
    base = G.propagate(rel, [(victim, P22)])
    lens = [len(base["routes"][a][P22]) - 1 for a in rel if a != victim]
    edges = {"customer-provider": sum(1 for a in rel for b, k in rel[a].items() if k == "customer"),
             "peer": sum(1 for a in rel for b, k in rel[a].items() if k == "peer") // 2}
    addr = ip("208.65.153.10")
    origin = G.reach(G.propagate(rel, [(victim, P22), (attacker, P22)])["routes"], addr)
    sub = G.reach(G.propagate(rel, [(victim, P22), (attacker, P24)])["routes"], addr)
    roa = {P22: (victim, 22)}
    adoption = []
    for frac in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
        vals = []
        for trial in range(20):
            rr = random.Random(100 + trial)
            rov = {a for a in rel if rr.random() < frac}
            res = G.reach(G.propagate(rel, [(victim, P22), (attacker, P24)], rov=rov, roa=roa)["routes"], addr)
            vals.append(sum(1 for v in res.values() if v == attacker) - 1)
        adoption.append({"frac": frac, "hijacked": sum(vals) / len(vals) / (len(rel) - 1)})
    # tier-1s alone doing ROV
    res = G.reach(G.propagate(rel, [(victim, P22), (attacker, P24)], rov=set(T["tier1"]) | set(T["tier2"]), roa=roa)
                  ["routes"], addr)
    transit_only = (sum(1 for v in res.values() if v == attacker) - 1) / (len(rel) - 1)
    sample_path = base["routes"][T["stubs"][40]][P22]
    return {"ases": len(rel), "tier1": len(T["tier1"]), "tier2": len(T["tier2"]), "stubs": len(T["stubs"]),
            "edges": edges, "rounds": base["rounds"], "mean_path": sum(lens) / len(lens), "max_path": max(lens),
            "victim": victim, "attacker": attacker, "origin_hijacked": sum(1 for v in origin.values() if v == attacker),
            "sub_hijacked": sum(1 for v in sub.values() if v == attacker), "adoption": adoption,
            "transit_only": transit_only, "sample_path": list(sample_path),
            "kinds": [rel[sample_path[i]][sample_path[i + 1]] for i in range(len(sample_path) - 1)]}


def compute_sdn() -> dict:
    from explainer.cs.net import dataplane as D
    from explainer.cs.net.ip import Prefix, ip
    p = D.Pipeline([("dst", 4), ("ttl", 1), ("dscp", 1)])
    acl = p.table("acl", "dst", "ternary")
    acl["rules"].append(((ip("10.9.0.0"), 0xFFFF0000), ("drop",)))
    route = p.table("route", "dst", "lpm")
    route["rules"] += [(Prefix.parse("10.0.0.0/8"), ("forward", 1)), (Prefix.parse("10.4.0.0/16"), ("forward", 3))]
    qos = p.table("qos", "dscp", "exact")
    qos["rules"].append((46, ("count", "voice")))
    ttl = p.table("ttl", "ttl")
    ttl["default"] = ("dec", "ttl")
    out = []
    for dst, t, d in (("10.4.0.2", 64, 0), ("10.7.0.2", 64, 46), ("10.9.1.1", 64, 0), ("10.4.0.2", 1, 0)):
        pkt = ip(dst).to_bytes(4, "big") + bytes([t, d]) + b"payload"
        port, newb, trace = p.process(pkt)
        out.append({"dst": dst, "ttl": t, "dscp": d, "port": port, "trace": [[a, list(b) if isinstance(b, tuple)
                                                                             else b] for a, b in trace]})
    return {"packets": out, "counters": p.counters}


def compute_internet() -> dict:
    n = our_internet()
    hosts = list(HOSTS)
    matrix = {}
    for a in hosts:
        for b in hosts:
            if a < b:
                r = n.ping(a, b)[0]
                matrix[f"{a}-{b}"] = {"ms": r["rtt"] * 1000, "path": r["path"]}
    trace = n.traceroute("pebble1", "pebble2")
    # a failure on the London-Amsterdam-Frankfurt route, and a stream of packets during reconvergence
    n2 = our_internet()
    before = n2.ping("pebble4", "pebble2")[0]
    n2.fail("ams", "fra")
    n2.events.clear()
    t0 = n2.now
    n2.converge(delays={"ams": 0.05, "lon": 0.25, "par": 0.15, "fra": 0.10})
    ids = []
    for k in range(40):
        ids.append(n2.inject("pebble4", n2.hosts["pebble2"]["addr"], ttl=32, at=t0 + k * 0.01))
    got = n2.run(until=t0 + 2)
    delivered = {pkt["id"] for t, node, pkt in got if node == "pebble2"}
    expired = {e[4] for e in n2.log if e[1] == "ttl expired"}
    down = {e[4] for e in n2.log if e[1] == "dropped: link down"}
    fate = []
    for k, i in enumerate(ids):
        fate.append({"t": k * 0.01, "fate": "delivered" if i in delivered else ("looped" if i in expired else
                                                                                ("dropped" if i in down else "lost"))})
    after = n2.ping("pebble4", "pebble2")[0]
    return {"cities": CITIES, "links": LINKS, "hosts": HOSTS, "matrix": matrix,
            "trace": [{"ttl": h["ttl"], "by": h["by"], "ms": h["rtt"] * 1000} for h in trace],
            "before": {"ms": before["rtt"] * 1000, "path": before["path"]},
            "after": {"ms": after["rtt"] * 1000, "path": after["path"]}, "fate": fate}


def compute_wireless() -> dict:
    from explainer.cs.net import wireless as W
    rng = np.random.default_rng(6)
    fading = [W.rayleigh_ber(s, 400_000, rng) for s in (0, 5, 10, 15, 20, 25, 30)]
    taps = [1.0, 0.7, 0.5j, 0.4, 0.3 - 0.2j]
    of = []
    for cp in (0, 2, 4, 8):
        res = W.ofdm(64, max(cp, 1) if cp else 1, taps, 30, rng, symbols=400)
        of.append({"cp": cp, "ber": res["ber_cp"] if cp else res["ber_nocp"]})
    H = W.ofdm(64, 8, taps, 30, rng, symbols=1)["H"]
    mimo = [{"n": k, "c10": W.mimo_capacity(k, k, 10, 400, rng), "c20": W.mimo_capacity(k, k, 20, 400, rng)}
            for k in (1, 2, 4, 8)]
    return {"fading": fading, "taps": [[t.real, t.imag] if isinstance(t, complex) else [t, 0] for t in taps],
            "ofdm": of, "H": H, "mimo": mimo}


def compute_frontier() -> dict:
    from explainer.cs.net import bgp as G
    from explainer.cs.net import dataplane as D
    n = our_internet()
    n.fail("ams", "fra")
    new = n.compute_tables()
    snap = {}
    delays = {"ams": 0.05, "lon": 0.25, "par": 0.15, "fra": 0.10}
    # the tables at t = 0.1: ams and fra have the new ones, lon and par the old
    old = our_internet().tables
    for r in n.routers:
        snap[r] = new[r] if delays.get(r, 0) <= 0.1 else old[r]
    owners = {info["prefix"]: info["gw"] for info in n.hosts.values()}
    fib = {r: [(p, hop) for p, hop in snap[r] if hop not in n.hosts] for r in n.routers}
    v = D.verify(fib, owners)
    v_new = D.verify({r: [(p, h) for p, h in new[r] if h not in n.hosts] for r in n.routers}, owners)
    bad = G.spp(G.BAD_GADGET, rounds=12)
    good = G.spp(G.GOOD_GADGET)
    return {"verify_mid": {"checked": v["checked"], "loops": [[p, list(c)] for p, c in v["loops"]],
                           "black_holes": v["black_holes"]},
            "verify_after": {"checked": v_new["checked"], "loops": len(v_new["loops"]), "black_holes": v_new["black_holes"]},
            "bad": [{str(k): list(x) if x else None for k, x in h.items()} for h in bad["history"]],
            "good": [{str(k): list(x) if x else None for k, x in h.items()} for h in good["history"]],
            "bad_stable": bad["stable"], "good_stable": good["stable"]}


def compute_hol() -> dict:
    """Saturated N x N switch, uniform destinations, one cell per input per slot.  FIFO inputs: only head cells may
    go, and each output takes one of the heads that want it.  VOQ: every input keeps a queue per output; a random
    maximal matching each slot."""
    rng = random.Random(12)
    rows = []
    for N in (2, 4, 8, 16, 32):
        heads = [rng.randrange(N) for _ in range(N)]
        sent = 0
        T = 20_000 if N <= 8 else 8_000
        for _ in range(T):
            want: dict = {}
            for i, d in enumerate(heads):
                want.setdefault(d, []).append(i)
            for d, ins in want.items():
                i = rng.choice(ins)
                sent += 1
                heads[i] = rng.randrange(N)
        fifo = sent / (T * N)
        # VOQ: saturated, so every input has a cell for every output; a maximal matching is a full permutation
        voq_sent = 0
        T2 = 2000
        for _ in range(T2):
            outs = list(range(N))
            rng.shuffle(outs)
            free = set(range(N))
            for i in range(N):
                for o in outs:
                    if o in free:
                        free.discard(o)
                        voq_sent += 1
                        break
        rows.append({"N": N, "fifo": fifo, "voq": voq_sent / (T2 * N)})
    return {"rows": rows, "limit": 2 - math.sqrt(2)}


def compute_ecmp() -> dict:
    rng = random.Random(13)
    out = []
    for k in (4, 8, 16):
        for flows in (k * 4, k * 32):
            ratios_mice, ratios_heavy = [], []
            for trial in range(200):
                loads = [0.0] * k
                heavy = [0.0] * k
                for f in range(flows):
                    p = rng.randrange(k)              # the hash of the flow's 5-tuple
                    loads[p] += 1.0
                    heavy[p] += rng.paretovariate(1.2)
                ratios_mice.append(max(loads) / (sum(loads) / k))
                ratios_heavy.append(max(heavy) / (sum(heavy) / k))
            out.append({"paths": k, "flows": flows, "equal": sum(ratios_mice) / len(ratios_mice),
                        "pareto": sum(ratios_heavy) / len(ratios_heavy)})
    # a k = 4 fat tree: hosts, switches, paths between pods
    kft = 4
    return {"rows": out, "fat_tree": {"k": kft, "hosts": kft ** 3 // 4, "switches": 5 * kft ** 2 // 4,
                                      "paths_between_pods": (kft // 2) ** 2}}


def compute_queueing() -> dict:
    from explainer.cs.net.sim import Internet
    rows = []
    mbps, size = 100, 1500
    S = size * 8 / (mbps * 1e6)
    for rho in (0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
        n = Internet(21)
        n.router("r1")
        n.router("r2")
        n.link("r1", "r2", mbps, 1000)
        n.host("h1", "10.1.0.2/24", "r1")
        n.host("h2", "10.2.0.2/24", "r2")
        n.converge()
        rng = random.Random(int(rho * 100))
        lam = rho / S
        t = 0.0
        while t < 4.0:
            t += rng.expovariate(lam)
            n.inject("h1", n.hosts["h2"]["addr"], size=size, kind="data", at=t)
        pings = []
        for k in range(400):
            pings.append(n.inject("h1", n.hosts["h2"]["addr"], size=84, kind="echo", at=0.5 + k * 0.008))
        got = n.run(until=6.0)
        rtts = sorted(t2 - pkt["sent"] for t2, node, pkt in got if node == "h1" and pkt["kind"] == "echo-reply")
        base = 2 * (1000e3 / 2.04e8 + 84 * 8 / (mbps * 1e6) + 2 * (0.1e3 / 2.04e8 + 84 * 8 / 1e9))
        mean_wait = sum(rtts) / len(rtts) - base
        pk = rho * S / (2 * (1 - rho))                # M/D/1 queueing delay, one way (the return is empty)
        rows.append({"rho": rho, "mean_ms": sum(rtts) / len(rtts) * 1000, "p99_ms": rtts[int(0.99 * len(rtts))] * 1000,
                     "wait_ms": mean_wait * 1000, "pk_ms": pk * 1000, "pings": len(rtts)})
    return {"rows": rows, "mbps": mbps, "size": size, "base_ms": rows[0]["mean_ms"] - rows[0]["wait_ms"]}


def compute_dv_internet() -> dict:
    """Distance vector on our internet's router graph, costs in whole milliseconds: rounds to converge, then the
    Amsterdam-Frankfurt cable cut, with and without split horizon."""
    from explainer.cs.net import routing as R
    n = our_internet()
    g = {a: {b: max(1, round(c)) for b, c in nb.items()} for a, nb in n.graph().items()}
    first = R.dv_run(g, infinity=10_000)
    out = {"rounds": first["converged"], "fra_from_lon": first["table"]["lon"]["fra"]}
    for mode in ("plain", "split"):
        f = R.dv_fail(g, "ams", "fra", mode=mode, infinity=10_000)
        h = f["after"]["history"]
        out[mode] = {"rounds": f["after"]["converged"], "lon_fra": [t["lon"]["fra"][0] for t in h][:12],
                     "ams_fra": [t["ams"]["fra"][0] for t in h][:12], "final_lon": list(f["after"]["table"]["lon"]["fra"])}
    sp = R.spf({a: {b: c for b, c in nb.items() if {a, b} != {"ams", "fra"}} for a, nb in g.items()}, "lon")
    out["spf_lon_fra"] = list(sp["fra"])
    return out


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
