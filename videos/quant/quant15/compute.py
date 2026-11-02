"""Every number in Part 15 (Exotics and Structured Products), computed and cached in .cache/quant15/.

    python -m videos.quant.quant15.compute [items] [--force]

Items (seconds to minutes on a CPU):

* ``market``    the CSI 500 (through its largest ETF, 510500) and the HSCEI, daily, 2015-2025; volatility and the
                January-February 2024 fall;
* ``barrier``   a down-and-out call watched continuously, daily, weekly and monthly: Monte Carlo against the closed
                form and Broadie-Glasserman-Kou's corrected barrier; its delta near the barrier;
* ``digital``   a digital's price, delta and gamma as expiry nears, and the call-spread overhedge by width;
* ``asian``     the arithmetic Asian by Monte Carlo, with and without the geometric control variate; the lookback;
* ``snowball``  the CSI 500 snowball: the fair coupon by volatility; the note's value over (spot, time) before and
                after knock-in; the dealer's delta and vega across spot;
* ``surrogate`` a neural network trained on Monte Carlo snowball prices: its error against fresh Monte Carlo, and
                its speed;
* ``book2024``  a book of snowballs issued monthly in 2021-2023 on the CSI 500, followed through January-February
                2024: knock-ins by day, and the dealers' delta hedge, from the surrogate;
* ``korea``     HSCEI-linked step-down ELS issued in 2021, followed to maturity in 2024;
* ``worstof``   a worst-of put on the CSI 500 and the HSCEI against correlation; the measured correlation;
* ``uvm``       uncertain-volatility bounds (Avellaneda, Levy and Paras) for a call spread, against Black-Scholes;
* ``envelope``  registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, exotics as X, pit

CACHE = Cache("quant15")
load = CACHE.load

DPM = 21  # trading days a month
TERMS = dict(ko=1.03, ki=0.75, lockup=3, months=24, r=0.02)


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


def _csi500():
    return data.yahoo_daily("510500.SS", "2015-01-01", "2025-11-30")


def _hscei():
    return data.yahoo_daily("^HSCE", "2015-01-01", "2025-11-30")


def _sigma():
    """The pricing volatility: the CSI 500 ETF's realized volatility over 2021-2023, the years the book was sold."""
    d = _csi500()
    m = (d["date"] >= 20210101) & (d["date"] <= 20231231)
    r = np.diff(np.log(d["close"][m]))
    return float(np.std(r) * np.sqrt(244))


# ---------------------------------------------------------------------------
def compute_market() -> dict:
    c, h = _csi500(), _hscei()
    out = {}
    for name, d in (("csi500", c), ("hscei", h)):
        r = np.diff(np.log(d["close"]))
        out[name] = {"date": d["date"], "close": d["close"], "vol_all": float(np.std(r) * np.sqrt(244))}
    m = (c["date"] >= 20231229) & (c["date"] <= 20240229)
    cc, dd = c["close"][m], c["date"][m]
    out["fall_2024"] = {"from": int(dd[0]), "to": int(dd[np.argmin(cc)]), "drop": float(cc.min() / cc[0] - 1)}
    out["sigma_2021_2023"] = _sigma()
    return _json(out)


def compute_barrier() -> dict:
    S, K, H, T, s, r = 100.0, 100.0, 85.0, 0.5, 0.25, 0.02
    P = X.gbm_paths(S, s, T, 2520, 100000, r, seed=3)  # 20 steps a trading day, 126 days
    pay = np.exp(-r * T) * np.maximum(P[-1] - K, 0)
    rows = []
    for name, every in (("monthly", 420), ("weekly", 100), ("daily", 20), ("hourly", 3), ("continuous (fine grid)", 1)):
        alive = P[::every].min(axis=0) > H
        mc = float(np.mean(pay * alive))
        n_obs = 2520 // every
        bgk = float(X.down_out_call(S, K, X.bgk_barrier(H, S, s, T / n_obs), T, s, r))
        rows.append({"name": name, "n_obs": n_obs, "mc": mc, "se": float(np.std(pay * alive) / np.sqrt(len(pay))),
                     "bgk": bgk})
    cont = float(X.down_out_call(S, K, H, T, s, r))
    van = float(bs.price(S, K, T, s, r))
    Sg = np.linspace(80, 130, 201)
    v = X.down_out_call(Sg, K, H, T, s, r)
    delta = np.gradient(v, Sg)
    return _json({"rows": rows, "continuous": cont, "vanilla": van, "S": Sg, "value": v, "delta": delta,
                  "params": {"S": S, "K": K, "H": H, "T": T, "sigma": s, "r": r}})


