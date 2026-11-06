"""Laws, chance and the arrow of time, built (Part 24).

* A best-system toy: polynomial laws of rising degree scored on noisy data for simplicity and strength, with a
  two-part description length (Part 15's MDL) deciding the trade-off.
* Lewis's Humean chance and the big bad bug: on a finite history of coin tosses, the chance itself gives positive
  probability to futures that would make the chance different (undermining futures), so the Principal Principle
  contradicts itself; the New Principle conditions on the theory of chance.
* Norton's dome: the solutions r(t) = (t - T)^4 / 144 of Newton's law r'' = sqrt(r), checked symbolically and
  numerically, for several starting times T.
* Chaos: the Lorenz system integrated, two trajectories 1e-9 apart diverging, and the largest Lyapunov exponent
  estimated by renormalized separation (about 0.9).
* The Kac ring: a reversible, recurrent toy dynamics whose coarse-grained colour imbalance still decays to equilibrium,
  recurs exactly after 2N steps, and retraces itself when reversed: Loschmidt and Zermelo made visible.
* Boltzmann entropy for a box of gas, and the improbability of fluctuations: why a Boltzmann brain is more likely than a
  low-entropy universe.
* Landauer's bound: kT ln 2 per erased bit, the information an AND gate destroys, and a Toffoli gate that destroys
  none.
"""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# The best-system account
# ---------------------------------------------------------------------------
def best_system(n: int = 40, noise: float = 0.6, seed: int = 24, max_degree: int = 7) -> dict:
    """Data from a falling-body law (height = 20 - 4.9 t^2 with noise). Each candidate `law' is a polynomial of
    degree d. Simplicity: the number of parameters, d + 1. Strength: how much of the data the law fixes, measured by
    the residual error. The two-part code length (parameters plus residuals, in bits) balances them: the best system
    is the quadratic."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 2, n)
    y = 20 - 4.9 * t ** 2 + noise * rng.standard_normal(n)
    rows = []
    for d in range(0, max_degree + 1):
        c = np.polyfit(t, y, d)
        res = y - np.polyval(c, t)
        rss = float(res @ res)
        sigma2 = max(rss / n, 1e-12)
        data_bits = 0.5 * n * math.log2(2 * math.pi * math.e * sigma2)
        model_bits = 0.5 * (d + 1) * math.log2(n)
        grid = np.linspace(0, 2, 81)
        rows.append({"degree": d, "params": d + 1, "rss": round(rss, 3), "model_bits": round(model_bits, 2),
                     "data_bits": round(data_bits, 2), "total": round(model_bits + data_bits, 2),
                     "coef": [round(float(x), 3) for x in c[::-1]],
                     "curve": [round(float(v), 3) for v in np.polyval(c, grid)]})
    best = min(rows, key=lambda r: r["total"])["degree"]
    return {"n": n, "noise": noise, "rows": rows, "best_degree": best,
            "data": [[round(float(a), 3), round(float(b), 3)] for a, b in zip(t, y)]}


# ---------------------------------------------------------------------------
# Humean chance and the big bad bug
# ---------------------------------------------------------------------------
def undermining(past_tosses: int = 10, past_heads: int = 5, future_tosses: int = 10) -> dict:
    """A Humean world of coin tosses. The chance of heads is fixed by the whole history: the frequency over all tosses.
    Suppose the actual whole history has frequency 1/2. Given the past, the chance theory assigns each possible future
    a probability; the futures in which the total frequency is not 1/2 are `undermining': had they happened, the
    chance would have been different. Their total chance is positive, so the Principal Principle (credence = chance,
    given the chance) would give positive credence to futures inconsistent with the chance information."""
    p = 0.5
    total = past_tosses + future_tosses
    needed = int(total * p) - past_heads        # future heads that keep the frequency at 1/2
    keep = math.comb(future_tosses, needed) * p ** future_tosses if 0 <= needed <= future_tosses else 0.0
    rows = []
    for k in range(future_tosses + 1):
        prob = math.comb(future_tosses, k) * p ** future_tosses
        freq = (past_heads + k) / total
        rows.append({"future_heads": k, "chance": round(prob, 5), "frequency": round(freq, 3),
                     "undermines": abs(freq - p) > 1e-12})
    return {"p": p, "past": [past_tosses, past_heads], "future": future_tosses, "rows": rows,
            "undermining_chance": round(1 - keep, 4), "consistent_chance": round(keep, 4)}


# ---------------------------------------------------------------------------
# Norton's dome
# ---------------------------------------------------------------------------
def norton_dome(Ts=(0.0, 1.0, 2.0, 3.0), t_max: float = 6.0, steps: int = 61) -> dict:
    """On Norton's dome a point mass obeys r'' = sqrt(r) (in suitable units). r(t) = 0 for all t is a solution; so is
    r(t) = 0 for t <= T and (t - T)^4 / 144 after, for every T: the mass may start sliding at any time, or never.
    The Reasoner checks r'' = sqrt(r) numerically on each solution."""
    ts = np.linspace(0, t_max, steps)
    sols = []
    for T in Ts:
        r = np.where(ts > T, (ts - T) ** 4 / 144.0, 0.0)
        rdd = np.where(ts > T, (ts - T) ** 2 / 12.0, 0.0)
        err = float(np.max(np.abs(rdd - np.sqrt(r))))
        sols.append({"T": T, "r": [round(float(v), 4) for v in r], "max_error": err})
    # numerical second derivative of one solution, as an independent check
    T = Ts[1]
    h = 1e-3
    f = lambda t: ((t - T) ** 4 / 144.0) if t > T else 0.0  # noqa: E731
    pts = [T + 0.5, T + 1.5, T + 2.5]
    num = [((f(t + h) - 2 * f(t) + f(t - h)) / h ** 2, math.sqrt(f(t))) for t in pts]
    # Earman's test: two models that agree at one time must agree at all times. The T-solutions agree up to min(T)
    pairs = [{"T1": a["T"], "T2": b["T"], "agree_until": min(a["T"], b["T"]),
              "differ_after": any(x != y for x, y in zip(a["r"], b["r"]))} for i, a in enumerate(sols)
             for b in sols[i + 1:]]
    return {"t": [round(float(x), 3) for x in ts], "solutions": sols, "pairs": pairs,
            "deterministic": not any(p["differ_after"] for p in pairs),
            "finite_difference_check": [{"t": t, "rdd": round(a, 5), "sqrt_r": round(b, 5)} for t, (a, b) in
                                        zip(pts, num)]}


# ---------------------------------------------------------------------------
# Chaos: the Lorenz system
# ---------------------------------------------------------------------------
def _lorenz(s, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    x, y, z = s
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])


def _rk4(s, dt):
    k1 = _lorenz(s)
    k2 = _lorenz(s + dt / 2 * k1)
    k3 = _lorenz(s + dt / 2 * k2)
    k4 = _lorenz(s + dt * k3)
    return s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def lorenz(t_max: float = 40.0, dt: float = 0.005, delta: float = 1e-9) -> dict:
    """Integrate the Lorenz system from (1, 1, 1) and from a point 1e-9 away; record both paths (thinned) and their
    separation. Estimate the largest Lyapunov exponent by renormalizing the separation every step (Benettin's
    method)."""
    n = int(t_max / dt)
    a = np.array([1.0, 1.0, 1.0])
    for _ in range(2000):          # settle onto the attractor
        a = _rk4(a, dt)
    b = a + np.array([delta, 0, 0])
    path_a, path_b, sep, times = [], [], [], []
    for i in range(n):
        a, b = _rk4(a, dt), _rk4(b, dt)
        if i % 10 == 0:
            path_a.append([round(float(v), 3) for v in a])
            path_b.append([round(float(v), 3) for v in b])
            sep.append(float(np.linalg.norm(a - b)))
            times.append(round(i * dt, 3))
    # Lyapunov exponent
    x = np.array([1.0, 1.0, 1.0])
    for _ in range(2000):
        x = _rk4(x, dt)
    y = x + np.array([1e-8, 0, 0])
    acc, m = 0.0, 40000
    for _ in range(m):
        x, y = _rk4(x, dt), _rk4(y, dt)
        d = np.linalg.norm(y - x)
        acc += math.log(d / 1e-8)
        y = x + (y - x) * (1e-8 / d)
    lam = acc / (m * dt)
    sep_arr = np.array(sep)
    reach = next((t for t, s in zip(times, sep) if s > 1.0), None)
    # prediction horizons: how long until an initial error delta grows to 1, for several deltas
    horizons = []
    for e in (1e-3, 1e-6, 1e-9, 1e-12):
        u = a.copy()
        v = u + np.array([e, 0, 0])
        t = 0.0
        while np.linalg.norm(u - v) < 1.0 and t < 200:
            u, v = _rk4(u, dt), _rk4(v, dt)
            t += dt
        horizons.append({"delta": e, "time": round(t, 2), "theory": round(math.log(1 / e) / lam, 2)})
    return {"path_a": path_a, "path_b": path_b, "times": times, "separation": [float(f"{s:.3e}") for s in sep_arr],
            "lyapunov": round(lam, 3), "reaches_one_at": reach, "delta": delta, "horizons": horizons}


# ---------------------------------------------------------------------------
# The Kac ring
# ---------------------------------------------------------------------------
def kac_ring(N: int = 200, marker_fraction: float = 0.1, steps: int = 450, seed: int = 1959) -> dict:
    """N sites on a ring, a fixed random set of `marked' edges (fraction mu), a ball at every site, black or white.
    Each step every ball moves one site clockwise and flips colour if it crosses a marked edge. The dynamics is
    deterministic, reversible (run it anticlockwise) and recurrent (every configuration returns after 2N steps).
    Start all white. The colour imbalance delta = (white - black) / N decays roughly like (1 - 2 mu)^t, the
    coarse-grained `entropy' rises; at t = 2N everything returns to white. Reverse the motion at time R and it
    retraces itself back to all white at 2R."""
    rng = np.random.default_rng(seed)
    marked = rng.random(N) < marker_fraction
    mu = float(marked.mean())
    colour = np.ones(N, dtype=int)             # +1 white, -1 black

    def step(c, forward=True):
        if forward:
            flipped = np.where(marked, -c, c)  # edge i between site i and i+1
            return np.roll(flipped, 1)
        c2 = np.roll(c, -1)
        return np.where(marked, -c2, c2)

    def ent(c):
        w = (c > 0).mean()
        ps = [p for p in (w, 1 - w) if p > 0]
        return -sum(p * math.log2(p) for p in ps) + 0.0

    c = colour.copy()
    delta, entropy = [], []
    for t in range(steps + 1):
        delta.append(round(float(c.mean()), 4))
        entropy.append(round(ent(c), 4))
        c = step(c)
    # reversal at R
    R = 60
    c = colour.copy()
    for _ in range(R):
        c = step(c)
    rev = [round(float(c.mean()), 4)]
    for _ in range(R):
        c = step(c, forward=False)
        rev.append(round(float(c.mean()), 4))
    theory = [round((1 - 2 * mu) ** t, 4) for t in range(steps + 1)]
    return {"N": N, "mu": round(mu, 4), "markers": int(marked.sum()), "delta": delta, "entropy": entropy,
            "theory": theory, "recurrence_at": 2 * N, "returns": delta[2 * N] == 1.0 if 2 * N <= steps else None,
            "half_way": delta[N] if N <= steps else None, "reverse_at": R, "reversed": rev,
            "reverse_returns": rev[-1] == 1.0, "marked": [int(i) for i in np.flatnonzero(marked)]}


def kac_both_ways(N: int = 2000, marker_fraction: float = 0.1, white: float = 0.8, steps: int = 30,
                  seed: int = 1876) -> dict:
    """Loschmidt made visible. Take a typical configuration with a low-entropy macrostate *now* (80% white), with
    nothing special about how it arose, and run the reversible ring both ways. The imbalance decays toward zero
    in the future and in the past: without a special beginning, the most probable past has higher entropy."""
    rng = np.random.default_rng(seed)
    marked = rng.random(N) < marker_fraction
    c0 = np.where(rng.random(N) < white, 1, -1)

    def fwd(c):
        return np.roll(np.where(marked, -c, c), 1)

    def bwd(c):
        c2 = np.roll(c, -1)
        return np.where(marked, -c2, c2)

    def ent(c):
        w = (c > 0).mean()
        return float(-sum(p * math.log2(p) for p in (w, 1 - w) if p > 0))

    f, b = c0.copy(), c0.copy()
    future, past = [ent(c0)], [ent(c0)]
    for _ in range(steps):
        f, b = fwd(f), bwd(b)
        future.append(ent(f))
        past.append(ent(b))
    ts = list(range(-steps, steps + 1))
    ents = [round(x, 4) for x in past[::-1]] + [round(x, 4) for x in future[1:]]
    return {"N": N, "t": ts, "entropy": ents, "now": round(ent(c0), 4), "future_end": round(future[-1], 4),
            "past_end": round(past[-1], 4)}


def kac_states(N: int = 36, marked=(2, 7, 11, 19, 23, 30), steps: int = 72) -> dict:
    """A small Kac ring for drawing: the colour of every ball at every step, for 2N steps (back to the start)."""
    m = np.zeros(N, dtype=bool)
    m[list(marked)] = True
    c = np.ones(N, dtype=int)
    states = [c.tolist()]
    for _ in range(steps):
        c = np.roll(np.where(m, -c, c), 1)
        states.append(c.tolist())
    whites = [sum(1 for v in st if v > 0) for st in states]
    return {"N": N, "marked": list(marked), "states": states, "whites": whites,
            "returns_at_2N": states[2 * N] == states[0] if 2 * N <= steps else None}


# ---------------------------------------------------------------------------
# Boltzmann entropy and fluctuations
# ---------------------------------------------------------------------------
def boltzmann(n: int = 100) -> dict:
    """n molecules in a box with two halves. Microstates: 2^n. A macrostate `k on the left' has C(n, k)
    microstates; S = k_B ln W. The probability of finding all on the left by chance: 2^-n. For a real gas of 1e23
    molecules, the exponent is astronomical; fluctuations are exponentially rarer the bigger they are, which is why
    a single fluctuating brain is vastly more probable than a fluctuating low-entropy universe."""
    W = [math.comb(n, k) for k in range(n + 1)]
    S = [math.log(w) for w in W]
    half = W[n // 2]
    fluct = [{"left": k, "log10_p": round(math.log10(W[k]) - n * math.log10(2), 2),
              "entropy_drop": round(S[n // 2] - S[k], 2)} for k in range(n // 2, n + 1, 10)]
    return {"n": n, "W_half_log10": round(math.log10(half), 2), "W_all_left": 1, "p_all_left_log10":
            round(-n * math.log10(2), 2), "S": [round(s, 3) for s in S], "fraction_within_10pct":
            round(sum(W[k] for k in range(int(0.4 * n), int(0.6 * n) + 1)) / 2 ** n, 4), "fluctuations": fluct}


# ---------------------------------------------------------------------------
# Landauer and reversible logic
# ---------------------------------------------------------------------------
K_B = 1.380649e-23


def landauer(T: float = 300.0) -> dict:
    """kT ln 2 at room temperature; the information an AND gate destroys on uniform inputs (2 bits in, H(1/4) bits
    out); a Toffoli gate is a bijection on 3 bits and destroys none."""
    e_bit = K_B * T * math.log(2)
    h_out = -(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75))
    lost_and = 2 - h_out
    tof = {}
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                tof[(a, b, c)] = (a, b, c ^ (a & b))
    bijective = len(set(tof.values())) == 8
    return {"T": T, "joules_per_bit": e_bit, "ev_per_bit": e_bit / 1.602176634e-19, "and_lost_bits": round(lost_and, 4),
            "and_min_energy": lost_and * e_bit, "toffoli_bijective": bijective,
            "toffoli": [{"in": list(k), "out": list(v)} for k, v in tof.items()]}


def szilard(T: float = 300.0, cycles: int = 20000, seed: int = 1929) -> dict:
    """Szilard's one-molecule engine. Insert a partition at fraction x of the box, look which side the molecule is on
    (one measurement), and let that side expand isothermally to the whole box: work kT ln(1/x) if left (probability
    x), kT ln(1/(1-x)) if right. The expected work is kT times the Shannon entropy of the measurement in nats, at
    most kT ln 2 at x = 1/2. Simulated over many cycles. Erasing the demon's one-bit record costs at least kT ln 2
    (Landauer), so the cycle gains nothing (Bennett)."""
    rng = np.random.default_rng(seed)
    kT = K_B * T
    rows = []
    for x in (0.1, 0.25, 0.5, 0.75, 0.9):
        pos = rng.random(cycles)
        w = np.where(pos < x, kT * math.log(1 / x), kT * math.log(1 / (1 - x)))
        h = -(x * math.log(x) + (1 - x) * math.log(1 - x))
        rows.append({"x": x, "simulated_kT": round(float(w.mean() / kT), 4), "theory_kT": round(h, 4),
                     "bits": round(h / math.log(2), 4)})
    return {"T": T, "rows": rows, "max_work_J": kT * math.log(2), "erasure_cost_J": kT * math.log(2),
            "net_kT": 0.0}


def new_principle(run: int = 3, futures=(10, 100, 1000, 10000)) -> dict:
    """Hall's and Lewis's New Principle: credence should match chance *conditional on the theory of chance*. In the
    toy world the theory T says the whole history has frequency 1/2, so for a future of n tosses after a balanced past
    it is the condition `exactly n/2 future heads'. For A = `the next `run' tosses are all heads', compare the Principal
    Principle's ch(A) = 2^-run with the New Principle's ch(A | T) = C(n - run, n/2 - run) / C(n, n/2). The two agree as
    the world grows: undermining matters only for propositions about a large part of history."""
    pp = 0.5 ** run
    rows = []
    for n in futures:
        k = n // 2
        # ratio C(n-run, k-run) / C(n, k) computed stably
        lr = (math.lgamma(n - run + 1) - math.lgamma(k - run + 1) - math.lgamma(n - k + 1)
              - (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)))
        rows.append({"future": n, "np": round(math.exp(lr), 5), "pp": pp})
    return {"run": run, "pp": pp, "rows": rows}


def arbitrary_functions(sectors: int = 36, samples: int = 200000, seed: int = 1896) -> dict:
    """Poincaré's roulette wheel (the method of arbitrary functions). A wheel with alternating red and black sectors
    is spun with initial speed v and decelerates uniformly, so its final angle is proportional to v^2. The outcome is
    a deterministic function of v, but it changes colour many times over any small range of speeds. For any smooth
    distribution of speeds, however lopsided, the chance of red comes out close to one half: deterministic chance
    from sensitivity."""
    rng = np.random.default_rng(seed)
    dists = {
        "normal(10, 1)": rng.normal(10, 1, samples),
        "uniform(8, 9)": rng.uniform(8, 9, samples),
        "gamma(4, 2.5)": rng.gamma(4, 2.5, samples),
        "skewed: 8 + exponential(0.7)": 8 + rng.exponential(0.7, samples),
    }
    rows = []
    for name, v in dists.items():
        v = np.abs(v)
        angle = v ** 2 / 2.0                         # radians, with unit deceleration
        sector = np.floor(angle / (2 * np.pi) * sectors).astype(int)
        red = float(np.mean(sector % 2 == 0))
        rows.append({"speeds": name, "red": round(red, 4)})
    # the outcome as a function of speed, for drawing
    vs = np.linspace(8.0, 8.6, 601)
    out = [int(np.floor((v ** 2 / 2.0) / (2 * np.pi) * sectors)) % 2 == 0 for v in vs]
    return {"sectors": sectors, "rows": rows, "v": [round(float(v), 4) for v in vs], "red_at_v": out}


def h_theorem(n: int = 6000, steps: int = 12, seed: int = 1872, bins: int = 24) -> dict:
    """Boltzmann's H falling, in a toy kinetic gas. n molecules move in the plane, all at speed 1 in random
    directions. Each round every molecule collides with a random partner: the pair keeps its total momentum and
    energy, and its relative velocity turns through a random angle. The distribution of one velocity component
    relaxes to Maxwell's Gaussian, and H = sum f log f (over a velocity histogram) falls to its minimum."""
    rng = np.random.default_rng(seed)
    a = rng.random(n) * 2 * np.pi
    v = np.column_stack([np.cos(a), np.sin(a)])
    edges = np.linspace(-3, 3, bins + 1)

    def H(v):
        h, _, _ = np.histogram2d(v[:, 0], v[:, 1], bins=[edges, edges])
        f = h / h.sum()
        f = f[f > 0]
        return float((f * np.log(f)).sum())

    def hist(v):
        h, _ = np.histogram(v[:, 0], bins=edges)
        return [round(float(x) / n / (edges[1] - edges[0]), 4) for x in h]

    Hs, hists = [round(H(v), 4)], [hist(v)]
    for _ in range(steps):
        idx = rng.permutation(n)
        i, j = idx[: n // 2], idx[n // 2:]
        cm = (v[i] + v[j]) / 2
        rel = (v[i] - v[j]) / 2
        th = rng.random(n // 2) * 2 * np.pi
        c, s = np.cos(th), np.sin(th)
        r2 = np.column_stack([c * rel[:, 0] - s * rel[:, 1], s * rel[:, 0] + c * rel[:, 1]])
        v[i], v[j] = cm + r2, cm - r2
        Hs.append(round(H(v), 4))
        hists.append(hist(v))
    centers = [round(float(x), 3) for x in (edges[:-1] + edges[1:]) / 2]
    sigma2 = float((v[:, 0] ** 2).mean())
    return {"n": n, "H": Hs, "hists": hists, "centers": centers, "energy": round(float((v ** 2).sum(1).mean()), 6),
            "sigma2": round(sigma2, 4)}


def free_gas(n: int = 46, seed: int = 1876, t_rev: float = 8.0, steps: int = 81, cells: int = 4) -> dict:
    """Loschmidt's reversal in the hook's toy gas: free molecules in a box, starting crowded in a corner. Coarse-grain
    the box into cells x cells and take the Shannon entropy of the occupation. It rises as the gas spreads; reverse
    every velocity at t_rev and it falls back to its starting value, by the same laws."""
    rng = np.random.default_rng(seed)
    box = (-3.0, 3.0, -2.2, 1.8)
    x0, x1, y0, y1 = box
    p = np.column_stack([x0 + (x1 - x0) * 0.2 * rng.random(n), y0 + (y1 - y0) * 0.2 * rng.random(n)])
    a = rng.random(n) * 2 * np.pi
    s = 1.1 * (0.6 + 0.8 * rng.random(n))
    v = np.column_stack([s * np.cos(a), s * np.sin(a)])

    def fold1(u, lo, hi):
        span = hi - lo
        m = np.mod(u - lo, 2 * span)
        return lo + np.where(m < span, m, 2 * span - m)

    def at(t):
        q = p + v * t
        return np.column_stack([fold1(q[:, 0], x0, x1), fold1(q[:, 1], y0, y1)])

    def ent(q):
        ix = np.clip(((q[:, 0] - x0) / (x1 - x0) * cells).astype(int), 0, cells - 1)
        iy = np.clip(((q[:, 1] - y0) / (y1 - y0) * cells).astype(int), 0, cells - 1)
        counts = np.bincount(ix * cells + iy, minlength=cells * cells) / n
        c = counts[counts > 0]
        return float(-(c * np.log2(c)).sum())

    ts = np.linspace(0, 2 * t_rev, steps)
    # forward to t_rev, then the reversed motion: the state at t_rev + u is the state at t_rev - u
    ents = [abs(round(ent(at(t if t <= t_rev else 2 * t_rev - t)), 4)) for t in ts]
    return {"t": [round(float(t), 3) for t in ts], "entropy": ents, "t_rev": t_rev, "max": round(math.log2(cells * cells), 4)}


def recurrence(max_n: int = 4, eps: float = 0.05, dt: float = 0.005, t_total: float = 40000.0) -> dict:
    """Poincaré recurrence in miniature: n independent rotors with incommensurable frequencies (square roots of
    primes) all start at phase 0. Count how often, over a long run, all n phases come back within eps of 0, and so
    the mean time between returns. Each extra rotor multiplies the wait several times over (here by five to seven):
    with 10^23 degrees of freedom the return is certain but unimaginably far off."""
    freqs = np.sqrt(np.array([2.0, 3.0, 5.0, 7.0, 11.0, 13.0]))[:max_n]
    rows = []
    chunk = 1_000_000
    for n in range(1, max_n + 1):
        f = freqs[:n]
        entries, prev, t0 = 0, True, 0.0
        first = None
        while t0 < t_total:
            ts = t0 + dt * np.arange(chunk)
            ph = np.mod(np.outer(ts, f), 1.0)
            near = np.all(np.minimum(ph, 1 - ph) < eps, axis=1)
            starts = near & ~np.concatenate([[prev], near[:-1]])
            k = np.flatnonzero(starts)
            if first is None and len(k):
                first = float(ts[k[0]])
            entries += int(starts.sum())
            prev = bool(near[-1])
            t0 = ts[-1] + dt
        rows.append({"rotors": n, "returns": entries, "mean_gap": round(t_total / max(entries, 1), 1),
                     "first_return": round(first, 2) if first else None})
    return {"eps": eps, "t_total": t_total, "rows": rows}
