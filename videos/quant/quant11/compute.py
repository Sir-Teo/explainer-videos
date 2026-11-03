"""Every number in Part 11 (Trading Options), computed and cached in .cache/quant11/.

    python -m videos.quant.quant11.compute [items] [--force]

Items (seconds to a few minutes on a CPU):

* ``scalp``      a long 30-day at-the-money BTC straddle bought at DVOL on 1 May 2021 and delta-hedged every hour
                 through the crash of 19 May: the P&L, its gamma and theta parts, and every hedge trade;
* ``edge``       the volatility seller's forecast: Part 10's month-by-month P&L of a sold, hedged 30-day BTC call,
                 split by whether DVOL exceeded a HAR forecast of the coming month's realized volatility (registered);
* ``mm``         a toy options market maker quoting in volatility to random client flow, with and without skewing its
                 quotes against its vega inventory;
* ``dispersion`` the average correlation of French's 49 industries, from rolling 36-month variances, 1929-2020: what
                 implied correlation measures, realized;
* ``alleged``    a toy model of the mechanics SEBI alleges (index support in the morning, options exposure, selling in
                 the afternoon), with linear price impact; an illustration, not evidence;
* ``hedging``    hedging a short option under costs: rehedging every step, Whalley-Wilmott bands, and a neural policy
                 trained to minimize the variance of hedged P&L plus costs (deep hedging);
* ``envelope``   registers the forecast-edge test.
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, hedge, paths, pit, quoting, surface, vol

CACHE = Cache("quant11")
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 11, {"envelope": "btc_vol_forecast_edge"})  # the series' trial counter as of this part

YEAR_H = 365 * 24


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


def _hours():
    dv = data.deribit_dvol(*surface.DVOL_RANGE)
    kl = data.binance_klines("BTCUSDT", "1h", *surface.SPOT_RANGE)
    spot_t = kl["time"] + 3600
    hours = np.arange(max(dv["time"][0], spot_t[0]), min(dv["time"][-1], spot_t[-1]) + 1, 3600.0)
    S = np.interp(hours, spot_t, kl["close"])
    iv = np.interp(hours, dv["time"], dv["close"]) / 100
    return hours, S, iv


def _ts(day: str) -> float:
    return datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()


# ---------------------------------------------------------------------------
def compute_scalp() -> dict:
    hours, S, iv = _hours()
    s = int(np.searchsorted(hours, _ts("2021-05-01") + 8 * 3600))
    H = 30 * 24
    path = S[s:s + H + 1]
    p = path / path[0] * 100.0
    tt = np.arange(H + 1) / YEAR_H
    T = H / YEAR_H
    sig = float(iv[s])
    legs = [hedge.delta_hedge(tt, p[None, :], 100.0, T, sig, cp=cp, position=1, record=[0]) for cp in (1, -1)]
    book = legs[0]["book"][0] + legs[1]["book"][0]
    gam = legs[0]["gamma"][0] + legs[1]["gamma"][0]
    the = legs[0]["theta"][0] + legs[1]["theta"][0]
    shares = legs[0]["shares"][0] + legs[1]["shares"][0]
    trades = np.diff(shares)
    big = np.argsort(np.abs(trades))[-12:]
    return _json({"start": hours[s], "S0": float(path[0]), "S": p, "t": tt * 365, "iv": sig,
                  "rv": float(paths.realized_vol(p, 1 / YEAR_H)), "pnl": float(book[-1]), "book": book, "gamma": gam,
                  "theta": the, "shares": shares, "premium": float(legs[0]["premium"][0] + legs[1]["premium"][0]),
                  "big_trades": sorted(big.tolist()), "low": float(p.min()), "low_day": float(tt[np.argmin(p)] * 365)})


def compute_edge() -> dict:
    from videos.quant.quant10.compute import load as load10
    b = load10("btc")
    start = np.asarray(b["start"])
    pnl = np.asarray(b["pnl"])
    ivs = np.asarray(b["iv"])
    hours, S, _ = _hours()
    # daily realized variance from hourly returns, then HAR (Part 7) refitted each day on the past, forecasting the
    # next 30 days' average daily variance
    day = (hours // 86400).astype(int)
    r = np.diff(np.log(S))
    rv_day, days = [], []
    for d in np.unique(day[1:]):
        m = day[1:] == d
        if m.sum() >= 20:
            rv_day.append(np.sum(r[m] ** 2))
            days.append(d)
    rv_day, days = np.array(rv_day), np.array(days)
    fc = np.full(len(days), np.nan)
    for i in range(400, len(days)):
        if i % 7 == 0 or not np.isfinite(fc[i - 1]):
            f = vol.har_fit(rv_day[:i])
            beta = f["beta"]
        X, _ = vol._har_design(np.concatenate([rv_day[i - 30:i + 1], [np.nan]]))
        # HAR's next-day variance forecast, used for the month ahead: volatility is persistent, and HAR's monthly
        # term carries most of a month's level
        h = float((np.column_stack([np.ones(1), X[-1:]]) @ beta)[0])
        fc[i] = max(h, 1e-8)
    sday = (start // 86400).astype(int)
    pos = np.searchsorted(days, sday)
    ok = (pos < len(days)) & np.isfinite(fc[np.minimum(pos, len(days) - 1)])
    fvol = np.sqrt(fc[np.minimum(pos, len(days) - 1)] * 365)
    signal = ivs > fvol
    sel = ok & signal
    off = ok & ~signal
    sub = np.arange(0, len(pnl), 30)  # non-overlapping months
    s_on = np.intersect1d(sub, np.where(sel)[0])
    s_off = np.intersect1d(sub, np.where(off)[0])
    mean = lambda idx: float(pnl[idx].mean()) if len(idx) else float("nan")  # noqa: E731
    se = lambda idx: float(pnl[idx].std(ddof=1) / np.sqrt(len(idx))) if len(idx) > 1 else float("nan")  # noqa: E731
    return _json({"n": int(ok.sum()), "share_on": float(sel.sum() / ok.sum()), "mean_all": mean(np.where(ok)[0]),
                  "mean_on": mean(np.where(sel)[0]), "mean_off": mean(np.where(off)[0]),
                  "nonoverlap_on": mean(s_on), "nonoverlap_off": mean(s_off), "se_on": se(s_on), "se_off": se(s_off),
                  "n_on": int(len(s_on)), "n_off": int(len(s_off)), "t": start[ok][::7], "iv": ivs[ok][::7],
                  "fvol": fvol[ok][::7], "rv": np.asarray(b["rv"])[ok][::7]})


def compute_mm() -> dict:
    g = np.random.default_rng(110)
    steps, fair = 2000, 0.60
    out = {}
    for name, skew in (("no skew", 0.0), ("skewed", 0.0015)):
        inv, pnl, invs = 0.0, 0.0, []
        g2 = np.random.default_rng(111)
        for _ in range(steps):
            q = quoting.quote(fair, inv, half_spread=0.01, skew_per_vega=skew, vega_limit=None)
            # clients arrive at random and trade with probability falling in how far the quote is from fair
            if g2.random() < 0.5:  # a client wants to sell vol to us (we buy at the bid)
                if g2.random() < np.exp(-60 * max(fair - q["bid"], 0) + 0.3):
                    inv += 1
                    pnl += fair - q["bid"]
            else:
                if g2.random() < np.exp(-60 * max(q["ask"] - fair, 0) + 0.3):
                    inv -= 1
                    pnl += q["ask"] - fair
            invs.append(inv)
        out[name] = {"inventory": np.array(invs)[::5], "spread_pnl": pnl, "max_abs": float(np.max(np.abs(invs))),
                     "sd": float(np.std(invs))}
    return _json(out)


def compute_dispersion() -> dict:
    k = data.ken_french_industries(49, weighting="value")
    d, R = np.asarray(k["date"]), np.asarray(k["returns"], float)
    ok = np.all(np.isfinite(R) & (R > -0.99), axis=0)
    R = R[:, ok]
    n = R.shape[1]
    w = np.full(n, 1 / n)
    win = 36
    t, rho = [], []
    for i in range(win, len(d) + 1):
        X = R[i - win:i]
        s = X.std(axis=0, ddof=1)
        si = (X @ w).std(ddof=1)
        rho.append(quoting.implied_correlation(si, w, s))
        t.append(d[i - 1] // 100 + ((d[i - 1] % 100) - 0.5) / 12)
    rho = np.array(rho)
    t = np.array(t)
    peaks = {}
    for lab, a, b_ in (("1929-33", 1929, 1934), ("1987", 1987, 1990), ("2008", 2008, 2011), ("2020", 2020, 2021)):
        m = (t >= a) & (t < b_)
        if m.any():
            peaks[lab] = float(rho[m].max())
    return _json({"t": t, "rho": rho, "n": int(n), "median": float(np.median(rho)), "peaks": peaks,
                  "low": float(rho.min()), "low_t": float(t[np.argmin(rho)])})


def compute_alleged() -> dict:
    # an index at 100 with linear price impact: buying or selling q units moves it by lam * q points.  Morning: buy Q
    # (the index rises lam Q).  Meanwhile: hold short-delta options exposure of D units, put on near the supported
    # level.  Afternoon: sell 2Q (the Q bought and Q more), and the index falls 2 lam Q to settle below its start.
    # P&L in units x points.  An illustration of the mechanics alleged, not evidence of them.
    lam, Q, D = 0.01, 100.0, 500.0
    t = np.linspace(0, 1, 121)
    up, down = lam * Q, 2 * lam * Q
    path = 100 + np.where(t <= 0.45, up * t / 0.45, np.where(t < 0.55, up, up - down * (t - 0.55) / 0.45))
    buy_avg = 100 + up / 2
    sell_avg = 100 + up - down / 2
    cash_leg = -Q * buy_avg + 2 * Q * sell_avg - Q * path[-1]  # the extra Q sold short is closed at the settlement
    impact_cost = -lam * Q * Q  # what a round trip of Q costs on its own
    options_leg = D * (path.max() - path[-1])
    return _json({"t": t, "index": path, "lam": lam, "Q": Q, "D": D, "cash_leg": cash_leg, "impact_cost": impact_cost,
                  "options_leg": options_leg, "net": cash_leg + options_leg, "move_up": up, "move_down": down,
                  "settle": float(path[-1])})


def _gbm(n_paths, n, T, sigma, seed):
    g = np.random.default_rng(seed)
    dt = T / n
    z = g.standard_normal((n_paths, n))
    lp = np.cumsum(-0.5 * sigma ** 2 * dt + sigma * np.sqrt(dt) * z, axis=1)
    return np.linspace(0, T, n + 1), 100 * np.exp(np.column_stack([np.zeros(n_paths), lp]))


def compute_hedging() -> dict:
    import torch
    torch.set_num_threads(1)
    T, n, sigma, cost = 30 / 365, 30 * 4, 0.6, 0.001  # a 30-day BTC-like option, rehedged up to every 6 hours, 10 bp
    t, S = _gbm(20000, n, T, sigma, 112)
    rows = []
    for bh in (0.0, 0.02, 0.05, 0.1):
        o = quoting.hedge_with_band(t, S, 100.0, T, sigma, cost, band_half=bh)
        rows.append({"rule": "fixed band" if bh else "every step", "param": bh, "sd": float(o["pnl"].std()),
                     "cost": float(o["cost"].mean()), "trades": float(o["trades"].mean())})
    for gr in (0.1, 1.0, 10.0):
        o = quoting.hedge_with_band(t, S, 100.0, T, sigma, cost, band_half=None, gamma_risk=gr)
        rows.append({"rule": "Whalley-Wilmott", "param": gr, "sd": float(o["pnl"].std()), "cost": float(o["cost"].mean()),
                     "trades": float(o["trades"].mean())})
    # deep hedging: a network maps (time left, log moneyness, current hedge) to the new hedge; trained on simulated
    # paths to minimize Var(P&L) + kappa * E[cost] through the simulator (Buehler, Gonon, Teichmann and Wood 2019)
    torch.manual_seed(0)
    net = torch.nn.Sequential(torch.nn.Linear(4, 32), torch.nn.Tanh(), torch.nn.Linear(32, 32), torch.nn.Tanh(),
                              torch.nn.Linear(32, 1))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    tt = torch.tensor(t, dtype=torch.float32)
    St = torch.tensor(S, dtype=torch.float32)
    prem = float(bs.price(100.0, 100.0, T, sigma))
    K = 100.0

    def run(Sb, train=True):
        m = Sb.shape[0]
        h = torch.zeros(m)
        cash = torch.full((m,), prem)
        costs = torch.zeros(m)
        for i in range(n):
            x = torch.stack([torch.full((m,), float((T - tt[i]) / T)), torch.log(Sb[:, i] / K) / (sigma * np.sqrt(T)), h], 1)
            # move a learned fraction of the way toward the Black-Scholes delta: standing still (a no-trade region)
            # is then as easy to learn as rehedging fully
            d1 = (torch.log(Sb[:, i] / K) + 0.5 * sigma ** 2 * (T - tt[i])) / (sigma * torch.sqrt(T - tt[i] + 1e-9))
            bsd = 0.5 * (1 + torch.erf(d1 / np.sqrt(2)))
            x = torch.cat([x, (bsd - h)[:, None] * 10], 1)
            new = h + torch.sigmoid(net(x).squeeze(-1)) * (bsd - h)
            tr = new - h
            cash = cash - tr * Sb[:, i] - cost * torch.abs(tr) * Sb[:, i]
            costs = costs + cost * torch.abs(tr) * Sb[:, i]
            h = new
        pnl = cash + h * Sb[:, -1] - cost * torch.abs(h) * Sb[:, -1] - torch.clamp(Sb[:, -1] - K, min=0)
        return pnl, costs + cost * torch.abs(h) * Sb[:, -1]

    state0 = {k: v.clone() for k, v in net.state_dict().items()}
    for kappa in (1.0, 4.0, 16.0):
        net.load_state_dict(state0)
        opt = torch.optim.Adam(net.parameters(), lr=3e-3)
        for it in range(500):
            idx = torch.randint(0, 15000, (1024,))
            pnl, c = run(St[idx])
            loss = pnl.var() + kappa * c.mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
        with torch.no_grad():
            pnl, c = run(St[15000:])
        rows.append({"rule": "deep hedge", "param": kappa, "sd": float(pnl.std()), "cost": float(c.mean()),
                     "trades": float("nan")})
        print(f"    deep hedge kappa {kappa}: sd {float(pnl.std()):.3f}, cost {float(c.mean()):.3f}", flush=True)
    return _json({"rows": rows, "premium": prem, "sigma": sigma, "cost_rate": cost, "steps": n})


def compute_envelope() -> dict:
    reg = {"btc_vol_forecast_edge": pit.register("btc_vol_forecast_edge", inspect.getsource(compute_edge),
                                                 {"signal": "DVOL > HAR forecast of 30-day realized vol",
                                                  "trade": "Part 10's sold, hourly-hedged 30-day ATM call"}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


# ===========================================================================
# The expansion (November 2026): the items behind chapters 1-18 of the ~57-minute part
# ===========================================================================
def _nw_t(x, lags=4) -> float:
    """Mean over its Newey-West standard error (overlapping windows)."""
    x = np.asarray(x, float)
    d = x - x.mean()
    v = d @ d / len(x)
    for lag in range(1, lags + 1):
        v += 2 * (1 - lag / (lags + 1)) * (d[lag:] @ d[:-lag]) / len(x)
    return float(x.mean() / np.sqrt(v / len(x)))


def _ssvi_day(day: str):
    from explainer.quant.house import volsurface as VS
    q = surface.build(day)
    w = q["iv"] ** 2 * q["T"]
    ok = (np.abs(q["k"]) < 0.6) & (q["T"] > 2 / 365)
    f = VS.fit_ssvi(q["k"][ok], q["T"][ok], w[ok], weights=q["vega"][ok])
    return q, f


def _ssvi_iv(f, k, T):
    from explainer.quant.house import volsurface as VS
    return np.sqrt(VS.ssvi_w(np.asarray(k, float), VS.theta_at(f, T), f["rho"], f["eta"], f["gamma"]) / T)


BOOK = [(1, 1.0, 1), (-1, 1.0, 1), (-1, 0.9, -2), (1, 1.1, 1)]   # (cp, strike / forward, quantity): ch1's five legs


def compute_explain() -> dict:
    """A five-leg book on the Surface day (10 Dec 2025, 08:00 UTC), revalued on the next day's surface: the Taylor
    terms of its P&L against the full revaluation."""
    q0, f0 = _ssvi_day(surface.DAYS[0])
    q1, f1 = _ssvi_day(surface.DAYS[1])
    T0, dt = 30 / 365, 1 / 365
    F0 = float(q0["S"] * np.exp(q0["basis_rate"] * T0))
    F1 = float(q1["S"] * np.exp(q1["basis_rate"] * (T0 - dt)))
    legs = [quoting.Leg(cp, m * F0, T0, n) for cp, m, n in BOOK]
    s0 = [float(_ssvi_iv(f0, np.log(L.K / F0), T0)) for L in legs]
    s1 = [float(_ssvi_iv(f1, np.log(L.K / F1), T0 - dt)) for L in legs]
    e = quoting.pnl_explain(legs, F0, F1, s0, s1, dt)
    atm0, atm1 = float(_ssvi_iv(f0, 0.0, T0)), float(_ssvi_iv(f1, 0.0, T0 - dt))
    g = quoting.book_greeks(legs, F0, atm0)
    cash = {"delta": g["delta"] * F0, "gamma_1pct": 0.5 * g["gamma"] * F0 ** 2 * 1e-4, "vega_pt": g["vega"] / 100,
            "theta_day": g["theta"] / 365, "price": g["price"]}
    be = atm0 * np.sqrt(1 / 365)
    return _json({**{k: float(v) for k, v in e.items()}, "F0": F0, "F1": F1, "move": F1 / F0 - 1, "atm0": atm0,
                  "atm1": atm1, "iv0": s0, "iv1": s1, "legs": [[cp, m, n] for cp, m, n in BOOK], "cash": cash,
                  "share": abs(e["unexplained"]) / max(abs(e["actual"]), 1e-9), "breakeven_daily": float(be),
                  "be50": float(0.5 * np.sqrt(1 / 365))})


def compute_scalp_shuffle() -> dict:
    s = load("scalp")
    P = np.asarray(s["S"], float)
    r = np.diff(np.log(P))
    H = len(r)
    tt = np.arange(H + 1) / YEAR_H
    T = H / YEAR_H
    g = np.random.default_rng(1102)
    n = 2000
    R = np.array([g.permutation(r) for _ in range(n)])
    paths_ = 100 * np.exp(np.column_stack([np.zeros(n), np.cumsum(R, 1)]))

    def straddle(X):
        return sum(hedge.delta_hedge(tt, X, 100.0, T, s["iv"], cp=cp, position=1)["pnl"] for cp in (1, -1))

    pnl = straddle(paths_)
    # the crash moved to the start: the 48 hours of the deepest fall, cut out and replayed from hour 24
    w = 48
    roll = np.array([np.sum(r[i:i + w]) for i in range(H - w)])
    c = int(np.argmin(roll))
    block = r[c:c + w]
    rest = np.concatenate([r[:c], r[c + w:]])
    early = np.concatenate([rest[:24], block, rest[24:]])
    p_early = 100 * np.exp(np.concatenate([[0.0], np.cumsum(early)]))
    pe = float(straddle(p_early[None, :])[0])
    rv = np.sqrt(np.sum(r ** 2) / (H / YEAR_H))
    real = float(s["pnl"])
    return _json({"pnl": pnl, "real": real, "pct": float(np.mean(pnl < real)), "mean": float(pnl.mean()),
                  "median": float(np.median(pnl)), "sd": float(pnl.std()), "p5": float(np.percentile(pnl, 5)),
                  "p95": float(np.percentile(pnl, 95)), "rv": float(rv), "n": n, "early": pe, "crash_hour": c,
                  "early_path": p_early[::2], "sample_paths": paths_[:40, ::4]})


def _straddle_run(p, tt, T, sig, mask):
    """A long straddle on one path, rehedged where ``mask`` is True: running hedge and marked book."""
    g0 = sum(bs.greeks(p[0], 100.0, T, sig, cp=cp)["delta"] for cp in (1, -1))
    v0 = sum(float(bs.price(p[0], 100.0, T, sig, cp=cp)) for cp in (1, -1))
    sh, cash = -float(g0), -v0 + float(g0) * p[0]
    shares, book = [sh], [0.0]
    for i in range(1, len(p)):
        tau = max(T - tt[i], 0.0)
        val = sum(float(bs.price(p[i], 100.0, tau, sig, cp=cp)) for cp in (1, -1))
        if mask[i] and i < len(p) - 1:
            d = -float(sum(bs.greeks(p[i], 100.0, tau, sig, cp=cp)["delta"] for cp in (1, -1)))
            cash -= (d - sh) * p[i]
            sh = d
        shares.append(sh)
        book.append(cash + sh * p[i] + val)
    return np.array(shares), np.array(book)


def compute_frequency() -> dict:
    hours, S, iv = _hours()
    H = 30 * 24
    T = H / YEAR_H
    tt = np.arange(H + 1) / YEAR_H
    starts = np.arange(0, len(S) - H - 1, 7 * 24)
    P = np.array([S[s:s + H + 1] / S[s] * 100 for s in starts])
    sig = iv[starts]
    out = {"start": hours[starts], "iv": sig, "rv": paths.realized_vol(P, 1 / YEAR_H)}
    rules = {}
    for cost in (0.0, 0.001):
        for name, every in (("hourly", 1), ("4-hourly", 4), ("daily", 24)):
            rules[(name, cost)] = sum(hedge.delta_hedge(tt, P, 100.0, T, sig, cp=cp, position=1, hedge_every=every,
                                                        cost=cost)["pnl"] for cp in (1, -1))
        mv = [hedge.delta_hedge_on_moves(tt, P, 100.0, T, sig, 0.02, cp=cp, cost=cost) for cp in (1, -1)]
        rules[("2% moves", cost)] = mv[0]["pnl"] + mv[1]["pnl"]
        if cost == 0.0:
            out["trades_moves"] = float(mv[0]["trades"].mean())
    gap = out["rv"] - sig
    stats = []
    for (name, cost), v in rules.items():
        stats.append({"rule": name, "cost": cost, "mean": float(v.mean()), "sd": float(v.std()),
                      "corr": float(np.corrcoef(v, gap)[0, 1]), "t": _nw_t(v)})
        out[f"pnl {name} {cost}"] = v
    d = rules[("hourly", 0.0)] - rules[("daily", 0.0)]
    r1 = np.diff(np.log(S))
    r24 = np.diff(np.log(S[::24]))
    vr = float(r24.var() / (24 * r1.var()))
    # one month raced live: the window starting nearest 1 March 2024
    j = int(np.argmin(np.abs(hours[starts] - _ts("2024-03-01"))))
    p, sg = P[j], float(sig[j])
    race = {}
    for name, every in (("hourly", 1), ("daily", 24)):
        m = np.zeros(H + 1, bool)
        m[::every] = True
        race[name] = _straddle_run(p, tt, T, sg, m)
    m, last = np.zeros(H + 1, bool), p[0]
    for i in range(1, H + 1):
        if abs(p[i] / last - 1) > 0.02:
            m[i], last = True, p[i]
    race["2% moves"] = _straddle_run(p, tt, T, sg, m)
    for k, (sh, bk) in race.items():
        out[f"race shares {k}"], out[f"race book {k}"] = sh, bk
    out.update({"stats": stats, "n": int(len(starts)), "diff_hd_mean": float(d.mean()), "diff_hd_t": _nw_t(d),
                "variance_ratio": vr, "race_path": p, "race_iv": sg, "race_start": float(hours[starts][j]),
                "race_rv": float(out["rv"][j])})
    return _json(out)


def _grid_iv(grid, k, T):
    h = load12("history")
    KG, TG = np.asarray(h["grid_k"]), np.asarray(h["grid_T"])
    grid = np.asarray(grid, float)
    w = np.array([np.interp(k, KG, grid[j]) ** 2 * TG[j] for j in range(len(TG))])
    wt = np.interp(T, TG, w, left=np.nan) if T >= TG[0] else w[0] * T / TG[0]
    return float(np.sqrt(wt / T))


def load12(name):
    from videos.quant.quant12.compute import load as _l
    return _l(name)


def compute_secondorder() -> dict:
    q0, f0 = _ssvi_day(surface.DAYS[0])
    T = 30 / 365
    F = float(q0["S"] * np.exp(q0["basis_rate"] * T))
    iv = lambda k: float(_ssvi_iv(f0, k, T))  # noqa: E731
    kc = quoting.delta_strike(F, T, iv, 0.25)
    kp = quoting.delta_strike(F, T, iv, -0.25, cp=-1)
    k10c = quoting.delta_strike(F, T, iv, 0.10)
    k10p = quoting.delta_strike(F, T, iv, -0.10, cp=-1)
    sc, sp, sa = iv(np.log(kc / F)), iv(np.log(kp / F)), iv(0.0)
    ks = np.linspace(-0.4, 0.4, 81)
    K = F * np.exp(ks)
    vv = quoting.vanna_volga(K, F, T, [kp, F, kc], [sp, sa, sc], sa)
    ss = np.array([iv(k) for k in ks])
    in_ = (K >= k10p) & (K <= k10c)
    inner = np.abs(ks) < 0.3
    # the weights x_i(K) of the three pillars, strike by strike (the sweep on screen)
    g3 = bs.greeks(F, np.array([kp, F, kc]), T, sa)
    A = np.vstack([g3["vega"], g3["vanna"], g3["volga"]])
    X = np.array([np.linalg.solve(A, [float(v) for v in (lambda g: (g["vega"], g["vanna"], g["volga"]))(
        bs.greeks(F, k_, T, sa))]) for k_ in K])
    # 100 weeks of the 30-day 25-delta risk reversal and butterfly (Part 12's weekly smiles)
    h = load12("history")
    rr, bf, atm, spot, days = [], [], [], [], []
    for row in h["rows"]:
        f_ = lambda k, g=row["grid"]: _grid_iv(g, k, T)  # noqa: E731
        c_ = quoting.delta_strike(1.0, T, f_, 0.25, lo=-0.4, hi=0.4)
        p_ = quoting.delta_strike(1.0, T, f_, -0.25, cp=-1, lo=-0.4, hi=0.4)
        a, b, m = f_(np.log(c_)), f_(np.log(p_)), f_(0.0)
        rr.append(a - b)
        bf.append(0.5 * (a + b) - m)
        atm.append(m)
        spot.append(row["S"])
        days.append(row["day"])
    rr, bf = np.array(rr), np.array(bf)
    # volga and vanna at the pillars, per unit vega (the 3D surface's flags)
    gp = {n: {k_: float(v) for k_, v in bs.greeks(F, kk, T, sa).items()} for n, kk in (("put", kp), ("atm", F),
                                                                                       ("call", kc))}
    return _json({"F": F, "T": T, "k25c": kc, "k25p": kp, "k10c": k10c, "k10p": k10p, "s25c": sc, "s25p": sp,
                  "atm": sa, "rr": sc - sp, "bf": 0.5 * (sc + sp) - sa, "ks": ks, "vv": vv, "ssvi": ss, "x": X,
                  "rmse_in": float(np.sqrt(np.mean((vv - ss)[in_] ** 2)) * 100),
                  "rmse_inner": float(np.sqrt(np.mean((vv - ss)[inner] ** 2)) * 100),
                  "maxerr_wing": float(np.max(np.abs(vv - ss)[~in_]) * 100) if (~in_).any() else 0.0,
                  "weekly_rr": rr, "weekly_bf": bf, "weekly_atm": np.array(atm), "weekly_S": np.array(spot),
                  "weekly_days": days, "share_rr_neg": float(np.mean(rr < 0)), "rr_min": float(rr.min()),
                  "rr_max": float(rr.max()), "bf_mean": float(bf.mean()), "pillars": gp})


_WEEKLY = {}


def _weekly() -> dict:
    """Every Wednesday of Part 12's grid (2024-2025) with a smile 28 days later: the six structures bought on that
    day's smile and settled at Binance's 08:00 price, and a straddle at that day's 28-day ATM vol hedged hourly."""
    if _WEEKLY:
        return _WEEKLY
    from datetime import timedelta
    h = load12("history")
    rows = h["rows"]
    days = [r["day"] for r in rows]
    kl = data.binance_klines("BTCUSDT", "1h", "2024-01", "2025-12")
    tk, ck = np.asarray(kl["time"]) + 3600, np.asarray(kl["close"])
    Hh = 28 / 365
    names = ["straddle", "strangle", "risk reversal", "butterfly", "call spread", "calendar"]
    res = {n: [] for n in names}
    cost = {n: [] for n in names}
    used, P, sig, feats = [], [], [], []
    for r in rows:
        d2 = (datetime.strptime(r["day"], "%Y-%m-%d") + timedelta(days=28)).strftime("%Y-%m-%d")
        if d2 not in days:
            continue
        r2 = rows[days.index(d2)]
        t0, t1 = _ts(r["day"]) + 8 * 3600, _ts(d2) + 8 * 3600
        F = float(np.interp(t0, tk, ck))
        S1 = float(np.interp(t1, tk, ck))
        px = lambda K, T, cp, g=r["grid"], F=F: float(bs.price(F, K, T, _grid_iv(g, np.log(K / F), T), cp=cp))  # noqa
        px2 = lambda K, T, cp: float(bs.price(S1, K, T, _grid_iv(r2["grid"], np.log(K / S1), T), cp=cp))  # noqa
        pay = lambda K, cp: max(cp * (S1 - K), 0.0)  # noqa: E731
        lo, hi = 0.9 * F, 1.1 * F
        legs = {"straddle": [(F, 1, 1), (F, -1, 1)], "strangle": [(hi, 1, 1), (lo, -1, 1)],
                "risk reversal": [(hi, 1, 1), (lo, -1, -1)], "butterfly": [(lo, 1, 1), (F, 1, -2), (hi, 1, 1)],
                "call spread": [(F, 1, 1), (hi, 1, -1)]}
        for n, L in legs.items():
            c = sum(q * px(K, Hh, cp) for K, cp, q in L)
            res[n].append(100 * (sum(q * pay(K, cp) for K, cp, q in L) - c) / F)
            cost[n].append(100 * c / F)
        c = px(F, 2 * Hh, 1) - px(F, Hh, 1)
        res["calendar"].append(100 * (px2(F, Hh, 1) - pay(F, 1) - c) / F)
        cost["calendar"].append(100 * c / F)
        m = (tk >= t0) & (tk <= t1)
        path = ck[m] / ck[m][0] * 100
        P.append(path[:673])
        sig.append(_grid_iv(r["grid"], 0.0, Hh))
        # features known on the day (chapter 18): the term slope and the risk reversal of that day's smile
        f7, f60 = _grid_iv(r["grid"], 0.0, 7 / 365), _grid_iv(r["grid"], 0.0, 60 / 365)
        fc = lambda k, g=r["grid"]: _grid_iv(g, k, 30 / 365)  # noqa: E731
        kc = quoting.delta_strike(1.0, 30 / 365, fc, 0.25, lo=-0.4, hi=0.4)
        kp = quoting.delta_strike(1.0, 30 / 365, fc, -0.25, cp=-1, lo=-0.4, hi=0.4)
        feats.append({"slope": f7 - f60, "rr": fc(np.log(kc)) - fc(np.log(kp))})
        used.append(r["day"])
    P = np.array(P)
    sig = np.array(sig)
    tt = np.arange(P.shape[1]) / YEAR_H
    legs = [hedge.delta_hedge(tt, P, 100.0, tt[-1], sig, cp=cp, position=1, record=list(range(len(P))))
            for cp in (1, -1)]
    hp = legs[0]["pnl"] + legs[1]["pnl"]
    book = legs[0]["book"] + legs[1]["book"]
    _WEEKLY.update({"days": used, "res": {k: np.array(v) for k, v in res.items()},
                    "cost": {k: np.array(v) for k, v in cost.items()}, "hedged": hp, "book": book[:, ::24],
                    "gamma": (legs[0]["gamma"] + legs[1]["gamma"])[:, -1], "theta": (legs[0]["theta"]
                                                                                    + legs[1]["theta"])[:, -1],
                    "sig": sig, "rv": paths.realized_vol(P, 1 / YEAR_H), "feats": feats, "P": P})
    return _WEEKLY


