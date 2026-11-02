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
"""

from __future__ import annotations

import time

import numpy as np
from scipy.stats import norm, qmc

from explainer.ai.cache import Cache
from explainer.quant.house import bs, engine as E, pit, stochvol as sv, trees

CACHE = Cache("quant16")
load = CACHE.load

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


ITEMS = {"mc": compute_mc, "qmc": compute_qmc, "mlmc": compute_mlmc, "american": compute_american,
         "greeks": compute_greeks, "fd": compute_fd, "adi": compute_adi, "fourier": compute_fourier,
         "race": compute_race, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
