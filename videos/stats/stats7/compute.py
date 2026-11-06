"""Precompute every number in Part 7 of *Statistics, Built* ("Randomness on Demand").

    python -m videos.stats.stats7.compute            # everything missing (about a minute)
    python -m videos.stats.stats7.compute --force shuffle

Results are cached in ``.cache/stats7/<name>.json``; scenes call ``load(name)``.  Every generator here is written out
in ``explainer.stats.kit.random`` (``randu``, ``lcg``, ``PCG32``) so that its output can be checked by hand; the samplers draw their uniforms
from ``pcg32``.  The riffle-shuffle distances are exact (Bayer & Diaconis's formula in integer arithmetic).

Items:
    randu        consecutive RANDU triples (15 planes) and PCG32 triples; the plane identity 9x - 6y + z
    lcg          a toy LCG mod 64: its cycle, a full-period choice, the lattice of pairs
    tests        chi-square (1-D and 3-D cells) and runs tests for RANDU and PCG32
    inverse      exponential and a discrete law by inversion
    rejection    Beta(2, 5) under a box: 600 darts, accepted or not; the acceptance rate 1/M
    special      Box-Muller pairs; Marsaglia-Tsang acceptance; Walker's alias table for a six-point law
    montecarlo   darts for pi; MC vs a grid for the volume of the d-ball; Buffon's needle and Lazzarini's 355/113
    simstudy     a simulation study: coverage of the Wald interval for a binomial share, with MC standard errors
    varred       antithetic and control variates for E e^U; importance sampling for P(Z > 4)
    chain        a three-state chain: mass flowing to the stationary law; detailed balance; PageRank on 7 pages
    shuffle      total variation after k riffle shuffles of 52 cards (exact); a simulated check for 5 cards
    metropolis   random-walk Metropolis on a two-humped target: three step sizes, traces and acceptance
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.kit.random import M31, M32, PCG32, AliasTable, lcg, marsaglia_tsang, randu

CACHE = Cache("stats7")
load = CACHE.load



def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, Fraction):
        return float(obj)
    return obj


def clipped_segments(xs, ys, rectangle):
    """Clip line segments to a rectangle without flattening off-scale values."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end - start
        lo, hi = 0.0, 1.0
        for k, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[k] == 0:
                if not lower <= start[k] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower - start[k]) / delta[k], (upper - start[k]) / delta[k]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start + lo * delta, start + hi * delta))
    return result


def compute_randu():
    r = randu(1, 3 * 3000 + 2) / M31
    trip = np.c_[r[:-2], r[1:-1], r[2:]][::3][:3000]
    ints = randu(1, 20002)
    k = (9 * ints[:-2] - 6 * ints[1:-1] + ints[2:]) / M31
    planes = sorted(set(np.round(k).astype(int).tolist()))
    p = PCG32(1907).random(9002)
    ptrip = np.c_[p[:-2], p[1:-1], p[2:]][::3][:3000]
    return nest({"randu": trip, "pcg": ptrip, "planes": planes, "n_planes": len(planes),
                 "first": (randu(1, 6)).tolist(), "pcg_first": [PCG32(42, 54).next32() for _ in range(1)]})


def compute_lcg():
    bad = lcg(5, 0, 64, 1, 40)  # multiplicative, period 16
    good = lcg(5, 3, 64, 1, 70)  # Hull-Dobell: c odd, a - 1 divisible by 4: full period 64
    per_bad = bad.index(bad[0], 1) if bad[0] in bad[1:] else None
    seen, per_good = {}, None
    for i, v in enumerate(good):
        if v in seen:
            per_good = i - seen[v]
            break
        seen[v] = i
    pairs = lcg(37, 1, 256, 7, 257)
    return nest({"bad": bad, "good": good, "per_bad": per_bad, "per_good": per_good,
                 "pairs": np.c_[pairs[:-1], pairs[1:]][:256]})


def runs_test(u: np.ndarray) -> float:
    """Wald-Wolfowitz runs above/below the median: z statistic."""
    s = u > np.median(u)
    runs = 1 + np.count_nonzero(s[1:] != s[:-1])
    n1, n2 = float(s.sum()), float((~s).sum())
    mu = 2 * n1 * n2 / (n1 + n2) + 1
    var = 2 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    return float((runs - mu) / np.sqrt(var))