def compute_digital() -> dict:
    K, s = 100.0, 0.25
    Sg = np.linspace(90, 110, 401)
    taus = {"a month": 21 / 252, "a day": 1 / 252, "an hour": 1 / (252 * 7)}
    curves = {}
    for name, T in taus.items():
        p = X.digital_call(Sg, K, T, s)
        d = np.gradient(p, Sg)
        g = np.gradient(d, Sg)
        curves[name] = {"price": p, "delta": d, "gamma": g, "max_delta": float(d.max()), "T": T}
    T = 21 / 252
    widths = [0.5, 1.0, 2.0, 5.0]
    spread = [{"eps": e, "price": float(X.call_spread_digital(100.0, K, T, s, e)),
               "max_delta": float(np.max(np.gradient(X.call_spread_digital(Sg, K, 1 / 252, s, e), Sg)))} for e in widths]
    return _json({"S": Sg, "curves": curves, "digital_atm": float(X.digital_call(100.0, K, T, s)), "spread": spread})


def compute_asian() -> dict:
    S, K, T, s, r, n = 100.0, 100.0, 1.0, 0.25, 0.02, 252
    geo_cf = float(X.geometric_asian_call(S, K, T, s, n, r))
    out = []
    for n_paths in (1000, 4000, 16000, 64000):
        ests, ests_cv = [], []
        for seed in range(20):
            P = X.gbm_paths(S, s, T, n, n_paths, r, seed=100 + seed)
            A = P[1:].mean(axis=0)
            G = np.exp(np.log(P[1:]).mean(axis=0))
            ya = np.exp(-r * T) * np.maximum(A - K, 0)
            yg = np.exp(-r * T) * np.maximum(G - K, 0)
            c = np.cov(ya, yg)
            b = c[0, 1] / c[1, 1]
            ests.append(ya.mean())
            ests_cv.append(ya.mean() - b * (yg.mean() - geo_cf))
        out.append({"n": n_paths, "sd_plain": float(np.std(ests)), "sd_cv": float(np.std(ests_cv)),
                    "mean_cv": float(np.mean(ests_cv))})
    P = X.gbm_paths(S, s, T, n, 64000, r, seed=7)
    look_mc = float(np.exp(-r * T) * np.mean(P[-1] - P.min(axis=0)))
    return _json({"rows": out, "geo_cf": geo_cf, "price": out[-1]["mean_cv"], "vanilla": float(bs.price(S, K, T, s, r)),
                  "lookback_cf": float(X.lookback_floating_call(S, T, s, r)), "lookback_mc_daily": look_mc})


