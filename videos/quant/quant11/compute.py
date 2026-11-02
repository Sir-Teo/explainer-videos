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
load = CACHE.load

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
    net = torch.nn.Sequential(torch.nn.Linear(3, 32), torch.nn.Tanh(), torch.nn.Linear(32, 32), torch.nn.Tanh(),
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
            # start from the Black-Scholes delta and learn the deviation: a residual policy
            d1 = (torch.log(Sb[:, i] / K) + 0.5 * sigma ** 2 * (T - tt[i])) / (sigma * torch.sqrt(T - tt[i] + 1e-9))
            bsd = 0.5 * (1 + torch.erf(d1 / np.sqrt(2)))
            new = bsd + net(x).squeeze(-1) * 0.5
            tr = new - h
            cash = cash - tr * Sb[:, i] - cost * torch.abs(tr) * Sb[:, i]
            costs = costs + cost * torch.abs(tr) * Sb[:, i]
            h = new
        pnl = cash + h * Sb[:, -1] - cost * torch.abs(h) * Sb[:, -1] - torch.clamp(Sb[:, -1] - K, min=0)
        return pnl, costs + cost * torch.abs(h) * Sb[:, -1]

    kappa = 1.0
    for it in range(250):
        idx = torch.randint(0, 15000, (1024,))
        pnl, c = run(St[idx])
        loss = pnl.var() + kappa * c.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        pnl, c = run(St[15000:])
    rows.append({"rule": "deep hedge", "param": kappa, "sd": float(pnl.std()), "cost": float(c.mean()), "trades": float("nan")})
    return _json({"rows": rows, "premium": prem, "sigma": sigma, "cost_rate": cost, "steps": n})


def compute_envelope() -> dict:
    reg = {"btc_vol_forecast_edge": pit.register("btc_vol_forecast_edge", inspect.getsource(compute_edge),
                                                 {"signal": "DVOL > HAR forecast of 30-day realized vol",
                                                  "trade": "Part 10's sold, hourly-hedged 30-day ATM call"}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


ITEMS = {"scalp": compute_scalp, "edge": compute_edge, "mm": compute_mm, "dispersion": compute_dispersion,
         "alleged": compute_alleged, "hedging": compute_hedging, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