def compute_strategies() -> dict:
    w = _weekly()
    rows = []
    for n, x in w["res"].items():
        rows.append({"name": n, "mean": float(x.mean()), "median": float(np.median(x)), "win": float(np.mean(x > 0)),
                     "sd": float(x.std()), "t": _nw_t(x), "min": float(x.min()), "max": float(x.max()),
                     "cost": float(w["cost"][n].mean())})
    return _json({"days": w["days"], "rows": rows, **{f"pnl {n}": x for n, x in w["res"].items()},
                  "n": len(w["days"]), "worst": min(rows, key=lambda r_: r_["win"])["name"]})


def compute_premium() -> dict:
    w = _weekly()
    x = w["hedged"]
    st = w["res"]["straddle"] / w["cost"]["straddle"]   # unhedged straddle return on premium (Coval-Shumway)
    return _json({"pnl": x, "mean": float(x.mean()), "median": float(np.median(x)), "share_pos": float(np.mean(x > 0)),
                  "t": _nw_t(x), "n": int(len(x)), "book": w["book"], "gamma": w["gamma"], "theta": w["theta"],
                  "iv": w["sig"], "rv": w["rv"], "straddle_ret_mean": float(st.mean()),
                  "straddle_ret_median": float(np.median(st)), "straddle_ret_t": _nw_t(st),
                  "share_rv_below": float(np.mean(w["rv"] < w["sig"])), "days": w["days"]})


