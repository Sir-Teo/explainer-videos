"""Precompute everything numerical in Part 5 of *Computer Science, Built* ("Memory and Time").

    python -m videos.cs.cs5.compute              # everything missing (about a minute)
    python -m videos.cs.cs5.compute --force meta

Results are cached in ``.cache/cs5/<name>.json``; scenes call ``load(name)``.  Circuits come from
``explainer/cs/pebble/seq.py`` (latches with feedback, simulated with unit gate delays; clocked circuits, simulated
cycle by cycle) and are checked against Python models.

Items:
    latch      the SR latch and the D flip-flop, tick by tick: set, hold, reset, the forbidden input, a setup violation
    phase      two cross-coupled inverters as a dynamical system: the vector field, trajectories, the two stable
               states and the saddle between them
    meta       metastability: resolution times from random initial imbalances (a histogram with an exponential tail),
               and the MTBF of one and two synchronizing flip-flops
    fsm        a Moore sequence detector for 1011, synthesized with binary, Gray and one-hot state codes (minimized
               logic, gates, flip-flops), each simulated against the specification
    nerode     Myhill-Nerode: a six-state DFA for binary numbers divisible by 3, minimized by partition refinement
    lfsr       the period of every LFSR of degree 2..8 (every feedback polynomial), against the count of primitive
               polynomials
    regfile    Pebble's register file (16 x 32) in gates and flip-flops, verified against a Python model, and what
               each extra port costs
    dram       a DRAM cell's charge leaking between refreshes, and the densities of SRAM and DRAM cells
"""

from __future__ import annotations

import itertools
import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import seq as S
from explainer.cs.pebble.hdl import Circuit

class MemoryCache(Cache):
    def load(self, name):
        if name == "hammerdefence" and not cache_current(name):
            from explainer.cache_lock import cache_lock
            with cache_lock(self.path(name)):
                if not cache_current(name):
                    self.save(name, compute_hammerdefence())
        return super().load(name)


CACHE = MemoryCache("cs5")
HAMMER_SCHEMA = 2


def cache_current(name):
    path = CACHE.path(name)
    if not path.exists():
        return False
    if name != "hammerdefence":
        return True
    import json
    return json.loads(path.read_text()).get("schema") == HAMMER_SCHEMA


def load(name):
    # Resolve the instance method at call time so cached-only QA can guard it
    # before any automatic schema upgrade takes place.
    return CACHE.load(name)