def compute_snowball() -> dict:
    sig = _sigma()
    vols = np.array([0.12, 0.16, 0.20, 0.24, 0.28, 0.32])
    coupons = [X.fair_coupon(v, n_paths=20000, seed=1, **TERMS) for v in vols]
    c0 = X.fair_coupon(sig, n_paths=40000, seed=1, **TERMS)
    # value over (spot, months elapsed), not knocked in and knocked in
    spots = np.linspace(0.65, 1.10, 19)
    months = np.arange(0, 24, 2)
    surf = np.zeros((len(months), len(spots)))
    surf_ki = np.zeros_like(surf)
    for i, m in enumerate(months):
        for j, S in enumerate(spots):
            kin = S < TERMS["ki"]
            surf[i, j] = X.snowball_price(sig, coupon=c0, S=S, elapsed_days=int(m * DPM), knocked_in=kin, n_paths=6000,
                                          seed=11, **TERMS)
            surf_ki[i, j] = X.snowball_price(sig, coupon=c0, S=S, elapsed_days=int(m * DPM), knocked_in=True,
                                             n_paths=6000, seed=11, **TERMS)
    # the dealer is short the note: its delta and vega are minus the note's; finite differences with common numbers
    sp = np.linspace(0.70, 1.05, 36)
    h, hv = 0.01, 0.01
    rows = []
    for S in sp:
        kin = S < TERMS["ki"]
        f = lambda SS, vv: X.snowball_price(vv, coupon=c0, S=SS, elapsed_days=6 * DPM, knocked_in=kin,  # noqa: E731
                                            n_paths=30000, seed=21, **TERMS)
        v0 = f(S, sig)
        d = (f(S + h, sig) - f(S - h, sig)) / (2 * h)
        vg = (f(S, sig + hv) - f(S, sig - hv)) / (2 * hv) / 100  # per vol point
        rows.append({"S": S, "value": v0, "note_delta": d, "note_vega": vg})
    return _json({"sigma": sig, "vols": vols, "coupons": coupons, "coupon": c0, "spots": spots, "months": months,
                  "surface": surf, "surface_ki": surf_ki, "greeks": rows, "terms": TERMS})


def _torch():
    import torch
    torch.set_num_threads(1)
    return torch


def _surrogate_data(sig, c0, n, seed, n_paths):
    g = np.random.default_rng(seed)
    S = g.uniform(0.6, 1.2, n)
    m = g.uniform(0, 23.5, n)
    kin = g.random(n) < 0.35
    kin |= S < TERMS["ki"]
    y = np.array([X.snowball_price(sig, coupon=c0, S=s_, elapsed_days=int(mm * DPM), knocked_in=bool(k), n_paths=n_paths,
                                   seed=int(1000 + i), **TERMS) for i, (s_, mm, k) in enumerate(zip(S, m, kin))])
    return np.column_stack([np.log(S), m / 24, kin.astype(float)]), y


def compute_surrogate() -> dict:
    torch = _torch()
    sn = load("snowball")
    sig, c0 = sn["sigma"], sn["coupon"]
    t0 = time.time()
    Xtr, ytr = _surrogate_data(sig, c0, 3000, 1, 3000)
    t_data = time.time() - t0
    Xte, yte = _surrogate_data(sig, c0, 150, 2, 40000)
    torch.manual_seed(0)
    net = torch.nn.Sequential(torch.nn.Linear(3, 64), torch.nn.SiLU(), torch.nn.Linear(64, 64), torch.nn.SiLU(),
                              torch.nn.Linear(64, 1))
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    xt = torch.tensor(Xtr, dtype=torch.float32)
    yt = torch.tensor(ytr[:, None], dtype=torch.float32)
    t0 = time.time()
    for step in range(4000):
        idx = torch.randint(0, len(xt), (256,))
        loss = torch.mean((net(xt[idx]) - yt[idx]) ** 2)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step == 3000:
            for gr in opt.param_groups:
                gr["lr"] = 1e-3
    t_train = time.time() - t0
    with torch.no_grad():
        pte = net(torch.tensor(Xte, dtype=torch.float32)).numpy().ravel()
        t0 = time.time()
        for _ in range(100):
            net(torch.tensor(Xte, dtype=torch.float32))
        t_net = (time.time() - t0) / (100 * len(Xte))
    t0 = time.time()
    X.snowball_price(sig, coupon=c0, n_paths=40000, seed=3, **TERMS)
    t_mc = time.time() - t0
    torch.save(net.state_dict(), CACHE.dir / "surrogate.pt")
    err = pte - yte
    return _json({"rmse": float(np.sqrt(np.mean(err ** 2))), "max_err": float(np.abs(err).max()),
                  "test_mc": yte, "test_net": pte, "t_net": t_net, "t_mc": t_mc, "t_data": t_data, "t_train": t_train,
                  "n_train": len(ytr), "train_paths": 3000, "test_paths": 40000})