def compute_kelly() -> dict:
    from videos.quant.quant10.compute import load as load10
    b = load10("btc")
    X = np.asarray(b["pnl"], float) / 100        # a sold, hedged one-month call per 100 of capital, as a return
    mu, var = float(X.mean()), float(X.var())
    f_ruin = 1 / abs(float(X.min()))
    f = np.linspace(0, min(f_ruin * 0.999, 3 * mu / var), 400)
    g = np.array([np.mean(np.log1p(fi * X)) for fi in f])
    j = int(np.argmax(g))
    return _json({"f": f, "g": g, "f_emp": float(f[j]), "g_max": float(g[j]), "f_gauss": mu / var,
                  "f_ruin": f_ruin, "mu": mu, "sd": float(np.sqrt(var)), "min": float(X.min()), "n": int(len(X)),
                  "skew": float(((X - mu) ** 3).mean() / var ** 1.5),
                  "g_at_gauss": float(np.mean(np.log1p(np.minimum(mu / var, f_ruin * 0.999) * X)))})


def _flow_days():
    import os
    root = data.DATA / "deribit" / "trades" / "BTC" / "option"
    return sorted(d for d in os.listdir(root) if "2024-01-01" <= d < "2025-12-01")


def compute_flow() -> dict:
    from collections import defaultdict
    days = _flow_days()
    hz = (300, 1800, 3600)
    E, M, SZ, BUY, OTMC, OTMP, VG = [], {h: [] for h in hz}, [], [], [], [], []
    rain = None
    lab = None
    for day in days:
        tr = [t for t in data.deribit_trades(day, hours=surface.HOURS)
              if None not in (t.get("price"), t.get("mark_price"), t.get("iv"), t.get("index_price"),
                              t.get("direction"), t.get("amount"))]
        by = defaultdict(list)
        for t in tr:
            by[t["instrument_name"]].append(t)
        day_e, day_m = [], {h: [] for h in hz}
        pts = []
        for name, L in by.items():
            exp, K, cp = surface.parse_instrument(name)
            ts = np.array([x["timestamp"] / 1e3 for x in L])
            T = (exp.timestamp() - ts) / (365 * 86400)
            I = np.array([x["index_price"] for x in L])
            p = np.array([x["price"] for x in L])
            mk = np.array([x["mark_price"] for x in L])
            iv = np.array([x["iv"] for x in L]) / 100
            s = np.array([1 if x["direction"] == "buy" else -1 for x in L])
            a = np.array([x["amount"] for x in L])
            g = bs.greeks(I, K, np.maximum(T, 1e-6), np.clip(iv, 0.05, 3), cp=cp)
            vega = g["vega"] / 100
            o = quoting.markouts(ts, s, p, mk, I, g["delta"], np.maximum(vega, 1e-9), hz)
            good = (T > 1 / 365) & (iv > 0.05) & (iv < 3) & (vega > 0.5) & (np.abs(o["edge"]) < 20)
            otm = (cp * (K - I)) > 0
            E.append(o["edge"][good])
            day_e.append(o["edge"][good])
            for h in hz:
                x = o[h][good]
                M[h].append(np.where(np.abs(x) < 30, x, np.nan))
                day_m[h].append(M[h][-1])
            SZ.append(a[good])
            BUY.append(s[good])
            OTMC.append((otm & (cp == 1))[good])
            OTMP.append((otm & (cp == -1))[good])
            VG.append((a * vega)[good])
            if day == "2025-06-04":
                for j in np.where(good)[0]:
                    pts.append((float(np.log(K / I[j])), float(T[j] * 365), int(s[j]), float(a[j]), float(ts[j])))
        if day == "2025-06-04":
            rain = np.array(sorted(pts, key=lambda r_: r_[4]))
            de = np.concatenate(day_e)
            lab = {"n": int(len(de)), "edge": float(de.mean()),
                   **{str(h): float(np.nanmean(np.concatenate(day_m[h]))) for h in hz}}
    E = np.concatenate(E)
    SZ = np.concatenate(SZ)
    BUY = np.concatenate(BUY)
    OTMC, OTMP, VG = np.concatenate(OTMC), np.concatenate(OTMP), np.concatenate(VG)
    big = SZ >= np.percentile(SZ, 95)
    out = {"days": len(days), "n": int(len(E)), "edge_mean": float(E.mean()), "edge_median": float(np.median(E)),
           "edge_big": float(np.median(E[big])), "edge_small": float(np.median(E[~big])), "lab": lab,
           "rain": rain}
    curve_all, curve_big, cov = [float(E.mean())], [float(E[big].mean())], []
    for h in hz:
        x = np.concatenate(M[h])
        ok = np.isfinite(x)
        cov.append(float(ok.mean()))
        curve_all.append(float(x[ok].mean()))
        curve_big.append(float(x[ok & big].mean()))
        # the same trades only, so the edge and the markouts compare like for like
        out[f"edge_on_{h}"] = float(E[ok].mean())
    out.update({"curve": curve_all, "curve_big": curve_big, "coverage": cov, "horizons": [0, *hz],
                "kept_1h": curve_all[-1] / out["edge_on_3600"]})
    tot = VG.sum()
    for lab_, m in (("otm call", OTMC), ("otm put", OTMP)):
        out[f"{lab_} bought"] = float(VG[m & (BUY > 0)].sum() / tot)
        out[f"{lab_} sold"] = float(VG[m & (BUY < 0)].sum() / tot)
    return _json(out)


