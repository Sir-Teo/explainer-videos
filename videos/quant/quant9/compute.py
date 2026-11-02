"""Every number in Part 9 (No Arbitrage), computed and cached in .cache/quant9/.

    python -m videos.quant.quant9.compute [items] [--force]

Items (seconds to a minute on a CPU):

* ``parity``   put-call parity on the Surface's trades (Deribit BTC options, 10 December 2025): the forward implied by
               every call-put pair, the basis per expiry as an annual rate, and how far each pair sits from its
               expiry's median;
* ``density``  SVI fits to two of the Surface's expiries and their Breeden-Litzenberger densities, with the static
               arbitrage checks;
* ``mot``      model-free bounds on a forward-start straddle between those expiries (martingale optimal transport),
               against the price with independent log-normal returns;
* ``ross``     Ross recovery in two synthetic economies: one where its assumption holds, one with permanent shocks;
* ``envelope``   the trial counter (this part tests no strategy);
* ``incomplete`` the no-arbitrage interval for a call as a one-period market gains states, and closes when the call
               itself is traded.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant.house import arbitrage as A
from explainer.quant.house import bs, smile, surface

CACHE = Cache("quant9")
load = CACHE.load

DAY = surface.DAYS[0]


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


# ---------------------------------------------------------------------------
def compute_parity() -> dict:
    from explainer.quant.data import deribit_trades
    trades = deribit_trades(DAY, hours=surface.HOURS)
    by = defaultdict(list)
    for t in trades:
        exp, K, cp = surface.parse_instrument(t["instrument_name"])
        s = t["timestamp"] / 1e3
        T = (exp.timestamp() - s) / surface.YEAR
        if T <= 1 / 365:
            continue
        by[(exp, K, cp)].append((s, t["mark_price"], t["price"], t["index_price"], T))
    rows = []  # (T, K/index, implied F/index from marks, from trade prices)
    for (e, K, cp), calls in by.items():
        if cp != 1 or (e, K, -1) not in by:
            continue
        puts = by[(e, K, -1)]
        pt = np.array([p[0] for p in puts])
        for s, cm, cpx, ci, T in calls:
            j = int(np.argmin(np.abs(pt - s)))
            if abs(pt[j] - s) > 600 or abs(np.log(K / ci)) > 0.2:
                continue
            ind = 0.5 * (ci + puts[j][3])
            dm = cm - puts[j][1]
            dt = cpx - puts[j][2]
            if dm < 1 - 1e-9 and dt < 1 - 1e-9:
                # inverse options: C - P = 1 - K/F (in BTC)  =>  F = K / (1 - (C - P))
                rows.append((T, K / ind, K / (1 - dm) / ind, K / (1 - dt) / ind, e.strftime("%Y-%m-%d")))
    T = np.array([r[0] for r in rows])
    fm = np.array([r[2] for r in rows])
    ft = np.array([r[3] for r in rows])
    ex = np.array([r[4] for r in rows])
    per = []
    for e in sorted(set(ex)):
        m = ex == e
        if m.sum() < 5:
            continue
        med = float(np.median(fm[m]))
        Te = float(np.median(T[m]))
        per.append({"expiry": e, "T": Te, "n": int(m.sum()), "ratio": med, "rate": float(np.log(med) / Te),
                    "resid_bp_mark": (1e4 * (fm[m] / med - 1)).tolist(),
                    "resid_bp_trade": (1e4 * (ft[m] / med - 1)).tolist()})
    allm = np.concatenate([e["resid_bp_mark"] for e in per])
    allt = np.concatenate([e["resid_bp_trade"] for e in per])
    return _json({"day": DAY, "n_pairs": int(len(rows)), "expiries": per,
                  "mark_p50": float(np.median(np.abs(allm))), "trade_p50": float(np.median(np.abs(allt))),
                  "trade_p90": float(np.percentile(np.abs(allt), 90)), "resid_trade": allt, "resid_mark": allm})


def _fit_expiry(q, e):
    m = np.array([x == e for x in q["expiry"]])
    T = float(q["T"][m][0])
    F = float(q["F"][m][0])
    p = smile.fit_svi(q["k"][m], q["iv"][m] ** 2 * T, weights=q["vega"][m])
    return m, T, F, p


def _pick_expiries(q, targets=(30 / 365, 100 / 365)):
    exps = q["expiries"]
    out = []
    for tg in targets:
        cand = [e for e in exps if e["n"] >= 15]
        out.append(min(cand, key=lambda e: abs(e["T"] - tg))["expiry"])
    return out


def compute_density() -> dict:
    q = surface.build(DAY)
    res = {"S": q["S"], "expiries": []}
    for e in _pick_expiries(q):
        m, T, F, p = _fit_expiry(q, e)
        K = np.linspace(0.2 * F, 3.0 * F, 1401)
        dens = smile.risk_neutral_density(p, F, T, K)
        C = smile.call_prices(p, F, T, K)
        chk = A.static_checks(K, C, F)
        kq = q["k"][m]
        res["expiries"].append({"expiry": e, "T": T, "F": F, "svi": p, "K_quotes": (F * np.exp(kq)).tolist(),
                                "iv_quotes": q["iv"][m].tolist(), "K": K, "iv_fit": smile.svi_iv(p, np.log(K / F), T),
                                "density": dens, "mass": float(np.trapezoid(dens, K)),
                                "mean": float(np.trapezoid(dens * K, K) / np.trapezoid(dens, K)), "checks": chk,
                                "p_down20": float(np.trapezoid(dens[K < 0.8 * F], K[K < 0.8 * F])),
                                "p_up20": float(np.trapezoid(dens[K > 1.2 * F], K[K > 1.2 * F]))})
    a, b = res["expiries"]
    kk = np.linspace(-0.6, 0.6, 121)
    w1 = smile.svi_total_variance(kk, *[a["svi"][x] for x in ("a", "b", "rho", "m", "s")])
    w2 = smile.svi_total_variance(kk, *[b["svi"][x] for x in ("a", "b", "rho", "m", "s")])
    res["calendar_violations"] = len(A.calendar_check(kk, w1, w2))
    return _json(res)


def compute_mot() -> dict:
    d = load("density")
    a, b = d["expiries"]
    out = {}
    grids = []
    for e, nb in ((a, 25), (b, 81)):
        # the earlier marginal on coarse bins, the later on fine ones: binning to conditional means shrinks a
        # distribution in convex order, so the coarse earlier one stays below the fine later one, as the
        # martingale property requires
        K, dens = np.asarray(e["K"]), np.asarray(e["density"])
        F = e["F"]
        x = K / F
        edges = np.linspace(x[0], x[-1], nb + 1)
        pts, w = [], []
        for i in range(nb):
            mm = (x >= edges[i]) & (x < edges[i + 1])
            mass = np.trapezoid(dens[mm], K[mm]) if mm.sum() > 1 else 0.0
            if mass > 1e-8:
                pts.append(np.sum(x[mm] * dens[mm]) / np.sum(dens[mm]))
                w.append(mass)
        w = np.array(w) / np.sum(w)
        grids.append((np.array(pts), w))
    (x, mu), (y, nu) = grids
    x = x / np.dot(x, mu)
    y = y / np.dot(y, nu)
    ks = np.linspace(0.3, 2.5, 200)
    gap = min(float(np.dot(nu, np.maximum(y - k, 0)) - np.dot(mu, np.maximum(x - k, 0))) for k in ks)
    if gap < -1e-9:
        raise ValueError(f"discretized marginals are not in convex order (worst call-price gap {gap:.2e})")
    bounds = A.mot_bounds(x, mu, y, nu, lambda s1, s2: abs(s2 / s1 - 1))
    # independent log-normal increments with the forward volatility between the two at-the-money vols
    T1, T2 = a["T"], b["T"]
    iv1 = smile.svi_iv(a["svi"], 0.0, T1)
    iv2 = smile.svi_iv(b["svi"], 0.0, T2)
    fwd_var = max(iv2 ** 2 * T2 - iv1 ** 2 * T1, 1e-8)
    model = float(2 * bs.price(1.0, 1.0, 1.0, np.sqrt(fwd_var), 0.0, 0.0, 1))  # E|R - 1| = straddle with unit T
    out.update({"T1": T1, "T2": T2, "lower": bounds["lower"], "upper": bounds["upper"], "model": model,
                "fwd_vol": float(np.sqrt(fwd_var / (T2 - T1))), "x": x, "mu": mu, "y": y, "nu": nu,
                "pi_lower": bounds["pi_lower"], "pi_upper": bounds["pi_upper"]})
    return _json(out)


def compute_ross() -> dict:
    g = np.random.default_rng(90)
    n = 9
    c = np.exp(np.linspace(-0.2, 0.2, n))  # consumption relative to trend, a stationary chain
    pi = np.exp(-((np.arange(n)[:, None] * 0.8 + n * 0.1 - np.arange(n)[None, :]) ** 2) / 3.0)
    pi /= pi.sum(axis=1, keepdims=True)
    delta, gamma = 0.98, 3.0
    P = delta * pi * (c[None, :] / c[:, None]) ** (-gamma)
    rec = A.ross_recovery(P)
    # with a permanent component: the kernel also carries an i.i.d. martingale shock, so state prices tilt toward
    # bad states in every transition, and the recovered probabilities inherit the tilt (Borovicka, Hansen and
    # Scheinkman 2016)
    tilt = np.exp(-0.6 * np.linspace(-1, 1, n))  # a permanent shock that is worse in low states
    tilt = tilt / (pi @ tilt)[:, None]
    P2 = P * tilt
    rec2 = A.ross_recovery(P2)
    stat = lambda M: np.linalg.matrix_power(M, 200)[0]  # noqa: E731  (stationary distribution)
    return _json({"c": c, "pi": pi, "P": P, "recovered": rec["F"], "delta": rec["delta"], "P2": P2,
                  "recovered2": rec2["F"], "delta2": rec2["delta"], "stat_true": stat(pi), "stat_rec2": stat(rec2["F"]),
                  "err1": float(np.max(np.abs(rec["F"] - pi))), "err2": float(np.max(np.abs(rec2["F"] - pi))),
                  "mean_true": float(stat(pi) @ np.log(c)), "mean_rec2": float(stat(rec2["F"]) @ np.log(c))})


def compute_incomplete() -> dict:
    r = 0.0
    out = []
    for n in (2, 3, 5, 9, 17, 33):
        z = np.linspace(-2, 2, n) if n > 2 else np.array([-1.0, 1.0])
        S = np.exp(0.2 * z)
        D = np.vstack([np.ones(n), S])
        p = np.array([1.0, 1.0])
        # the stock's price must lie inside its payoffs' range; rescale to make it a martingale under some measure
        if not (S.min() < 1 < S.max()):
            continue
        call = np.maximum(S - 1.0, 0.0)
        h = A.superhedge(D, p, call)
        out.append({"states": n, "lower": h["lower"], "upper": h["upper"]})
    bs_price = float(bs.price(1.0, 1.0, 1.0, 0.2))
    return _json({"rows": out, "bs": bs_price})


def compute_envelope() -> dict:
    from explainer.quant.house import pit
    return {"trials": pit.trials_so_far(), "registered": {}}  # this part tests no strategy


ITEMS = {"envelope": compute_envelope, "parity": compute_parity, "density": compute_density, "mot": compute_mot, "ross": compute_ross,
         "incomplete": compute_incomplete}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
