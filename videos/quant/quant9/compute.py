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

Added for the full lecture (all seeded; about ten CPU-minutes in all, the neural dual the longest):

* ``futures_basis``  Deribit's dated BTC futures, same hours (fetched through the data layer, checksummed in the
                   manifest): each future's price over the index against the forward that option parity implies;
* ``ftap``         the one-period market (bond; stock paying 80, 100, 125): state prices as the stock's price moves,
                   the zero-cost line, and the teaching simplex's pivots at prices 100 and 130;
* ``kernel``       Bitcoin's empirical pricing kernel: Q from the Surface's 16-day density over P from 16-day
                   returns (Binance daily closes, April 2021 to November 2025), with a stationary-bootstrap band;
* ``tree``         one-step replication, CRR convergence in N, exact replication along 1,000 paths, an American put;
* ``superlp``      the super-replication LP in the (bond, delta) plane solved by the teaching simplex, and its dual;
* ``completing``   a digital's no-arbitrage interval as traded calls are added; ``super_tree`` dynamic
                   super-replication on a trinomial tree against Black-Scholes;
* ``girsanov``     200,000 P-paths reweighted to Q; the effective sample size;
* ``free_lunch``   the doubling strategy run on a time-changed Brownian motion; the inverse Bessel bubble;
* ``numeraire``    N(d1) and N(d2) as probabilities; Margrabe by formula and by Monte Carlo under two numeraires; a
                   Surface call in dollars and in bitcoin;
* ``butterflies``  butterflies on raw quotes and on the SVI fit; butterflies of shrinking width become the density;
* ``density_fit``, ``density_specs``, ``density_term``  the SVI fit replayed; four specifications and their tails;
                   the density on every expiry, with the calendar check;
* ``ross_sweep``   power iteration, and recovery error against the strength of a permanent component (200 economies);
* ``mot_dual``, ``mot_claims``, ``mot_grid``, ``mot_entropic``  the model-free hedge, other claims, grid refinement
                   and entropic iterations;
* ``sv_sim``       Shleifer and Vishny's limits of arbitrage, simulated: forced liquidation against flow sensitivity;
* ``neural_mot``   a neural dual of the MOT upper bound, three seeds, against the LP.
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
    rows = A.implied_forward(deribit_trades(DAY, hours=surface.HOURS))  # (T, K/index, F/index marks, trades, expiry)
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


# ---------------------------------------------------------------------------
# The full lecture: new items
# ---------------------------------------------------------------------------
S3 = np.array([80.0, 100.0, 125.0])  # the one-period market of chapters 3-7: a bond and a stock paying these


def _ftap_lp(p_stock):
    """max t s.t. D psi = (1, p), psi_j - t - s_j = 0, all >= 0, as the teaching simplex's standard form."""
    D = np.vstack([np.ones(3), S3])
    Aeq = np.zeros((5, 7))
    Aeq[:2, :3], Aeq[2:, :3], Aeq[2:, 3], Aeq[2:, 4:] = D, np.eye(3), -1, -np.eye(3)
    c = np.zeros(7)
    c[3] = -1
    return A.simplex(c, Aeq, [1.0, p_stock, 0, 0, 0])


def compute_futures_basis() -> dict:
    from explainer.quant.data import deribit_trades
    fut = deribit_trades(DAY, hours=surface.HOURS, kind="future")
    par = {e["expiry"]: e for e in load("parity")["expiries"]}
    by = defaultdict(list)
    for t in fut:
        by[t["instrument_name"]].append((t["timestamp"] / 1e3, t["price"], t["index_price"]))
    rows, perp = [], None
    for name, tr in sorted(by.items()):
        s, px, ind = (np.array(c, float) for c in zip(*tr))
        ratio = px / ind
        if name.endswith("PERPETUAL"):
            perp = {"n": len(tr), "basis_bp": float(1e4 * (np.median(ratio) - 1))}
            continue
        from datetime import datetime, timezone
        exp = datetime.strptime(name.split("-")[1], "%d%b%y").replace(hour=8, tzinfo=timezone.utc)
        T = float(np.median((exp.timestamp() - s) / surface.YEAR))
        e = exp.strftime("%Y-%m-%d")
        r = {"name": name, "expiry": e, "T": T, "n": len(tr), "ratio": float(np.median(ratio)),
             "rate": float(np.log(np.median(ratio)) / T)}
        if e in par:
            r.update({"opt_ratio": par[e]["ratio"], "opt_rate": par[e]["rate"], "opt_n": par[e]["n"],
                      "gap_bp": float(1e4 * (r["ratio"] / par[e]["ratio"] - 1))})
        rows.append(r)
    gaps = [abs(r["gap_bp"]) for r in rows if "gap_bp" in r]
    return _json({"day": DAY, "n_trades": len(fut), "rows": rows, "perp": perp, "n_matched": len(gaps),
                  "gap_p50": float(np.median(gaps)), "gap_max": float(np.max(gaps))})