MM = {"Q": 10, "A": 0.45, "k": 1.5, "offs": (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0), "phi": 0.02, "disc": 0.995}


def compute_mm_learn() -> dict:
    p = {k: v for k, v in MM.items()}
    dp = quoting.mm_value_iteration(**p)
    V0 = float(dp["V"][p["Q"]])
    acts = dp["acts"]
    offs = np.asarray(p["offs"])
    skew_of = lambda pol: np.array([offs[acts[a][0]] - offs[acts[a][1]] for a in pol])  # noqa: E731
    steps = 800_000
    ck = sorted(set([0, 10_000, 25_000] + list(range(0, steps + 1, 20_000))))
    part = CACHE.partial("mm_learn", {"steps": steps, "ck": ck, **{k: list(v) if isinstance(v, tuple) else v
                                                                     for k, v in p.items()}})
    for seed in range(5):
        if str(seed) in part:
            continue
        o = quoting.mm_q_learning(steps=steps, seed=seed, checkpoints=ck, **p)
        vals = [float(quoting.mm_policy_value(o["snapshots"][c], **p)[p["Q"]]) for c in ck]
        part[str(seed)] = {"value": vals, "skew": {str(c): skew_of(o["snapshots"][c]).tolist() for c in ck},
                           "policy": o["policy"].tolist()}
        print(f"    mm_learn seed {seed}: {100 * vals[-1] / V0:.0f}% of the optimum", flush=True)
    runs = [part[str(s)] for s in range(5)]
    sym = []
    for j in range(len(offs)):
        a = acts.index((j, j))
        sym.append(float(quoting.mm_policy_value([a] * (2 * p["Q"] + 1), **p)[p["Q"]]))
    qs = np.arange(-p["Q"], p["Q"] + 1)
    gl = quoting.glft_quotes(qs, p["A"] / 2, p["k"], p["phi"])   # a client on each side half the time
    snap = lambda x: int(np.argmin(np.abs(offs - np.clip(x, offs[0], offs[-1]))))  # noqa: E731
    gpol = [acts.index((snap(b), snap(a))) for b, a in zip(gl["bid"], gl["ask"])]
    v_glft = float(quoting.mm_policy_value(gpol, **p)[p["Q"]])
    # live: the trained agent (seed 0) and the best symmetric quote on the same 2,000 clients
    g = np.random.default_rng(1105)
    u, f = g.random(2000), g.random(2000)
    agent = runs[0]["policy"]
    jbest = int(np.argmax(sym))
    live = {}
    for name, pol in (("learned", agent), ("symmetric", [acts.index((jbest, jbest))] * len(qs))):
        i, inv, cash = p["Q"], [], 0.0
        for s in range(2000):
            b, a = acts[pol[i]]
            if u[s] < 0.5 and i < 2 * p["Q"] and f[s] < min(p["A"] * np.exp(-p["k"] * offs[b]), 1):
                i += 1
                cash += offs[b]
            elif u[s] >= 0.5 and i > 0 and f[s] < min(p["A"] * np.exp(-p["k"] * offs[a]), 1):
                i -= 1
                cash += offs[a]
            cash -= p["phi"] * (i - p["Q"]) ** 2
            inv.append(i - p["Q"])
        live[name] = {"inventory": inv, "score": cash, "max_abs": int(np.max(np.abs(inv)))}
    vals = np.array([r_["value"] for r_ in runs])
    return _json({"V_dp": V0, "dp_skew": dp["skew"], "dp_bid": dp["bid"], "dp_ask": dp["ask"], "q": qs,
                  "checkpoints": ck, "values": vals, "pct_final": vals[:, -1] / V0,
                  "skews": {str(s): runs[s]["skew"] for s in range(5)}, "sym_values": sym, "sym_best": max(sym),
                  "sym_best_offset": float(offs[jbest]), "glft_value": v_glft, "glft_skew": gl["skew"],
                  "glft_bid": gl["bid"], "glft_ask": gl["ask"], "live": live, "params": {k: v for k, v in p.items()}})