def _net():
    torch = _torch()
    net = torch.nn.Sequential(torch.nn.Linear(3, 64), torch.nn.SiLU(), torch.nn.Linear(64, 64), torch.nn.SiLU(),
                              torch.nn.Linear(64, 1))
    net.load_state_dict(torch.load(CACHE.dir / "surrogate.pt"))
    return net


def compute_book2024() -> dict:
    torch = _torch()
    load("surrogate")
    net = _net()
    d = _csi500()
    dates, px = d["date"], d["close"]
    # notes struck at the first trading day of each month, January 2021 to December 2023
    starts = []
    for y in (2021, 2022, 2023):
        for mo in range(1, 13):
            i = int(np.searchsorted(dates, y * 10000 + mo * 100 + 1))
            starts.append(i)
    end = int(np.searchsorted(dates, 20240301))
    w0 = int(np.searchsorted(dates, 20231201))
    notes = []
    for i0 in starts:
        S0 = px[i0]
        status = {"start": int(dates[i0]), "ko": None, "ki": None}
        for k in range(i0 + 1, end):
            age = k - i0
            rel = px[k] / S0
            m = age / DPM
            if age >= TERMS["months"] * DPM:
                break
            if status["ki"] is None and rel < TERMS["ki"]:
                status["ki"] = int(dates[k])
            if age % DPM == 0 and m >= TERMS["lockup"] and rel >= TERMS["ko"]:
                status["ko"] = int(dates[k])
                break
        status["S0"] = float(S0)
        status["i0"] = i0
        notes.append(status)
    # each day of December 2023 - February 2024: notes alive, knocked in, and the dealers' total delta (short the notes)
    days = list(range(w0, end))
    alive_n, kin_n, delta = [], [], []
    for k in days:
        a = kin = 0
        dl = 0.0
        for nt in notes:
            age = k - nt["i0"]
            if age <= 0 or age >= TERMS["months"] * DPM:
                continue
            ko_date = nt["ko"]
            if ko_date is not None and ko_date <= dates[k]:
                continue
            a += 1
            ki_now = nt["ki"] is not None and nt["ki"] <= dates[k]
            kin += int(ki_now)
            rel = px[k] / nt["S0"]
            with torch.no_grad():
                h = 0.005
                xx = torch.tensor([[np.log(rel + h), age / DPM / 24, float(ki_now)],
                                   [np.log(rel - h), age / DPM / 24, float(ki_now)]], dtype=torch.float32)
                v = net(xx).numpy().ravel()
            dl += float((v[0] - v[1]) / (2 * h) / nt["S0"])  # note delta per unit of index, per note of notional 1
        alive_n.append(a)
        kin_n.append(kin)
        delta.append(dl)
    return _json({"dates": dates[days], "close": px[days], "alive": alive_n, "knocked_in": kin_n, "dealer_delta": delta,
                  "notes": [{k: v for k, v in n.items() if k != "i0"} for n in notes],
                  "n_ki_total": sum(1 for n in notes if n["ki"] is not None),
                  "n_ki_2024": sum(1 for n in notes if n["ki"] is not None and n["ki"] >= 20240101)})