def compute_ftap() -> dict:
    D = np.vstack([np.ones(3), S3])
    prices = np.arange(81.0, 125.0, 1.0)
    psi = [A.ftap(D, [1.0, p])["psi"] for p in prices]
    out = {"prices": prices, "psi": np.array(psi)}
    for p in (100.0, 125.0, 130.0):
        r = A.ftap(D, [1.0, p])
        out[f"ftap_{int(p)}"] = {k: v for k, v in r.items()}
    for p in (100.0, 130.0):
        r = _ftap_lp(p)
        out[f"simplex_{int(p)}"] = {"status": r["status"], "x": r.get("x"), "farkas": r.get("farkas"),
                                    "steps": [{"phase": a, "enter": b, "leave": c, "obj": o, "x": x}
                                              for a, b, c, o, x in r["steps"]]}
    # the zero-cost line: theta = (S0, -1) pays S0 - s_j
    out["zero_cost_dir"] = {str(int(p)): (p - S3).tolist() for p in (100.0, 125.0, 130.0)}
    return _json(out)


def compute_kernel() -> dict:
    from scipy.stats import gaussian_kde
    from explainer.quant.data import binance_klines
    from explainer.quant.house import econ
    d = load("density")
    e = d["expiries"][0]                                    # the 16-day expiry
    K, q, F, T = np.asarray(e["K"]), np.asarray(e["density"]), e["F"], e["T"]
    S0 = d["S"]
    b = binance_klines("BTCUSDT", "1d", "2021-04", "2025-11")
    c = np.asarray(b["close"])
    h = int(round(T * 365))
    r = np.log(c[h::h] / c[:-h:h][:len(c[h::h])])           # non-overlapping h-day log returns
    grid = np.linspace(0.70 * F, 1.30 * F, 121)
    qg = np.interp(grid, K, q)

    def p_of(rs):
        kde = gaussian_kde(rs)
        return kde(np.log(grid / S0)) / grid                 # change of variables to the price at expiry

    pg = p_of(r)
    m = qg / pg
    curves = []

    def stat(rs):
        curves.append(qg / p_of(rs))
        return 0.0
    econ.stationary_bootstrap(r, stat, mean_block=3, B=1000, seed=9)
    M = np.array(curves)
    lo, hi = np.percentile(M, 5, axis=0), np.percentile(M, 95, axis=0)
    left, mid, right = (grid < 0.85 * F), (np.abs(grid / F - 1) < 0.03), (grid > 1.15 * F)
    ml, mm, mr = float(np.median(m[left])), float(np.median(m[mid])), float(np.median(m[right]))
    shape = "u" if (mr > mm and np.median(lo[right]) > np.median(hi[mid])) else ("decreasing" if ml > mm > mr else "other")
    return _json({"grid": grid, "q": qg, "p": pg, "m": m, "lo": lo, "hi": hi, "F": F, "S": S0, "T": T, "h_days": h,
                  "n_windows": int(len(r)), "mean_ret": float(np.mean(r)), "vol_ret": float(np.std(r)),
                  "m_left": ml, "m_mid": mm, "m_right": mr, "shape": shape,
                  "m_at_m20": float(np.interp(0.8 * F, grid, m)), "m_at_p20": float(np.interp(1.2 * F, grid, m))})


def compute_tree() -> dict:
    from explainer.quant.house import trees
    S0, K, sig = 100.0, 100.0, 0.25
    one = {"Su": 120.0, "Sd": 80.0, "Vu": 20.0, "Vd": 0.0}
    one["Delta"] = (one["Vu"] - one["Vd"]) / (one["Su"] - one["Sd"])
    one["B"] = one["Vd"] - one["Delta"] * one["Sd"]
    one["V"] = one["Delta"] * S0 + one["B"]
    one["q"] = (S0 - one["Sd"]) / (one["Su"] - one["Sd"])
    Ns = list(range(1, 201))
    prices = [trees.crr(S0, K, 1.0, sig, N=n)["price"] for n in Ns]
    bsp = float(bs.price(S0, K, 1.0, sig))
    four = trees.crr(S0, K, 1.0, sig, N=4)
    u, pq = four["u"], four["p"]
    L = {4: {"spots": S0 * u ** (2 * np.arange(5) - 4)}}       # the 4-step tree, every node's value and delta
    L[4]["values"] = np.maximum(L[4]["spots"] - K, 0)
    for n in range(3, -1, -1):
        sp = S0 * u ** (2 * np.arange(n + 1) - n)
        nxt = L[n + 1]
        L[n] = {"spots": sp, "values": pq * nxt["values"][1:] + (1 - pq) * nxt["values"][:-1],
                "delta": (nxt["values"][1:] - nxt["values"][:-1]) / (nxt["spots"][1:] - nxt["spots"][:-1])}
    # replicate along paths of the 4-step tree (real-world up-probability 0.6: the hedge does not care)
    g = np.random.default_rng(4)
    errs, ledger = [], None
    for k in range(1000):
        j, cash, shares = 0, four["price"], 0.0
        S = S0
        led = [(S, four["price"], 0.0)]
        for n in range(4):
            dlt = float(L[n]["delta"][j])
            cash -= (dlt - shares) * S
            shares = dlt
            up = g.random() < 0.6
            j += int(up)
            S = S0 * u ** (2 * j - (n + 1))
            led.append((S, cash + shares * S, shares))
        errs.append(abs(cash + shares * S - max(S - K, 0)))
        if k == 0:
            ledger = led
    # an American put (r = 5%): the nodes where exercising beats waiting
    r_, N = 0.05, 4
    dt = 1.0 / N
    uu = np.exp(sig * np.sqrt(dt))
    p = (np.exp(r_ * dt) - 1 / uu) / (uu - 1 / uu)
    V = np.maximum(K - S0 * uu ** (2 * np.arange(N + 1) - N), 0)
    ex_nodes = []
    for n in range(N - 1, -1, -1):
        Sn = S0 * uu ** (2 * np.arange(n + 1) - n)
        cont = np.exp(-r_ * dt) * (p * V[1:] + (1 - p) * V[:-1])
        ex = np.maximum(K - Sn, 0)
        for jj in np.where(ex > cont + 1e-12)[0]:
            ex_nodes.append({"n": n, "j": int(jj), "S": float(Sn[jj]), "exercise": float(ex[jj]), "hold": float(cont[jj])})
        V = np.maximum(cont, ex)
    am = float(V[0])
    eu = float(trees.crr(S0, K, 1.0, sig, r=r_, N=4, cp=-1)["price"])
    return _json({"one": one, "N": Ns, "prices": prices, "bs": bsp, "four_price": four["price"], "q": pq,
                  "layers": {str(n): {k: np.asarray(v).tolist() for k, v in L[n].items()} for n in L}, "u": u,
                  "rep_max_err": float(np.max(errs)), "rep_paths": 1000, "ledger": ledger, "am_put": am, "eu_put": eu,
                  "ex_nodes": ex_nodes})