def _deep_train(kappa, seed, t, S, sigma, cost, T, iters=500, record_every=25, ck=(0, 100, 250, 500), ckpt=None):
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    n = S.shape[1] - 1
    K = 100.0
    net = torch.nn.Sequential(torch.nn.Linear(4, 32), torch.nn.Tanh(), torch.nn.Linear(32, 32), torch.nn.Tanh(),
                              torch.nn.Linear(32, 1))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    tt = torch.tensor(t, dtype=torch.float32)
    St = torch.tensor(S, dtype=torch.float32)
    prem = float(bs.price(100.0, 100.0, T, sigma))

    def feats(Sb, i, h):
        m = Sb.shape[0]
        d1 = (torch.log(Sb / K) + 0.5 * sigma ** 2 * (T - tt[i])) / (sigma * torch.sqrt(T - tt[i] + 1e-9))
        bsd = 0.5 * (1 + torch.erf(d1 / np.sqrt(2)))
        x = torch.stack([torch.full((m,), float((T - tt[i]) / T)), torch.log(Sb / K) / (sigma * np.sqrt(T)), h,
                         (bsd - h) * 10], 1)
        return x, bsd

    def run(Sb):
        m = Sb.shape[0]
        h, cash, costs = torch.zeros(m), torch.full((m,), prem), torch.zeros(m)
        for i in range(n):
            x, bsd = feats(Sb[:, i], i, h)
            new = h + torch.sigmoid(net(x).squeeze(-1)) * (bsd - h)
            tr = new - h
            cash = cash - tr * Sb[:, i] - cost * torch.abs(tr) * Sb[:, i]
            costs = costs + cost * torch.abs(tr) * Sb[:, i]
            h = new
        pnl = cash + h * Sb[:, -1] - cost * torch.abs(h) * Sb[:, -1] - torch.clamp(Sb[:, -1] - K, min=0)
        return pnl, costs + cost * torch.abs(h) * Sb[:, -1]

    def frac_curve():
        # the learned policy at mid-life and the money: the share of the gap to delta it closes, by gap size
        with torch.no_grad():
            gaps = torch.linspace(-0.3, 0.3, 61)
            i = n // 2
            Sb = torch.full((61,), K)
            _, bsd = feats(Sb, i, torch.zeros(61))
            h = bsd - gaps
            x, _ = feats(Sb, i, h)
            return torch.sigmoid(net(x).squeeze(-1)).numpy().tolist()

    g = torch.Generator().manual_seed(seed)
    loss_hist, snaps, start = [], {}, 0
    if ckpt is not None and ckpt.exists():   # resume a run that was killed (the machine is shared)
        st = torch.load(ckpt, weights_only=False)
        net.load_state_dict(st["net"])
        opt.load_state_dict(st["opt"])
        g.set_state(st["gen"])
        loss_hist, snaps, start = st["loss"], st["snaps"], st["it"]
    for it in range(start, iters + 1):
        if ckpt is not None and it % 10 == 0 and it > start:
            ckpt.parent.mkdir(parents=True, exist_ok=True)
            torch.save({"net": net.state_dict(), "opt": opt.state_dict(), "gen": g.get_state(), "loss": loss_hist,
                        "snaps": snaps, "it": it}, ckpt.with_suffix(".tmp"))
            ckpt.with_suffix(".tmp").replace(ckpt)
        if it in ck:
            snaps[str(it)] = frac_curve()
        if it == iters:
            break
        idx = torch.randint(0, 15000, (512,), generator=g)
        pnl, c = run(St[idx])
        loss = pnl.var() + kappa * c.mean()
        if it % record_every == 0:
            loss_hist.append(float(loss.detach()))
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        pnl, c = run(St[15000:])
        loss_hist.append(float(pnl.var() + kappa * c.mean()))
    return {"loss": loss_hist, "snaps": snaps, "sd": float(pnl.std()), "cost": float(c.mean())}