def compute_korea() -> dict:
    """A stylized Korean step-down ELS on the HSCEI: 3 years, early redemption every 6 months if the index is above
    90, 90, 85, 85, 80% of its start, a 50% knock-in watched daily, coupon 6% a year. Issued on the first trading day
    of each month of 2021, followed to maturity in 2024."""
    d = _hscei()
    dates, px = d["date"], d["close"]
    steps = [0.90, 0.90, 0.85, 0.85, 0.80, 0.75]
    rows = []
    for mo in range(1, 13):
        i0 = int(np.searchsorted(dates, 20210000 + mo * 100 + 1))
        S0 = px[i0]
        out = {"start": int(dates[i0]), "S0": float(S0)}
        ki = False
        redeemed = None
        last = i0
        for half in range(1, 7):
            target = min(i0 + half * 123, len(px) - 1)  # about six months of Hong Kong trading days
            if px[last:target + 1].min() < 0.5 * S0:
                ki = True
            last = target
            if px[target] >= steps[half - 1] * S0:
                redeemed = (int(dates[target]), 0.06 * half / 2)
                break
        out["knocked_in"] = bool(ki)
        if redeemed:
            out["outcome"] = "redeemed"
            out["date"], out["return"] = redeemed
        else:
            out["outcome"] = "matured"
            out["date"] = int(dates[last])
            final = px[last] / S0
            out["return"] = float(final - 1) if ki and final < steps[-1] else 0.18
        rows.append(out)
    m = (dates >= 20200101) & (dates <= 20250101)
    return _json({"rows": rows, "date": dates[m], "close": px[m], "steps": steps})


def compute_worstof() -> dict:
    c, h = _csi500(), _hscei()
    common = np.intersect1d(c["date"], h["date"])
    m = (common >= 20210101) & (common <= 20231231)
    cd = common[m]
    rc = np.diff(np.log(c["close"][np.searchsorted(c["date"], cd)]))
    rh = np.diff(np.log(h["close"][np.searchsorted(h["date"], cd)]))
    rho_meas = float(np.corrcoef(rc, rh)[0, 1])
    s1, s2 = float(np.std(rc) * np.sqrt(244)), float(np.std(rh) * np.sqrt(244))
    rhos = np.linspace(-0.2, 1.0, 13)
    single = [X.worst_of_put(1.0, 1.0, 1.0, s1, s1, 1.0, seed=5), X.worst_of_put(1.0, 1.0, 1.0, s2, s2, 1.0, seed=5)]
    prices = [X.worst_of_put(1.0, 1.0, 1.0, s1, s2, float(r_), seed=5) for r_ in rhos]
    return _json({"rhos": rhos, "prices": prices, "rho_measured": rho_meas, "sig1": s1, "sig2": s2,
                  "single": single})


def compute_uvm() -> dict:
    K1, K2, T = 95.0, 105.0, 0.5
    grid = np.linspace(40, 200, 321)
    pay = lambda x: (np.maximum(x - K1, 0) - np.maximum(x - K2, 0)) / (K2 - K1)  # noqa: E731
    up = X.uvm_price(pay, grid, T, 0.15, 0.35)
    lo = X.uvm_price(pay, grid, T, 0.15, 0.35, upper=False)
    bs_mid = (bs.price(grid, K1, T, 0.25) - bs.price(grid, K2, T, 0.25)) / (K2 - K1)
    bs_lo = (bs.price(grid, K1, T, 0.15) - bs.price(grid, K2, T, 0.15)) / (K2 - K1)
    bs_hi = (bs.price(grid, K1, T, 0.35) - bs.price(grid, K2, T, 0.35)) / (K2 - K1)
    m = (grid >= 70) & (grid <= 130)
    return _json({"S": grid[m], "upper": up[m], "lower": lo[m], "bs25": bs_mid[m], "bs15": bs_lo[m], "bs35": bs_hi[m],
                  "at100": {"upper": float(np.interp(100, grid, up)), "lower": float(np.interp(100, grid, lo)),
                            "bs15": float(np.interp(100, grid, bs_lo)), "bs35": float(np.interp(100, grid, bs_hi)),
                            "bs25": float(np.interp(100, grid, bs_mid))}})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


ITEMS = {"market": compute_market, "barrier": compute_barrier, "digital": compute_digital, "asian": compute_asian,
         "snowball": compute_snowball, "surrogate": compute_surrogate, "book2024": compute_book2024,
         "korea": compute_korea, "worstof": compute_worstof, "uvm": compute_uvm, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
