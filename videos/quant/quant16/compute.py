"""Every number in Part 16 (Computing Prices), computed and cached in .cache/quant16/.

    python -m videos.quant.quant16.compute [items] [--force]

Items (seconds to a few minutes each on a CPU):

* ``mc``        Monte Carlo error against paths for a European call: plain, antithetic, control variate, Sobol; and
                importance sampling for a deep out-of-the-money call;
* ``qmc``       an arithmetic Asian by pseudo-random, Sobol and Sobol with the Brownian bridge: spread over 20
                scrambles at each size; the first two coordinates of random and Sobol points;
* ``mlmc``      multilevel against standard Monte Carlo (Euler paths) for a continuously averaged Asian: cost against
                accuracy, and the variance by level;
* ``american``  the American put: Longstaff-Schwartz's lower bound, Andersen-Broadie's upper bound by inner sample
                size, a 2,000-step tree and the PSOR finite-difference price;
* ``greeks``    delta and vega by bumps, pathwise and likelihood ratio, for a call and a digital; adjoint
                differentiation's cost against bumping, by the number of Greeks;
* ``fd``        explicit, implicit, Crank-Nicolson and Rannacher: error against grid, the explicit scheme's instability,
                and the digital's gamma oscillation near expiry;
* ``adi``       Heston by Douglas and Craig-Sneyd ADI against the COS price, by grid;
* ``fourier``   Carr-Madan's FFT against COS for Heston: error against the number of terms and time;
* ``race``      one problem (the Heston call), every method: error against wall-clock time;
* ``envelope``  registers nothing (no strategy is tested); the counter.

Added with the expansion (hook + nineteen chapters; the items above are unchanged):

* ``mc_live`` the running estimate and its 95% band to 10^6 paths, and the band's coverage over 1,000 seeds;
* ``rng`` inverse transform and Box-Muller normals (KS), a counter-based stream out of order, a Python loop's cost;
* ``control`` Kemna-Vorst's geometric control, the stock as control, antithetics, strata, Latin hypercubes;
* ``is_sweep`` importance sampling's variance and effective sample size against the shift; cross-entropy;
* ``discrepancy`` L2-star discrepancy for random, Halton and Sobol points; the net property; scrambled error bars;
* ``effdim`` step, bridge and principal-component constructions: the variance per coordinate; QMC with PCA;
* ``mlmc_trace`` / ``mlmc_milstein`` the adaptive multilevel loop logged; Euler against Milstein;
* ``lsm_live`` / ``bermudan_ref`` / ``maxcall`` / ``dual_path`` Longstaff-Schwartz recorded date by date, a true
  Bermudan reference, the five-asset max-call against Part 17, one traced outer path of the dual;
* ``bump_h`` / ``aad_scale`` the bump's error over (h, n); adjoint against bumping as the inputs grow;
* ``fd_live`` / ``lcp`` / ``adi_grid`` the explicit march, the American LCP by PSOR and by penalty, ADI grids;
* ``lewis`` / ``cos_density`` / ``race_cv`` Lewis against COS, COS's density by cosines, Monte Carlo with a control;
* ``parallel`` / ``qae`` / ``cheb`` / ``rqmc_median`` the machine, amplitude estimation, a Chebyshev pricer, RQMC.

Wall-clock numbers (``race``, ``aad_scale``, ``parallel``, ``lcp``, ``cheb``) are best-of-N on one core of a shared
machine, and are paired with machine-independent counts where the narration compares them.
"""

from __future__ import annotations

import time

import numpy as np
from scipy.stats import norm, qmc

from explainer.ai.cache import Cache
from explainer.quant.house import bs, engine as E, pit, stochvol as sv, trees

CACHE = Cache("quant16")
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 16)  # the series' trial counter as of this part

S0, K, T, SIG, R = 100.0, 100.0, 1.0, 0.2, 0.05
HES = (0.04, 1.5, 0.04, 0.5, -0.7)  # v0, kappa, theta, xi, rho


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _heston_ref():
    cf = lambda u, TT: sv.heston_cf(u, TT, *HES)  # noqa: E731
    return float(sv.cos_price(cf, S0, K, T, 1, N=4096, L=40)[0])


# ---------------------------------------------------------------------------
def compute_mc() -> dict:
    ex = float(bs.price(S0, K, T, SIG, R))
    ns = [1024, 4096, 16384, 65536, 262144]
    rows = {m: [] for m in ("plain", "antithetic", "control", "sobol")}
    for n in ns:
        for m in ("plain", "antithetic", "control"):
            errs = [E.mc_call(S0, K, T, SIG, R, n, m, seed=s)[0] - ex for s in range(20)]
            rows[m].append(float(np.sqrt(np.mean(np.square(errs)))))
        errs = []
        for s in range(20):
            z = E.normals(n, 1, "sobol", seed=s)[:, 0]
            ST = S0 * np.exp((R - 0.5 * SIG ** 2) * T + SIG * np.sqrt(T) * z)
            errs.append(np.exp(-R * T) * np.maximum(ST - K, 0).mean() - ex)
        rows["sobol"].append(float(np.sqrt(np.mean(np.square(errs)))))
    K2 = 160.0
    ex2 = float(bs.price(S0, K2, T, SIG, R))
    pl = [E.mc_call(S0, K2, T, SIG, R, 100000, "plain", seed=s) for s in range(5)]
    im = [E.mc_call(S0, K2, T, SIG, R, 100000, "is", seed=s) for s in range(5)]
    return _json({"exact": ex, "ns": ns, "rmse": rows, "deep": {"K": K2, "exact": ex2,
                  "plain_se": float(np.mean([p[1] for p in pl])), "is_se": float(np.mean([p[1] for p in im])),
                  "share_in_money": float(norm.cdf(bs.d1_d2(S0, K2, T, SIG, R)[1]))}})


def compute_qmc() -> dict:
    ns = [256, 1024, 4096, 16384]
    out = {}
    for name, kind, br in (("pseudo-random", "mc", False), ("Sobol", "sobol", False), ("Sobol + bridge", "sobol", True)):
        sd = []
        for n in ns:
            v = [E.asian_call_paths(S0, K, T, SIG, R, n, 64, kind, br, seed=s) for s in range(20)]
            sd.append(float(np.std(v)))
        out[name] = sd
    rand = np.random.default_rng(1).random((256, 2))
    sob = qmc.Sobol(d=2, scramble=True, seed=1).random(256)
    return _json({"ns": ns, "sd": out, "rand": rand, "sobol": sob})


def compute_mlmc() -> dict:
    eps = [0.04, 0.02, 0.01]
    ref = E.mlmc(0.003, S0, K, T, SIG, R, seed=11)["estimate"]  # one tight reference for every target
    ml, st = [], []
    g = np.random.default_rng(4)
    for e in eps:
        m = E.mlmc(e, S0, K, T, SIG, R, seed=3)
        ml.append(m)
        # the standard estimator at the same finest step (Giles's comparison): N = 2 var(P_L) / eps^2 paths of 2^L steps
        n = 2 ** m["levels"]
        P = E._plain_euler(n, 20000, S0, K, T, SIG, R, g)
        N = int(np.ceil(2 * P.var() / e ** 2))
        st.append({"steps": n, "N": N, "cost": float(N * n)})
    return _json({"eps": eps, "mlmc": ml, "standard": st, "ref": ref})


def compute_american() -> dict:
    tree = trees.crr(S0, K, T, SIG, R, q=0.0, N=2000, cp=-1, american=True)["price"]
    fd = E.fd_american_put(S0, K, T, SIG, R, nS=300, nt=300)
    euro = float(bs.price(S0, K, T, SIG, R, cp=-1))
    lo, coefs = E.lsm_put(S0, K, T, SIG, R, 25, 200000, seed=1, return_policy=True)
    tree25 = trees.crr(S0, K, T, SIG, R, q=0.0, N=25, cp=-1, american=True)["price"]
    ab = []
    for ni in (50, 200, 800, 1600):
        hi, se = E.andersen_broadie_put(S0, K, T, SIG, R, coefs, n_steps=25, n_outer=400, n_inner=ni, seed=2)
        ab.append({"inner": ni, "upper": hi, "se": se})
    return _json({"tree2000": float(tree), "fd": fd, "european": euro, "lsm": lo, "bermudan_tree25": float(tree25),
                  "ab": ab})