# ---------------------------------------------------------------------------
# latches, tick by tick
# ---------------------------------------------------------------------------
def compute_latch() -> dict:
    sr = S.sr_latch()
    prog = [(1, 1)] * 3 + [(0, 1)] * 4 + [(1, 1)] * 5 + [(1, 0)] * 4 + [(1, 1)] * 5 + [(0, 0)] * 4 + [(1, 1)] * 9
    h = sr.run(lambda t: {"S_": prog[t][0], "R_": prog[t][1]}, len(prog), init={"Q": 0, "Qn": 1})
    ms = S.master_slave()
    T = 48
    clk = [(t // 6) % 2 for t in range(T)]
    D = [1 if (1 <= t < 8) or (20 <= t < 33) or (40 <= t < 44) else 0 for t in range(T)]
    hm = ms.run(lambda t: {"D": D[t], "C": clk[t]}, T, init=S.MS_INIT)
    # a setup violation: D changes at the very tick of the rising edge
    Dv = [1 if 6 <= t < 30 else 0 for t in range(T)]
    hv = ms.run(lambda t: {"D": Dv[t], "C": clk[t]}, T, init=S.MS_INIT)
    ring = S.ring(3).run(lambda t: {}, 18, init={"x0": 0, "x1": 1, "x2": 0})
    return {"sr": {"S_": h["S_"], "R_": h["R_"], "Q": h["Q"], "Qn": h["Qn"]},
            "ms": {"C": clk, "D": D, "M": hm["M"], "Q": hm["Q"]},
            "violation": {"C": clk, "D": Dv, "M": hv["M"], "Q": hv["Q"]},
            "ring": ring["x0"]}


# ---------------------------------------------------------------------------
# the latch as a dynamical system
# ---------------------------------------------------------------------------
GAIN = 6.0  # the inverter's slope at its threshold is -GAIN/2 = -3 (a gentle inverter, so the picture is visible)


def inv(v):
    return 0.5 * (1 - np.tanh(GAIN * (v - 0.5)))


def field(v1, v2):
    """dv1/dt = f(v2) - v1, dv2/dt = f(v1) - v2 (time in units of the gate's RC)."""
    return inv(v2) - v1, inv(v1) - v2


def integrate(p, T=8.0, dt=0.01):
    pts = [tuple(p)]
    v1, v2 = p
    for _ in range(int(T / dt)):
        # RK4
        k1 = field(v1, v2)
        k2 = field(v1 + dt / 2 * k1[0], v2 + dt / 2 * k1[1])
        k3 = field(v1 + dt / 2 * k2[0], v2 + dt / 2 * k2[1])
        k4 = field(v1 + dt * k3[0], v2 + dt * k3[1])
        v1 += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        v2 += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pts.append((float(v1), float(v2)))
    return pts


def stable_point():
    v = 0.0
    for _ in range(200):  # fixed point of v = f(f(v)) near 0
        v = float(inv(inv(v)))
    return v


def compute_phase() -> dict:
    g = np.linspace(0.02, 0.98, 17)
    arrows = []
    for a in g:
        for b in g:
            d = field(a, b)
            arrows.append([float(a), float(b), float(d[0]), float(d[1])])
    starts = [(0.05, 0.9), (0.9, 0.05), (0.3, 0.95), (0.95, 0.3), (0.5, 0.02), (0.02, 0.5), (0.98, 0.6), (0.6, 0.98),
              (0.51, 0.49), (0.49, 0.51), (0.2, 0.25), (0.75, 0.8)]
    trajs = [integrate(s, T=6.0)[::5] for s in starts]
    lo = stable_point()
    slope = -GAIN / 2
    return {"arrows": arrows, "trajs": trajs, "stable": [[lo, float(inv(lo))], [float(inv(lo)), lo]],
            "saddle": [0.5, 0.5], "slope": slope, "lambda_unstable": abs(slope) - 1, "lambda_stable": -1 - abs(slope)}


def compute_meta() -> dict:
    """A data edge arrives at a random moment near the clock edge, leaving the latch with a small random imbalance
    d along the unstable direction.  It resolves when |v1 - v2| > 0.9.  Near the saddle the imbalance grows like
    e^{lambda t}, so t = ln(0.9 / |d|) / lambda and P(t > T) = e^{-lambda T} 0.9 / eps."""
    rng = np.random.default_rng(5)
    lam = GAIN / 2 - 1
    eps = 0.2
    N = 40000
    d = rng.uniform(-eps, eps, N)
    # integrate every case at once (Euler, dt = 0.005), recording when each one resolves
    v1, v2 = 0.5 + d / 2, 0.5 - d / 2
    times = np.full(N, np.nan)
    t, dt = 0.0, 0.005
    while np.isnan(times).any() and t < 40:
        k1, k2 = field(v1, v2)
        v1, v2 = v1 + dt * k1, v2 + dt * k2
        t += dt
        done = np.isnan(times) & (np.abs(v1 - v2) > 0.9)
        times[done] = t
    times = np.nan_to_num(times, nan=40.0)
    lin = np.log(0.9 / np.maximum(np.abs(d), 1e-300)) / lam
    sample, offset = times[:300].tolist(), float(np.median(times - lin))
    hist, edges = np.histogram(times, bins=48, range=(0, 12))
    surv = [(float(T), float((times > T).mean())) for T in np.linspace(0, 12, 49)]
    # MTBF of a synchronizer, with textbook-scale constants
    tau, T0, fclk, fdata = 20e-12, 20e-12, 1e9, 100e6
    one = math.exp(0.5e-9 / tau) / (T0 * fclk * fdata)
    two = math.exp(1.5e-9 / tau) / (T0 * fclk * fdata)
    return {"hist": hist.tolist(), "edges": edges.tolist(), "surv": surv, "lambda": lam, "eps": eps,
            "sample_exact": sample, "linear_offset": offset, "max_time": float(times.max()),
            "mtbf": {"tau": tau, "T0": T0, "fclk": fclk, "fdata": fdata, "one_s": one, "two_s": two,
                     "one_hours": one / 3600, "two_years": two / 3.156e7}}


# ---------------------------------------------------------------------------
# a state machine, synthesized three ways
# ---------------------------------------------------------------------------
# Moore detector of the pattern 1011 (overlapping): state = how much of the pattern has been seen
FSM_STATES = ["S0", "S1", "S10", "S101", "S1011"]
FSM_NEXT = {("S0", 0): "S0", ("S0", 1): "S1", ("S1", 0): "S10", ("S1", 1): "S1", ("S10", 0): "S0",
            ("S10", 1): "S101", ("S101", 0): "S10", ("S101", 1): "S1011", ("S1011", 0): "S10", ("S1011", 1): "S1"}
FSM_OUT = {"S1011": 1}


def encodings():
    gray = [0, 1, 3, 2, 6]
    return {"binary": {s: i for i, s in enumerate(FSM_STATES)},
            "Gray": {s: gray[i] for i, s in enumerate(FSM_STATES)},
            "one-hot": {s: 1 << i for i, s in enumerate(FSM_STATES)}}


def prime_implicants(on, dc, n):
    """Quine-McCluskey with don't-cares: terms are (value, mask) with mask bits = variables eliminated."""
    terms = {(m, 0) for m in on | dc}
    primes = set()
    while terms:
        nxt, used = set(), set()
        tl = sorted(terms)
        for (v1, m1), (v2, m2) in itertools.combinations(tl, 2):
            if m1 == m2 and bin(v1 ^ v2).count("1") == 1:
                nxt.add((v1 & v2, m1 | (v1 ^ v2)))
                used.add((v1, m1))
                used.add((v2, m2))
        primes |= terms - used
        terms = nxt
    return primes


def covers(t, m):
    v, mask = t
    return (m & ~mask) == (v & ~mask)


def min_cover(on, dc, n):
    """A small sum of products: essential primes first, then greedily the prime covering most remaining minterms."""
    if not on:
        return []
    primes = sorted(prime_implicants(on, dc, n), key=lambda t: (bin(t[1]).count("1") * -1, t))
    left, chosen = set(on), []
    while left:
        ess = [p for p in primes if any(sum(covers(q, m) for q in primes) == 1 and covers(p, m) for m in left)]
        pick = ess[0] if ess else max(primes, key=lambda p: (sum(covers(p, m) for m in left), bin(p[1]).count("1")))
        chosen.append(pick)
        left = {m for m in left if not covers(pick, m)}
    return chosen


def synth(enc: dict) -> dict:
    """Next-state and output logic as minimized sums of products over (state bits, input), unused codes as
    don't-cares; built as a Seq and simulated against the specification."""
    nb = max(enc.values()).bit_length()
    nvars = nb + 1  # variable 0 is the input bit, 1.. are the state bits
    codes = {c: s for s, c in enc.items()}
    funcs = {}
    dc = {m for m in range(1 << nvars) if (m >> 1) not in codes}
    for bit in range(nb):
        on = {(c << 1) | x for c, s in codes.items() for x in (0, 1) if (enc[FSM_NEXT[(s, x)]] >> bit) & 1}
        funcs[f"n{bit}"] = min_cover(on, dc, nvars)
    on_out = {(c << 1) | x for c, s in codes.items() for x in (0, 1) if FSM_OUT.get(s, 0)}
    funcs["y"] = min_cover(on_out, dc, nvars)
    # build it
    sq = S.Seq("1011 detector")
    c = sq.c
    x = c.input("x")
    q = sq.reg("s", nb, init=enc["S0"])
    var = [x] + q
    neg = {}

    def lit(i, val):
        if val:
            return var[i]
        if i not in neg:
            neg[i] = c.not_(var[i])
        return neg[i]

    def sop(terms):
        if not terms:
            return c.const(0)
        outs = []
        for v, mask in terms:
            lits = [lit(i, (v >> i) & 1) for i in range(nvars) if not (mask >> i) & 1]
            t = lits[0]
            for l_ in lits[1:]:
                t = c.and_(t, l_)
            outs.append(t)
        o = outs[0]
        for t in outs[1:]:
            o = c.or_(o, t)
        return o

    sq.set_next("s", [sop(funcs[f"n{b}"]) for b in range(nb)])
    c.output("y", sop(funcs["y"]))
    # simulate against the specification on random streams (outputs are Moore: they depend on the state)
    rng = np.random.default_rng(3)
    stream = rng.integers(0, 2, (400, 64))
    sq.reset(64)
    state = ["S0"] * 64
    ok = True
    for t in range(400):
        out = sq.step({"x": stream[t]})
        want = np.array([FSM_OUT.get(s, 0) for s in state])
        ok &= bool(np.array_equal(out["y"], want))
        state = [FSM_NEXT[(s, int(b))] for s, b in zip(state, stream[t])]
    terms = sum(len(v) for v in funcs.values())
    lits = sum(nvars - bin(m).count("1") for v in funcs.values() for _, m in v)
    return {"flip_flops": nb, "gates": c.size(), "terms": terms, "literals": lits, "verified": ok,
            "codes": {s: format(code, f"0{nb}b") for s, code in enc.items()}}


def compute_fsm() -> dict:
    # an example input and the detector's states and outputs
    xs = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1]
    st, trace = "S0", []
    for x in xs:
        trace.append({"x": x, "state": st, "y": FSM_OUT.get(st, 0)})
        st = FSM_NEXT[(st, x)]
    trace.append({"x": None, "state": st, "y": FSM_OUT.get(st, 0)})
    return {"states": FSM_STATES, "next": [[s, x, FSM_NEXT[(s, x)]] for s in FSM_STATES for x in (0, 1)],
            "trace": trace, "encodings": {k: synth(v) for k, v in encodings().items()}}


# ---------------------------------------------------------------------------
# Myhill-Nerode
# ---------------------------------------------------------------------------
def minimize(states, alphabet, delta, accept):
    """Moore's partition refinement: start from {accepting, rejecting}; split blocks whose states disagree on which
    block some letter leads to; stop when nothing splits.  Returns every round's partition."""
    block = {s: int(s in accept) for s in states}
    rounds = [dict(block)]
    while True:
        sig = {s: (block[s],) + tuple(block[delta[(s, a)]] for a in alphabet) for s in states}
        ids, new = {}, {}
        for s in states:
            new[s] = ids.setdefault(sig[s], len(ids))
        if len(set(new.values())) == len(set(block.values())):
            return rounds
        block = new
        rounds.append(dict(block))


def compute_nerode() -> dict:
    # binary numbers read most significant bit first; state = value mod 6; accept multiples of 3
    states = list(range(6))
    delta = {(r, b): (2 * r + b) % 6 for r in states for b in (0, 1)}
    accept = {0, 3}
    rounds = minimize(states, (0, 1), delta, accept)
    final = rounds[-1]
    # check the minimal machine on every string up to length 12
    nblocks = len(set(final.values()))
    for L in range(1, 13):
        for bits in itertools.product((0, 1), repeat=L):
            r = 0
            for b in bits:
                r = delta[(r, b)]
            v = int("".join(map(str, bits)), 2)
            assert (r in accept) == (v % 3 == 0)
    return {"states": states, "delta": [[r, b, delta[(r, b)]] for r in states for b in (0, 1)],
            "accept": sorted(accept), "rounds": [[final_r[s] for s in states] for final_r in rounds],
            "minimal": nblocks}


# ---------------------------------------------------------------------------
# LFSRs
# ---------------------------------------------------------------------------
def lfsr_period(poly: int, n: int) -> int:
    """Period of the Galois LFSR for the degree-n polynomial (bit i = coefficient of x^i), from state 1: the order
    of x modulo the polynomial."""
    s, t = 1, 0
    while True:
        s <<= 1
        if s >> n & 1:
            s ^= poly
        t += 1
        if s == 1:
            return t
        if t > (1 << n):
            return 0


def totient(m: int) -> int:
    r, x, p = m, m, 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            r -= r // p
        p += 1
    if x > 1:
        r -= r // x
    return r


def compute_lfsr() -> dict:
    rows = []
    for n in range(2, 9):
        periods = {}
        for mid in range(1 << (n - 1)):
            poly = (1 << n) | (mid << 1) | 1  # x^n + ... + 1
            periods[poly] = lfsr_period(poly, n)
        maximal = [p for p, t in periods.items() if t == (1 << n) - 1]
        rows.append({"n": n, "polys": len(periods), "maximal": len(maximal), "expected": totient((1 << n) - 1) // n,
                     "example": min(maximal), "periods": sorted(set(periods.values()))})
        assert len(maximal) == totient((1 << n) - 1) // n
    # the 4-bit sequence for x^4 + x^3 + 1 (Fibonacci form, taps at bits 3 and 2)
    l4 = S.lfsr((3, 2), 4)
    l4.reset(1)
    seq4 = [int(l4.step({})["r"][0]) for _ in range(16)]
    return {"rows": rows, "seq4": seq4}


# ---------------------------------------------------------------------------
# the register file
# ---------------------------------------------------------------------------
def compute_regfile() -> dict:
    rf = S.register_file(16, 32)
    rng = np.random.default_rng(4)
    copies = 256
    rf.reset(copies)
    model = np.zeros((copies, 16), dtype=np.int64)
    idx = np.arange(copies)
    for _ in range(64):
        we = rng.integers(0, 2, copies)
        wa = rng.integers(0, 16, copies)
        wd = rng.integers(0, 1 << 32, copies)
        ra = rng.integers(0, 16, copies)
        rb = rng.integers(0, 16, copies)
        out = rf.step({"we": we, "wa": wa, "wd": wd, "ra": ra, "rb": rb})
        assert np.array_equal(out["a"], model[idx, ra]) and np.array_equal(out["b"], model[idx, rb])
        m = (we == 1) & (wa != 0)
        model[idx[m], wa[m]] = wd[m]
    counts = rf.c.counts()
    # what ports cost: one read port is a 16:1 multiplexer tree per bit
    mux_bit = 15 * 4  # fifteen 2:1 multiplexers of four gates each (AND, AND, OR, NOT)
    return {"gates": rf.c.size(), "counts": counts, "flip_flops": rf.flip_flops, "depth": rf.c.depth(),
            "cycles": 64, "copies": copies, "read_port_gates": 32 * mux_bit, "regs": 16, "width": 32}


# ---------------------------------------------------------------------------
# DRAM
# ---------------------------------------------------------------------------
def compute_dram() -> dict:
    # charge on a cell capacitor leaks with a time constant long enough to survive 64 ms with margin
    tau = 0.25  # seconds (cells vary over orders of magnitude; refresh is set by the weakest)
    t = np.linspace(0, 0.256, 513)
    refresh = 0.064
    v_no = np.exp(-t / tau)
    v_ref = np.exp(-(t % refresh) / tau)
    return {"t": t.tolist(), "v_no": v_no.tolist(), "v_ref": v_ref.tolist(), "threshold": 0.5, "refresh": refresh,
            "tau": tau, "fail_no_refresh": float(-tau * math.log(0.5))}


# ---------------------------------------------------------------------------
# The Frontier chapter (videos/cs/SYLLABUS.md 1.1): defending against Rowhammer, by probability and by counting
# ---------------------------------------------------------------------------
REFRESH_S = 0.064      # every row is refreshed once per 64 ms
T_RC_S = 46.25e-9      # DDR4 row cycle time: one activation per bank at most every tRC
THRESHOLDS = [         # (year, activations of one aggressor row before a flip, source)
    (2014, 139_000, r"DDR3 \ (Kim et al.)"), (2020, 10_000, r"new DDR4 \ (Kim et al.)"),
    (2020, 4_800, r"most vulnerable \ (Kim et al.)")]


def misra_gries(stream, k: int, threshold: int):
    """A bounded-window teaching model inspired by Misra--Gries.

    Every live counter is positive. At ``threshold``, model an immediate victim
    refresh and remove that aggressor's counter. Within n input activations, the
    undercount since its last mitigation is at most floor(n/(k+1)). This does not
    model physical victim contributions, rolling refresh windows or queues, and
    is not Graphene's spillover-counter implementation.
    """
    if k < 1 or threshold < 1:
        raise ValueError("positive counter count and refresh threshold required")
    counters: dict[int, int] = {}
    since = {}
    worst = {}
    for r in stream:
        since[r] = since.get(r, 0) + 1
        worst[r] = max(worst.get(r, 0), since[r])
        if r in counters:
            counters[r] += 1
        elif len(counters) < k:
            counters[r] = 1
        else:
            for q in list(counters):
                counters[q] -= 1
                if counters[q] == 0:
                    del counters[q]
        if counters.get(r, 0) >= threshold:
            # A retained zero can become negative on the next full-table miss,
            # occupying a slot forever. Refresh must free the counter.
            del counters[r]
            since[r] = 0
    return worst


def compute_hammerdefence() -> dict:
    window = int(REFRESH_S / T_RC_S)            # activations one bank can make between refreshes
    year = 365 * 24 * 3600
    annual_opportunities = math.ceil(year / T_RC_S)
    para = []
    for t in (139_000, 50_000, 10_000, 4_800, 2_000, 1_000, 500):
        # Every activation can end a run of t missed mitigations. Counting only
        # disjoint t-activation attempts misses overlapping opportunities. The
        # union bound does not require those runs to be independent.
        p = -math.expm1(math.log(1e-2 / annual_opportunities) / t)
        para.append({"t": t, "p": p})
    # trigger a refresh at t/2; Misra-Gries undercounts by at most window/(k+1), so k >= 2 window / t keeps every
    # row below t between refreshes of its neighbours
    counters = [{"t": t, "k": math.ceil(2 * window / t)} for t in (139_000, 10_000, 4_800, 1_000, 100)]
    # a many-sided attack against a small tracker (TRRespass's insight), simulated: 20 aggressor rows, round robin,
    # with one benign access in every eight
    rng = np.random.default_rng(5)
    t = 10_000
    aggressors = list(range(20))
    n = window
    stream = np.empty(n, np.int64)
    stream[:] = np.array(aggressors * (n // 20 + 1))[:n]
    benign = rng.random(n) < 1 / 8
    stream[benign] = rng.integers(1000, 65_536, benign.sum())
    sim = []
    for k in (4, 16, 64, math.ceil(2 * window / t)):
        worst = misra_gries(stream.tolist(), k, t // 2)
        top = max(worst[a] for a in aggressors)
        sim.append({"k": k, "max_unrefreshed": int(top), "flips": bool(top >= t), "bound": t // 2 + window // (k + 1)})
    return {"schema": HAMMER_SCHEMA, "window": window, "annual_opportunities": annual_opportunities,
            "thresholds": THRESHOLDS, "para": para, "counters": counters, "sim_t": t,
            "sim_aggressors": len(aggressors), "sim": sim}


ITEMS = {
    "latch": compute_latch, "phase": compute_phase, "meta": compute_meta, "fsm": compute_fsm,
    "nerode": compute_nerode, "lfsr": compute_lfsr, "regfile": compute_regfile, "dram": compute_dram,
    "hammerdefence": compute_hammerdefence,
}

if __name__ == "__main__":
    import sys
    requested = [x for x in sys.argv[1:] if not x.startswith("-")]
    if not {"--force", "--help", "-h"}.intersection(sys.argv[1:]):
        if (not requested or "hammerdefence" in requested) and CACHE.path("hammerdefence").exists():
            if not cache_current("hammerdefence"):
                load("hammerdefence")
    CACHE.main(ITEMS, __doc__)
