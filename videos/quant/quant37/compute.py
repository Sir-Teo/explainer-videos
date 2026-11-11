"""Every number in Part 37 (Market Impact and Execution), computed and cached in .cache/quant37/.

    python -m videos.quant.quant37.compute [items] [--force]

Data: Binance's public aggregated trades for the BTCUSDT perpetual, 16-25 May 2023 (ten days), its best-quote stream
on 16, 17, 20 and 21 May (Part 36's grid), and one-minute bars for 2023 (Part 35's loader). Models: the latent book,
Almgren-Chriss, decay kernels, and the House's queue-reactive simulator.

* ``aggregate``   aggregate impact: the price change over windows against the signed volume imbalance, and against
                  the signed volume itself (log-log slope);
* ``propagator``  the response function R(l), the sign autocorrelation and the fitted propagator G(l) in event time,
                  with power-law exponents against the diffusivity condition beta = (1 - gamma)/2;
* ``latent``      a metaorder in the latent order book: impact against size at a fixed duration (linear, then square
                  root) and the decay after the order stops;
* ``ac``          Almgren-Chriss schedules and the efficient frontier, for a Bitcoin-sized example;
* ``kernels``     optimal schedules under exponential, power-law and non-convex decay kernels; round trips;
* ``ow``          Obizhaeva-Wang: the discrete optimum against the closed form as the grid refines;
* ``rl``          a Q-learning executor in the queue-reactive simulator against TWAP, a dump and heuristics;
* ``volume``      the intraday volume curve (VWAP schedule) and participation;
* ``resilience``  the book after sweeps on Bitcoin: how fast the best queues refill, and whether the price reverts;
* ``research``    Obizhaeva-Wang against TWAP by resilience, the Fredholm residual, and the optimal schedule under
                  Bitcoin's fitted power-law propagator.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import execution as E, lob as L, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant37")
load = pit.counted(CACHE.load, 37)
DAYS = tuple(f"2023-05-{k:02d}" for k in range(16, 26))
BOOK_DAYS = ("2023-05-16", "2023-05-17", "2023-05-20", "2023-05-21")
TICK = 0.1


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _trades(day):
    return data.binance_aggtrades_day("BTCUSDT", day)


def compute_aggregate() -> dict:
    out = {"phi": {}}
    Qs, Ds, Vday, sig = [], [], [], []
    for w, name in ((10000, "10 s"), (60000, "1 min"), (300000, "5 min")):
        cs, ms, ns = [], [], []
        for d in DAYS:
            a = _trades(d)
            c, m, se, n = E.aggregate_impact(a["time"], a["price"] / TICK, a["qty"], a["sign"], w, bins=10)
            cs.append(c), ms.append(m), ns.append(n)
        # pool the days, weighting each bin by its count
        cen = np.linspace(-0.9, 0.9, 10)
        mm = []
        for j in range(10):
            num = sum(float(m[np.argmin(np.abs(c - cen[j]))] * n[np.argmin(np.abs(c - cen[j]))]) for c, m, n in
                      zip(cs, ms, ns) if len(c) and np.min(np.abs(c - cen[j])) < 0.1)
            den = sum(float(n[np.argmin(np.abs(c - cen[j]))]) for c, m, n in zip(cs, ms, ns) if len(c) and
                      np.min(np.abs(c - cen[j])) < 0.1)
            mm.append(num / den if den else float("nan"))
        out["phi"][name] = {"centers": cen, "mean": mm}
    for d in DAYS:
        a = _trades(d)
        t = a["time"]
        k = ((t - t[0]) // 60000).astype(int)
        q = a["qty"] * a["sign"]
        Q = np.bincount(k, weights=q)
        last = np.zeros(k[-1] + 1, int)
        last[k] = np.arange(len(k))
        p = a["price"] / TICK
        Qs.append(Q[1:])
        Ds.append(np.diff(p[last]))
        Vday.append(float(a["qty"].sum()))
        sig.append(float(np.std(np.diff(p[last]))))
    Q, dp = np.concatenate(Qs), np.concatenate(Ds)
    edges = np.quantile(np.abs(Q), np.linspace(0, 1, 11))
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        k = (np.abs(Q) >= lo) & (np.abs(Q) <= hi)
        rows.append({"q": float(np.median(np.abs(Q[k]))), "impact": float(np.mean(dp[k] * np.sign(Q[k]))),
                     "se": float(np.std(dp[k]) / math.sqrt(k.sum())), "n": int(k.sum())})
    x = np.log([r["q"] for r in rows[1:]])
    y = np.log([r["impact"] for r in rows[1:]])
    slope = float(np.polyfit(x, y, 1)[0])
    return _json({"phi": out["phi"], "size": rows, "slope": slope, "v_day": float(np.mean(Vday)),
                  "sigma_min": float(np.mean(sig)), "n_min": int(len(Q))})


def _mids_at_trades(day):
    b = data.binance_book_day("BTCUSDT", day)
    a = _trades(day)
    m = L.mid(b) / TICK
    gi = np.clip(np.searchsorted(b["time"], a["time"], side="right") - 2, 0, len(m) - 1)
    return m[gi], a["sign"]


def compute_propagator() -> dict:
    ps, ss = [], []
    off = 0.0
    for d in BOOK_DAYS:
        p, s = _mids_at_trades(d)
        ps.append(p - p[0] + off)
        off = ps[-1][-1]
        ss.append(s)
    p, s = np.concatenate(ps), np.concatenate(ss)
    lags = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
    R = E.response_function(p, s, lags)
    acf = L.sign_acf(s, lags)
    g, G = E.propagator_fit(p, s, n_lag=1000)
    ok = (np.array(lags) >= 10) & (np.array(lags) <= 1000) & (acf > 0)
    gamma = float(-np.polyfit(np.log(np.array(lags)[ok]), np.log(acf[ok]), 1)[0])
    ll = np.arange(100, 1001)
    beta = float(-np.polyfit(np.log(ll), np.log(np.maximum(G[ll], 1e-9)), 1)[0])
    return _json({"lags": lags, "R": R, "acf": acf, "G": G[:1001:5], "G_lags": np.arange(0, 1001, 5), "gamma": gamma,
                  "beta": beta, "beta_theory": (1 - gamma) / 2, "G_peak": float(G.max()),
                  "G_peak_lag": int(np.argmax(G)), "n": int(len(p))})


def compute_latent() -> dict:
    sizes = np.logspace(-2, 3, 16)
    rows = []
    for Q in sizes:
        out = E.latent_book(rate=float(Q), t_exec=1.0, L=1.0, D=1.0, half_width=60.0, nx=1201, record=50)
        rows.append({"Q": float(out["Q"]), "I": float(out["p"][-1])})
    path = E.latent_book(rate=50.0, t_exec=1.0, t_after=9.0, L=1.0, D=1.0, half_width=60.0, nx=1201, record=300)
    x = np.log([r["Q"] for r in rows])
    y = np.log([r["I"] for r in rows])
    lo = float(np.polyfit(x[:4], y[:4], 1)[0])
    hi = float(np.polyfit(x[-4:], y[-4:], 1)[0])
    return _json({"rows": rows, "slope_small": lo, "slope_large": hi, "path_t": path["t"], "path_p": path["p"],
                  "path_Q": path["Q"]})


def compute_ac() -> dict:
    ag = load("aggregate")
    sigma = ag["sigma_min"] * TICK                    # dollars per minute
    X, T, n = 5000.0, 60.0, 60                        # 5,000 BTC over an hour, minute by minute
    # temporary impact from the minute flows: a minute's signed volume of about q BTC moves the price by I(q); an
    # executor pays on average half the move it causes, so eta = I(q)/(2q) dollars per BTC per (BTC a minute)
    row = min(ag["size"], key=lambda r: abs(r["q"] - 100.0))
    eta = 0.5 * row["impact"] * TICK / row["q"]
    gamma = 0.0
    lams = np.logspace(-9, -4, 26)
    front = [E.almgren_chriss(X, T, n, sigma, eta, float(lm), gamma) for lm in lams]
    show = {}
    for lm in (0.0, 1e-7, 1e-6, 1e-5):
        r = E.almgren_chriss(X, T, n, sigma, eta, lm, gamma)
        show[f"{lm:g}"] = {"x": r["x"], "cost": r["cost"], "sd": math.sqrt(r["var"])}
    return _json({"X": X, "T": T, "n": n, "sigma": sigma, "eta": eta, "lams": lams,
                  "cost": [f["cost"] for f in front], "sd": [math.sqrt(f["var"]) for f in front], "show": show,
                  "price": float(np.median(_trades(DAYS[1])["price"])), "v_day": ag["v_day"],
                  "sigma_day": sigma * math.sqrt(1440), "eta_q": row["q"], "eta_impact": row["impact"]})


def compute_kernels() -> dict:
    n, T, X = 101, 1.0, 1.0
    t = np.linspace(0, T, n)
    ks = {"exponential": np.exp(-5 * t), "power law": (1 + 20 * t) ** -0.4, "permanent": np.ones(n)}
    out = {}
    for name, G in ks.items():
        Gm = G[np.abs(np.subtract.outer(np.arange(n), np.arange(n)))]
        v = np.full(n, X / n) if name == "permanent" else E.kernel_optimal(G, X)
        out[name] = {"G": G, "v": v, "cost": E.kernel_cost(v, G), "twap": E.kernel_cost(np.full(n, X / n), G),
                     "min_eig": float(np.min(np.linalg.eigvalsh(Gm))), "neg": float(np.sum(v[v < 0])),
                     "block0": float(v[0]), "blockT": float(v[-1])}
    # a positive-definite but non-convex kernel (Gaussian): the optimum alternates buys and sells, and refining the grid
    # makes the oscillation grow without bound while the cost keeps falling (Alfonsi, Schied and Slynko 2012)
    gauss = []
    for m in (6, 11, 16, 21):
        tg = np.linspace(0, T, m)
        G = np.exp(-(5 * tg) ** 2)
        v = E.kernel_optimal(G, X)
        gauss.append({"n": m, "t": tg, "v": v, "cost": E.kernel_cost(v, G), "twap": E.kernel_cost(np.full(m, X / m), G),
                      "max": float(np.abs(v).max()), "sell": float(-np.sum(v[v < 0]))})
    # a kernel that is not positive definite (impact that lasts a fixed time, then vanishes): a round trip that makes money
    box = (t < 0.3).astype(float)
    Gm = box[np.abs(np.subtract.outer(np.arange(n), np.arange(n)))]
    w, V = np.linalg.eigh(Gm)
    rt = V[:, 0] - V[:, 0].mean()
    rt = rt / np.abs(rt).sum()
    out["box"] = {"G": box, "min_eig": float(w[0]), "round_trip": rt, "rt_cost": E.kernel_cost(rt, box)}
    return _json({"t": t, "kernels": out, "gauss": gauss})


def compute_ow() -> dict:
    X, T, rho = 1.0, 1.0, 10.0
    cf = E.ow_closed_form(X, T, rho)
    rows = []
    for n in (5, 10, 20, 50, 100, 200, 500, 1000):
        t = np.linspace(0, T, n)
        G = np.exp(-rho * t)
        v = E.kernel_optimal(G, X)
        dt = T / (n - 1)
        rows.append({"n": n, "cost": E.kernel_cost(v, G), "block": float(v[0]),
                     "rate": float(v[n // 2] / dt), "min": float(v.min())})
    n = 200
    t = np.linspace(0, T, n)
    v = E.kernel_optimal(np.exp(-rho * t), X)
    rhos = [0.0, 1.0, 5.0, 20.0, 100.0]
    return _json({"X": X, "T": T, "rho": rho, "closed": cf, "rows": rows, "v": v, "t": t,
                  "by_rho": [{"rho": r, **E.ow_closed_form(X, T, r)} for r in rhos]})


def compute_resilience() -> dict:
    """After sweeps (the mid jumps ten ticks or more in 100 ms, events at least 30 s apart, 16-17 May): the best-queue
    depth relative to its median over the preceding 5 s, and the price path in the sweep's direction, in ticks, for 5
    minutes before and after."""
    ks = [0, 1, 2, 5, 10, 20, 50, 100, 300, 600, 1200, 3000]
    pre_ks = [10, 50, 100, 300]
    deps, paths, pres, n = [], [], [], 0
    for d in BOOK_DAYS[:2]:
        b = data.binance_book_day("BTCUSDT", d)
        m = L.mid(b) / TICK
        dep = b["bq"] + b["aq"]
        dm = np.diff(m)
        ev = np.flatnonzero(np.abs(dm) >= 10) + 1
        ev = ev[(ev > 400) & (ev < len(m) - 3001)]
        keep, last = [], -10 ** 9
        for e in ev:
            if e - last > 300:
                keep.append(e)
                last = e
        ev = np.array(keep)
        s = np.sign(dm[ev - 1])
        base = np.array([np.median(dep[e - 50:e - 1]) for e in ev])
        deps.append(np.array([dep[e:e + 301] / bb for e, bb in zip(ev, base)]))
        paths.append(np.array([s * (m[ev + k] - m[ev - 1]) for k in ks]).T)
        pres.append(np.array([s * (m[ev - 1] - m[ev - 1 - k]) for k in pre_ks]).T)
        n += len(ev)
    D = np.concatenate(deps)
    P = np.concatenate(paths)
    R = np.concatenate(pres)
    curve = np.median(D, 0)
    half = int(np.argmax(curve >= 1 - 0.5 * (1 - curve[0])))
    return _json({"n": n, "depth": curve[:51], "half_steps": half, "ks": ks, "path": P.mean(0),
                  "path_se": P.std(0) / math.sqrt(len(P)), "pre_ks": pre_ks, "pre": R.mean(0)})


def compute_research() -> dict:
    """The research chapter's checks: Obizhaeva-Wang against TWAP across resilience, analytically and on a grid; the
    first-order condition's residual; and the optimal schedule under the power-law propagator fitted to Bitcoin."""
    X, T = 1.0, 1.0
    rows = []
    for rt in (0.1, 1.0, 3.0, 10.0, 30.0, 100.0):
        cf = E.ow_closed_form(X, T, rt)
        twap = (1 / rt) * (1 - (1 - math.exp(-rt)) / rt)       # (1/2) int int e^{-rho|t-s|} (X/T)^2 ds dt
        n = 400
        t = np.linspace(0, T, n)
        G = np.exp(-rt * t)
        v = E.kernel_optimal(G, X)
        Gm = G[np.abs(np.subtract.outer(np.arange(n), np.arange(n)))]
        f = Gm @ v
        rows.append({"rhoT": rt, "ow": cf["cost"], "twap": twap, "saving": 1 - cf["cost"] / twap,
                     "grid": E.kernel_cost(v, G), "grid_twap": E.kernel_cost(np.full(n, X / n), G),
                     "fredholm_spread": float((f.max() - f.min()) / f.mean())})
    p = load("propagator")
    beta, l0 = p["beta"], max(p["G_peak_lag"], 1)
    n, step = 201, 100                                         # 20,000 trades, a decision every 100
    lag = np.arange(n) * step
    G = (1 + lag / l0) ** -beta
    v = E.kernel_optimal(G, 1.0)
    btc = {"beta": beta, "l0": l0, "trades": int((n - 1) * step), "v": v, "block0": float(v[0]), "blockT": float(v[-1]),
           "min": float(v.min()), "cost": E.kernel_cost(v, G), "twap": E.kernel_cost(np.full(n, 1.0 / n), G),
           "mid_rate": float(v[n // 2])}
    return _json({"rows": rows, "btc": btc})


def _qr_fit():
    tr = data.binance_book_day("BTCUSDT", "2023-05-17")
    unit = float(np.median(np.r_[tr["bq"], tr["aq"]]) / 4)
    return L.qr_fit(tr, unit=unit, n_q=30)


def compute_rl() -> dict:
    fit = _qr_fit()
    inv, steps, sub = 20, 20, 10
    train = E.QueueExec(fit, inv, steps, sub, seed=1)
    Q, curve = E.q_learn(train, actions=(0, 1, 2, 4), episodes=60000, alpha=0.05, eps0=0.3, seed=37)

    def rl(s):
        return (0, 1, 2, 4)[int(np.argmax(Q[s]))]

    def front(s):
        return 2 if s[0] < 10 else 0 if s[1] == 0 else 2

    pols = {"TWAP": lambda s: 1, "dump at once": lambda s: inv, "front-loaded": front,
            "sell when the bid is thin": lambda s: (2 if s[2] == 0 else 1 if s[2] == 1 else 0) if s[0] < steps - 1
            else inv, "Q-learning": rl}
    res = {}
    for name, pol in pols.items():
        c = E.run_policy(E.QueueExec(fit, inv, steps, sub, seed=99), pol, 5000)
        res[name] = {"mean": float(c.mean()), "sd": float(c.std()), "se": float(c.std() / math.sqrt(len(c)))}
    # what the learned policy does: mean units sold at each step from the full inventory path
    env = E.QueueExec(fit, inv, steps, sub, seed=7)
    sold = np.zeros(steps)
    for _ in range(2000):
        s = env.reset()
        done = False
        while not done:
            k = min(rl(s), s[1])
            sold[s[0]] += k
            s, _, done = env.step(k)
    return _json({"curve": curve, "res": res, "sold": sold / 2000, "inv": inv, "steps": steps, "sub": sub,
                  "episodes": 60000})


def compute_volume() -> dict:
    k = data.binance_klines("BTCUSDT", "1m", "2023-01", "2023-12", market="futures/um")
    t = np.asarray(k["time"], float)
    v = np.asarray(k["volume"], float)
    mod = ((t % 86400) // 60).astype(int)
    curve = np.bincount(mod, weights=v, minlength=1440) / np.maximum(np.bincount(mod, minlength=1440), 1)
    hourly = curve.reshape(24, 60).sum(1)
    share = hourly / hourly.sum()
    dow = ((t // 86400 + 3) % 7).astype(int)          # 0 = Monday (1970-01-01 was a Thursday)
    by_dow = [float(v[dow == d].mean()) for d in range(7)]
    daily = float(v.sum() / (len(v) / 1440))
    return _json({"hourly_share": share, "by_dow": by_dow, "daily": daily, "minute_curve": curve[::10]})


ITEMS = {"aggregate": compute_aggregate, "propagator": compute_propagator, "latent": compute_latent,
         "ac": compute_ac, "kernels": compute_kernels, "ow": compute_ow, "rl": compute_rl, "volume": compute_volume, "resilience": compute_resilience,
         "research": compute_research}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