def compute_greeks() -> dict:
    out = {"call": E.greeks_three_ways(S0, K, T, SIG, R, 200000), "digital": E.greeks_three_ways(S0, K, T, SIG, R, 200000,
                                                                                                 payoff="digital")}
    d1, d2 = bs.d1_d2(S0, K, T, SIG, R)
    out["exact"] = {"call": {"delta": float(norm.cdf(d1)), "vega": float(S0 * norm.pdf(d1) * np.sqrt(T))},
                    "digital": {"delta": float(np.exp(-R * T) * norm.pdf(d2) / (S0 * SIG * np.sqrt(T))),
                                "vega": float(-np.exp(-R * T) * norm.pdf(d2) * d1 / SIG)}}
    reps = [E.aad_greeks(S0, K, T, SIG, R, 20000, 50, seed=s) for s in range(5)]
    out["aad"] = reps[0]
    out["aad_ratio"] = float(np.median([r["t_aad"] / r["t_price"] for r in reps]))
    out["bump_ratio"] = float(np.median([r["t_bump"] / r["t_price"] for r in reps]))
    out["n_greeks"] = len(reps[0]["aad"])
    return _json(out)


def compute_fd() -> dict:
    ex = float(bs.price(S0, K, T, SIG, R))
    grids = [25, 50, 100, 200, 400]
    rows = {"implicit": [], "cn": [], "cn+rannacher": []}
    for n in grids:
        rows["implicit"].append(abs(E.fd_european(S0, K, T, SIG, R, nS=n, nt=n, scheme="implicit")[0] - ex))
        rows["cn"].append(abs(E.fd_european(S0, K, T, SIG, R, nS=n, nt=n, scheme="cn")[0] - ex))
        rows["cn+rannacher"].append(abs(E.fd_european(S0, K, T, SIG, R, nS=n, nt=n, scheme="cn", rannacher=2)[0] - ex))
    # explicit: stable only if dt < dS^2 / (sigma^2 S_max^2)
    nS = 100
    stab = {}
    for nt in (2000, 200):
        try:
            p = E.fd_european(S0, K, T, SIG, R, nS=nS, nt=nt, scheme="explicit")[0]
        except Exception:
            p = float("nan")
        stab[str(nt)] = p
    dS = 4 * K / nS
    nt_min = float(T * (SIG * 4 * K) ** 2 / dS ** 2)
    # the digital's gamma a short time before expiry: CN rings, Rannacher does not
    Tg = 0.02
    out_g = {}
    for name, rn in (("cn", 0), ("cn+rannacher", 2)):
        # a fine price grid and large time steps (sigma^2 S^2 dt / dS^2 >> 1), as desks run near expiry: CN rings
        _, S, V = E.fd_european(S0, K, Tg, SIG, R, nS=800, nt=4, scheme="cn", payoff="digital", rannacher=rn)
        g = np.gradient(np.gradient(V, S), S)
        m = (S > 85) & (S < 115)
        out_g[name] = {"S": S[m], "gamma": g[m]}
    d1, d2 = bs.d1_d2(S[m], K, Tg, SIG, R)
    exact_g = -np.exp(-R * Tg) * norm.pdf(d2) * d1 / (S[m] ** 2 * SIG ** 2 * Tg)
    return _json({"exact": ex, "grids": grids, "errors": rows, "explicit": stab, "explicit_nt_min": nt_min,
                  "gamma": out_g, "gamma_exact": exact_g, "gamma_S": S[m]})


