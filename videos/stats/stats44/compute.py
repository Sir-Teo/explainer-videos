"""Precompute every number in Part 44 of *Statistics, Built* ("Martingales, Markov Chains and Brownian Motion").

    OMP_NUM_THREADS=1 python -m videos.stats.stats44.compute            # everything missing (a few minutes)
    python -m videos.stats.stats44.compute --force board

Results are cached in ``.cache/stats44/<name>.json``.  Markov's *Eugene Onegin* and Gehan's 6-MP trial are the
Museum's; everything else is exact arithmetic or a seeded simulation.

Items:
    onegin      Markov's chain fitted to 20,000 letters; block counts against independence and against the chain
    borel       Borel's paradox: conditioning on a meridian vs on the equator, by simulation
    lr          likelihood-ratio paths under the null and the alternative; Ville's bound
    ruin        gambler's ruin exactly; the doubling strategy with a bounded bankroll
    urn         Polya's urn: share paths and the uniform limit
    azuma       empty bins: McDiarmid's bound against simulation
    mclt        the AR(1) least-squares estimate: the martingale CLT at phi = 0.5 and its failure near a unit root
    mcmc        a random-walk Metropolis chain: autocorrelation, batch means, the iid SE's error
    mixing      the lab: d(t) for the lazy cycle and hypercube, spectral gaps, coupling times, 52 riffled cards
    polya       random walks returning to the origin in one, two and three dimensions
    bm          the Levy-Ciesielski construction level by level; quadratic and total variation
    donsker     scaled walks, the reflection principle, the Dickey-Fuller limits
    lil         random-walk paths against the iterated-logarithm envelope
    counting    a counting process, its compensator and martingale; Nelson-Aalen on the 6-MP placebo arm
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import chains as CH

CACHE = Cache("stats44")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def eff_reps(per_rep, nominal=0.9) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    if v == 0:
        return len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


def compute_onegin():
    x = museum.onegin()
    f = CH.two_state_fit(x)
    m = 100
    blocks = x.reshape(-1, m).sum(1)
    p = f["share1"]
    var_iid = m * p * (1 - p)
    var_chain = CH.block_count_variance(p, f["r"], m)
    # the chain's own long-run variance for a block of 100, and the dispersion ratios Markov computed
    return {"n": len(x), "vowels": int(x.sum()), "counts": f["counts"], "P": f["P"], "pi1": f["pi1"], "r": f["r"],
            "share": p, "blocks": blocks, "mean_block": float(blocks.mean()), "var_block": float(blocks.var(ddof=1)),
            "var_iid": var_iid, "var_chain": var_chain, "markov": museum.MARKOV_1913, "first": x[:60]}


def compute_borel():
    g = rng(4401)
    n = 2_000_000
    z = g.uniform(-1, 1, n)  # uniform on the sphere: z = sin(latitude) uniform, longitude uniform
    lon = g.uniform(-math.pi, math.pi, n)
    lat = np.arcsin(z)
    eps = 0.01
    near_meridian = np.abs(lon) < eps  # a thin wedge: points near a great circle through the poles
    near_equator = np.abs(lat) < eps
    hm, e = np.histogram(lat[near_meridian], bins=36, range=(-math.pi / 2, math.pi / 2), density=True)
    he, e2 = np.histogram(lon[near_equator], bins=36, range=(-math.pi, math.pi), density=True)
    return {"meridian_hist": hm, "meridian_edges": e, "equator_hist": he, "equator_edges": e2,
            "n_meridian": int(near_meridian.sum()), "n_equator": int(near_equator.sum())}


def compute_lr():
    g = rng(4402)
    n, reps = 1000, 4000
    x0 = (g.random((reps, n)) < 0.5).astype(int)
    L0 = CH.betting_paths(x0, 0.5, 0.6)
    x1 = (g.random((60, n)) < 0.6).astype(int)
    L1 = CH.betting_paths(x1, 0.5, 0.6)
    kl01 = 0.5 * math.log(0.5 / 0.6) + 0.5 * math.log(0.5 / 0.4)
    kl10 = 0.6 * math.log(0.6 / 0.5) + 0.4 * math.log(0.4 / 0.5)
    cross = float(np.mean(L0.max(axis=1) >= 10))
    idx = np.unique(np.round(np.geomspace(1, n, 200)).astype(int)) - 1
    return {"n": n, "reps": reps, "log0": np.log(L0[:40, idx]), "log1": np.log(L1[:20, idx]), "idx": idx + 1,
            "cross10": cross, "final_below_1": float(np.mean(L0[:, -1] < 1)), "kl_null": kl01, "kl_alt": kl10,
            "median_final0": float(np.median(L0[:, -1])), "mean_final0_20": float(L0[:, 19].mean())}


def compute_ruin():
    rows = []
    for p, nm in [(0.5, "fair"), (18 / 38, "roulette")]:
        for a, b in [(10, 20), (50, 100), (100, 200)]:
            r = CH.ruin(p, a, b)
            rows.append({"p": p, "name": nm, "a": a, "b": b, "win": r["win"], "duration": r["duration"]})
    q = 20 / 38
    k = 10
    lose_all = q ** k
    ev_fair = (1 - 0.5 ** k) - (2 ** k - 1) * 0.5 ** k
    ev_roul = (1 - lose_all) - (2 ** k - 1) * lose_all
    g = rng(4403)
    # the doubling gambler with unlimited credit: the stake needed before the first win
    first = g.geometric(0.5, 200_000)
    need = 2.0 ** first - 1
    return {"rows": rows, "k": k, "bank": 2 ** k - 1, "lose_all_roulette": lose_all, "lose_all_fair": 0.5 ** k,
            "ev_fair": ev_fair, "ev_roulette": ev_roul, "mean_need": float(need.mean()), "median_need": float(np.median(need)),
            "max_need": float(need.max())}


def compute_urn():
    g = rng(4404)
    paths = CH.polya_urn(2000, 24, g)
    limits = CH.polya_urn(600, 2000, g)[:, -1]
    h, e = np.histogram(limits, bins=20, range=(0, 1), density=True)
    return {"paths": paths[:, ::5], "steps": np.arange(1, 2001)[::5], "hist": h, "edges": e,
            "ks_p": float(stats.kstest(limits, "uniform").pvalue)}


def compute_azuma():
    g = rng(4405)
    n, reps = 1000, 20_000
    Z = np.empty(reps)
    for r in range(reps):
        Z[r] = n - np.unique(g.integers(0, n, n)).size
    mean = n * (1 - 1 / n) ** n
    ts = np.arange(5, 61, 5)
    emp = [float(np.mean(np.abs(Z - mean) >= t)) for t in ts]
    bound = [CH.mcdiarmid(t, np.ones(n)) for t in ts]
    return {"n": n, "mean_theory": mean, "mean": float(Z.mean()), "sd": float(Z.std()), "ts": ts, "emp": emp, "bound": bound,
            "hist": np.histogram(Z, bins=40, range=(mean - 40, mean + 40))[0], "lo": mean - 40, "hi": mean + 40}


def ar1_paths(phi, n, reps, g):
    e = g.standard_normal((reps, n + 1))
    y = np.zeros((reps, n + 1))
    for i in range(1, n + 1):
        y[:, i] = phi * y[:, i - 1] + e[:, i]
    return y


def ar1_fit_many(y):
    """Least squares for y_t = c + phi y_{t-1} + e_t, as practice fits it (with an intercept), for each row."""
    a, b = y[:, :-1], y[:, 1:]
    ac = a - a.mean(1, keepdims=True)
    bc = b - b.mean(1, keepdims=True)
    phi = np.sum(ac * bc, 1) / np.sum(ac * ac, 1)
    r = bc - phi[:, None] * ac
    s2 = np.sum(r * r, 1) / (y.shape[1] - 3)
    return phi, np.sqrt(s2 / np.sum(ac * ac, 1))


def compute_mclt():
    g = rng(4406)
    out = {}
    for phi, n in [(0.5, 200), (0.98, 100)]:
        y = ar1_paths(phi, n, 20_000, g)
        ph, se = ar1_fit_many(y)
        z = np.sqrt(n) * (ph - phi) / math.sqrt(1 - phi ** 2)
        h, e = np.histogram(z, bins=50, range=(-5, 3), density=True)
        out[str(phi)] = {"n": n, "hist": h, "edges": e, "mean": float(ph.mean()), "skew": float(stats.skew(z)),
                         "cover": float(np.mean(np.abs(ph - phi) <= 1.645 * se))}
    return out


def compute_mcmc():
    g = rng(4407)
    x = CH.rwm_normal(200_000, 0.5, g)
    acf = [1.0] + [float(np.corrcoef(x[:-k], x[k:])[0, 1]) for k in range(1, 61)]
    tau = 1 + 2 * sum(a for a in acf[1:] if a > 0)
    se_iid = float(x.std() / math.sqrt(len(x)))
    return {"trace": x[:2000], "acf": acf, "tau": tau, "se_iid": se_iid, "se_bm": CH.batch_means_se(x, 50),
            "se_tau": se_iid * math.sqrt(tau), "accept": float(np.mean(np.diff(x) != 0))}


def compute_mixing():
    n = 20
    P = CH.lazy_cycle(n)
    pi = np.full(n, 1 / n)
    ts = np.arange(0, 401, 4)
    dc = CH.distance_curve(P, pi, ts, starts=[0])
    hyper = {}
    for d in (10, 40):
        H = CH.lazy_hypercube_weight(d)
        pih = stats.binom.pmf(np.arange(d + 1), d, 0.5)
        tt = np.arange(0, 6 * d + 1)
        hyper[str(d)] = {"t": tt, "d": CH.distance_curve(H, pih, tt, starts=[0]), "tmix": CH.mixing_time(H, pih, starts=[0]),
                         "gap": CH.spectral_gap(H)}
    g = rng(4408)
    ct = CH.coupling_time_cycle(n, 4000, g)
    tail = [float(np.mean(ct > t)) for t in ts]
    riffle = [CH.riffle_tv(52, k) for k in range(1, 11)]
    return {"n": n, "ts": ts, "d_cycle": dc, "tmix_cycle": CH.mixing_time(P, pi, starts=[0]), "gap_cycle": CH.spectral_gap(P),
            "relax_cycle": 1 / CH.spectral_gap(P), "coupling_tail": tail, "coupling_mean": float(ct.mean()), "hyper": hyper,
            "riffle": riffle}


def compute_polya():
    g = rng(4409)
    steps = [10, 100, 1000, 10_000]
    out = {}
    for d in (1, 2, 3):
        out[str(d)] = [CH.polya_return(d, s, 800 if s < 10_000 else 300, g) for s in steps]
    return {"steps": steps, "ret": out, "polya3": 0.3405}


def compute_bm():
    g = rng(4410)
    t = np.linspace(0, 1, 2 ** 10 + 1)
    paths = CH.levy_ciesielski(10, t, g)
    keep = [0, 1, 2, 3, 5, 10]
    qv = []
    for lev in range(2, 11):
        step = 2 ** (10 - lev)
        sub = paths[-1][::step]
        q = CH.quadratic_variation(sub)
        qv.append({"level": lev, "pieces": 2 ** lev, "qv": q["qv"], "tv": q["tv"]})
    # a finer path for the quadratic variation at high resolution
    tt = np.linspace(0, 1, 2 ** 16 + 1)
    fine = np.concatenate([[0], np.cumsum(g.standard_normal(2 ** 16) / math.sqrt(2 ** 16))])
    qfine = [{"pieces": 2 ** k, **CH.quadratic_variation(fine[:: 2 ** (16 - k)])} for k in range(4, 17, 2)]
    return {"t": t, "levels": {str(k): paths[k] for k in keep}, "qv": qv, "qfine": qfine}


def compute_donsker():
    g = rng(4411)
    walks = {}
    for n in (10, 100, 1000):
        s = np.concatenate([[0], np.cumsum(g.choice((-1.0, 1.0), n))]) / math.sqrt(n)
        walks[str(n)] = {"t": np.linspace(0, 1, n + 1), "s": s}
    n, reps = 1000, 20_000
    steps = g.choice((-1, 1), size=(reps, n)).astype(np.int8)
    S = np.cumsum(steps, axis=1, dtype=np.int32)
    mx = S.max(axis=1) / math.sqrt(n)
    xs = np.linspace(0, 3, 61)
    emp = [float(np.mean(mx >= v)) for v in xs]
    refl = [float(2 * stats.norm.sf(v)) for v in xs]
    df = CH.dickey_fuller(250, 20_000, g)
    df_big = CH.dickey_fuller(2000, 4000, g)
    return {"walks": walks, "xs": xs, "max_emp": emp, "max_refl": refl,
            "df_t_hist": np.histogram(df["t"], bins=50, range=(-4.5, 3), density=True)[0],
            "df_t_q05": float(np.quantile(df["t"], 0.05)), "df_t_q05_big": float(np.quantile(df_big["t"], 0.05)),
            "df_rho_q05": float(np.quantile(df["n_rho"], 0.05)), "df_t_mean": float(df["t"].mean()),
            "df_t_frac_neg": float(np.mean(df["t"] < 0))}


def compute_lil():
    g = rng(4412)
    n = 1_000_000
    idx = np.unique(np.round(np.geomspace(3, n, 400)).astype(int)) - 1
    paths = []
    ratios = []
    for _ in range(6):
        s = np.cumsum(g.choice((-1, 1), n).astype(np.int8), dtype=np.int64)
        paths.append(s[idx])
        late = slice(1000, n)
        ratios.append(float(np.max(np.abs(s[late]) / CH.lil_envelope(np.arange(1001, n + 1)))))
    return {"idx": idx + 1, "paths": paths, "env": CH.lil_envelope(idx + 1), "clt": 1.645 * np.sqrt(idx + 1), "ratios": ratios}


def compute_counting():
    g = rng(4413)
    n = 200
    T = g.exponential(1.0, n)
    C = g.uniform(0, 2.5, n)
    time, event = np.minimum(T, C), (T <= C).astype(int)
    grid = np.linspace(0, 2.5, 501)
    N = np.array([np.sum((time <= s) & (event == 1)) for s in grid])
    # compensator with the true hazard 1: integral of the number at risk
    Lam = np.array([np.sum(np.minimum(time, s)) for s in grid])
    M = N - Lam
    G = museum.gehan()
    t0, e0 = G["time"][G["group"] == 0], G["event"][G["group"] == 0]
    ut = np.unique(t0[e0 == 1])
    na, var = [], []
    h, v = 0.0, 0.0
    for u in ut:
        at_risk = np.sum(t0 >= u)
        d = np.sum((t0 == u) & (e0 == 1))
        h += d / at_risk
        v += d / at_risk ** 2
        na.append(h)
        var.append(v)
    return {"grid": grid, "N": N, "Lam": Lam, "M": M, "events": int(event.sum()), "n": n, "na_t": ut, "na": na,
            "na_se": np.sqrt(var)}


def compute_board():
    rows = []
    g = rng(4414)
    for phi, n, st in [(0.5, 200, "phi = 0.5, n = 200"), (0.98, 100, "phi = 0.98, n = 100")]:
        y = ar1_paths(phi, n, 20_000, g)
        ph, se = ar1_fit_many(y)
        cov = np.abs(ph - phi) <= 1.645 * se
        rows.append(Row(44, "AR(1) least squares (with intercept)", st, "coverage", 0.9, float(cov.mean()), eff_reps(cov)))
    # MCMC: the mean of N(0, 1) from 20,000 RWM steps, batch means against the iid formula
    reps = 600
    c_bm, c_iid = [], []
    for _ in range(reps):
        x = CH.rwm_normal(20_000, 0.5, g, x0=g.standard_normal())
        m = x.mean()
        c_bm.append(abs(m) <= 1.645 * CH.batch_means_se(x, 30))
        c_iid.append(abs(m) <= 1.645 * x.std() / math.sqrt(len(x)))
    rows.append(Row(44, "MCMC mean, batch-means SE", "RWM on N(0, 1), 20,000 steps", "coverage", 0.9, float(np.mean(c_bm)), eff_reps(c_bm)))
    rows.append(Row(44, "MCMC mean, i.i.d. SE", "RWM on N(0, 1), 20,000 steps", "coverage", 0.9, float(np.mean(c_iid)), eff_reps(c_iid)))
    # testing a fair coin while watching: betting (Ville) against peeking at a z test, up to 1,000 tosses
    reps, n = 4000, 1000
    x = (g.random((reps, n)) < 0.5).astype(int)
    L = CH.betting_paths(x, 0.5, 0.6)
    L2 = CH.betting_paths(x, 0.5, 0.4)
    wealth = 0.5 * (L + L2)  # bet on both sides: still a nonnegative martingale with mean one
    ok_bet = ~(wealth.max(axis=1) >= 10)
    k = np.arange(1, n + 1)
    zstat = (np.cumsum(x, axis=1) - 0.5 * k) / np.sqrt(0.25 * k)
    looks = np.arange(9, n, 10)  # look every 10 tosses
    ok_peek = ~(np.abs(zstat[:, looks]) >= 1.645).any(axis=1)
    rows.append(Row(44, "betting test, reject at wealth 10", "a fair coin watched for 1,000 tosses", "size", 0.1,
                    float(1 - ok_bet.mean()), len(ok_bet)))
    rows.append(Row(44, "z test at every 10th toss", "a fair coin watched for 1,000 tosses", "size", 0.1,
                    float(1 - ok_peek.mean()), len(ok_peek)))
    save_rows(44, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "onegin": compute_onegin, "borel": compute_borel, "lr": compute_lr, "ruin": compute_ruin, "urn": compute_urn,
    "azuma": compute_azuma, "mclt": compute_mclt, "mcmc": compute_mcmc, "mixing": compute_mixing, "polya": compute_polya,
    "bm": compute_bm, "donsker": compute_donsker, "lil": compute_lil, "counting": compute_counting, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