def compute_hedging_replay() -> dict:
    T, n, sigma, cost = 30 / 365, 30 * 4, 0.6, 0.001
    t, S = _gbm(20000, n, T, sigma, 112)     # the same 20,000 paths as ``hedging``
    # one cost weight, three seeds (the shared machine's budget); the other weights are ``hedging``'s single runs
    part = CACHE.partial("hedging_replay", {"kappas": [1], "seeds": [0, 1, 2], "iters": 500, "batch": 512})
    for kappa in (1.0,):
        for seed in range(3):
            key = f"{kappa:g}-{seed}"
            if key not in part:
                part[key] = _deep_train(kappa, seed, t, S, sigma, cost, T,
                                        ckpt=CACHE.dir / "hedging_replay_ckpt" / f"{key}.pt")
                print(f"    deep hedge kappa {kappa:g} seed {seed}: sd {part[key]['sd']:.3f}", flush=True)
    runs = {k: part[k] for k in part.done}
    return _json({"runs": runs, "steps": list(range(0, 500, 25)) + [500], "gaps": np.linspace(-0.3, 0.3, 61),
                  "checkpoints": [0, 100, 250, 500]})


def compute_greekhedge() -> dict:
    from explainer.quant.house import sim
    T, days, per = 30 / 365, 30, 4
    n = days * per
    dt = T / n
    out = {}
    for name, xi in (("GBM", 0.0), ("Heston", 1.2)):
        S, v = sim.heston_euler(100.0, 0.25, 3.0, 0.25, xi, -0.5, T, n, 10000, seed=1110)
        sig = np.sqrt(np.maximum(v, 1e-4))
        res = {}
        for rule in ("delta", "delta-gamma", "delta-gamma-vega"):
            pnl = np.zeros(S.shape[0])
            for i in range(n):
                s0, s1, a, b = S[:, i], S[:, i + 1], sig[:, i], sig[:, i + 1]
                tau0, tau1 = T - i * dt, T - (i + 1) * dt
                gb = {k_: -sum(bs.greeks(s0, 100.0, tau0, a, cp=cp)[k_] for cp in (1, -1))
                      for k_ in ("price", "delta", "gamma", "vega")}
                v1 = -sum(bs.price(s1, 100.0, max(tau1, 0.0), b, cp=cp) for cp in (1, -1))
                dpnl = v1 - gb["price"]
                n1 = n2 = np.zeros_like(s0)
                g7 = bs.greeks(s0, s0, 7 / 365, a)
                g60 = bs.greeks(s0, s0, 60 / 365, a)
                if rule == "delta-gamma":
                    n1 = -gb["gamma"] / g7["gamma"]
                elif rule == "delta-gamma-vega":
                    det = g7["gamma"] * g60["vega"] - g60["gamma"] * g7["vega"]
                    n1 = (-gb["gamma"] * g60["vega"] + g60["gamma"] * gb["vega"]) / det
                    n2 = (-g7["gamma"] * gb["vega"] + g7["vega"] * gb["gamma"]) / det
                sh = -(gb["delta"] + n1 * g7["delta"] + n2 * g60["delta"])
                dpnl = dpnl + n1 * (bs.price(s1, s0, 7 / 365 - dt, b) - g7["price"])
                dpnl = dpnl + n2 * (bs.price(s1, s0, 60 / 365 - dt, b) - g60["price"]) + sh * (s1 - s0)
                pnl += dpnl
            res[rule] = {"sd": float(pnl.std()), "mean": float(pnl.mean()),
                         "hist": np.histogram(np.clip(pnl, -15, 15), bins=60, range=(-15, 15))[0]}
        out[name] = res
    # the Greek-space picture at the start: a short straddle, and two hedge options
    gk = lambda K, T_: {k_: float(v) for k_, v in bs.greeks(100.0, K, T_, 0.5).items()}  # noqa: E731
    book = {k_: -(gk(100.0, T)[k_] + float(bs.greeks(100.0, 100.0, T, 0.5, cp=-1)[k_])) for k_ in
            ("delta", "gamma", "vega")}
    i7, i60 = gk(100.0, 7 / 365), gk(100.0, 60 / 365)
    sol = quoting.greek_hedge(book, (i7, i60))
    # vega by expiry bucket, and a parallel hedge with the 90-day option, under a steepening move
    exps = np.array([7, 30, 60, 90, 180])
    qty = np.array([-3.0, -2.0, 1.0, 0.0, 2.5])
    vb = np.array([qty[j] * gk(100.0, exps[j] / 365)["vega"] / 100 for j in range(5)])
    v90 = gk(100.0, 90 / 365)["vega"] / 100
    hq = -vb.sum() / v90
    after = vb.copy()
    after[3] += hq * v90
    move = np.array([4.0, 2.5, 1.0, 0.0, -1.5])          # vol points: the short end up, the long end down
    return _json({"sims": out, "book": book, "i7": i7, "i60": i60, "sol": sol, "buckets": exps, "vega_by": vb,
                  "vega_after": after, "hedge_qty": hq, "move": move, "leftover": float(after @ move),
                  "before": float(vb @ move)})


def compute_pin_sim() -> dict:
    from explainer.quant.house import sim
    T, n = 2 / 365, 192
    out = {}
    for name, g in (("none", 0.0), ("long", 1.0), ("short", -1.0)):
        t, P = sim.pin_simulation(100.0, 100.0, T, 0.5, g, 0.08, n, 2000, seed=1111)
        x = P[:, -1]
        out[name] = {"terminal": x, "near": float(np.mean(np.abs(x - 100) < 0.5)),
                     "hist": np.histogram(np.clip(x, 94, 106), bins=48, range=(94, 106))[0],
                     "paths": P[:60, ::4]}
    return _json({**out, "t": np.linspace(0, 48, n + 1)[::4], "T_hours": 48.0, "impact": 0.08})


def compute_pin_btc() -> dict:
    import calendar
    kl = data.binance_klines("BTCUSDT", "1h", "2021-01", "2025-12")
    t = np.asarray(kl["time"]) + 3600
    c = np.asarray(kl["close"])
    dt_ = [datetime.fromtimestamp(x, tz=timezone.utc) for x in t]
    wd = np.array([d.weekday() for d in dt_])
    hr = np.array([d.hour for d in dt_])
    last = np.array([d.day + 7 > calendar.monthrange(d.year, d.month)[1] for d in dt_])
    dist = np.abs(c / 1000 - np.round(c / 1000))
    groups = {"all hours": np.ones(len(c), bool), "Fridays 08:00": (wd == 4) & (hr == 8),
              "monthly expiries": (wd == 4) & (hr == 8) & last, "Fridays 07:00": (wd == 4) & (hr == 7)}
    p0 = float(np.mean(dist < 0.1))
    out = {}
    for k, m in groups.items():
        x = dist[m]
        share = float(np.mean(x < 0.1))
        out[k] = {"n": int(m.sum()), "share": share, "mean": float(x.mean()),
                  "z": float((share - p0) / np.sqrt(p0 * (1 - p0) / m.sum())),
                  "hist": np.histogram(x, bins=10, range=(0, 0.5))[0] / m.sum()}
    return _json({"groups": out, "first": str(dt_[0].date()), "last": str(dt_[-1].date())})