def compute_superlp() -> dict:
    X = np.maximum(S3 - 100.0, 0)
    # min B + 100 Delta s.t. B + Delta s_j - e_j = X_j, B = B1 - B2, Delta = D1 - D2, all >= 0
    Aeq = np.hstack([np.ones((3, 1)), -np.ones((3, 1)), S3[:, None], -S3[:, None], -np.eye(3)])
    c = np.r_[1, -1, 100, -100, 0, 0, 0]
    r = A.simplex(c, Aeq, X)
    verts = [{"phase": a, "B": float(x[0] - x[1]), "Delta": float(x[2] - x[3]), "obj": float(c @ x)}
             for a, _, _, _, x in r["steps"]]
    # lower: max B + 100 Delta s.t. B + Delta s_j <= X_j
    Aeq2 = np.hstack([np.ones((3, 1)), -np.ones((3, 1)), S3[:, None], -S3[:, None], np.eye(3)])
    r2 = A.simplex(-c, Aeq2, X)
    h = A.superhedge(np.vstack([np.ones(3), S3]), [1.0, 100.0], X)
    # the dual over the risk-neutral segment q = (1 - a) (5/9, 0, 4/9) + a (0, 1, 0)
    a = np.linspace(0, 1, 101)
    q = np.outer(1 - a, [5 / 9, 0, 4 / 9]) + np.outer(a, [0, 1, 0])
    return _json({"X": X, "upper": r["fun"], "B": float(r["x"][0] - r["x"][1]), "Delta": float(r["x"][2] - r["x"][3]),
                  "lower": float(-r2["fun"]), "verts": verts, "highs_upper": h["upper"], "highs_lower": h["lower"],
                  "seg_a": a, "seg_q": q, "seg_value": q @ X})


def compute_completing() -> dict:
    n = 33
    z = np.linspace(-2.5, 2.5, n)
    S = np.exp(0.25 * z - 0.5 * 0.25 ** 2)
    w = np.exp(-z ** 2 / 2)
    w /= w.sum()
    S = S / np.dot(w, S)                                     # a martingale under w: the "true" Q
    target = (S > 1.1).astype(float)                         # a digital paying 1 above 1.1
    order = [1.0, 0.8, 1.25, 0.9, 1.1, 0.7, 1.4, 1.05, 0.95, 1.2]
    rows, strikes = [], []
    for k in [None] + order:
        if k is not None:
            strikes.append(k)
        Dm = [np.ones(n), S] + [np.maximum(S - kk, 0) for kk in strikes]
        p = [1.0, 1.0] + [float(np.dot(w, np.maximum(S - kk, 0))) for kk in strikes]
        h = A.superhedge(np.vstack(Dm), np.array(p), target)
        rows.append({"n_strikes": len(strikes), "strike": k, "lower": max(h["lower"], 0.0), "upper": h["upper"]})
    return _json({"S": S, "w": w, "true": float(np.dot(w, target)), "rows": rows})


def compute_super_tree() -> dict:
    Ns = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    up = [A.superhedge_tree(100, 100, 1.0, 0.25, N)["upper"] for N in Ns]
    lo = [A.superhedge_tree(100, 100, 1.0, 0.25, N)["lower"] for N in Ns]
    return _json({"N": Ns, "upper": up, "lower": lo, "bs": float(bs.price(100, 100, 1.0, 0.25)),
                  "bs20": float(bs.price(100, 100, 1.0, 0.20))})