def compute_adi() -> dict:
    ref = _heston_ref()
    rows = []
    for nS, nv in ((20, 10), (40, 20), (80, 40), (160, 80)):
        for sch in ("do", "cs"):
            t0 = time.perf_counter()
            p = E.heston_adi(S0, K, T, *HES, r=0.0, nS=nS, nv=nv, nt=nS // 2, scheme=sch)
            rows.append({"nS": nS, "nv": nv, "scheme": sch, "price": p, "err": abs(p - ref), "time": time.perf_counter() - t0})
    return _json({"ref": ref, "rows": rows})


def compute_fourier() -> dict:
    ref = _heston_ref()
    cf = lambda u, TT: sv.heston_cf(u, TT, *HES)  # noqa: E731
    rows = []
    # L = 16: the strongly negative correlation gives a fat left tail, and L = 12 truncates it at about 1e-5
    for N in (16, 32, 64, 128, 256, 512):
        t0 = time.perf_counter()
        p = float(sv.cos_price(cf, S0, K, T, 1, N=N, L=16)[0])
        rows.append({"method": "COS", "N": N, "err": abs(p - ref), "time": time.perf_counter() - t0})
    for N in (512, 1024, 4096, 16384):
        t0 = time.perf_counter()
        kk, C = E.carr_madan(cf, S0, T, 0.0, N=N, eta=0.25)
        p = float(np.interp(K, kk, C))
        rows.append({"method": "Carr-Madan", "N": N, "err": abs(p - ref), "time": time.perf_counter() - t0})
    return _json({"ref": ref, "rows": rows})


def compute_race() -> dict:
    """The Heston call (r = 0): every method's error against its wall-clock time."""
    ref = _heston_ref()
    cf = lambda u, TT: sv.heston_cf(u, TT, *HES)  # noqa: E731
    pts = []

    def add(method, f):
        # best of several runs, so a fast method is not charged for one-off warm-up
        best = np.inf
        for _ in range(5):
            t0 = time.perf_counter()
            p = f()
            best = min(best, time.perf_counter() - t0)
            if best > 0.2:
                break
        pts.append({"method": method, "err": abs(p - ref), "time": best})

    for n in (5000, 20000, 80000, 320000):
        t0 = time.perf_counter()
        pay = np.maximum(sv.heston_qe(S0, *HES, T, 50, n, seed=n)[-1] - K, 0)
        # Monte Carlo's error is random; report its expected size, the standard error
        pts.append({"method": "Monte Carlo (QE, 50 steps)", "err": float(pay.std() / np.sqrt(n)),
                    "time": time.perf_counter() - t0, "actual": float(abs(pay.mean() - ref))})
    for nS in (20, 40, 80, 160):
        add("ADI (Craig-Sneyd)", lambda nS=nS: E.heston_adi(S0, K, T, *HES, r=0.0, nS=nS, nv=nS // 2, nt=nS // 2))
    for N in (64, 128, 256):
        add("COS", lambda N=N: float(sv.cos_price(cf, S0, K, T, 1, N=N, L=16)[0]))
    for N in (1024, 4096, 16384):
        add("Carr-Madan FFT", lambda N=N: float(np.interp(K, *E.carr_madan(cf, S0, T, 0.0, N=N, eta=0.25))))
    return _json({"ref": ref, "points": pts})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


# ---------------------------------------------------------------------------
# The expansion (hook + nineteen chapters): new items. The items above are unchanged.


def _bs_pay(z, K=K):
    return np.exp(-R * T) * np.maximum(S0 * np.exp((R - 0.5 * SIG ** 2) * T + SIG * np.sqrt(T) * z) - K, 0)


def compute_mc_live() -> dict:
    """Ch 1: the running estimate and its 95% band for three seeds to a million paths; the band's coverage."""
    ex = float(bs.price(S0, K, T, SIG, R))
    n = 1_000_000
    ck = np.unique(np.round(np.logspace(1, 6, 200)).astype(int))
    runs = []
    for seed in range(3):
        y = _bs_pay(np.random.default_rng(100 + seed).standard_normal(n))
        cs, cs2 = np.cumsum(y), np.cumsum(y * y)
        m = cs[ck - 1] / ck
        sd = np.sqrt(np.maximum(cs2[ck - 1] / ck - m * m, 0))
        runs.append({"mean": m, "se": sd / np.sqrt(ck), "first": y[:300]})
    sdY = float(np.std(_bs_pay(np.random.default_rng(99).standard_normal(n))))
    # coverage of mean +- 1.96 s/sqrt(n) at n = 10^4 over 1,000 seeds
    g = np.random.default_rng(7)
    hit = 0
    for _ in range(10):
        y = _bs_pay(g.standard_normal((100, 10_000)))
        m, s = y.mean(1), y.std(1, ddof=1) / 100
        hit += int(np.sum(np.abs(m - ex) <= 1.96 * s))
    return _json({"exact": ex, "ck": ck, "runs": runs, "sd": sdY, "coverage": hit / 1000, "cover_n": 10_000,
                  "cover_seeds": 1000, "cent_paths": (1.96 * sdY / 0.01) ** 2, "cent_paths_1se": (sdY / 0.01) ** 2})


def compute_rng() -> dict:
    """Ch 2: normals by inverse transform and by Box-Muller (Kolmogorov-Smirnov), a counter-based stream reproduced
    out of order, and the price of a Python loop."""
    from scipy.stats import kstest
    from scipy.special import ndtri
    g = np.random.default_rng(11)
    u = g.random(1_000_000)
    z_inv = ndtri(u)
    u1, u2 = g.random(500_000), g.random(500_000)
    rr = np.sqrt(-2 * np.log(u1))
    z_bm = np.concatenate([rr * np.cos(2 * np.pi * u2), rr * np.sin(2 * np.pi * u2)])
    ks_inv, ks_bm = kstest(z_inv, "norm"), kstest(z_bm, "norm")

    # counter-based: path j's normals are a pure function of (key, j); compute in any order, same bits
    def path(j):
        return np.random.Generator(np.random.Philox(key=[2026, j])).standard_normal(64)

    fwd = np.stack([path(j) for j in range(1000)])
    order = np.random.default_rng(3).permutation(1000)
    shuf = np.empty_like(fwd)
    for j in order:
        shuf[j] = path(j)
    same = bool(np.array_equal(fwd, shuf))
    # a sequential stream: the same draw count, but path 7's numbers depend on how many came before
    seq = np.random.default_rng(5).standard_normal((1000, 64))
    alone = np.random.default_rng(5).standard_normal(64)
    seq_same = bool(np.array_equal(seq[7], alone))

    zz = np.random.default_rng(0).standard_normal(100_000)

    def loop():
        s = 0.0
        for x in zz:
            s += max(100 * np.exp(0.03 + 0.2 * x) - 100, 0.0)
        return s

    def vec():
        return float(np.maximum(100 * np.exp(0.03 + 0.2 * zz) - 100, 0).sum())

    def best(f, k):
        b = np.inf
        for _ in range(k):
            t0 = time.perf_counter()
            f()
            b = min(b, time.perf_counter() - t0)
        return b

    tl, tv = best(loop, 3), best(vec, 20)
    rho = -0.7
    Lc = np.linalg.cholesky(np.array([[1, rho], [rho, 1]]))
    return _json({"ks_inv": float(ks_inv.statistic), "ks_inv_p": float(ks_inv.pvalue), "ks_bm": float(ks_bm.statistic),
                  "ks_bm_p": float(ks_bm.pvalue), "n": 1_000_000, "philox_same": same, "seq_same": seq_same,
                  "t_loop": tl, "t_vec": tv, "speedup": tl / tv, "chol": Lc, "rho": rho})


def compute_control() -> dict:
    """Ch 3: Kemna-Vorst's geometric control for the arithmetic Asian, the stock as a control, antithetics,
    stratification and Latin hypercubes."""
    out = {"geo": [], "stock": []}
    for s in range(5):
        out["geo"].append(E.asian_control(S0, K, T, SIG, R, 20000, 64, seed=s))
        out["stock"].append(E.asian_control(S0, K, T, SIG, R, 20000, 64, seed=s, control="stock"))
    summ = {k: {"rho": float(np.mean([x["rho"] for x in v])), "ratio": float(np.mean([x["ratio"] for x in v])),
                "b": float(np.mean([x["b"] for x in v])), "price": float(np.mean([x["price"] for x in v])),
                "se": float(np.mean([x["se"] for x in v]))} for k, v in out.items()}
    # the scatter: 2,000 (control, payoff) pairs
    g = np.random.default_rng(1)
    dt = T / 64
    t = dt * np.arange(1, 65)
    W = np.cumsum(np.sqrt(dt) * g.standard_normal((2000, 64)), axis=1)
    S = S0 * np.exp((R - 0.5 * SIG ** 2) * t + SIG * W)
    Y = np.exp(-R * T) * np.maximum(S.mean(1) - K, 0)
    Cg = np.exp(-R * T) * np.maximum(np.exp(np.log(S).mean(1)) - K, 0)
    Cs = np.exp(-R * T) * S[:, -1]
    # antithetics: corr(f(Z), f(-Z)) for the call, the straddle, and the gain at equal work 1/(1 + rho)
    z = np.random.default_rng(2).standard_normal(400_000)
    call = lambda zz: _bs_pay(zz)  # noqa: E731
    strad = lambda zz: np.exp(-R * T) * np.abs(S0 * np.exp((R - 0.5 * SIG ** 2) * T + SIG * np.sqrt(T) * zz) - K)  # noqa
    rho_c = float(np.corrcoef(call(z), call(-z))[0, 1])
    rho_s = float(np.corrcoef(strad(z), strad(-z))[0, 1])
    # stratification of the terminal normal: variance ratio against plain at equal paths, 200 repeats of n = 4,096
    n = 4096
    plain = [E.mc_call(S0, K, T, SIG, R, n, seed=1000 + s)[0] for s in range(200)]
    st16 = [E.stratified_call(S0, K, T, SIG, R, n, 16, seed=2000 + s)[0] for s in range(200)]
    st256 = [E.stratified_call(S0, K, T, SIG, R, n, 256, seed=3000 + s)[0] for s in range(200)]
    # small samples for the picture: 500 repeats with n = 64, plain against 16 strata
    sm_plain = [E.mc_call(S0, K, T, SIG, R, 64, seed=5000 + s)[0] for s in range(500)]
    sm_st = [E.stratified_call(S0, K, T, SIG, R, 64, 16, seed=6000 + s)[0] for s in range(500)]
    # Latin hypercube on the 64-dimensional Asian: 100 repeats of n = 1,024
    from scipy.special import ndtri

    def asian_from_u(u):
        W_ = np.cumsum(np.sqrt(dt) * ndtri(u), axis=1)
        S_ = S0 * np.exp((R - 0.5 * SIG ** 2) * t + SIG * W_)
        return float(np.exp(-R * T) * np.maximum(S_.mean(1) - K, 0).mean())

    lhs = [asian_from_u(qmc.LatinHypercube(d=64, seed=7000 + s).random(1024)) for s in range(100)]
    mcs = [asian_from_u(np.random.default_rng(8000 + s).random((1024, 64))) for s in range(100)]
    return _json({"summary": summ, "geo_exact": E.geometric_asian_call(S0, K, T, SIG, R, 64),
                  "scatter": {"Y": Y, "Cg": Cg, "Cs": Cs}, "anti": {"call": rho_c, "straddle": rho_s},
                  "strat": {"n": n, "plain_sd": float(np.std(plain)), "s16_sd": float(np.std(st16)),
                            "s256_sd": float(np.std(st256))},
                  "strat_small": {"plain": sm_plain, "strat": sm_st, "exact": float(bs.price(S0, K, T, SIG, R))},
                  "lhs": {"lhs_sd": float(np.std(lhs)), "mc_sd": float(np.std(mcs)), "n": 1024}})


def compute_is_sweep() -> dict:
    """Ch 4: importance sampling's variance against the shift, the effective sample size, cross-entropy's iterates."""
    K2 = 160.0
    drift, vol = (R - 0.5 * SIG ** 2) * T, SIG * np.sqrt(T)
    z = np.random.default_rng(3).standard_normal(400_000)
    f = lambda zz: np.exp(-R * T) * np.maximum(S0 * np.exp(drift + vol * zz) - K2, 0)  # noqa: E731
    th = np.round(np.linspace(0, 7, 141), 4)
    var, ess, mean = [], [], []
    for t_ in th:
        zz = z + t_
        w = np.exp(-t_ * zz + 0.5 * t_ * t_)
        y = f(zz) * w
        var.append(float(y.var()))
        mean.append(float(y.mean()))
        ess.append(float(w.sum() ** 2 / (w * w).sum() / len(w)))
    var = np.array(var)
    ratio = var[0] / var
    star = float((np.log(K2 / S0) - drift) / vol)
    i_star = int(np.argmin(np.abs(th - star)))
    ce = [E.is_cross_entropy(lambda zz: f(zz), 0.0, 20000, 4, seed=s) for s in range(5)]
    hist = {}
    for t_ in (0.0, 2.75, 6.0):
        zz = z[:20000] + t_
        w = np.exp(-t_ * zz + 0.5 * t_ * t_)
        y = f(zz) * w
        hist[str(t_)] = {"y": y[y > 0][:3000], "share_zero": float(np.mean(y == 0))}
    return _json({"K": K2, "theta": th, "ratio": ratio, "ess": ess, "mean": mean, "exact": float(bs.price(S0, K2, T, SIG, R)),
                  "theta_strike": star, "ratio_strike": float(ratio[i_star]), "theta_best": float(th[np.argmax(ratio)]),
                  "ratio_best": float(ratio.max()), "ratio_5": float(ratio[np.argmin(np.abs(th - 5))]),
                  "ce": ce, "hist": hist, "share_in_money": float(np.mean(f(z) > 0))})


def compute_discrepancy() -> dict:
    """Ch 5: star discrepancy against n for random, Halton and Sobol points; the net property; Halton's late
    dimensions; scrambling for an error bar."""
    ms = list(range(6, 15))
    rows = {}
    for d, mmax in ((2, 14), (16, 12)):
        r_ = {"random": [], "Halton": [], "Sobol": []}
        for m in ms:
            if m > mmax:
                continue
            n = 2 ** m
            r_["random"].append(float(np.mean([E.l2_star_discrepancy(np.random.default_rng(s).random((n, d)))
                                               for s in range(3)])))
            r_["Halton"].append(E.l2_star_discrepancy(qmc.Halton(d, scramble=False).random(n + 1)[1:]))
            r_["Sobol"].append(E.l2_star_discrepancy(qmc.Sobol(d, scramble=False).random_base2(m)))
        rows[str(d)] = {"ns": [2 ** m for m in ms if m <= mmax], **r_}
    sob16 = qmc.Sobol(2, scramble=False).random_base2(8)
    rnd = np.random.default_rng(4).random((256, 2))

    def occupancy(x, m):
        out = {}
        for a in range(m + 1):
            nx, ny = 2 ** a, 2 ** (m - a)
            ix, iy = np.floor(x[:, 0] * nx).astype(int), np.floor(x[:, 1] * ny).astype(int)
            c = np.zeros((nx, ny), int)
            np.add.at(c, (ix, iy), 1)
            out[f"{nx}x{ny}"] = {"empty": int((c == 0).sum()), "double": int((c > 1).sum())}
        return out

    occ = {str(m): {"sobol": occupancy(sob16[:2 ** m], m), "random": occupancy(rnd[:2 ** m], m)} for m in (4, 6, 8)}
    hal = qmc.Halton(30, scramble=False).random(1001)[1:, 28:30]
    sob = qmc.Sobol(30, scramble=False).random_base2(10)[:, 28:30]
    # drop the first Sobol point (the origin), and keep 1,024 points: the net property breaks
    keep = qmc.Sobol(2, scramble=False).random(1025)[1:]
    d_drop = E.l2_star_discrepancy(keep)
    d_keep = E.l2_star_discrepancy(qmc.Sobol(2, scramble=False).random_base2(10))
    # an error bar from 10 independent scramblings: a one-year call by inverse-normal Sobol, 1,024 points each
    from scipy.special import ndtri
    ex = float(bs.price(S0, K, T, SIG, R))
    est = [float(_bs_pay(ndtri(qmc.Sobol(1, scramble=True, seed=s).random_base2(10)[:, 0])).mean()) for s in range(10)]
    vdc = [{"n": n_, "bits": format(n_, "b"), "x": float(qmc.Sobol(1, scramble=False).random(n_ + 1)[n_, 0])}
           for n_ in range(1, 9)]
    return _json({"rows": rows, "sobol256": sob16, "random256": rnd, "occupancy": occ, "halton_29_30": hal,
                  "sobol_29_30": sob, "drop_first": d_drop, "keep_first": d_keep, "rqmc": est, "exact": ex, "vdc": vdc})


def compute_effdim() -> dict:
    """Ch 2 (lab) and ch 6: three square roots of Brownian motion's covariance, the variance each coordinate
    carries, and quasi-Monte Carlo on the Asian with the principal-component construction."""
    a = np.ones(64) / 64
    shares, cols = {}, {}
    for k in ("step", "bridge", "pca"):
        L = E.path_matrix(64, T, k)
        shares[k] = E.variance_captured(a, L)
        cols[k] = E.path_matrix(16, T, k)[:, :16]
    i8 = np.arange(1, 9)
    L8 = E.brownian_bridge(np.eye(8), T).T
    dev8 = float(np.abs(L8 @ L8.T - np.minimum.outer(i8, i8) / 8).max())
    i64 = np.arange(1, 65)
    L64 = E.path_matrix(64, T, "bridge")
    dev64 = float(np.abs(L64 @ L64.T - np.minimum.outer(i64, i64) / 64).max())
    # the Asian by Sobol through the principal-component construction (same 20 scrambles and sizes as `qmc`)
    from scipy.special import ndtri
    Lp = E.path_matrix(64, T, "pca")
    dt = T / 64
    t = dt * np.arange(1, 65)
    ns = [256, 1024, 4096, 16384]
    sd = []
    for n in ns:
        v = []
        for s in range(20):
            z = ndtri(np.clip(qmc.Sobol(64, scramble=True, seed=s).random(n), 1e-12, 1 - 1e-12))
            W = z @ Lp.T
            S = S0 * np.exp((R - 0.5 * SIG ** 2) * t + SIG * W)
            v.append(float(np.exp(-R * T) * np.maximum(S.mean(1) - K, 0).mean()))
        sd.append(float(np.std(v)))
    lam = np.sort(np.linalg.eigvalsh(np.minimum.outer(i64, i64) * dt))[::-1]
    return _json({"shares": shares, "cols16": cols, "dev8": dev8, "dev64": dev64, "ns": ns, "pca_sd": sd,
                  "eig": lam[:8], "eig_kl": [T ** 2 / ((j - 0.5) ** 2 * np.pi ** 2) for j in range(1, 9)]})


def compute_mlmc_trace() -> dict:
    """Ch 7: the adaptive loop of the multilevel estimator at eps = 0.01, logged pass by pass, four seeds (seed 3
    is the run cached in `mlmc`)."""
    part = CACHE.partial("mlmc_trace", {"eps": 0.01, "seeds": [3, 4, 5, 6]})
    for s in (3, 4, 5, 6):
        if str(s) not in part:
            part[str(s)] = _json(E.mlmc_run(0.01, S0, K, T, SIG, R, seed=s, trace=True))
    return {"eps": 0.01, "runs": [part[str(s)] for s in (3, 4, 5, 6)]}


def compute_mlmc_milstein() -> dict:
    """Ch 7: the corrections' variance by level for Euler and Milstein (a European call), Milstein multilevel on the
    Asian against the Euler run of `mlmc`, and one coupled fine/coarse pair of paths per level for the picture."""
    part = CACHE.partial("mlmc_milstein", {"v": 2})
    if "levels" not in part:
        g = np.random.default_rng(0)
        lv = {}
        for sch in ("euler", "milstein"):
            lv[sch] = [float(np.var(E._mlmc_level_scheme(l, 20000, S0, K, T, SIG, R, 2, g, sch, "call")))
                       for l in range(1, 9)]
        part["levels"] = lv
    for e in (0.04, 0.02, 0.01, 0.005):
        if f"mil{e}" not in part:
            part[f"mil{e}"] = _json(E.mlmc_run(e, S0, K, T, SIG, R, seed=3, scheme="milstein"))
    if "eul0.005" not in part:
        part["eul0.005"] = _json(E.mlmc_run(0.005, S0, K, T, SIG, R, seed=3))
    lv = part["levels"]
    beta = {k: float(-np.polyfit(np.arange(3, 9), np.log2(v[2:]), 1)[0]) for k, v in lv.items()}
    g = np.random.default_rng(12)
    pairs = []
    for l in (1, 2, 3, 4):
        nf = 2 ** l
        dW = np.sqrt(T / nf) * g.standard_normal(nf)
        dWc = dW.reshape(-1, 2).sum(1)
        f = [S0]
        for d in dW:
            f.append(f[-1] * (1 + R * T / nf + SIG * d))
        c = [S0]
        for d in dWc:
            c.append(c[-1] * (1 + R * T / (nf // 2) + SIG * d))
        pairs.append({"fine": f, "coarse": c})
    return _json({"levels": lv, "beta": beta, "eps": [0.04, 0.02, 0.01, 0.005],
                  "milstein": [part[f"mil{e}"] for e in (0.04, 0.02, 0.01, 0.005)], "euler_0.005": part["eul0.005"],
                  "pairs": pairs})


def compute_lsm_live() -> dict:
    """Ch 8: Longstaff-Schwartz run backward on the 200,000 paths of `american` (the same draws), recorded date by
    date for 2,000 shown paths; the tree's boundary; the basis-and-paths sweep out of sample; the value regression."""
    tr = E.lsm_put_trace(S0, K, T, SIG, R, 25, 200000, seed=1, n_show=2000)
    ev = E.lsm_put_eval(tr["coefs"], S0, K, T, SIG, R, 25, 400000, seed=7)
    tv = E.lsm_put_trace(S0, K, T, SIG, R, 25, 200000, seed=1, n_show=0, regress="value")
    tree = trees.crr(S0, K, T, SIG, R, q=0.0, N=2000, cp=-1, american=True, boundary=True)
    tb = np.asarray(tree["boundary"])
    tt = np.asarray(tree["times"])
    part = CACHE.partial("lsm_sweep", {"deg": [1, 2, 3, 4, 5], "n": [1000, 10000, 100000], "seeds": 5})
    for dg in (1, 2, 3, 4, 5):
        for n in (1000, 10000, 100000):
            key = f"{dg}_{n}"
            if key not in part:
                vals = []
                for s in range(5):
                    _, cf = E.lsm_put(S0, K, T, SIG, R, 25, n, seed=100 + s, degree=dg, return_policy=True)
                    vals.append(E.lsm_put_eval(cf, S0, K, T, SIG, R, 25, 100000, seed=500 + s, degree=dg)[0])
                part[key] = vals
    sweep = {k: part[k] for k in part.done}
    paths = np.asarray(tr["paths"])[:300]
    return _json({"price_in": tr["price"], "eval": ev, "tvr_in": tv["price"], "boundary": tr["boundary"],
                  "records": tr["records"], "paths": paths, "tree_t": tt[::20], "tree_b": tb[::20],
                  "tree_price": tree["price"], "sweep": sweep})


def compute_bermudan_ref() -> dict:
    """Ch 9: the 25-date Bermudan put on fine trees that may exercise only on the dates (the `bermudan_tree25` number
    in `american` was a 25-step tree, not this)."""
    return {"n_steps": [500, 1000, 2500, 5000],
            "price": [E.bermudan_tree(S0, K, T, SIG, R, 25, n) for n in (500, 1000, 2500, 5000)]}


def compute_maxcall() -> dict:
    """Ch 9: Longstaff-Schwartz on Broadie and Glasserman's five-asset Bermudan max-call, by the number of fitting
    paths, against Part 17's deep optimal stopping (read from its cache, not recomputed)."""
    from explainer.quant.house import deep
    p = dict(deep.MAX_CALL)
    part = CACHE.partial("maxcall", {"fits": [2000, 20000, 200000], "eval": 2000000})
    for nf in (2000, 20000, 200000):
        if str(nf) not in part:
            part[str(nf)] = E.lsm_max_call(p, nf, 2000000, seed=1)
    import json as _j
    from explainer.tts import REPO_ROOT
    st = _j.loads((REPO_ROOT / ".cache" / "quant17" / "stopping.json").read_text())["5"]
    return _json({"params": {k: v for k, v in p.items() if k != "paper"}, "paper": p["paper"],
                  "lsm": {k: part[k] for k in ("2000", "20000", "200000")},
                  "deep": {"lower": st["lower"], "se": st["se"]}})


def compute_dual_path() -> dict:
    """Ch 9: one outer path of Andersen and Broadie's bound, traced: the payoff, the policy's martingale and the
    running maximum of their gap (the same construction as engine.andersen_broadie_put, n_outer = 1)."""
    _, coefs = E.lsm_put(S0, K, T, SIG, R, 25, 200000, seed=1, return_policy=True)
    n_steps, n_inner, deg = 25, 400, 3
    dt = T / n_steps
    g = np.random.default_rng(21)

    def exercise(i, s):
        if i == n_steps:
            return K - s > 0
        b = coefs[i]
        if b is None or i == 0:
            return np.zeros_like(s, bool)
        return (K - s > 0) & ((K - s) > np.vander(s / K, deg + 1) @ b)

    def continuation(i, s, keep=False):
        if i == n_steps:
            return np.zeros_like(s), None
        cur = np.repeat(s, n_inner)
        val = np.zeros(len(cur))
        alive = np.ones(len(cur), bool)
        fan = [cur[:12].copy()]
        for j in range(i + 1, n_steps + 1):
            cur = cur * np.exp((R - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * g.standard_normal(len(cur)))
            if j <= i + 3:
                fan.append(cur[:12].copy())
            ex = alive & exercise(j, cur)
            val[ex] = (K - cur[ex]) * np.exp(-R * (j - i) * dt)
            alive &= ~ex
        return val.reshape(len(s), n_inner).mean(1), np.array(fan)

    best_path = None
    for trial in range(40):  # pick an outer path that goes into the money, so the picture has something to show
        S = np.array([S0])
        C, fan0 = continuation(0, S, True)
        Ss, hs, pis, gaps, fans, Ls = [S0], [0.0], [0.0], [0.0], [fan0], []
        pi = np.zeros(1)
        best = np.maximum(K - S, 0) - pi
        for i in range(1, n_steps + 1):
            S = S * np.exp((R - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * g.standard_normal(1))
            h = np.maximum(K - S, 0)
            Cn, fan = continuation(i, S, True)
            Lv = np.where(exercise(i, S), h, Cn)
            pi = pi + np.exp(-R * i * dt) * Lv - np.exp(-R * (i - 1) * dt) * C
            gap = np.exp(-R * i * dt) * h - pi
            best = np.maximum(best, gap)
            Ss.append(float(S[0]))
            hs.append(float(np.exp(-R * i * dt) * h[0]))
            pis.append(float(pi[0]))
            gaps.append(float(gap[0]))
            fans.append(fan if fan is not None else np.array([[S[0]]]))
            C = Cn
        if min(Ss) < 88 and best_path is None:
            best_path = {"S": Ss, "h": hs, "pi": pis, "gap": gaps, "max": float(best[0]),
                         "fans": [f.tolist() for f in fans]}
            break
    return _json({"dt": dt, "path": best_path, "inner": n_inner})


def compute_bump_h() -> dict:
    """Ch 10: the central-difference delta's error against the bump h and the paths n, with common random numbers and
    with independent draws (30 seeds each)."""
    d1 = (np.log(S0 / K) + (R + 0.5 * SIG ** 2) * T) / (SIG * np.sqrt(T))
    ex = float(norm.cdf(d1))
    hs = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    ns = [1000, 3000, 10000, 30000, 100000]

    def pay(s, z):
        return np.exp(-R * T) * np.maximum(s * np.exp((R - 0.5 * SIG ** 2) * T + SIG * np.sqrt(T) * z) - K, 0)

    out = {}
    for crn in (True, False):
        grid = []
        for n in ns:
            row = []
            for h in hs:
                e = []
                for s in range(30):
                    gg = np.random.default_rng(100 + s)
                    z1 = gg.standard_normal(n)
                    z2 = z1 if crn else gg.standard_normal(n)
                    e.append((pay(S0 + h, z1).mean() - pay(S0 - h, z2).mean()) / (2 * h) - ex)
                row.append(float(np.sqrt(np.mean(np.square(e)))))
            grid.append(row)
        out["crn" if crn else "indep"] = grid
    return _json({"exact": ex, "hs": hs, "ns": ns, **out})


def compute_aad_scale() -> dict:
    """Ch 11: adjoint against bumping as the inputs grow, on a basket Asian (2d inputs): wall-clock (best of nine,
    this machine) and the machine-independent counts (tape nodes and element operations)."""
    part = CACHE.partial("aad_scale", {"ds": [1, 2, 4, 8, 16, 32, 64], "n": 4000, "steps": 12, "reps": 9,
                                       "bump_reps": "9, or 2 at d >= 32"})
    for d in (1, 2, 4, 8, 16, 32, 64):
        if str(d) not in part:
            part[str(d)] = E.aad_basket(d, 4000, 12, seed=0, reps=9, bump_reps=9 if d < 32 else 2)
    rows = [part[str(d)] for d in (1, 2, 4, 8, 16, 32, 64)]
    return {"rows": rows, "machine": "one core of the build machine (shared, under load); best of nine (bumps at "
                                     "32 and 64 assets: best of two)"}


def compute_fd_live() -> dict:
    """Ch 12: the explicit scheme marching the call's grid back from expiry, stable (2,000 steps) and unstable (200),
    every slice kept for the 3D picture (100 price points to 400)."""
    nS = 100
    Smax = 4 * K
    S = np.linspace(0, Smax, nS + 1)
    dS = S[1]
    out = {}
    for nt, every in ((2000, 50), (200, 5)):
        dt = T / nt
        V = np.maximum(S - K, 0)
        i = np.arange(1, nS)
        a = 0.5 * SIG ** 2 * S[i] ** 2 / dS ** 2 - 0.5 * R * S[i] / dS
        b = -SIG ** 2 * S[i] ** 2 / dS ** 2 - R
        c = 0.5 * SIG ** 2 * S[i] ** 2 / dS ** 2 + 0.5 * R * S[i] / dS
        sl, taus = [V.copy()], [0.0]
        for n in range(nt):
            tau = (n + 1) * dt
            inner = V[1:-1] + dt * (a * V[:-2] + b * V[1:-1] + c * V[2:])
            V = np.concatenate([[0.0], inner, [Smax - K * np.exp(-R * tau)]])
            if (n + 1) % every == 0:
                sl.append(V.copy())
                taus.append(tau)
        out[str(nt)] = {"slices": np.clip(np.asarray(sl), -1e6, 1e6), "tau": taus,
                        "first_bad": next((k for k, s_ in enumerate(sl) if np.max(np.abs(s_ - np.maximum(S - K, 0)))
                                           > 50), None)}
    lam = SIG ** 2 * Smax ** 2 * (T / 200) / dS ** 2
    return _json({"S": S, "runs": out, "lambda_max_200": lam, "lambda_max_2000": lam / 10})


def compute_lcp() -> dict:
    """Ch 13: the American put as a complementarity problem, by projected SOR and by the penalty method; the free
    boundary; the value surface for 3D; one PSOR solve traced sweep by sweep."""
    def best_of(f, k=3):
        b, out = np.inf, None
        for _ in range(k):
            t0 = time.perf_counter()
            out = f()
            b = min(b, time.perf_counter() - t0)
        return out, b

    pen, t_pen = best_of(lambda: E.fd_american_penalty(S0, K, T, SIG, R, 400, 400), 3)
    psor, t_psor = best_of(lambda: E.fd_american_put(S0, K, T, SIG, R, nS=200, nt=200), 2)
    tree = trees.crr(S0, K, T, SIG, R, q=0.0, N=2000, cp=-1, american=True, boundary=True)
    surf = E.fd_american_penalty(S0, K, T, SIG, R, 200, 200, keep=5)
    Sg = np.asarray(surf["S"])
    m = (Sg >= 50) & (Sg <= 150)
    sl = np.asarray(surf["slices"])[:, m]
    taus = np.linspace(0, T, len(sl))
    euro = np.array([[float(bs.price(s, K, max(tau, 1e-9), SIG, R, cp=-1)) for s in Sg[m]] for tau in taus])
    # one PSOR time step traced: the residual after each sweep (the first CN step from the payoff, 200 points)
    nS = 200
    Sx = np.linspace(0, 4 * K, nS + 1)
    dt = T / 200
    i = np.arange(1, nS)
    a = 0.5 * dt * (SIG ** 2 * i ** 2 - R * i)
    b = -dt * (SIG ** 2 * i ** 2 + R)
    c = 0.5 * dt * (SIG ** 2 * i ** 2 + R * i)
    payoff = np.maximum(K - Sx, 0)
    V = payoff.copy()
    rhs = V[1:-1] + 0.5 * (a * V[:-2] + b * V[1:-1] + c * V[2:])
    x = V[1:-1].copy()
    res, clipped = [], []
    for _it in range(60):
        err, cl = 0.0, 0
        for j in range(nS - 1):
            left = x[j - 1] if j > 0 else K
            right = x[j + 1] if j < nS - 2 else 0.0
            y = (rhs[j] + 0.5 * (a[j] * left + c[j] * right)) / (1 - 0.5 * b[j])
            yy = x[j] + 1.2 * (y - x[j])
            if yy < payoff[j + 1]:
                cl += 1
            y = max(payoff[j + 1], yy)
            err += (y - x[j]) ** 2
            x[j] = y
        res.append(float(np.sqrt(err)))
        clipped.append(cl)
        if err < 1e-20:
            break
    return _json({"penalty": {"price": pen["price"], "its_mean": float(np.mean(pen["iterations"])),
                              "its_max": int(np.max(pen["iterations"])), "time": t_pen, "grid": 400,
                              "boundary": pen["boundary"]},
                  "psor": {"price": psor, "time": t_psor, "grid": 200},
                  "tree": {"price": tree["price"], "t": np.asarray(tree["times"])[::20],
                           "b": np.asarray(tree["boundary"])[::20]},
                  "surface": {"S": Sg[m], "tau": taus, "american": sl, "european": euro,
                              "boundary": [np.nan] + list(np.asarray(surf["boundary"])[4::5])},
                  "psor_trace": {"res": res, "clipped": clipped}})


def compute_adi_grid() -> dict:
    """Ch 14: uniform against non-uniform grids; the price surface u(S, v) and its Greeks off the grid."""
    ref = _heston_ref()
    rows = []
    for n in (40, 80, 160):
        for uni in (True, False):
            p = E.heston_adi(S0, K, T, *HES, r=0.0, nS=n, nv=n // 2, nt=n // 2, uniform=uni)
            rows.append({"nS": n, "nv": n // 2, "uniform": uni, "err": abs(p - ref)})
    Sg, vg, G = E.heston_adi_grid(S0, K, T, *HES, r=0.0, nS=80, nv=40, nt=40)
    from scipy.interpolate import RegularGridInterpolator
    f = RegularGridInterpolator((vg, Sg), G, method="cubic")
    Sd = np.linspace(60, 140, 41)
    vd = np.linspace(0.0, 0.2, 21)
    VV, SS = np.meshgrid(vd, Sd, indexing="ij")
    U = f((VV, SS))
    dS, dv = Sd[1] - Sd[0], vd[1] - vd[0]
    delta = np.gradient(U, dS, axis=1)
    gamma = np.gradient(delta, dS, axis=1)
    vega = np.gradient(U, dv, axis=0)
    return _json({"ref": ref, "rows": rows, "S": Sd, "v": vd, "u": U, "delta": delta, "gamma": gamma, "vega": vega,
                  "gridS": Sg[(Sg > 0) & (Sg < 300)], "gridv": vg[vg < 1.0]})


def compute_lewis() -> dict:
    """Ch 15: Lewis's single integral against COS; Carr-Madan's error against the damping alpha; the damped call
    and its transform for the picture."""
    ref = _heston_ref()
    cf = lambda u, TT: sv.heston_cf(u, TT, *HES)  # noqa: E731
    t0 = time.perf_counter()
    lw = E.lewis_call(cf, S0, K, T)
    t_l = time.perf_counter() - t0
    alphas = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    cm = []
    for al in alphas:
        try:
            kk, C = E.carr_madan(cf, S0, T, 0.0, N=4096, eta=0.25, alpha=al)
            cm.append(float(abs(np.interp(K, kk, C) - ref)))
        except Exception:
            cm.append(float("nan"))
    ks = np.linspace(-1.5, 1.0, 101)
    Cs = sv.cos_price(cf, S0, S0 * np.exp(ks), T, 1, N=1024, L=16)
    u = np.linspace(0, 25, 201)
    al = 1.5
    phi = cf(u - (al + 1) * 1j, T) * np.exp(1j * (u - (al + 1) * 1j) * np.log(S0))
    psi = phi / (al ** 2 + al - u ** 2 + 1j * (2 * al + 1) * u)
    # Lewis's integrand on the line Im u = -1/2
    k0 = 0.0
    lw_int = (np.exp(1j * u * k0) * cf(u - 0.5j, T)).real / (u * u + 0.25)
    return _json({"ref": ref, "lewis": lw, "diff": lw - ref, "t_lewis": t_l, "alphas": alphas, "cm_err": cm,
                  "k": ks, "C": Cs, "u": u, "psi_re": psi.real, "psi_im": psi.imag, "lewis_integrand": lw_int})


def compute_cos_density() -> dict:
    """Ch 16: the Heston log-return density rebuilt by cosines term by term; the coefficients' decay; the truncation
    range's effect; the COS lab's numbers."""
    cf = lambda u, TT: sv.heston_cf(u, TT, *HES)  # noqa: E731
    c1, c2 = sv.cumulants(cf, T)
    Lw = 16
    a, b = c1 - Lw * np.sqrt(c2), c1 + Lw * np.sqrt(c2)
    y = np.linspace(-1.0, 0.6, 321)

    def dens(N, a_=a, b_=b):
        k = np.arange(N)
        w = k * np.pi / (b_ - a_)
        A = 2 / (b_ - a_) * (cf(w, T) * np.exp(-1j * w * a_)).real
        A[0] *= 0.5
        return (A[None, :] * np.cos(np.outer(y - a_, w))).sum(1), A

    true, Afull = dens(4096)
    rec = {str(N): dens(N)[0] for N in (2, 4, 8, 16, 32, 64, 128)}
    ref = _heston_ref()
    Ls, errL = [4, 6, 8, 10, 12, 16, 20, 30, 40], []
    for L_ in Ls:
        errL.append(float(abs(sv.cos_price(cf, S0, K, T, 1, N=4096, L=L_)[0] - ref)))
    return _json({"y": y, "true": true, "rec": rec, "A": np.abs(Afull[:200]), "a": a, "b": b, "c1": c1, "c2": c2,
                  "L": Ls, "errL": errL})


def compute_race_cv() -> dict:
    """Ch 16: Monte Carlo in the race again, with the stock as a control variate (its mean is S0, since r = 0), at
    the same four sizes and seeds as `race`; the standard error is plotted, as for the plain runs."""
    ref = _heston_ref()
    pts = []
    for n in (5000, 20000, 80000, 320000):
        t0 = time.perf_counter()
        ST = sv.heston_qe(S0, *HES, T, 50, n, seed=n)[-1]
        pay = np.maximum(ST - K, 0)
        b = np.cov(pay, ST)[0, 1] / np.var(ST, ddof=1)
        y = pay - b * (ST - S0)
        pts.append({"method": "Monte Carlo, control variate", "err": float(y.std() / np.sqrt(n)),
                    "time": time.perf_counter() - t0, "actual": float(abs(y.mean() - ref)),
                    "ratio": float(pay.var() / y.var())})
    return _json({"ref": ref, "points": pts})


def _par_worker(args):
    seed, n = args
    z = np.random.default_rng(seed).standard_normal(n)
    return float(np.maximum(100 * np.exp(0.03 + 0.2 * z) - 100, 0).sum())


def compute_parallel() -> dict:
    """Ch 17: one 10^6-path pricing as a Python loop, vectorised numpy, float32, and split over 1, 2 and 4 processes
    (best of three each; this machine, shared)."""
    import datetime
    from concurrent.futures import ProcessPoolExecutor
    n = 1_000_000

    def best(f, k=3):
        b = np.inf
        for _ in range(k):
            t0 = time.perf_counter()
            f()
            b = min(b, time.perf_counter() - t0)
        return b

    z = np.random.default_rng(0).standard_normal(n)
    z32 = z.astype(np.float32)

    def loop():
        s = 0.0
        for x in z[:100_000]:
            s += max(100 * np.exp(0.03 + 0.2 * x) - 100, 0.0)
        return s

    t_loop = best(loop, 2) * 10  # timed on a tenth, scaled: the loop is linear in n
    t_np = best(lambda: np.maximum(100 * np.exp(0.03 + 0.2 * z) - 100, 0).sum(), 5)
    t_32 = best(lambda: np.maximum(np.float32(100) * np.exp(np.float32(0.03) + np.float32(0.2) * z32)
                                   - np.float32(100), 0).sum(), 5)
    t_gen = best(lambda: _par_worker((0, n)), 3)
    procs = {}
    for w in (1, 2, 4):
        with ProcessPoolExecutor(max_workers=w) as ex:
            list(ex.map(_par_worker, [(s, 1000) for s in range(w)]))  # start the workers first
            procs[str(w)] = best(lambda: list(ex.map(_par_worker, [(s, n // w) for s in range(w)])), 3)
    import os
    return {"n": n, "t_loop": t_loop, "t_numpy": t_np, "t_float32": t_32, "t_gen_numpy": t_gen, "procs": procs,
            "date": datetime.date.today().isoformat(), "load": list(os.getloadavg()), "cores": os.cpu_count()}


def compute_qae() -> dict:
    """Ch 18: maximum-likelihood amplitude estimation, simulated exactly, against Monte Carlo at equal oracle calls;
    one run's likelihood after each power for the replay."""
    a = 0.3
    schedules = [tuple([0] + [2 ** k for k in range(Kp)]) for Kp in range(0, 13)]
    out = []
    for sch in schedules:
        errs, calls = [], None
        for rep in range(40):
            r_ = E.mlae(a, sch, 50, seed=1000 * len(sch) + rep)
            errs.append(r_["estimates"][-1] - a)
            calls = r_["calls"][-1]
        out.append({"powers": len(sch), "calls": calls, "rmse": float(np.sqrt(np.mean(np.square(errs)))),
                    "mc": float(np.sqrt(a * (1 - a) / calls)), "errs": errs})
    x = np.log10([o["calls"] for o in out])
    yq = np.log10([o["rmse"] for o in out])
    slope = float(np.polyfit(x[3:], yq[3:], 1)[0])
    one = E.mlae(a, schedules[6], 50, seed=7)
    th = np.linspace(1e-4, np.pi / 2 - 1e-4, 1500)
    curves = []
    for k in range(1, len(schedules[6]) + 1):
        ll = np.zeros_like(th)
        for mk, h in zip(schedules[6][:k], one["hits"][:k]):
            q = np.clip(np.sin((2 * mk + 1) * th) ** 2, 1e-300, 1 - 1e-16)
            ll += h * np.log(q) + (50 - h) * np.log1p(-q)
        curves.append(np.exp(ll - ll.max()))
    return _json({"a": a, "shots": 50, "rows": out, "slope": slope, "one": one, "theta_grid": th, "curves": curves,
                  "powers6": schedules[6]})


def compute_cheb() -> dict:
    """Ch 19: a Chebyshev pricer for the Heston call over (S0, v0), built from COS prices at the nodes; its error
    against the nodes per axis; the cost of a query."""
    box = ((70.0, 130.0), (0.01, 0.09))
    kap, the, xi, rho = HES[1:]

    def price(S, v0):
        return float(sv.cos_price(lambda u, TT: sv.heston_cf(u, TT, v0, kap, the, xi, rho), S, K, T, 1, N=512,
                                  L=16)[0])

    g = np.random.default_rng(0)
    test = np.c_[g.uniform(*box[0], 200), g.uniform(*box[1], 200)]
    truth = np.array([price(s, v) for s, v in test])
    xs, ys = np.linspace(*box[0], 25), np.linspace(*box[1], 25)
    XX, YY = np.meshgrid(xs, ys, indexing="ij")
    disp_truth = np.array([[price(x, y) for y in ys] for x in xs])
    rows = []
    for n in (4, 8, 12, 16, 24, 32):
        t0 = time.perf_counter()
        m = E.chebyshev2d(price, box, n)
        t_build = time.perf_counter() - t0
        est = E.chebyshev2d_eval(m, test[:, 0], test[:, 1])
        surf = np.abs(E.chebyshev2d_eval(m, XX, YY) - disp_truth)
        rows.append({"n": n, "calls": n * n, "max_err": float(np.abs(est - truth).max()), "t_build": t_build,
                     "err_surface": np.log10(np.maximum(surf, 1e-12)), "x": m["x"], "y": m["y"]})
    m = E.chebyshev2d(price, box, 32)

    def best(f, k=20):
        b = np.inf
        for _ in range(k):
            t0 = time.perf_counter()
            f()
            b = min(b, time.perf_counter() - t0)
        return b

    t_cheb = best(lambda: E.chebyshev2d_eval(m, np.array([101.3]), np.array([0.042])))
    t_cos = best(lambda: price(101.3, 0.042))
    return _json({"box": box, "rows": rows, "xs": xs, "ys": ys, "t_cheb": t_cheb, "t_cos": t_cos})


def compute_rqmc_median() -> dict:
    """Ch 19: mean against median of 11 scrambled Sobol estimates of a smooth integral (int_0^1 e^u du), 30 repeats."""
    I = np.e - 1
    ms = [4, 6, 8, 10, 12]
    me, md = [], []
    for m in ms:
        a_, b_ = [], []
        for rep in range(30):
            ests = [np.exp(qmc.Sobol(1, scramble=True, seed=1000 * rep + k).random_base2(m)[:, 0]).mean()
                    for k in range(11)]
            a_.append(np.mean(ests) - I)
            b_.append(np.median(ests) - I)
        me.append(float(np.sqrt(np.mean(np.square(a_)))))
        md.append(float(np.sqrt(np.mean(np.square(b_)))))
    return {"ns": [2 ** m for m in ms], "mean": me, "median": md}



def compute_mlmc_call() -> dict:
    """Ch 7: the theorem's textbook case, a European call (Lipschitz payoff): multilevel cost against eps for Euler
    (beta = gamma = 1: eps^-2 (log eps)^2) and Milstein (beta = 2 > gamma: eps^-2)."""
    part = CACHE.partial("mlmc_call", {"eps": [0.04, 0.02, 0.01, 0.005], "seed": 3})
    for sch in ("euler", "milstein"):
        for e in (0.04, 0.02, 0.01, 0.005):
            key = f"{sch}{e}"
            if key not in part:
                part[key] = _json(E.mlmc_run(e, S0, K, T, SIG, R, seed=3, scheme=sch, payoff="call"))
    return {"eps": [0.04, 0.02, 0.01, 0.005], "exact": float(bs.price(S0, K, T, SIG, R)),
            "euler": [part[f"euler{e}"] for e in (0.04, 0.02, 0.01, 0.005)],
            "milstein": [part[f"milstein{e}"] for e in (0.04, 0.02, 0.01, 0.005)]}


def compute_drop_first() -> dict:
    """Ch 5: dropping Sobol's first point (the origin) to dodge the inverse normal's -infinity, against keeping it:
    the error of scrambled Sobol on a smooth integral, int e^{u1 + u2} over the square, 100 scramblings each."""
    I = (np.e - 1) ** 2
    out = {}
    for m in (6, 8, 10, 12):
        keep, drop = [], []
        for s in range(100):
            sob = qmc.Sobol(2, scramble=True, seed=s)
            x = sob.random(2 ** m + 1)
            keep.append(np.exp(x[:-1].sum(1)).mean() - I)
            drop.append(np.exp(x[1:].sum(1)).mean() - I)
        out[str(2 ** m)] = {"keep": float(np.sqrt(np.mean(np.square(keep)))),
                            "drop": float(np.sqrt(np.mean(np.square(drop))))}
    return {"rows": out}


def _bermudan_tree(S0, K, T, sigma, r, dates, steps_per=40):
    """A CRR tree for a Bermudan put exercisable on ``dates`` equally spaced dates (the last at T)."""
    n = dates * steps_per
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    q = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    j = np.arange(n + 1)
    V = np.maximum(K - S0 * u ** (n - 2 * j), 0.0)
    for i in range(n - 1, -1, -1):
        V = disc * (q * V[:-1] + (1 - q) * V[1:])
        if i > 0 and i % steps_per == 0:
            Si = S0 * u ** (i - 2 * np.arange(i + 1))
            V = np.maximum(V, K - Si)
    return float(V[0])


def compute_paths_basis() -> dict:
    """The research chapter: paths against basis functions in Longstaff-Schwartz (Glasserman and Yu 2004).  The
    regression's sample Gram matrix converges only when the number of paths is large against the fourth moments of the
    basis functions; for orthonormal Hermite polynomials of a Gaussian E[h_k^4] grows geometrically (about 9^k), for
    normalized monomials of a lognormal like exp(c k^2).  Then the experiment: a Bermudan put, a fixed out-of-sample set
    of paths to value each fitted policy (a lower bound), degree against number of paths, a tree as the truth."""
    z, w = np.polynomial.hermite_e.hermegauss(240)
    w = w / w.sum()
    from math import factorial
    m4_bm = []
    for k in range(0, 31):
        c = np.zeros(k + 1)
        c[k] = 1.0
        hk = np.polynomial.hermite_e.hermeval(z, c) / np.sqrt(float(factorial(k)))
        m4_bm.append(float(np.sum(w * hk ** 4)))
    sig_t = 0.2  # sigma sqrt(t) of the lognormal at one year
    ks = np.arange(0, 13)
    m4_gbm = list(np.exp(4 * sig_t ** 2 * ks ** 2))   # E[S^{4k}] / E[S^{2k}]^2 for S = exp(sigma W_t)
    out = {"m4_bm": m4_bm, "m4_gbm": m4_gbm, "k_bm": list(range(31)), "k_gbm": ks}
    # the Longstaff-Schwartz experiment: S0 36, K 40, sigma 20%, r 6%, one year, 50 exercise dates
    S0, K, sig, r, T, D = 36.0, 40.0, 0.2, 0.06, 1.0, 50
    true = _bermudan_tree(S0, K, T, sig, r, D, steps_per=60)
    dt = T / D
    disc = np.exp(-r * dt)

    def paths(n, seed):
        rng = np.random.default_rng(seed)
        Z = rng.standard_normal((n, D))
        return S0 * np.exp(np.cumsum((r - 0.5 * sig ** 2) * dt + sig * np.sqrt(dt) * Z, axis=1))

    def basis(x, deg):
        return np.vander(x / K, deg + 1, increasing=True)

    def fit(S, deg):
        n = len(S)
        cash = np.maximum(K - S[:, -1], 0.0)
        betas = [None] * D
        for t in range(D - 2, -1, -1):
            cash = cash * disc
            ex = K - S[:, t]
            itm = ex > 0
            if itm.sum() > deg + 1:
                X = basis(S[itm, t], deg)
                b = np.linalg.lstsq(X, cash[itm], rcond=None)[0]
                betas[t] = b
                cont = X @ b
                go = ex[itm] > cont
                idx = np.where(itm)[0][go]
                cash[idx] = ex[idx]
        return betas

    def value(S, betas, deg):
        n = len(S)
        alive = np.ones(n, bool)
        pv = np.zeros(n)
        for t in range(D - 1):
            b = betas[t]
            ex = K - S[:, t]
            if b is None:
                continue
            cand = alive & (ex > 0)
            if cand.any():
                cont = basis(S[cand, t], deg) @ b
                go = ex[cand] > cont
                idx = np.where(cand)[0][go]
                pv[idx] = ex[idx] * np.exp(-r * (t + 1) * dt)
                alive[idx] = False
        pv[alive] = np.maximum(K - S[alive, -1], 0.0) * np.exp(-r * T)
        return float(pv.mean()), float(pv.std() / np.sqrt(n))

    test = paths(100000, 1616)
    Ns = [500, 2000, 10000, 50000]
    degs = list(range(1, 13))
    grid = {}
    for N in Ns:
        rows = []
        for deg in degs:
            vals = []
            for seed in range(3):
                b = fit(paths(N, 100 * N + seed), deg)
                vals.append(value(test, b, deg)[0])
            rows.append({"deg": deg, "mean": float(np.mean(vals)), "min": float(np.min(vals)), "max": float(np.max(vals))})
        grid[str(N)] = rows
    out["lsm"] = {"S0": S0, "K": K, "sigma": sig, "r": r, "T": T, "dates": D, "true": true, "grid": grid,
                  "test_se": value(test, fit(paths(50000, 7), 3), 3)[1]}
    return _json(out)


ITEMS = {"paths_basis": compute_paths_basis, "mc": compute_mc, "qmc": compute_qmc, "mlmc": compute_mlmc, "american": compute_american,
         "greeks": compute_greeks, "fd": compute_fd, "adi": compute_adi, "fourier": compute_fourier,
         "race": compute_race, "envelope": compute_envelope,
         "mc_live": compute_mc_live, "rng": compute_rng, "control": compute_control, "is_sweep": compute_is_sweep,
         "discrepancy": compute_discrepancy, "effdim": compute_effdim, "mlmc_trace": compute_mlmc_trace,
         "mlmc_milstein": compute_mlmc_milstein, "lsm_live": compute_lsm_live, "bermudan_ref": compute_bermudan_ref,
         "maxcall": compute_maxcall, "dual_path": compute_dual_path, "bump_h": compute_bump_h,
         "aad_scale": compute_aad_scale, "fd_live": compute_fd_live, "lcp": compute_lcp, "adi_grid": compute_adi_grid,
         "lewis": compute_lewis, "cos_density": compute_cos_density, "race_cv": compute_race_cv,
         "parallel": compute_parallel, "qae": compute_qae, "cheb": compute_cheb, "rqmc_median": compute_rqmc_median,
         "mlmc_call": compute_mlmc_call, "drop_first": compute_drop_first}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