def compute_early() -> dict:
    from explainer.quant.house import trees
    S, K, T, r, sig, D = 100.0, 100.0, 2 / 12, 0.04, 0.3, 2.0
    tD = T - 3 / 52
    big = trees.american_call_dividend(S, K, T, r, sig, D, tD, N=400)
    N = 10
    small = trees.american_call_dividend(S, K, T, r, sig, D, tD, N=N)
    dt = T / N
    u = np.exp(sig * np.sqrt(dt))
    Sx = S - D * np.exp(-r * tD)
    layers = [[float(Sx * u ** (2 * j - n) + (D * np.exp(-r * (tD - n * dt)) if n * dt < tD else 0.0))
               for j in range(n + 1)] for n in range(N + 1)]
    # the race at the deepest node exercised: the dividend against the time value given up
    n_, j_, s_ = max(small["region"], key=lambda x: x[2]) if small["region"] else (0, 0, S)
    tau = T - tD
    put = float(bs.price(s_ - D, K, tau, sig, r, cp=-1))
    tv = K * (1 - np.exp(-r * tau))
    # the desk question: deep ITM, dividend tomorrow of 2, rates 4%, two months left, the put worth 0.3
    dq = {"D": 2.0, "carry": float(100 * (1 - np.exp(-0.04 * 2 / 12))), "put": 0.3}
    # the dividend play: expected gain per unit dividend of a wash of w contracts against open interest OI
    e = np.linspace(0, 1, 41)
    w = np.linspace(0, 5, 41)
    E, W = np.meshgrid(e, w, indexing="ij")
    gain = W * (1 - E) / (1 + W)             # per unit OI and dividend
    g = np.random.default_rng(1112)
    others, mine, exer = 30, 20, int(round(0.6 * 30)) + 20
    pool = np.array([0] * others + [1] * mine)
    assigned = g.permutation(len(pool))[:exer]
    hit = np.zeros(len(pool), bool)
    hit[assigned] = True
    return _json({"S": S, "K": K, "T": T, "r": r, "sigma": sig, "D": D, "tD": tD, "price": big["price"],
                  "european": big["european"], "layers": layers, "region": small["region"], "N": N,
                  "tD_step": tD / dt, "node": [n_, j_, s_], "put": put, "carry": float(tv), "dq": dq,
                  "dq_ex": bool(dq["D"] > dq["carry"] + dq["put"]), "e": e, "w": w, "gain": gain,
                  "lottery": {"pool": pool, "hit": hit, "others": others, "mine": mine, "exercised": exer,
                              "mine_free": int(np.sum((pool == 1) & ~hit)),
                              "expected_free": mine * (1 - exer / (others + mine))}})


def compute_cor3m() -> dict:
    c = data.cboe_index("COR3M")
    d, v = c["date"], c["close"]
    yr = d // 10000
    t = yr + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365
    peaks = {}
    for y in range(int(yr.min()), int(yr.max()) + 1):
        m = yr == y
        peaks[str(y)] = {"max": float(v[m].max()), "min": float(v[m].min()), "argmax": int(d[m][np.argmax(v[m])]),
                         "argmin": int(d[m][np.argmin(v[m])])}
    i = int(np.argmax(v))
    toy = quoting.implied_correlation(0.20, [1 / 3] * 3, [0.25, 0.30, 0.35])
    big = quoting.implied_correlation(0.20, np.full(50, 1 / 50), np.full(50, 0.30))
    return _json({"t": t[::2], "v": v[::2], "n": int(len(v)), "mean": float(v.mean()), "max": float(v[i]),
                  "argmax": int(d[i]), "years": peaks, "first": int(d[0]), "last": int(d[-1]), "toy": toy,
                  "big": big, "big_approx": (0.2 / 0.3) ** 2})


def compute_dispersion_sim() -> dict:
    """A one-factor market of 20 stocks at 30% vol, index options priced at an implied correlation of 0.5: short the
    index straddle and long the members', vega-matched, hedged daily, in 400 scenarios of realized correlation."""
    N, n, T, s, rho_i = 20, 63, 63 / 252, 0.30, 0.5
    sI = float(np.sqrt(s * s * (1 / N + (1 - 1 / N) * rho_i)))
    g = np.random.default_rng(1113)
    scen = 400
    rho = g.uniform(0.05, 0.95, scen)
    dt = T / n
    f = g.standard_normal((scen, n))
    e = g.standard_normal((scen, N, n))
    z = np.sqrt(rho)[:, None, None] * f[:, None, :] + np.sqrt(1 - rho)[:, None, None] * e
    lr = -0.5 * s * s * dt + s * np.sqrt(dt) * z
    X = 100 * np.exp(np.concatenate([np.zeros((scen, N, 1)), np.cumsum(lr, 2)], 2))
    I = X.mean(1)
    tt = np.linspace(0, T, n + 1)
    st = lambda P, sg: sum(hedge.delta_hedge(tt, P, 100.0, T, sg, cp=cp, position=1)["pnl"] for cp in (1, -1))  # noqa
    idx = -st(I, sI)
    mem = st(X.reshape(scen * N, n + 1), s).reshape(scen, N).mean(1)
    # scale the member leg so its vega matches the index leg's (ATM straddle vega is about sigma-free)
    pnl = idx + mem
    rr = np.array([np.corrcoef(np.diff(np.log(X[j]), axis=1))[np.triu_indices(N, 1)].mean() for j in range(scen)])
    return _json({"rho_real": rr, "pnl": pnl, "idx": idx, "mem": mem, "rho_impl": rho_i, "sigma_index": sI,
                  "corr": float(np.corrcoef(rho_i - rr, pnl)[0, 1]), "share_right_sign":
                  float(np.mean(np.sign(pnl) == np.sign(rho_i - rr))), "N": N})


def compute_shortdated() -> dict:
    days = _flow_days()
    kl = data.binance_klines("BTCUSDT", "1h", "2024-01", "2025-12")
    tk, ck = np.asarray(kl["time"]) + 3600, np.asarray(kl["close"])
    rows, tickets = [], []
    for day in days:
        for t in data.deribit_trades(day, hours=surface.HOURS):
            if None in (t.get("price"), t.get("index_price"), t.get("direction"), t.get("amount")):
                continue
            exp, K, cp = surface.parse_instrument(t["instrument_name"])
            ts = t["timestamp"] / 1e3
            T = exp.timestamp() - ts
            if T <= 0 or T > 2 * 86400:
                continue
            ST = float(np.interp(exp.timestamp(), tk, ck))
            I = t["index_price"]
            prem = t["price"] * I
            pay = max(cp * (ST - K), 0.0)
            otm = (cp * (K - I)) > 0
            s = 1 if t["direction"] == "buy" else -1
            rows.append((s, t["amount"], prem, pay, otm, T / 3600))
            if otm and s > 0:
                tickets.append((prem, pay, K / I, cp))
    a = np.array(rows, float)
    s, amt, prem, pay, otm, Th = a.T
    out = {"n": int(len(a))}
    for lab, m in (("otm", otm == 1), ("otm24", (otm == 1) & (Th < 24)), ("itm", otm == 0)):
        b = m & (s > 0)
        sl = m & (s < 0)
        out[lab] = {"n_buy": int(b.sum()), "ret_buy": float((pay[b] - prem[b]).sum() / prem[b].sum()),
                    "worthless": float(np.mean(pay[b] == 0)), "profitable": float(np.mean(pay[b] > prem[b])),
                    "n_sell": int(sl.sum()), "ret_sell": float((pay[sl] - prem[sl]).sum() / prem[sl].sum()),
                    "paid": float(prem[b].sum()), "back": float(pay[b].sum())}
    tk_ = np.array(tickets)  # every short-dated OTM buy over the hundred Wednesdays; sixty are drawn for the grid
    g = np.random.default_rng(1114)
    pick = g.choice(len(tk_), size=min(60, len(tk_)), replace=False) if len(tk_) else []
    out["tickets"] = tk_[np.sort(pick)] if len(tk_) else np.zeros((0, 4))
    # the theory: expected payoff over price of an OTM call, at implied 50% and realized 45%, as expiry nears
    taus = np.geomspace(30 / 365, 1 / (365 * 24), 60)
    k = 0.05
    exact = bs.price(1.0, np.exp(k), taus, 0.45) / bs.price(1.0, np.exp(k), taus, 0.50)
    approx = (0.45 / 0.5) ** 3 * np.exp(-k * k / (2 * taus) * (1 / 0.45 ** 2 - 1 / 0.5 ** 2))
    out.update({"taus_h": taus * 365 * 24, "ratio_exact": exact, "ratio_approx": approx})
    return _json(out)


def compute_alleged_surface() -> dict:
    lam = 0.01
    Q = np.linspace(0, 200, 41)
    D = np.linspace(0, 400, 41)
    QQ, DD = np.meshgrid(Q, D, indexing="ij")
    net = -lam * QQ ** 2 + 2 * lam * QQ * DD
    return _json({"Q": Q, "D": D, "net": net, "lam": lam, "share_pos": float(np.mean(net > 0))})