def compute_girsanov() -> dict:
    mu, sig, T, S0, K, n = 0.10, 0.25, 1.0, 100.0, 100.0, 200_000
    lam = mu / sig
    g = np.random.default_rng(5)
    W = g.standard_normal(n) * np.sqrt(T)
    ST = S0 * np.exp((mu - 0.5 * sig ** 2) * T + sig * W)
    Z = np.exp(-lam * W - 0.5 * lam ** 2 * T)
    pay = np.maximum(ST - K, 0)
    naive = float(pay.mean())
    wp = Z * pay
    ess = float(Z.sum() ** 2 / (Z ** 2).sum() / n)
    lam2 = 0.60 / sig
    Z2 = np.exp(-lam2 * W - 0.5 * lam2 ** 2 * T)
    ess2 = float(Z2.sum() ** 2 / (Z2 ** 2).sum() / n)
    # 150 paths to draw, 50 steps
    m, steps = 150, 50
    dW = g.standard_normal((m, steps)) * np.sqrt(T / steps)
    Wp = np.c_[np.zeros(m), np.cumsum(dW, 1)]
    t = np.linspace(0, T, steps + 1)
    paths = S0 * np.exp((mu - 0.5 * sig ** 2) * t + sig * Wp)
    Zp = np.exp(-lam * Wp[:, -1] - 0.5 * lam ** 2 * T)
    mean_P = paths.mean(0)
    mean_Q = (paths * Zp[:, None]).sum(0) / Zp.sum()
    return _json({"mu": mu, "sigma": sig, "lam": lam, "n": n, "price_weighted": float(wp.mean()),
                  "se": float(wp.std() / np.sqrt(n)), "price_naive": naive, "bs": float(bs.price(S0, K, T, sig)),
                  "ess": ess, "ess_pred": float(np.exp(-lam ** 2 * T)), "ess60": ess2, "ess60_pred": float(np.exp(-lam2 ** 2 * T)),
                  "t": t, "paths": paths, "Zp": Zp, "mean_P": mean_P, "mean_Q": mean_Q, "ST": ST[:20000], "Z": Z[:20000]})


def compute_free_lunch() -> dict:
    from scipy.stats import norm
    g = np.random.default_rng(10)
    # the doubler: X is a Brownian motion run on the clock ln(T / (T - t)); stop when it first reaches +1
    n, dt, L = 20000, 0.05, 2500.0
    X = np.zeros(n)
    mn = np.zeros(n)
    alive = np.ones(n, bool)
    hit_clock = np.full(n, np.inf)
    k = 0
    while alive.any() and k * dt < L:
        idx = np.where(alive)[0]
        X[idx] += g.standard_normal(len(idx)) * np.sqrt(dt)
        mn[idx] = np.minimum(mn[idx], X[idx])
        k += 1
        done = idx[X[idx] >= 1.0]
        hit_clock[done] = k * dt
        alive[done] = False
    ks = [1, 3, 10]
    frac = {str(kk): float(np.mean(mn < -kk)) for kk in ks}
    # 120 paths to draw, on the clock up to 60, mapped to real time t = T (1 - e^{-clock}), T = 1
    m, dtd, Ld = 120, 0.02, 60.0
    steps = int(Ld / dtd)
    Y = np.c_[np.zeros(m), np.cumsum(g.standard_normal((m, steps)) * np.sqrt(dtd), 1)]
    stop = np.argmax(Y >= 1.0, axis=1)
    stop[(Y < 1.0).all(1)] = steps
    clock = np.arange(steps + 1) * dtd
    sel = np.unique(np.r_[np.arange(0, 400, 2), np.arange(400, steps + 1, 25)])
    draw = [Y[i, sel[sel <= stop[i]]].tolist() for i in range(m)]
    # the inverse Bessel bubble: S = 1 / |B|, B a 3-d Brownian motion from (1, 0, 0)
    bub = {}
    for T in (0.25, 1.0, 4.0):
        B = np.array([1.0, 0, 0]) + np.sqrt(T) * g.standard_normal((2_000_000, 3))
        s = 1 / np.linalg.norm(B, axis=1)
        bub[str(T)] = {"mc": float(s.mean()), "se": float(s.std() / np.sqrt(len(s))), "exact": float(2 * norm.cdf(1 / np.sqrt(T)) - 1)}
    mb, sb = 100, 100
    tb = np.linspace(0, 1, sb + 1)
    inc = g.standard_normal((mb, sb, 3)) * np.sqrt(1 / sb)
    Bp = np.array([1.0, 0, 0]) + np.concatenate([np.zeros((mb, 1, 3)), np.cumsum(inc, 1)], 1)
    Sp = 1 / np.linalg.norm(Bp, axis=2)
    mean_exact = 2 * norm.cdf(1 / np.sqrt(np.maximum(tb, 1e-9))) - 1
    return _json({"n": n, "frac": frac, "frac_exact": {str(kk): 1 / (1 + kk) for kk in ks},
                  "unhit": float(alive.mean()), "clock_max": L, "draw_clock": clock[sel].tolist(), "draw": draw,
                  "draw_stop": stop.tolist(), "bubble": bub, "bub_t": tb, "bub_paths": Sp, "bub_mean": mean_exact})