def compute_tests():
    n = 300_000
    ur = randu(1, n) / M31
    up = PCG32(7).random(n)
    out = {}
    for name, u in (("randu", ur), ("pcg", up)):
        c1 = np.bincount(np.minimum((u * 10).astype(int), 9), minlength=10)
        chi1 = float(((c1 - n / 10) ** 2 / (n / 10)).sum())
        t = u[: (n // 3) * 3].reshape(-1, 3)
        idx = np.minimum((t * 10).astype(int), 9)
        cell = idx[:, 0] * 100 + idx[:, 1] * 10 + idx[:, 2]
        c3 = np.bincount(cell, minlength=1000)
        e3 = len(t) / 1000
        chi3 = float(((c3 - e3) ** 2 / e3).sum())
        out[name] = {"chi1": chi1, "p1": float(stats.chi2.sf(chi1, 9)), "chi3": chi3, "p3": float(stats.chi2.sf(chi3, 999)),
                     "runs_z": runs_test(u)}
    return nest(out)


def histogram_density(draws, edges):
    """Keep omitted tail mass in the denominator of a displayed histogram."""
    return np.histogram(draws, edges)[0] / (len(draws) * np.diff(edges))


def compute_inverse():
    u = PCG32(11).random(4000)
    x = -np.log1p(-u)
    ed = np.linspace(0, 6, 31)
    pmf = np.array([0.1, 0.25, 0.3, 0.2, 0.15])
    cdf = np.cumsum(pmf)
    k = np.searchsorted(cdf, u[:2000], side="right")
    return nest({"u": u[:60], "x": x[:60], "hist": histogram_density(x, ed), "edges": ed, "pmf": pmf, "cdf": cdf,
                 "freq": np.bincount(k, minlength=5) / 2000})


def compute_rejection():
    g = PCG32(13)
    M = float(stats.beta.pdf(0.2, 2, 5))
    x, y = g.random(600), g.random(600) * M
    acc = y <= stats.beta.pdf(x, 2, 5)
    xs = PCG32(14).random(60000)
    ys = PCG32(15).random(60000) * M
    a2 = ys <= stats.beta.pdf(xs, 2, 5)
    ed = np.linspace(0, 1, 26)
    return nest({"M": M, "x": x, "y": y, "acc": acc.astype(int), "rate": float(acc.mean()), "rate_big": float(a2.mean()),
                 "hist": np.histogram(xs[a2], ed, density=True)[0], "edges": ed})


def compute_special():
    g = PCG32(21)
    u1, u2 = 1 - g.random(1500), g.random(1500)  # U1 in (0, 1]: log is finite
    r = np.sqrt(-2 * np.log(u1))
    z1, z2 = r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)
    gam, rate = marsaglia_tsang(2.5, 4000, np.random.Generator(np.random.PCG64(22)))
    p = [0.05, 0.3, 0.1, 0.25, 0.2, 0.1]
    tab = AliasTable.build(p)
    prob, alias = tab.prob, tab.alias
    gg = PCG32(23)
    col = (gg.random(30000) * 6).astype(int)
    keep = gg.random(30000) < prob[col]
    draws = np.where(keep, col, alias[col])
    return nest({"u1": u1[:600], "u2": u2[:600], "z1": z1, "z2": z2, "gamma_rate": rate, "gamma_mean": float(gam.mean()),
                 "gamma_hist": histogram_density(gam, np.linspace(0, 10, 41)), "p": p, "prob": prob, "alias": alias,
                 "alias_freq": np.bincount(draws, minlength=6) / 30000})


def compute_montecarlo():
    g = PCG32(31)
    x, y = g.random(4000), g.random(4000)
    inside = (x * x + y * y) <= 1
    est = 4 * np.cumsum(inside) / np.arange(1, 4001)
    # d-ball: exact MC standard error and midpoint-grid error at the same actual budget m**d.
    from math import gamma, pi

    out = {"d": [], "true": [], "mc_err": [], "grid_err": [], "grid_n": []}
    N = 1_000_000
    for d in range(1, 11):
        true = 2.0 if d == 1 else pi ** (d / 2) / gamma(d / 2 + 1)
        m = int(round(N ** (1 / d)))
        actual_n = m ** d
        mc = np.sqrt(true * (2 ** d - true) / actual_n)
        out["grid_n"].append(actual_n)
        t2 = (2 * np.arange(m) + 1 - m) ** 2  # lattice coordinate (2j + 1 - m)/m, squared and scaled by m^2
        dist = {0: 1}
        for _ in range(d):  # the distribution of sum of t^2 over the grid, by repeated convolution
            nd: dict = {}
            for k, v in dist.items():
                for s_ in t2:
                    if k + s_ <= m * m:
                        nd[k + int(s_)] = nd.get(k + int(s_), 0) + v
            dist = nd
        vol = (2 / m) ** d * sum(dist.values())
        out["d"].append(d)
        out["true"].append(true)
        out["mc_err"].append(mc / true)
        out["grid_err"].append(abs(vol - true) / true)
    # Buffon's needle: needle length l = 5/6 of the spacing (Lazzarini, 1901), 3,408 throws
    gb = np.random.Generator(np.random.PCG64(1777))
    l, t = 5 / 6, 1.0
    ests = []
    for _ in range(20000):
        yc = gb.uniform(0, t / 2, 3408)
        th = gb.uniform(0, np.pi / 2, 3408)
        hits = np.count_nonzero(yc <= l / 2 * np.sin(th))
        ests.append(2 * l * 3408 / (t * hits) if hits else np.nan)
    ests = np.asarray(ests)
    p_lazz = float(np.mean(np.abs(ests - np.pi) <= abs(355 / 113 - np.pi)))
    return nest({"x": x[:1500], "y": y[:1500], "inside": inside[:1500].astype(int), "est": est[np.r_[np.arange(0, 4000, 10), 3999]], "est_n": np.r_[np.arange(1, 4001, 10), 4000],
                 "ball": out, "buffon_sd": float(np.nanstd(ests)), "buffon_p": p_lazz, "lazz": 355 / 113,
                 "lazz_err": float(abs(355 / 113 - np.pi)), "buffon_hits_lazz": 1808})


def compute_simstudy():
    rng = np.random.Generator(np.random.PCG64(2019))
    n, reps = 30, 4000
    ps = np.round(np.arange(0.02, 0.99, 0.02), 2)
    cov, mcse, wil = [], [], []
    z = 1.959964
    for p in ps:
        k = rng.binomial(n, p, reps)
        ph = k / n
        se = np.sqrt(ph * (1 - ph) / n)
        c = np.mean((ph - z * se <= p) & (p <= ph + z * se))
        cov.append(float(c))
        mcse.append(float(np.sqrt(c * (1 - c) / reps)))
        den = 1 + z * z / n
        cen = (ph + z * z / (2 * n)) / den
        half = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
        wil.append(float(np.mean((cen - half <= p) & (p <= cen + half))))
    exact = []
    for p in ps:
        k = np.arange(n + 1)
        ph = k / n
        se = np.sqrt(ph * (1 - ph) / n)
        inside = (ph - z * se <= p) & (p <= ph + z * se)
        exact.append(float(stats.binom.pmf(k, n, p)[inside].sum()))
    return nest({"n": n, "reps": reps, "ps": ps, "cover": cov, "mcse": mcse, "wilson": wil, "exact": exact})


def compute_varred():
    rng = np.random.Generator(np.random.PCG64(77))
    n = 1000
    reps = 4000
    plain, anti, ctrl = [], [], []
    for _ in range(reps):
        u = rng.random(n)
        plain.append(np.exp(u).mean())
        h = rng.random(n // 2)
        anti.append(((np.exp(h) + np.exp(1 - h)) / 2).mean())
        f = np.exp(u)
        b = 6 * (3 - np.e)  # known population Cov(exp(U),U)/Var(U); fixed, unbiased control
        ctrl.append(f.mean() - b * (u.mean() - 0.5))
    truth = np.e - 1
    # importance sampling for P(Z > 4)
    p_true = float(stats.norm.sf(4))
    N = 100_000
    zs = rng.standard_normal((200, N))
    plain_is = (zs > 4).mean(1)
    ys = rng.standard_normal((200, N)) + 4
    w = np.exp(-4 * ys + 8)  # phi(y) / phi(y - 4)
    imp = ((ys > 4) * w).mean(1)
    return nest({"truth": truth, "control_b": 6 * (3 - np.e), "sd_plain": float(np.std(plain)), "sd_anti": float(np.std(anti)), "sd_ctrl": float(np.std(ctrl)),
                 "mean_plain": float(np.mean(plain)), "mean_anti": float(np.mean(anti)), "mean_ctrl": float(np.mean(ctrl)),
                 "p_true": p_true, "plain_is": plain_is[:60], "imp": imp[:60], "sd_plain_is": float(plain_is.std()),
                 "sd_imp": float(imp.std()), "zero_share": float(np.mean(plain_is == 0)), "N": N})


def compute_chain():
    P = np.array([[0.7, 0.2, 0.1], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    pi0 = np.array([1.0, 0.0, 0.0])
    flows = [pi0]
    for _ in range(12):
        flows.append(flows[-1] @ P)
    w, V = np.linalg.eig(P.T)
    st = np.real(V[:, np.argmin(np.abs(w - 1))])
    st = st / st.sum()
    # random walk on a small graph: stationary = degree / 2|E|
    edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)]
    n = 6
    A = np.zeros((n, n))
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    deg = A.sum(1)
    Q = A / deg[:, None]
    wq, Vq = np.linalg.eig(Q.T)
    sq = np.real(Vq[:, np.argmin(np.abs(wq - 1))])
    sq = sq / sq.sum()
    # PageRank: 7 pages
    links = {0: [1, 2], 1: [2], 2: [0], 3: [2, 4], 4: [5, 6, 2], 5: [2, 6], 6: [4]}
    m = 7
    L = np.zeros((m, m))
    for i, outs in links.items():
        for j in outs:
            L[i, j] = 1 / len(outs)
    G = 0.85 * L + 0.15 / m
    pr = np.ones(m) / m
    hist = [pr]
    for _ in range(40):
        pr = pr @ G
        hist.append(pr)
    return nest({"P": P, "flows": flows, "stationary": st, "eig": np.sort(np.abs(w))[::-1], "edges": edges, "deg": deg,
                 "walk_stat": sq, "links": {str(k): v for k, v in links.items()}, "pagerank": pr, "pr_hist": hist[:12]})


def eulerian_row(n: int) -> list[int]:
    """Eulerian counts; inversion preserves the counts used in forward-riffle TV.

    For a deck listed in its final order, forward-riffle rising sequences are
    descents of its inverse permutation plus one, not descents of the deck.
    """
    row = [1]
    for k in range(2, n + 1):
        new = [0] * k
        for j in range(k):
            a = row[j] if j < len(row) else 0
            b = row[j - 1] if j - 1 >= 0 else 0
            new[j] = (j + 1) * a + (k - j) * b
        row = new
    return row


def compute_shuffle():
    out = {}
    for n in (52, 5):
        A = eulerian_row(n)
        fact = 1
        for i in range(2, n + 1):
            fact *= i
        tv = []
        for k in range(1, 15):
            two = 2 ** k
            denom = two ** n
            s = Fraction(0)
            for r, a in enumerate(A, start=1):
                pk = Fraction(comb(two + n - r, n), denom)
                s += a * abs(pk - Fraction(1, fact))
            tv.append(float(s / 2))
        out[str(n)] = tv
    # simulate GSR riffle shuffles of 5 cards (120 orderings) and estimate TV against uniform, k = 1..8
    rng = np.random.Generator(np.random.PCG64(1992))
    from itertools import permutations
    perms = {p: i for i, p in enumerate(permutations(range(5)))}
    sim = []
    for k in range(1, 9):
        counts = np.zeros(len(perms))
        for _ in range(60000):
            deck = list(range(5))
            for _ in range(k):
                c = rng.binomial(5, 0.5)
                L, R = deck[:c], deck[c:]
                new = []
                while L or R:
                    if rng.random() < len(L) / (len(L) + len(R)):
                        new.append(L.pop(0))
                    else:
                        new.append(R.pop(0))
                deck = new
            counts[perms[tuple(deck)]] += 1
        sim.append(float(0.5 * np.abs(counts / 60000 - 1 / len(perms)).sum()))
    out["sim5"] = sim
    return nest(out)


def compute_metropolis():
    def logf(x):
        return np.logaddexp(np.log(0.3) - 0.5 * ((x + 2) / 0.6) ** 2 - np.log(0.6), np.log(0.7) - 0.5 * ((x - 2) / 0.9) ** 2 - np.log(0.9))
    out = {}
    for sd in (0.1, 1.5, 20.0):
        rng = np.random.Generator(np.random.PCG64(1953))
        x, xs, acc = 0.0, [], 0
        for _ in range(6000):
            y = x + sd * rng.standard_normal()
            if np.log(rng.random()) < logf(y) - logf(x):
                x, acc = y, acc + 1
            xs.append(x)
        xs = np.asarray(xs)
        out[str(sd)] = {"trace": xs[:600], "rate": acc / 6000, "hist": histogram_density(xs, np.linspace(-5, 6, 45)),
                        "mean": float(xs.mean())}
    grid = np.linspace(-5, 6, 300)
    out["grid"] = grid
    out["target"] = np.exp(logf(grid)) / np.sqrt(2 * np.pi)
    out["edges"] = np.linspace(-5, 6, 45)
    out["true_mean"] = 0.3 * -2 + 0.7 * 2
    return nest(out)


ITEMS = {
    "randu": compute_randu, "lcg": compute_lcg, "tests": compute_tests, "inverse": compute_inverse,
    "rejection": compute_rejection, "special": compute_special, "montecarlo": compute_montecarlo,
    "simstudy": compute_simstudy, "varred": compute_varred, "chain": compute_chain, "shuffle": compute_shuffle,
    "metropolis": compute_metropolis,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