def compute_shortvol() -> dict:
    kf = data.ken_french_daily()
    vx = data.fred("VIXCLS", start="2016-01-01")
    d0, d1 = 20161230, 20201231
    m = (kf["date"] >= d0) & (kf["date"] <= d1)
    dates = kf["date"][m]
    lvl = 100 * np.cumprod(1 + kf["mkt"][m])
    lvl = lvl / lvl[0] * 100
    vix = np.interp(dates, vx["date"], vx["value"]) / 100
    skew = 2.5                                  # illustrative: vol rises 2.5 x the log-distance below spot
    vol = lambda S, K, v: v * (1 + skew * np.maximum(np.log(S / K), 0))  # noqa: E731
    roll = 21
    T0 = roll / 252
    books = {}
    for name, hk in (("near hedges", 0.825), ("deep hedges", 0.60)):
        pnl, short_k, long_k, start = [0.0], None, None, 0
        val_prev = 0.0
        for i in range(len(dates)):
            if i % roll == 0:
                if i:
                    tau = 0.0
                    val = (-bs.price(lvl[i], short_k, tau, 0.2, cp=-1) + bs.price(lvl[i], long_k, tau, 0.2, cp=-1))
                    pnl.append(pnl[-1] + float(val) - val_prev)
                short_k, long_k, start = 0.97 * lvl[i], hk * lvl[i], i
                val_prev = float(-bs.price(lvl[i], short_k, T0, vol(lvl[i], short_k, vix[i]), cp=-1)
                                 + bs.price(lvl[i], long_k, T0, vol(lvl[i], long_k, vix[i]), cp=-1))
                continue
            tau = max(T0 - (i - start) / 252, 1e-6)
            val = float(-bs.price(lvl[i], short_k, tau, vol(lvl[i], short_k, vix[i]), cp=-1)
                        + bs.price(lvl[i], long_k, tau, vol(lvl[i], long_k, vix[i]), cp=-1))
            pnl.append(pnl[-1] + val - val_prev)
            val_prev = val
        books[name] = np.array(pnl[:len(dates)])
    out = {"dates": dates, "level": lvl, "vix": vix * 100}
    for name, x in books.items():
        out[f"pnl {name}"] = x
        peak = np.maximum.accumulate(x)
        for lab, a, b in (("feb2018", 20180101, 20180331), ("mar2020", 20200201, 20200430)):
            mm = (dates >= a) & (dates <= b)
            out[f"dd {name} {lab}"] = float((x - peak)[mm].min())
        q = dates < 20200201
        out[f"before {name}"] = float(x[q][-1])
        out[f"end {name}"] = float(x[-1])
    # the question: a one-month hedge at 20% and 40% out of the money, at VIX 15: cost, and payoff in a 35% crash
    out["q_cost20"] = float(bs.price(100, 80, T0, vol(100, 80, 0.15), cp=-1))
    out["q_cost40"] = float(bs.price(100, 60, T0, vol(100, 60, 0.15), cp=-1))
    out["q_pay20"], out["q_pay40"] = 15.0, 0.0
    out["skew"] = skew
    return _json(out)


def _har_daily():
    hours, S, _ = _hours()
    day = (hours // 86400).astype(int)
    r = np.diff(np.log(S))
    rv_day, days = [], []
    for d in np.unique(day[1:]):
        m = day[1:] == d
        if m.sum() >= 20:
            rv_day.append(np.sum(r[m] ** 2))
            days.append(d)
    return np.array(days), np.array(rv_day)


def _ridge(X, y, lam=1.0):
    mu, sd = X.mean(0), X.std(0) + 1e-12
    Z = (X - mu) / sd
    b = np.linalg.solve(Z.T @ Z + lam * np.eye(Z.shape[1]), Z.T @ (y - y.mean()))
    return lambda x: (x - mu) / sd @ b + y.mean()


def _boost(X, y, n_trees=50, lr=0.1, depth=2, min_leaf=4):
    """Gradient boosting of depth-2 regression trees on squared error (Friedman 2001), small enough to read."""
    def fit_tree(X, r, d):
        best = None
        if d > 0 and len(r) >= 2 * min_leaf:
            for j in range(X.shape[1]):
                xs = np.unique(np.quantile(X[:, j], np.linspace(0.05, 0.95, 16)))
                for c in xs:
                    L = X[:, j] <= c
                    if L.sum() < min_leaf or (~L).sum() < min_leaf:
                        continue
                    sse = ((r[L] - r[L].mean()) ** 2).sum() + ((r[~L] - r[~L].mean()) ** 2).sum()
                    if best is None or sse < best[0]:
                        best = (sse, j, c, L)
        if best is None:
            v = float(r.mean())
            return lambda x: np.full(len(x), v)
        _, j, c, L = best
        lt, rt = fit_tree(X[L], r[L], d - 1), fit_tree(X[~L], r[~L], d - 1)
        return lambda x: np.where(x[:, j] <= c, lt(x), rt(x))

    base = float(y.mean())
    trees_, f = [], np.full(len(y), base)
    for _ in range(n_trees):
        t_ = fit_tree(X, y - f, depth)
        trees_.append(t_)
        f = f + lr * t_(X)
    return lambda x: base + lr * sum(t_(x) for t_ in trees_)


def compute_frontier_ml() -> dict:
    w = _weekly()
    y = np.asarray(w["hedged"], float)
    days = w["days"]
    dd, rvd = _har_daily()
    from explainer.quant.house import vol as V_
    X = []
    for i, d in enumerate(days):
        di = int(_ts(d) // 86400)
        j = int(np.searchsorted(dd, di))
        past = rvd[:j]
        f = V_.har_fit(past)
        Xh, _ = V_._har_design(np.concatenate([past[-31:], [np.nan]]))
        hv = float(np.sqrt(max(float((np.column_stack([np.ones(1), Xh[-1:]]) @ f["beta"])[0]), 1e-8) * 365))
        trail = float(np.sqrt(past[-30:].mean() * 365))
        iv = float(w["sig"][i])
        X.append([iv - hv, iv - trail, w["feats"][i]["rr"], w["feats"][i]["slope"]])
    X = np.array(X)
    n0, gap = 30, 4                       # the first fit has 26 weeks whose outcomes are known
    pred = {"ridge": [], "boost": [], "signal": []}
    band = {"ridge": [], "boost": []}
    g = np.random.default_rng(1115)
    for t in range(n0, len(y)):
        tr = np.arange(0, t - gap + 1)
        pred["ridge"].append(float(_ridge(X[tr], y[tr])(X[t:t + 1])[0]))
        pred["boost"].append(float(_boost(X[tr], y[tr])(X[t:t + 1])[0]))
        pred["signal"].append(-1.0 if X[t, 0] > 0 else 1.0)
        for name, fn in (("ridge", _ridge), ("boost", _boost)):
            bb = []
            for b in range(5):
                rs = g.choice(tr, size=len(tr), replace=True)
                bb.append(float(fn(X[rs], y[rs])(X[t:t + 1])[0]))
            band[name].append(bb)
    yo = y[n0:]
    out = {"weeks": np.arange(n0, len(y)), "y": yo, "y_all": y, "X": X, "n_oos": int(len(yo)),
           "features": ["IV - HAR", "IV - RV30", "RR25", "7d - 60d"]}
    for k, p in pred.items():
        p = np.array(p)
        out[f"pred {k}"] = p
        if k != "signal":
            out[f"r2 {k}"] = float(1 - np.sum((yo - p) ** 2) / np.sum((yo - y[:n0].mean()) ** 2))
            out[f"corr {k}"] = float(np.corrcoef(p, yo)[0, 1])
            out[f"band {k}"] = np.array(band[k]).T
            # cumulative squared error, for the replay's curve
            out[f"cmse {k}"] = np.cumsum((yo - p) ** 2) / np.arange(1, len(yo) + 1)
        sell = p < 0
        out[f"trade {k}"] = float(np.mean(np.where(sell, -yo, 0.0)))
        out[f"t {k}"] = _nw_t(np.where(sell, -yo, 0.0))
    out["cmse mean"] = np.cumsum((yo - np.array([y[:i - gap + 1].mean() for i in range(n0, len(y))])) ** 2) / \
        np.arange(1, len(yo) + 1)
    out["trade always"] = float(np.mean(-yo))
    out["t always"] = _nw_t(-yo)
    reg = pit.register("btc_hedged_straddle_ml", inspect.getsource(compute_frontier_ml),
                       {"target": "4-week hourly-hedged ATM straddle P&L", "features": out["features"],
                        "models": ["ridge", "depth-2 boosting"], "walk_forward": "past only, 4-week gap"}, trials=1)
    out["registered"] = reg
    out["trials"] = pit.trials_so_far()
    return _json(out)


def compute_buckets() -> dict:
    """Vega by expiry bucket for a small book, a parallel hedge with the 90-day option, and a steepening move."""
    gk = lambda T_: float(bs.greeks(100.0, 100.0, T_ / 365, 0.5)["vega"]) / 100  # noqa: E731
    exps = np.array([7, 30, 60, 90, 180])
    qty = np.array([-3.0, -2.0, 1.0, 0.0, 2.5])
    vb = qty * np.array([gk(e) for e in exps])
    hq = -vb.sum() / gk(90)
    after = vb.copy()
    after[3] += hq * gk(90)
    move = np.array([4.0, 2.5, 1.0, -0.5, -1.5])          # vol points: the short end up, the long end down
    return _json({"buckets": exps, "vega_by": vb, "vega_after": after, "hedge_qty": hq, "move": move,
                  "before": float(vb @ move), "after": float(after @ move), "parallel_after": float(after.sum())})


ITEMS_NEW = {"buckets": compute_buckets, "explain": compute_explain, "scalp_shuffle": compute_scalp_shuffle, "frequency": compute_frequency,
             "secondorder": compute_secondorder, "strategies": compute_strategies, "premium": compute_premium,
             "kelly": compute_kelly, "flow": compute_flow, "mm_learn": compute_mm_learn,
             "hedging_replay": compute_hedging_replay, "greekhedge": compute_greekhedge, "pin_sim": compute_pin_sim,
             "pin_btc": compute_pin_btc, "early": compute_early, "cor3m": compute_cor3m,
             "dispersion_sim": compute_dispersion_sim, "shortdated": compute_shortdated,
             "alleged_surface": compute_alleged_surface, "shortvol": compute_shortvol,
             "frontier_ml": compute_frontier_ml}


ITEMS = {"scalp": compute_scalp, "edge": compute_edge, "mm": compute_mm, "dispersion": compute_dispersion,
         "alleged": compute_alleged, "hedging": compute_hedging, "envelope": compute_envelope, **ITEMS_NEW}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