def compute_numeraire() -> dict:
    from scipy.stats import norm
    S0, K, T, sig = 100.0, 100.0, 1.0, 0.25
    d1 = (np.log(S0 / K) + 0.5 * sig ** 2 * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    out = {"Nd1": float(norm.cdf(d1)), "Nd2": float(norm.cdf(d2)), "call": float(bs.price(S0, K, T, sig))}
    # Margrabe: exchange S2 for S1
    s1 = s2 = 0.30
    rho = 0.5
    sR = np.sqrt(s1 ** 2 + s2 ** 2 - 2 * rho * s1 * s2)
    form = float(100 * bs.price(1.0, 1.0, T, sR))
    g = np.random.default_rng(11)
    n = 1_000_000
    z1 = g.standard_normal(n)
    z2 = rho * z1 + np.sqrt(1 - rho ** 2) * g.standard_normal(n)
    A1 = 100 * np.exp(-0.5 * s1 ** 2 * T + s1 * np.sqrt(T) * z1)
    A2 = 100 * np.exp(-0.5 * s2 ** 2 * T + s2 * np.sqrt(T) * z2)
    pq = np.maximum(A1 - A2, 0)
    R = np.exp(-0.5 * sR ** 2 * T + sR * np.sqrt(T) * g.standard_normal(n))
    ps = 100 * np.maximum(R - 1, 0)
    out.update({"sR": float(sR), "margrabe": form, "mc_Q": float(pq.mean()), "se_Q": float(pq.std() / np.sqrt(n)),
                "mc_S2": float(ps.mean()), "se_S2": float(ps.std() / np.sqrt(n))})
    # a Surface call (107 days, at the forward) in dollars and in bitcoin
    e = load("density")["expiries"][1]
    Kg, q, F = np.asarray(e["K"]), np.asarray(e["density"]), e["F"]
    q = q / np.trapezoid(q, Kg)
    Kc = round(F / 5000) * 5000
    usd = float(np.trapezoid(np.maximum(Kg - Kc, 0) * q, Kg))
    qb = q * Kg / np.trapezoid(q * Kg, Kg)                   # the bitcoin measure: density times s / F
    btc = float(np.trapezoid(np.maximum(Kg - Kc, 0) / Kg * qb, Kg))
    out.update({"K_btc": float(Kc), "F_btc": float(F), "usd": usd, "btc": btc, "btc_times_F": float(btc * np.trapezoid(q * Kg, Kg)),
                "Q_itm": float(np.trapezoid(q[Kg > Kc], Kg[Kg > Kc])), "QB_itm": float(np.trapezoid(qb[Kg > Kc], Kg[Kg > Kc]))})
    return _json(out)


def compute_butterflies() -> dict:
    from explainer.quant.data import deribit_trades
    q = surface.build(DAY)
    d = load("density")
    a = d["expiries"][0]
    e, F, T = a["expiry"], a["F"], a["T"]
    m = np.array([x == e for x in q["expiry"]])
    K = q["K"][m]
    o = np.argsort(K)
    K, iv = K[o], q["iv"][m][o]
    C_mark = bs.price(F, K, T, iv, 0.0, 0.0, 1)               # from the Surface's quotes (Deribit marks)
    mark_chk = A.static_checks(K, C_mark, F)
    # raw trade prices: each instrument's median trade price (BTC) times the forward, puts turned into calls by parity
    tr = deribit_trades(DAY, hours=surface.HOURS)
    by = defaultdict(list)
    for t in tr:
        ex, k_, cp = surface.parse_instrument(t["instrument_name"])
        if ex.strftime("%Y-%m-%d") == e:
            by[(k_, cp)].append(t["price"] * F)
    raw = {}
    for (k_, cp), v in by.items():
        c = float(np.median(v)) + (0 if cp == 1 else F - k_)
        if (cp == 1) == (k_ >= F):                          # out of the money only, as the Surface
            raw[k_] = c
    Kr = np.array(sorted(raw))
    Cr = np.array([raw[k_] for k_ in Kr])
    raw_chk = A.static_checks(Kr, Cr, F)
    svi = a["svi"]
    Kf = np.linspace(0.6 * F, 1.5 * F, 901)
    svi_chk = A.static_checks(Kf, smile.call_prices(svi, F, T, Kf), F)
    # butterflies of shrinking width over the strike axis: (C(K-h) - 2C(K) + C(K+h)) / h^2
    flies = {}
    for h in (8000.0, 4000.0, 2000.0, 1000.0, 500.0):
        Kc = np.arange(0.7 * F, 1.3 * F + 1, h)
        flies[str(int(h))] = {"K": Kc, "q": (smile.call_prices(svi, F, T, Kc - h) - 2 * smile.call_prices(svi, F, T, Kc)
                                             + smile.call_prices(svi, F, T, Kc + h)) / h ** 2}
    dig = -np.gradient(smile.call_prices(svi, F, T, Kf), Kf)
    return _json({"expiry": e, "F": F, "T": T, "K_mark": K, "C_mark": C_mark, "mark_fly": len(mark_chk["butterfly"]),
                  "mark_mono": len(mark_chk["monotone"]), "K_raw": Kr, "C_raw": Cr, "raw_fly": len(raw_chk["butterfly"]),
                  "raw_mono": len(raw_chk["monotone"]), "raw_fly_at": [float(Kr[i + 1]) for i in raw_chk["butterfly"]],
                  "svi_fly": len(svi_chk["butterfly"]), "svi_ok": svi_chk["ok"], "flies": flies, "Kf": Kf,
                  "Cf": smile.call_prices(svi, F, T, Kf), "digital": dig, "mass": a["mass"], "mean": a["mean"]})


def _svi_resid(k, w, wt):
    def resid(p):
        return np.sqrt(wt) * (smile.svi_total_variance(k, *p) - w)
    return resid


def compute_density_fit() -> dict:
    from scipy import optimize
    q = surface.build(DAY)
    e = load("density")["expiries"][1]
    m = np.array([x == e["expiry"] for x in q["expiry"]])
    k, iv, T, F, vg = q["k"][m], q["iv"][m], e["T"], e["F"], q["vega"][m]
    w = iv ** 2 * T
    res = _svi_resid(k, w, vg)
    p0 = [max(w.min() * 0.5, 1e-4), 0.1, -0.2, 0.0, 0.2]
    lo = [-w.max(), 1e-6, -0.999, -1.0, 1e-3]
    hi = [w.max() * 2, 2.0 / (1 + 0.999), 0.999, 1.0, 2.0]
    ck = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50, 64, 80, 100, 150, 200]
    kk = np.linspace(-0.7, 0.6, 131)
    Kd = F * np.exp(kk)
    Kg = np.linspace(0.3 * F, 2.2 * F, 600)
    steps = []
    for n in ck:
        r = optimize.least_squares(res, p0, bounds=(lo, hi), max_nfev=n)
        p = dict(zip(("a", "b", "rho", "m", "s"), r.x))
        ivm = smile.svi_iv(p, k, T)
        rmse = float(np.sqrt(np.sum(vg * (ivm - iv) ** 2) / np.sum(vg)) * 100)
        steps.append({"nfev": n, "rmse": rmse, "iv": smile.svi_iv(p, kk, T), "dens": smile.risk_neutral_density(p, F, T, Kg)})
    return _json({"expiry": e["expiry"], "T": T, "F": F, "k": k, "iv": iv, "kk": kk, "Kd": Kd, "Kg": Kg, "steps": steps})


def _mix_price(par, F, K, T, n):
    w = np.abs(par[:n]) / np.abs(par[:n]).sum()
    f = np.exp(par[n:2 * n])
    f = f * F / np.dot(w, f)                                  # the mixture's mean is the forward
    s = np.abs(par[2 * n:3 * n]) + 0.05
    return sum(w[i] * bs.price(f[i], K, T, s[i], 0.0, 0.0, 1) for i in range(n)), (w, f, s)


def compute_density_specs() -> dict:
    from scipy import interpolate, optimize
    q = surface.build(DAY)
    e = load("density")["expiries"][1]
    m = np.array([x == e["expiry"] for x in q["expiry"]])
    k, iv, T, F, vg = q["k"][m], q["iv"][m], e["T"], e["F"], q["vega"][m]
    Kq = F * np.exp(k)
    Kg = np.linspace(0.3 * F, 2.2 * F, 1901)
    out = {"expiry": e["expiry"], "T": T, "F": F, "specs": []}

    def summarize(name, Cg, ivq):
        h = Kg[1] - Kg[0]
        dens = np.zeros_like(Cg)
        dens[1:-1] = (Cg[2:] - 2 * Cg[1:-1] + Cg[:-2]) / h ** 2
        neg = float(-np.trapezoid(np.minimum(dens, 0), Kg))
        dp = np.maximum(dens, 0)
        rm = float(np.sqrt(np.sum(vg * (ivq - iv) ** 2) / np.sum(vg)) * 100)
        out["specs"].append({"name": name, "rmse": rm, "dens": dp, "neg_mass": neg,
                             "down30": float(np.trapezoid(dp[Kg < 0.7 * F], Kg[Kg < 0.7 * F])),
                             "down20": float(np.trapezoid(dp[Kg < 0.8 * F], Kg[Kg < 0.8 * F])),
                             "up30": float(np.trapezoid(dp[Kg > 1.3 * F], Kg[Kg > 1.3 * F]))})
    svi = e["svi"]
    summarize("svi", smile.call_prices(svi, F, T, Kg), smile.svi_iv(svi, k, T))
    o = np.argsort(k)
    sp = interpolate.UnivariateSpline(k[o], iv[o], w=np.sqrt(vg[o] / vg.max()), k=3, s=len(k) * 1e-4)
    kg = np.log(Kg / F)
    ivg = sp(np.clip(kg, k.min(), k.max()))                   # flat beyond the last quote
    summarize("spline", bs.price(F, Kg, T, ivg, 0.0, 0.0, 1), sp(k))
    C_q = bs.price(F, Kq, T, iv, 0.0, 0.0, 1)
    for n in (2, 3):
        best = None
        g = np.random.default_rng(12)
        for start in range(6):
            p0 = np.r_[np.ones(n), np.log(F) + 0.2 * g.standard_normal(n), 0.2 + 0.4 * g.random(n)]
            r = optimize.least_squares(lambda pp: np.sqrt(vg) * (_mix_price(pp, F, Kq, T, n)[0] - C_q) / F, p0,
                                       max_nfev=3000)
            if best is None or r.cost < best.cost:
                best = r
        Cm = _mix_price(best.x, F, Kg, T, n)[0]
        ivm = bs.implied_vol(_mix_price(best.x, F, Kq, T, n)[0], F, Kq, T, 0.0, 0.0, 1)
        summarize(f"mix{n}", Cm, ivm)
    d30 = [s["down30"] for s in out["specs"]]
    out.update({"Kg": Kg, "down30_spread": float(max(d30) - min(d30)), "rmse_max": max(s["rmse"] for s in out["specs"])})
    return _json(out)


def compute_density_term() -> dict:
    q = surface.build(DAY)
    S0 = q["S"]
    x = np.linspace(0.4, 1.8, 281)
    ridges, svis = [], []
    for ex in q["expiries"]:
        if ex["n"] < 6 or ex["T"] < 5 / 365:
            continue
        m, T, F, p = _fit_expiry(q, ex["expiry"])
        K = x * S0
        dens = smile.risk_neutral_density(p, F, T, np.linspace(x[0] * S0, x[-1] * S0, len(x)))
        ridges.append({"expiry": ex["expiry"], "T": T, "F": F, "dens": dens * S0, "atm": float(smile.svi_iv(p, 0.0, T))})
        svis.append((T, p))
    kk = np.linspace(-0.5, 0.5, 101)
    viol = []
    for (T1, p1), (T2, p2) in zip(svis, svis[1:]):
        w1 = smile.svi_total_variance(kk, *[p1[c] for c in ("a", "b", "rho", "m", "s")])
        w2 = smile.svi_total_variance(kk, *[p2[c] for c in ("a", "b", "rho", "m", "s")])
        viol.append(len(A.calendar_check(kk, w1, w2)))
    return _json({"x": x, "S": S0, "ridges": ridges, "calendar": viol, "n_pairs": len(viol),
                  "calendar_total": int(sum(viol))})


def _ross_economy(rng=None, n=9, strength=1.0, base=None):
    if base is None:
        c = np.exp(np.linspace(-0.2, 0.2, n))
        pi = np.exp(-((np.arange(n)[:, None] * 0.8 + n * 0.1 - np.arange(n)[None, :]) ** 2) / 3.0)
        delta, gamma = 0.98, 3.0
    else:
        c, pi, delta, gamma = base
    pi = pi / pi.sum(axis=1, keepdims=True)
    P = delta * pi * (c[None, :] / c[:, None]) ** (-gamma)
    tilt = np.exp(-0.6 * strength * np.linspace(-1, 1, n))
    tilt = tilt / (pi @ tilt)[:, None]
    P2 = P * tilt
    return pi, P2


def compute_ross_sweep() -> dict:
    r = load("ross")
    P = np.asarray(r["P"])
    pit = A.power_iteration(P, 60)
    strengths = np.linspace(0, 1, 11)
    one = []
    for s in strengths:
        pi, P2 = _ross_economy(strength=s)
        one.append(float(np.max(np.abs(A.ross_recovery(P2)["F"] - pi))))
    g = np.random.default_rng(15)
    many = []
    for _ in range(200):
        n = 9
        c = np.exp(np.linspace(-1, 1, n) * g.uniform(0.1, 0.3))
        rho = g.uniform(0.5, 0.95)
        width = g.uniform(1.0, 5.0)
        mid = (n - 1) / 2
        pi = np.exp(-((mid + rho * (np.arange(n)[:, None] - mid) - np.arange(n)[None, :]) ** 2) / width)
        base = (c, pi, g.uniform(0.95, 0.99), g.uniform(1.0, 6.0))
        row = []
        for s in strengths:
            pi_, P2 = _ross_economy(strength=s, base=base)
            row.append(float(np.max(np.abs(A.ross_recovery(P2)["F"] - pi_))))
        many.append(row)
    many = np.array(many)
    return _json({"z": pit["z"], "delta_iter": pit["delta"], "delta": r["delta"], "strengths": strengths, "err_one": one,
                  "err_lo": np.percentile(many, 5, axis=0), "err_hi": np.percentile(many, 95, axis=0),
                  "err_med": np.median(many, axis=0), "n_econ": len(many)})


def _mot_marginals(nb1, nb2):
    d = load("density")
    a, b = d["expiries"]
    grids = []
    for e, nb in ((a, nb1), (b, nb2)):
        K, dens = np.asarray(e["K"]), np.asarray(e["density"])
        x = K / e["F"]
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
    x, y = x / np.dot(x, mu), y / np.dot(y, nu)
    ks = np.linspace(0.3, 2.5, 400)
    gap = min(float(np.dot(nu, np.maximum(y - k, 0)) - np.dot(mu, np.maximum(x - k, 0))) for k in ks)
    return x, mu, y, nu, gap


def _straddle(s1, s2):
    return abs(s2 / s1 - 1)


def compute_mot_dual() -> dict:
    m = load("mot")
    x, mu, y, nu = (np.asarray(m[k]) for k in ("x", "mu", "y", "nu"))
    up = A.mot_dual(x, mu, y, nu, _straddle, sign=-1.0)
    lo = A.mot_dual(x, mu, y, nu, _straddle, sign=1.0)
    out = {"x": x, "y": y, "mu": mu, "nu": nu}
    for nm, r in (("up", up), ("lo", lo)):
        out[nm] = {"value": r["value"], "dual_value": r["dual_value"], "u": r["u"], "v": r["v"], "h": r["h"],
                   "slack": r["slack"], "pi": r["pi"]}
    return _json(out)


def compute_mot_claims() -> dict:
    m = load("mot")
    x, mu, y, nu = (np.asarray(m[k]) for k in ("x", "mu", "y", "nu"))
    claims = {"straddle": _straddle, "fwd_call": lambda a, b: max(b / a - 1, 0.0), "sq": lambda a, b: (b - a) ** 2,
              "logsq": lambda a, b: np.log(b / a) ** 2}
    out = {}
    for k, c in claims.items():
        r = A.mot_bounds(x, mu, y, nu, c)
        out[k] = {"lower": r["lower"], "upper": r["upper"]}
    out["sq_exact"] = float(np.dot(nu, y ** 2) - np.dot(mu, x ** 2))
    return _json(out)


def compute_mot_grid() -> dict:
    rows = []
    for nb1, nb2 in ((9, 25), (13, 41), (17, 57), (25, 81), (33, 121), (41, 161), (49, 201)):
        x, mu, y, nu, gap = _mot_marginals(nb1, nb2)
        row = {"bins1": nb1, "bins2": nb2, "atoms1": len(x), "atoms2": len(y), "gap": gap}
        if gap >= -1e-9:
            r = A.mot_bounds(x, mu, y, nu, _straddle)
            row.update({"lower": r["lower"], "upper": r["upper"]})
        rows.append(row)
    return _json({"rows": rows})


def compute_mot_entropic() -> dict:
    m = load("mot")
    x, mu, y, nu = (np.asarray(m[k]) for k in ("x", "mu", "y", "nu"))
    out = {"lp_upper": m["upper"], "lp_lower": m["lower"], "runs": []}
    for eps in (0.1, 0.03, 0.01, 0.003):
        for sign in (-1.0, 1.0):
            r = A.entropic_mot(x, mu, y, nu, _straddle, eps=eps, iters=2000, sign=sign, log_every=20)
            out["runs"].append({"eps": eps, "side": "upper" if sign < 0 else "lower", "value": r["value"],
                                "trace": r["trace"], "pi": r["pi"] if sign < 0 else None})
    return _json(out)


def compute_sv_sim() -> dict:
    """Shleifer and Vishny (1997), simulated: a mispricing D that is certain to close by date T (a Brownian bridge
    to zero), a fund that holds the convergence trade at leverage L, investors who withdraw a times the fund's loss
    (and add a times its gain), and a margin rule that liquidates the fund when equity falls below half its start."""
    T, sig, L, floor, n = 20, 0.012, 6.0, 0.5, 1000
    out = {"T": T, "sigma": sig, "L": L, "floor": floor, "rows": [], "examples": {}}
    for a in (0.0, 0.5, 1.0, 2.0):
        g = np.random.default_rng(16)
        liq, d_at_liq, d_max = 0, [], []
        ex = []
        for path in range(n):
            D, E, cap = 0.0, 1.0, 1.0
            Ds, Es, Ps = [0.0], [1.0], [L]
            dead = False
            for t in range(T):
                dD = -D / (T - t) + sig * g.standard_normal() * (1.0 if t < T - 1 else 0.0)
                Dn = D + dD if t < T - 1 else 0.0
                pnl = cap * L * (-(Dn - D))                   # the trade gains as the spread closes
                ret = pnl / cap
                E = E + pnl
                cap = max(cap + pnl + a * ret * cap, 0.0)       # capital under management: performance-based flows
                D = Dn
                Ds.append(D); Es.append(cap); Ps.append(0.0 if dead else L * cap)
                if cap < floor and not dead:
                    dead = True
                    liq += 1
                    d_at_liq.append(D)
                    break
            d_max.append(max(Ds))
            if path < 3:
                ex.append({"D": Ds, "cap": Es, "dead": dead})
        out["rows"].append({"a": a, "p_liq": liq / n, "d_at_liq": float(np.mean(d_at_liq)) if d_at_liq else None,
                            "d_max_mean": float(np.mean(d_max))})
        out["examples"][str(a)] = ex
    return _json(out)


def compute_neural_mot() -> dict:
    import torch
    from explainer.quant.house import deep
    torch.set_num_threads(1)
    m = load("mot")
    x, mu, y, nu = (np.asarray(m[k]) for k in ("x", "mu", "y", "nu"))
    params = {"steps": 10000, "gamma": 3000.0, "width": 64, "lr": 1e-2, "seeds": [0, 1, 2]}
    part = CACHE.partial("neural_mot", params)
    gx, gy = np.linspace(0.6, 1.5, 28), np.linspace(0.4, 2.0, 36)
    snaps = [0, 100, 300, 1000, 3000, 10000]
    for s in params["seeds"]:
        if str(s) in part:
            continue
        r = deep.mot_neural(x, mu, y, nu, _straddle, steps=params["steps"], gamma=params["gamma"], width=params["width"],
                            lr=params["lr"], seed=s, log_every=50, snapshots=snaps, grid=(gx, gy))
        part[str(s)] = {"trace": r["trace"].tolist(), "bound": r["bound"], "violation": r["violation"],
                        "snaps": {str(k): v.tolist() for k, v in r["snapshots"].items()}}
    runs = [part[str(s)] for s in params["seeds"]]
    bounds = [r_["bound"] for r_ in runs]
    return _json({**params, "lp": m["upper"], "gx": gx, "gy": gy, "snap_steps": snaps, "runs": runs, "bounds": bounds,
                  "gap_pct": [100 * (b / m["upper"] - 1) for b in bounds]})


ITEMS = {"envelope": compute_envelope, "parity": compute_parity, "density": compute_density, "mot": compute_mot,
         "ross": compute_ross, "incomplete": compute_incomplete, "futures_basis": compute_futures_basis,
         "ftap": compute_ftap, "kernel": compute_kernel, "tree": compute_tree, "superlp": compute_superlp,
         "completing": compute_completing, "super_tree": compute_super_tree, "girsanov": compute_girsanov,
         "free_lunch": compute_free_lunch, "numeraire": compute_numeraire, "butterflies": compute_butterflies,
         "density_fit": compute_density_fit, "density_specs": compute_density_specs,
         "density_term": compute_density_term, "ross_sweep": compute_ross_sweep, "mot_dual": compute_mot_dual,
         "mot_claims": compute_mot_claims, "mot_grid": compute_mot_grid, "mot_entropic": compute_mot_entropic,
         "sv_sim": compute_sv_sim, "neural_mot": compute_neural_mot}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
