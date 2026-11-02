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
    out = _json({"rmse": float(np.sqrt(np.mean(err ** 2))), "max_err": float(np.abs(err).max()),
                 "test_mc": yte, "test_net": pte, "t_net": t_net, "t_mc": t_mc, "t_data": t_data, "t_train": t_train,
                 "n_train": len(ytr), "train_paths": 3000, "test_paths": 40000})
    # the training and test data, kept so the training can be replayed (surrogate_replay) without regenerating them
    out.update({"Xtr": Xtr, "ytr": ytr, "Xte": Xte, "yte": yte})
    return out


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
    alive_n, kin_n, delta, gamma, jump = [], [], [], [], []
    for k in days:
        a = kin = 0
        dl = gm = jp = 0.0
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
            dl += float((v[0] - v[1]) / (2 * h) * rel)  # index exposure in units of note notional (delta x S / S0)
            # the hedge's change for a 1% rise at today's state (gamma), and the drop on a knock-in day (the jump)
            with torch.no_grad():
                xx = torch.tensor([[np.log(rel * 1.01 * (1 + s_)), age / DPM / 24, float(ki_now)] for s_ in (h, -h)]
                                  + [[np.log(rel * 0.99 * (1 + s_)), age / DPM / 24, float(ki_now)] for s_ in (h, -h)],
                                  dtype=torch.float32)
                w = net(xx).numpy().ravel()
            gm += float(((w[0] - w[1]) / (2 * h) * 1.01 - (w[2] - w[3]) / (2 * h) * 0.99) / 2)
            d_now = float((v[0] - v[1]) / (2 * h) * rel)
            if ki_now and nt["ki"] == int(dates[k]) and "prev" in nt:
                jp += d_now - nt["prev"]  # the note's hedge today (knocked in) against yesterday's (not yet)
            nt["prev"] = d_now
        alive_n.append(a)
        kin_n.append(kin)
        delta.append(dl)
        gamma.append(gm)
        jump.append(jp)
    return _json({"dates": dates[days], "close": px[days], "alive": alive_n, "knocked_in": kin_n, "dealer_delta": delta,
                  "dealer_gamma": gamma, "ki_jump": jump,
                  "notes": [{k: v for k, v in n.items() if k not in ("i0", "prev")} for n in notes],
                  "n_ki_total": sum(1 for n in notes if n["ki"] is not None),
                  "n_ki_2024": sum(1 for n in notes if n["ki"] is not None and n["ki"] >= 20240101)})


def _korea_rows(year: int) -> dict:
    """A stylized Korean step-down ELS on the HSCEI: 3 years, early redemption every 6 months if the index is above
    90, 90, 85, 85, 80% of its start, a 50% knock-in watched daily, coupon 6% a year. Issued on the first trading day
    of each month of ``year``, followed to maturity."""
    d = _hscei()
    dates, px = d["date"], d["close"]
    steps = [0.90, 0.90, 0.85, 0.85, 0.80, 0.75]
    rows = []
    for mo in range(1, 13):
        i0 = int(np.searchsorted(dates, year * 10000 + mo * 100 + 1))
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
    m = (dates >= (year - 1) * 10000 + 101) & (dates <= (year + 4) * 10000 + 101)
    return {"rows": rows, "date": dates[m], "close": px[m], "steps": steps}


def compute_korea() -> dict:
    """The stylized step-down ELS (see _korea_rows) issued each month of 2021, followed to maturity in 2024."""
    return _json(_korea_rows(2021))


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


# ---------------------------------------------------------------------------
# The expansion (November 2026): the note taken apart, the buyers' record, barriers in 3D and their static hedge,
# the digital's hedge simulated, the snowball's outcomes and Greeks surfaces, cliquets, the hedged UVM, model risk
# on the Surface, the book's vega, the surrogate's training replay, and unbiased digital Greeks.
# ---------------------------------------------------------------------------
TOTAL = TERMS["months"] * DPM
DT = 1 / (12 * DPM)


def _unit_note(sig, elapsed, n_paths, seed, q=0.0, r=None, chunk=10000):
    """Unit paths for a note `elapsed` days old: GBM from 1, so a note at spot S reads S times them (common random
    numbers across spots for free). Returns what the payoff needs: the observation rows, the running minimum, the
    final value and the discount factors. Simulated in chunks of 10,000 paths to keep memory small."""
    r = TERMS["r"] if r is None else r
    rem = TOTAL - elapsed
    obs = [(m, m * DPM - elapsed) for m in range(TERMS["lockup"], TERMS["months"] + 1) if m * DPM >= elapsed]
    rows, mins, lasts = [], [], []
    for k in range(0, n_paths, chunk):
        p = X.gbm_paths(1.0, sig, rem * DT, rem, min(chunk, n_paths - k), r, q, seed * 1000 + k // chunk)
        rows.append(np.array([p[i] for _, i in obs]))
        mins.append(p.min(axis=0))
        lasts.append(p[-1])
        del p
    return {"rows": np.concatenate(rows, axis=1), "months": np.array([m for m, _ in obs]),
            "disc": np.exp(-r * DT * np.array([i for _, i in obs])), "min": np.concatenate(mins),
            "last": np.concatenate(lasts), "dT": np.exp(-r * rem * DT)}


def _note_value(U, S, knocked_in, coupon):
    """The snowball's value at spot S on unit paths U (the same payoff as exotics.snowball_price)."""
    n = U["rows"].shape[1]
    alive = np.ones(n, bool)
    pv = np.zeros(n)
    for k, m in enumerate(U["months"]):
        hit = alive & (S * U["rows"][k] >= TERMS["ko"])
        pv[hit] = (1 + coupon * m / 12) * U["disc"][k]
        alive &= ~hit
    kin = knocked_in | (S * U["min"] < TERMS["ki"])
    lost = alive & kin
    pv[lost] = (1 + np.minimum(S * U["last"][lost] - 1, 0)) * U["dT"]
    keep = alive & ~kin
    pv[keep] = (1 + coupon * TERMS["months"] / 12) * U["dT"]
    return float(pv.mean())


def compute_decompose() -> dict:
    """The snowball at its fair coupon taken apart on one set of paths: a zero-coupon bond, the value of being repaid
    early, the knock-out coupon strip, the coupon paid at maturity, and the down-and-in put the buyer is short. The
    pieces must add up to the note. Then the fair coupon against the issuer's funding spread, and the reverse
    convertible's fair coupon in closed form."""
    sig = _sigma()
    r, n = TERMS["r"], 40000
    P = X.gbm_paths(1.0, sig, 2.0, TOTAL, n, r, seed=1)
    A, B = X.snowball_AB(sig, n_paths=n, seed=1, **TERMS)
    c = (1 - A) / B
    pv, kom, kin = X.snowball_payoff(P, DPM, c, **TERMS)
    T = 2.0
    dT = np.exp(-r * T)
    ko = kom > 0
    t_ko = kom * DPM * DT
    d_ko = np.where(ko, np.exp(-r * t_ko), 0)
    alive_ki = (~ko) & kin
    alive_ok = (~ko) & (~kin)
    blocks = {
        "bond": dT,
        "early": float(np.mean(np.where(ko, d_ko - dT, 0))),
        "strip": float(np.mean(np.where(ko, d_ko * c * kom / 12, 0))),
        "maturity_coupon": float(np.mean(np.where(alive_ok, dT * c * 2, 0))),
        "dip": -float(np.mean(np.where(alive_ki, dT * np.maximum(1 - P[-1], 0), 0))),
    }
    total = sum(blocks.values())
    assert abs(total - pv.mean()) < 1e-10, (total, pv.mean())
    funding = []
    for s in (0.0, 0.005, 0.01, 0.02):
        a, b = X.snowball_AB(sig, n_paths=n, seed=1, disc_spread=s, **TERMS)
        funding.append({"s": s, "coupon": (1 - a) / b, "A": a, "B": b})
    rc = []
    for s in (0.0, 0.005, 0.01, 0.02):
        put = float(bs.price(1.0, 1.0, 1.0, 0.20, r, 0.0, -1))
        rc.append({"s": s, "put": put, "coupon": float(np.exp((r + s) * 1.0) * (1 + put) - 1)})
    return _json({"sigma": sig, "coupon": c, "A": A, "B": B, "blocks": blocks, "total": total, "pv_mean": float(pv.mean()),
                  "se": float(pv.std() / np.sqrt(n)), "funding": funding, "rc": rc, "n_paths": n})


def compute_buyers() -> dict:
    """One stylized snowball (15% a year, knock-out 103% monthly after 3 months, knock-in 75% daily, 24 months)
    issued on the first trading day of every month 2017-2023 on the CSI 500 ETF and followed on the real path: what
    each buyer got, against holding the index over the same months and a 2% deposit. One path, so a description of
    what happened, not a sample of what could."""
    d = _csi500()
    D, P = d["date"], d["close"]
    ko, ki, lock, M, cpn = TERMS["ko"], TERMS["ki"], TERMS["lockup"], TERMS["months"], 0.15
    rows = []
    for y in range(2017, 2024):
        for mo in range(1, 13):
            i0 = int(np.searchsorted(D, y * 10000 + mo * 100 + 1))
            S0 = P[i0]
            out = None
            kin = False
            for a in range(1, M * DPM + 1):
                if i0 + a >= len(P):
                    out = "open"
                    break
                rr = P[i0 + a] / S0
                if rr < ki:
                    kin = True
                if a % DPM == 0 and a // DPM >= lock and rr >= ko:
                    out = ("KO", a // DPM, cpn * (a // DPM) / 12)
                    break
            if out == "open":
                continue
            if out is None:
                rr = P[i0 + M * DPM] / S0
                out = ("KI", M, float(min(rr - 1, 0))) if kin and rr < 1 else ("full", M, cpn * M / 12)
            kind, months, ret = out
            j = i0 + months * DPM
            rows.append({"start": int(D[i0]), "end": int(D[j]), "S0": float(S0), "outcome": kind, "months": months,
                         "ret": ret, "ann": ret / (months / 12), "index": float(P[j] / S0 - 1),
                         "deposit": 0.02 * months / 12, "touched_ki": bool(kin)})
    by_year = {}
    for y in range(2017, 2024):
        rr = [r_ for r_ in rows if r_["start"] // 10000 == y]
        by_year[y] = {"n": len(rr), "KO": sum(r_["outcome"] == "KO" for r_ in rr),
                      "KI": sum(r_["outcome"] == "KI" for r_ in rr), "full": sum(r_["outcome"] == "full" for r_ in rr),
                      "mean_ann": float(np.mean([r_["ann"] for r_ in rr])),
                      "index_ann": float(np.mean([r_["index"] / (r_["months"] / 12) for r_ in rr]))}
    losses = [r_ for r_ in rows if r_["ret"] < 0]
    beat = sum(r_["ret"] > r_["index"] for r_ in rows)
    m = (D >= 20170101) & (D <= 20251130)
    return _json({"rows": rows, "by_year": by_year, "n": len(rows), "n_loss": len(losses),
                  "worst": float(min(r_["ret"] for r_ in rows)), "mean_ann": float(np.mean([r_["ann"] for r_ in rows])),
                  "beat_index": beat, "date": D[m], "close": P[m]})


def compute_barrier_surface() -> dict:
    """The down-and-out call's value and delta over (spot, time to expiry), in closed form, and the image term."""
    K, H, s, r = 100.0, 85.0, 0.25, 0.02
    Sg = np.linspace(80, 130, 61)
    taus = np.linspace(0.005, 0.5, 40)
    V = np.array([X.down_out_call(Sg, K, H, t, s, r) for t in taus])
    van = np.array([bs.price(Sg, K, t, s, r) for t in taus])
    Dl = np.gradient(V, Sg, axis=1)
    return _json({"S": Sg, "tau": taus, "value": V, "vanilla": van, "delta": Dl, "K": K, "H": H, "sigma": s, "r": r})


def compute_static() -> dict:
    """Carr, Ellis and Gupta's static hedge of a down-and-in call (S = K = 100, H = 90, six months, r = q = 0):
    hold K/H puts struck at H^2/K, swap them for the call at the touch. True price minus the hedge's cost under
    Black-Scholes (where it is exact up to monitoring) and under Heston with rho = 0 and rho = -0.7 (a skew), 50,000
    paths of 500 steps; and at the touch on a few paths, the cash the swap leaves on the table."""
    from explainer.quant.house import stochvol as sv
    S0, K, H, T, n = 100.0, 100.0, 90.0, 0.5, 500
    w, Kp = X.static_dic_hedge(K, H, S0)
    hp = dict(v0=0.0625, kappa=2.0, theta=0.0625, xi=0.8)
    out = {"weight": w, "strike": Kp, "models": {}}

    def cos_put(v, tau, strike, rho, F):
        cf = lambda u, TT: sv.heston_cf(u, TT, v, hp["kappa"], hp["theta"], hp["xi"], rho)  # noqa: E731
        return float(sv.cos_price(cf, F, strike, tau, cp=-1)[0])

    for name, rho in (("BS", None), ("Heston, rho = 0", 0.0), ("Heston, rho = -0.7", -0.7)):
        dic, paths_show = [], []
        for b in range(5):  # 5 batches of 10,000 paths, to keep memory small
            if rho is None:
                S = X.gbm_paths(S0, 0.25, T, n, 10000, seed=11 + b)
                v = None
            else:
                S, v = sv.heston_qe(S0, hp["v0"], hp["kappa"], hp["theta"], hp["xi"], rho, T, n, 10000, seed=11 + b,
                                    return_v=True)
            hit = S.min(axis=0) <= H
            dic.append(np.where(hit, np.maximum(S[-1] - K, 0), 0))
            if b == 0:
                idx = np.where(hit)[0][:10]
                for j in idx:
                    it = int(np.argmax(S[:, j] <= H))
                    tau = T * (n - it) / n
                    St = float(S[it, j])
                    if rho is None:
                        call = float(bs.price(St, K, tau, 0.25))
                        put = w * float(bs.price(St, Kp, tau, 0.25, 0, 0, -1))
                    else:
                        put = w * cos_put(float(v[it, j]), tau, Kp, rho, St)
                        call = cos_put(float(v[it, j]), tau, K, rho, St) + St - K  # parity, r = 0
                    paths_show.append({"path": S[::5, j], "touch": it / n * T, "S_touch": St, "call": call, "put": put,
                                       "gap": call - put, "end": float(S[-1, j])})
        dic = np.concatenate(dic)
        if rho is None:
            put0 = w * float(bs.price(S0, Kp, T, 0.25, 0, 0, -1))
        else:
            put0 = w * cos_put(hp["v0"], T, Kp, rho, S0)
        out["models"][name] = {"dic": float(dic.mean()), "se": float(dic.std() / np.sqrt(len(dic))), "hedge": put0,
                               "gap": float(dic.mean() - put0), "paths": paths_show}
    out["exact_dic_bs"] = float(bs.price(S0, K, T, 0.25) - X.down_out_call(S0, K, H, T, 0.25))
    return _json(out)


def compute_digital_hedge() -> dict:
    """A short digital and a short call spread (width 2) delta-hedged for a month, rebalanced 21, 84 or 336 times:
    the hedging P&L's spread and tail on 40,000 paths, and one path's ledger, day by day."""
    from scipy.stats import norm
    K, s, T = 100.0, 0.25, 21 / 252
    eps = 2.0

    def d_dig(S, tau):
        tau = np.maximum(tau, 1e-12)
        d2 = (np.log(S / K) - 0.5 * s * s * tau) / (s * np.sqrt(tau))
        return norm.pdf(d2) / (S * s * np.sqrt(tau))

    def d_call(S, k, tau):
        tau = np.maximum(tau, 1e-12)
        return norm.cdf((np.log(S / k) + 0.5 * s * s * tau) / (s * np.sqrt(tau)))

    res, show = {}, {}
    for n in (21, 84, 336):
        P = X.gbm_paths(100.0, s, T, n, 40000, 0.0, seed=5)
        dt = T / n
        for name in ("digital", "spread"):
            if name == "digital":
                v0 = float(X.digital_call(100.0, K, T, s))
                pay = (P[-1] > K) * 1.0
            else:
                v0 = float(X.call_spread_digital(100.0, K, T, s, eps))
                pay = (np.maximum(P[-1] - K + eps, 0) - np.maximum(P[-1] - K, 0)) / eps
            cash = np.zeros(P.shape[1])
            pos = np.zeros(P.shape[1])
            led = []
            for i in range(n):
                tau = T - i * dt
                dd = d_dig(P[i], tau) if name == "digital" else (d_call(P[i], K - eps, tau) - d_call(P[i], K, tau)) / eps
                cash += (pos - dd) * P[i]
                pos = dd
                if n == 21:
                    led.append({"S": float(P[i, 7]), "delta": float(dd[7])})
            pnl = v0 + cash + pos * P[-1] - pay
            h, e = np.histogram(np.clip(pnl, -1.0, 0.6), bins=40, range=(-1.0, 0.6))
            res.setdefault(name, []).append({"n": n, "price": v0, "sd": float(pnl.std()), "q01": float(np.quantile(pnl, 0.01)),
                                             "mean": float(pnl.mean()), "hist": h, "edges": e})
            if n == 21:
                show[name] = {"ledger": led, "S_T": float(P[-1, 7]), "pnl": float(pnl[7])}
    return _json({"rows": res, "show": show, "eps": eps, "K": K, "sigma": s, "T": T})


def compute_onetouch() -> dict:
    """A down one-touch (S = 100, H = 90, six months, 25% vol, r = 0): the closed form by reflection, Monte Carlo at
    1,000 steps with and without the BGK shift, and twice the digital put."""
    S, H, T, s = 100.0, 90.0, 0.5, 0.25
    cf = X.one_touch(S, H, T, s)
    P = X.gbm_paths(S, s, T, 1000, 30000, seed=2)
    mc = float(np.mean(P.min(axis=0) <= H))
    from scipy.stats import norm
    dig = float(norm.cdf((np.log(H / S) + 0.5 * s * s * T) / (s * np.sqrt(T))))
    return _json({"closed": cf, "mc": mc, "mc_se": float(np.sqrt(mc * (1 - mc) / 30000)),
                  "bgk": X.one_touch(S, X.bgk_barrier(H, S, s, T / 1000), T, s), "digital_put": dig, "two_digital": 2 * dig,
                  "driftless": 2 * float(norm.cdf(np.log(H / S) / (s * np.sqrt(T))))})


def compute_digital_skew() -> dict:
    """A 30-day digital call on bitcoin from the Surface (Part 12's SSVI fit of 10 December 2025): Black-Scholes at
    the at-the-money vol, against the price with the smile's slope, D = -dC/dK = N(d2) - vega x dsigma/dK."""
    from scipy.interpolate import CubicSpline
    from scipy.stats import norm
    import json
    srf = json.loads((CACHE.dir.parent / "quant12" / "surface.json").read_text())
    T = float(srf["grid_T"][2])
    k = np.asarray(srf["grid_k"], float)
    iv = np.asarray(srf["grid_iv"], float)[2]
    sp = CubicSpline(k, iv)
    kk = np.linspace(-0.2, 0.2, 41)
    sig, dsig_dk = sp(kk), sp(kk, 1)
    K = np.exp(kk)  # per unit forward, r = 0
    d1 = (-kk + 0.5 * sig ** 2 * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    vega = norm.pdf(d1) * np.sqrt(T)
    skew_price = norm.cdf(d2) - vega * dsig_dk / K
    atm = float(sp(0.0))
    flat = norm.cdf((-kk - 0.5 * atm ** 2 * T) / (atm * np.sqrt(T)))
    own = norm.cdf(d2)
    # a finite-difference check: -dC/dK with the smile moving
    h = 1e-4
    C = lambda kx: float(bs.price(1.0, np.exp(kx), T, float(sp(kx))))  # noqa: E731
    fd = [-(C(np.log(Kx + h)) - C(np.log(Kx - h))) / (2 * h) for Kx in K]
    return _json({"T": T, "k": kk, "iv": sig, "skew_price": skew_price, "flat": flat, "own_vol": own, "fd": fd,
                  "atm": atm, "at_k": {"k": 0.1, "flat": float(np.interp(0.1, kk, flat)),
                                       "skew": float(np.interp(0.1, kk, skew_price))},
                  "atm_diff": float(np.interp(0.0, kk, skew_price) - np.interp(0.0, kk, flat))})


def compute_asian_scatter() -> dict:
    """The control variate seen: 4,000 paths' arithmetic and geometric Asian payoffs, the regression line, and the
    correlation that sets the variance reduction; one path with its running average and minimum."""
    S, K, T, s, r, n = 100.0, 100.0, 1.0, 0.25, 0.02, 252
    P = X.gbm_paths(S, s, T, n, 4000, r, seed=21)
    A = P[1:].mean(axis=0)
    G = np.exp(np.log(P[1:]).mean(axis=0))
    ya = np.exp(-r * T) * np.maximum(A - K, 0)
    yg = np.exp(-r * T) * np.maximum(G - K, 0)
    c = np.cov(ya, yg)
    b = c[0, 1] / c[1, 1]
    rho = c[0, 1] / np.sqrt(c[0, 0] * c[1, 1])
    p = P[:, 3]
    return _json({"ya": ya[:1500], "yg": yg[:1500], "b": float(b), "rho": float(rho),
                  "ratio": float(1 / np.sqrt(1 - rho ** 2)), "path": p, "avg": np.cumsum(p[1:]) / np.arange(1, n + 1),
                  "min": np.minimum.accumulate(p), "geo_cf": float(X.geometric_asian_call(S, K, T, s, n, r)),
                  "var_ratio_cont": 1 / 3})


def compute_outcomes() -> dict:
    """The snowball at its fair coupon on 40,000 paths: how often it knocks out and when, how often it ends knocked
    in and what is left, its expected life; 300 paths kept for the picture, with the fair coupon's A and B (the
    note's value is A + c B)."""
    sig = _sigma()
    A, B = X.snowball_AB(sig, n_paths=40000, seed=1, **TERMS)
    c = (1 - A) / B
    P = X.gbm_paths(1.0, sig, 2.0, TOTAL, 40000, TERMS["r"], seed=1)
    pv, kom, kin = X.snowball_payoff(P, DPM, c, **TERMS)
    ko = kom > 0
    lost = (~ko) & kin
    hist = np.bincount(kom[ko], minlength=25)[:25]
    sel = np.arange(300)
    ki_day = np.where(kin[sel], np.argmax(P[:, sel] < TERMS["ki"], axis=0), -1)
    return _json({"sigma": sig, "coupon": c, "A": A, "B": B, "p_ko": float(ko.mean()), "p_lost": float(lost.mean()),
                  "p_full": float(((~ko) & (~kin)).mean()), "mean_ko_month": float(kom[ko].mean()),
                  "p_first": float((kom == TERMS["lockup"]).mean()), "ko_hist": hist,
                  "mean_lost": float(pv[lost].mean() / np.exp(-TERMS["r"] * 2)), "q05": float(np.quantile(pv, 0.05)),
                  "life": float(np.where(ko, kom, 24).mean()), "pv_mean": float(pv.mean()), "pv": pv,
                  "show": {"paths": P[::3, sel].T, "ko_month": kom[sel], "ki_day": ki_day // 3}})


def compute_coupon_q() -> dict:
    """The fair coupon by carry (a dividend yield, or the futures discount the hedger earns) and by knock-in level,
    each a linear solve c* = (1 - A)/B on 20,000 paths."""
    sig = _sigma()
    tq = {k: v for k, v in TERMS.items()}
    qs = [0.0, 0.02, 0.04, 0.06, 0.08]
    by_q = []
    for q in qs:
        a, b = X.snowball_AB(sig, q=q, n_paths=20000, seed=1, **tq)
        by_q.append({"q": q, "coupon": (1 - a) / b, "A": a, "B": b})
    by_ki = []
    for ki in (0.65, 0.70, 0.75, 0.80, 0.85):
        t2 = dict(tq)
        t2["ki"] = ki
        a, b = X.snowball_AB(sig, n_paths=20000, seed=1, **t2)
        by_ki.append({"ki": ki, "coupon": (1 - a) / b})
    return _json({"sigma": sig, "by_q": by_q, "by_ki": by_ki})


def compute_greeks3d() -> dict:
    """The issuer's Greeks over (spot, months since issue), not knocked in and knocked in: the issuer is short the
    note, so its delta, gamma and vega are minus the note's. Finite differences on common random numbers (spot
    bump 0.01, vol bump one point), 30,000 paths per month; saved month by month so a killed run resumes."""
    sig, c = _sigma(), load("decompose")["coupon"]
    spots = np.round(np.linspace(0.66, 1.12, 24), 4)
    months = list(range(0, 24))
    part = CACHE.partial("greeks3d", {"sig": sig, "c": c, "n": 30000, "spots": spots.tolist()})
    h, hv = 0.01, 0.01
    for m in months:
        key = str(m)
        if key in part:
            continue
        e = m * DPM
        U0, Uu, Ud = (_unit_note(v, e, 30000, 100 + m) for v in (sig, sig + hv, sig - hv))
        row = {}
        for flag in (False, True):
            vals, dl, gm, vg = [], [], [], []
            for S in spots:
                v0 = _note_value(U0, S, flag, c)
                vp, vm = _note_value(U0, S + h, flag, c), _note_value(U0, S - h, flag, c)
                vals.append(v0)
                dl.append(-(vp - vm) / (2 * h))
                gm.append(-(vp - 2 * v0 + vm) / h ** 2)
                vg.append(-(_note_value(Uu, S, flag, c) - _note_value(Ud, S, flag, c)) / (2 * hv) / 100)
            row["ki" if flag else "alive"] = {"value": vals, "delta": dl, "gamma": gm, "vega": vg}
        part[key] = row
    out = {"spots": spots, "months": months, "sigma": sig, "coupon": c}
    for flag in ("alive", "ki"):
        for g in ("value", "delta", "gamma", "vega"):
            out[f"{flag}_{g}"] = [part[str(m)][flag][g] for m in months]
    return _json(out)


def compute_bump_curve() -> dict:
    """The issuer's delta just above the knock-in (spot 0.77, six months in, not knocked in) against the bump size
    h, with common random numbers and with independent draws for the up and down prices, three seeds each."""
    sig, c = _sigma(), load("decompose")["coupon"]
    hs = [0.0025, 0.005, 0.01, 0.02, 0.04]
    e, S = 6 * DPM, 0.77
    crn, ind = [], []
    for seed in range(3):
        U = _unit_note(sig, e, 30000, 300 + seed)
        U2 = _unit_note(sig, e, 30000, 400 + seed)
        crn.append([-(_note_value(U, S + h, False, c) - _note_value(U, S - h, False, c)) / (2 * h) for h in hs])
        ind.append([-(_note_value(U, S + h, False, c) - _note_value(U2, S - h, False, c)) / (2 * h) for h in hs])
    return _json({"h": hs, "crn": crn, "independent": ind, "S": S})


def compute_korea2015() -> dict:
    """The same stylized step-down ELS issued on the first trading day of each month of 2015, near the HSCEI's 2015
    peak, followed through the fall to February 2016 and to maturity."""
    return _json(_korea_rows(2015))


def compute_corr_regimes() -> dict:
    """Correlations of daily log returns: CSI 500 ETF against the CSI 1000 ETF (512100) and the HSCEI, in calm and
    in falls. 512100's Yahoo closes jump by a factor of 2.7 on 4 November 2016, a rebasing, not a market move: the
    series is used from 2017 and any day with a move above 15% is dropped (none remain)."""
    c, k, h = _csi500(), data.yahoo_daily("512100.SS", "2015-01-01", "2025-11-30"), _hscei()

    def rets(a, b):
        d = np.intersect1d(a["date"], b["date"])
        d = d[d >= 20170101]
        ra = np.diff(np.log(a["close"][np.searchsorted(a["date"], d)]))
        rb = np.diff(np.log(b["close"][np.searchsorted(b["date"], d)]))
        ok = (np.abs(ra) < 0.15) & (np.abs(rb) < 0.15)
        return d[1:][ok], ra[ok], rb[ok], int((~ok).sum())

    windows = [("2021--2023", 20210101, 20231231), ("Jan--Feb 2024", 20240101, 20240229),
               ("Feb--Mar 2020", 20200201, 20200331), ("2017--2025", 20170101, 20251130)]
    out = {}
    for nm, b in (("CSI 1000", k), ("HSCEI", h)):
        d, ra, rb, dropped = rets(c, b)
        rows = []
        for w, lo, hi in windows:
            m = (d >= lo) & (d <= hi)
            rows.append({"window": w, "n": int(m.sum()), "rho": float(np.corrcoef(ra[m], rb[m])[0, 1]),
                         "vol_a": float(np.std(ra[m]) * np.sqrt(244)), "vol_b": float(np.std(rb[m]) * np.sqrt(244))})
        s = np.std(ra)
        dn, up = ra < -s, ra > s
        out[nm] = {"rows": rows, "dropped": dropped, "down": float(np.corrcoef(ra[dn], rb[dn])[0, 1]),
                   "up": float(np.corrcoef(ra[up], rb[up])[0, 1])}
    # the conditioning bias: the same exceedance correlations for a bivariate normal with the full-sample rho
    g = np.random.default_rng(0)
    rho = out["HSCEI"]["rows"][3]["rho"]
    z1 = g.standard_normal(400000)
    z2 = rho * z1 + np.sqrt(1 - rho ** 2) * g.standard_normal(400000)
    dn = z1 < -1
    out["gaussian_down"] = float(np.corrcoef(z1[dn], z2[dn])[0, 1])
    out["gaussian_rho"] = rho
    return _json(out)


def compute_worstof_ac() -> dict:
    """A worst-of snowball on the CSI 500 and CSI 1000 ETFs at their 2021-2023 vols: the fair coupon against the
    correlation, by the linear solve, 20,000 paths each; and the single-index coupons."""
    rg = load("corr_regimes")["CSI 1000"]["rows"][0]
    s1, s2 = rg["vol_a"], rg["vol_b"]
    rhos = [0.3, 0.5, 0.7, 0.8, 0.9, 1.0]
    out = []
    for rho in rhos:
        a, b = X.worst_of_autocall_AB(s1, s2, rho, n_paths=20000, seed=8, **{k: v for k, v in TERMS.items()})
        out.append({"rho": rho, "coupon": (1 - a) / b})
    singles = []
    for s in (s1, s2):
        a, b = X.snowball_AB(s, n_paths=20000, seed=8, **TERMS)
        singles.append((1 - a) / b)
    return _json({"sig1": s1, "sig2": s2, "rows": out, "single": singles, "rho_measured": rg["rho"]})


def compute_cliquet() -> dict:
    """A locally capped and floored cliquet (12 monthly periods, local floor -3%, global floor 0) over volatility and
    local cap, on 200,000 paths with common random numbers; then a capped cliquet with no local floor, and the
    reverse cliquet max(C + sum min(r_i, 0), 0); and Part 13's spread of a cliquet across five models fitted to one
    Surface (read from its cache, not recomputed)."""
    vols = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    caps = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
    grid = [[X.cliquet_bs(s, 12, cap=cp, floor=-0.03, gfloor=0.0, n_paths=200000, seed=0)[0] for s in vols] for cp in caps]
    nofloor = [X.cliquet_bs(s, 12, cap=0.02, floor=-1.0, gfloor=0.0, n_paths=200000, seed=0)[0] for s in vols]
    rev = [X.cliquet_bs(s, 12, reverse=0.30, n_paths=200000, seed=0)[0] for s in vols]
    g3 = np.array(grid[2])
    i = int(np.argmax(g3))
    q13 = None
    try:
        import json
        q13 = float(json.loads((CACHE.dir.parent / "quant13" / "exotics.json").read_text())["cliquet_spread"])
    except (OSError, KeyError, ValueError):
        q13 = None
    ridge = [float(vols[int(np.argmax(row))]) for row in grid]
    return _json({"vols": vols, "caps": caps, "grid": grid, "nofloor": nofloor, "reverse": rev, "peak_vol": vols[i],
                  "peak": float(g3[i]), "ridge": ridge, "q13_spread": q13,
                  "vega_peak": float((g3[min(i + 1, 9)] - g3[max(i - 1, 0)]) / (vols[min(i + 1, 9)] - vols[max(i - 1, 0)]) / 100)})


def compute_uvm_book() -> dict:
    """Uncertain volatility (15-35%) on a call spread 95-105, six months: the legs priced separately against the
    spread as one book (non-additivity), and the Lagrangian hedge with 90 and 110 calls bought or sold at their
    Black-Scholes 25% prices (Avellaneda and Paras 1996), with the optimiser's iterates."""
    K1, K2, T = 95.0, 105.0, 0.5
    grid = np.linspace(40, 200, 161)
    cs = lambda x: (np.maximum(x - K1, 0) - np.maximum(x - K2, 0)) / (K2 - K1)  # noqa: E731
    U = lambda f, up=True: float(np.interp(100.0, grid, X.uvm_solve(f(grid), grid, T, 0.15, 0.35, n_t=200, upper=up)))  # noqa: E731
    legs = [U(lambda x: np.maximum(x - K1, 0) / (K2 - K1)), U(lambda x: -np.maximum(x - K2, 0) / (K2 - K1))]
    calls = [lambda x: np.maximum(x - 90.0, 0), lambda x: np.maximum(x - 110.0, 0)]
    mkt = [float(bs.price(100.0, k, T, 0.25)) for k in (90.0, 110.0)]
    up = X.uvm_lagrangian(cs, calls, mkt, grid, 100.0, T, 0.15, 0.35, n_t=200, maxfev=80)
    neg = X.uvm_lagrangian(lambda x: -cs(x), calls, mkt, grid, 100.0, T, 0.15, 0.35, n_t=200, maxfev=80)
    return _json({"upper": U(cs), "lower": U(cs, False), "legs": legs, "legs_sum": sum(legs),
                  "hedged_upper": up["price"], "hedged_lower": -neg["price"], "w_upper": up["weights"],
                  "w_lower": [-w for w in neg["weights"]], "iterates": up["iterates"],
                  "bs25": float((bs.price(100.0, K1, T, 0.25) - bs.price(100.0, K2, T, 0.25)) / (K2 - K1)), "mkt": mkt})


def compute_uvm_film() -> dict:
    """The Black-Scholes-Barenblatt equation marching back from expiry for the call spread (seller's side): the
    value and the volatility it chooses, every 10 of 400 steps, on spot 60-140."""
    K1, K2, T = 95.0, 105.0, 0.5
    grid = np.linspace(40, 200, 321)
    pay = (np.maximum(grid - K1, 0) - np.maximum(grid - K2, 0)) / (K2 - K1)
    V, film = X.uvm_solve(pay, grid, T, 0.15, 0.35, n_t=400, keep_every=10)
    m = (grid >= 60) & (grid <= 140)
    return _json({"S": grid[m], "tau": [T * 10 * k / 400 for k in range(len(film))],
                  "V": [f[0][m] for f in film], "sig": [f[1][m] for f in film]})


def compute_modelrisk() -> dict:
    """Same vanillas, different exotics: local vol, Heston, Bates and variance gamma, each fitted to the bitcoin
    Surface of 10 December 2025 in Part 13 (its cache read, never written), simulated on 20,000 daily paths for 120
    days at zero rates. Per unit of spot: the 90-day at-the-money call, a down-and-out call (barrier 0.8), a one-touch
    at 0.8, a double-no-touch (0.8, 1.25), and the fair coupon of a 4-month autocall (monthly knock-out at 1, daily
    knock-in at 0.7); the 79-day smiles against the market's quotes; and a few paths of each model."""
    import videos.quant.quant13.compute as Q13
    q = Q13.load("calibrate")["quotes"]
    qk, qd, qiv = (np.asarray(q[x], float) for x in ("k", "days", "iv"))
    mq = qd == 79
    out = {"models": {}, "market": {"k": qk[mq], "iv": qiv[mq]}}
    kk = np.linspace(-0.25, 0.25, 11)
    for m in ("LV", "Heston", "Bates", "VG"):
        S = np.exp(Q13._simulate(m, n_paths=20000, days=120, seed=7))
        T = 90
        mn, mx = S[:T + 1].min(axis=0), S[:T + 1].max(axis=0)
        obs = [30, 60, 90, 120]
        a = X.autocall_on_paths(S, obs, 1.0, 0.7, np.zeros(4)).mean()
        b = X.autocall_on_paths(S, obs, 1.0, 0.7, np.array([1, 2, 3, 4]) / 12).mean() - a
        smile = []
        for k in kk:
            p = float(np.mean(np.maximum(S[79] - np.exp(k), 0)))
            try:
                from explainer.quant.house import stochvol as sv
                smile.append(float(sv.implied_vols(np.array([p]), 1.0, np.array([np.exp(k)]), 79 / 365)[0]))
            except Exception:  # noqa: BLE001
                smile.append(float("nan"))
        out["models"][m] = {"vanilla90": float(np.mean(np.maximum(S[T] - 1, 0))),
                            "doc": float(np.mean(np.maximum(S[T] - 1, 0) * (mn > 0.8))),
                            "onetouch": float(np.mean(mn <= 0.8)), "dnt": float(np.mean((mn > 0.8) & (mx < 1.25))),
                            "coupon": float((1 - a) / b), "smile_k": kk, "smile": smile, "paths": S[:, :40].T}
    return _json(out)


def compute_robust() -> dict:
    """Glasserman and Xu's worst case for the snowball: its 40,000 discounted payoffs at the fair coupon (the
    `outcomes` paths) re-weighted by exponential tilting, the lowest value within relative entropy eta of the model,
    and the weights the 300 shown paths receive."""
    o = load("outcomes")
    pv = np.asarray(o["pv"])
    etas = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5]
    rows, shown = [], {}
    for e in etas:
        v, th, w = X.kl_worst_case(pv, e, side=-1)
        rows.append({"eta": e, "value": v, "theta": th, "p_lost": float(np.sum(w * (pv < 0.97 * np.exp(-0.04))))})
        if e in (0.05, 0.2, 0.5):
            shown[str(e)] = (w[:300] * len(pv)).tolist()
    return _json({"rows": rows, "shown": shown, "base": float(pv.mean())})


def compute_book_vega() -> dict:
    """A stylized book: one snowball of notional 1 issued on the first trading day of each month of 2021-2023 on the
    CSI 500, followed on the real path to the end of 2024. Each day, every live note's issuer vega and gamma are read
    from the `greeks3d` tables (spot, months, knocked in or not) and summed."""
    from scipy.interpolate import RegularGridInterpolator
    g = load("greeks3d")
    sp, mo = np.asarray(g["spots"]), np.asarray(g["months"], float)
    f = {}
    for flag in ("alive", "ki"):
        for k in ("vega", "gamma", "delta"):
            f[(flag, k)] = RegularGridInterpolator((mo, sp), np.asarray(g[f"{flag}_{k}"]), bounds_error=False,
                                                   fill_value=None)
    d = _csi500()
    dates, px = d["date"], d["close"]
    starts = [int(np.searchsorted(dates, y * 10000 + mo_ * 100 + 1)) for y in (2021, 2022, 2023) for mo_ in range(1, 13)]
    a, b = int(np.searchsorted(dates, 20210104)), int(np.searchsorted(dates, 20241231))
    notes = []
    for i0 in starts:
        S0 = px[i0]
        ko, ki = None, None
        for k in range(i0 + 1, len(px)):
            age = k - i0
            if age > TOTAL:
                break
            rel = px[k] / S0
            if ki is None and rel < TERMS["ki"]:
                ki = k
            if age % DPM == 0 and age // DPM >= TERMS["lockup"] and rel >= TERMS["ko"]:
                ko = k
                break
        notes.append((i0, S0, ko, ki))
    vega, gamma, live, n_ki = [], [], [], []
    for k in range(a, b + 1):
        v = gm = 0.0
        n_live = n_k = 0
        for i0, S0, ko, ki in notes:
            age = k - i0
            if age < 0 or age >= TOTAL or (ko is not None and k >= ko):
                continue
            n_live += 1
            flag = "ki" if (ki is not None and k >= ki) else "alive"
            n_k += flag == "ki"
            rel = float(np.clip(px[k] / S0, sp[0], sp[-1]))
            x = (min(age / DPM, mo[-1]), rel)
            v += float(f[(flag, "vega")](x))
            gm += float(f[(flag, "gamma")](x)) * rel * 0.01  # change of the hedge per 1% move, in notes' worth
        vega.append(v)
        gamma.append(gm)
        live.append(n_live)
        n_ki.append(n_k)
    i_pk = int(np.argmax(vega))
    return _json({"dates": dates[a:b + 1], "close": px[a:b + 1], "vega": vega, "gamma": gamma, "live": live, "ki": n_ki,
                  "peak": {"date": int(dates[a + i_pk]), "vega": vega[i_pk], "live": live[i_pk]}})


def compute_surrogate_replay() -> dict:
    """The surrogate's training replayed: three seeds, the test error against 40,000-path Monte Carlo every 100
    steps, the network's price over spot six months in at six checkpoints (seed 0); against a degree-4 polynomial in
    (log spot, months), separate by knock-in flag, fitted to the same 3,000 labels; and the labels' own noise."""
    torch = _torch()
    s = load("surrogate")
    Xtr, ytr, Xte, yte = (np.asarray(s[k], float) for k in ("Xtr", "ytr", "Xte", "yte"))
    xt = torch.tensor(Xtr, dtype=torch.float32)
    yt = torch.tensor(ytr[:, None], dtype=torch.float32)
    xe = torch.tensor(Xte, dtype=torch.float32)
    sg = np.linspace(0.62, 1.18, 57)
    curve_x = {flag: torch.tensor(np.column_stack([np.log(sg), np.full_like(sg, 6 / 24), np.full_like(sg, float(flag))]),
                                  dtype=torch.float32) for flag in (0, 1)}
    checkpoints = [0, 100, 300, 1000, 2000, 4000]
    steps = list(range(0, 4001, 100))
    rmse, curves = [], {}
    for seed in (0, 1, 2):
        torch.manual_seed(seed)
        net = torch.nn.Sequential(torch.nn.Linear(3, 64), torch.nn.SiLU(), torch.nn.Linear(64, 64), torch.nn.SiLU(),
                                  torch.nn.Linear(64, 1))
        opt = torch.optim.Adam(net.parameters(), lr=3e-3)
        hist = []
        for step in range(4001):
            if step in steps:
                with torch.no_grad():
                    hist.append(float(np.sqrt(np.mean((net(xe).numpy().ravel() - yte) ** 2))))
                    if seed == 0 and step in checkpoints:
                        curves[str(step)] = {str(fl): net(curve_x[fl]).numpy().ravel().tolist() for fl in (0, 1)}
            if step == 4000:
                break
            idx = torch.randint(0, len(xt), (256,))
            loss = torch.mean((net(xt[idx]) - yt[idx]) ** 2)
            opt.zero_grad()
            loss.backward()
            opt.step()
            if step == 3000:
                for gr in opt.param_groups:
                    gr["lr"] = 1e-3
        rmse.append(hist)

    def feats(Xm, deg=4):
        a, b, k = Xm[:, 0], Xm[:, 1], Xm[:, 2]
        F = np.column_stack([a ** i * b ** j for i in range(deg + 1) for j in range(deg + 1 - i)])
        return np.column_stack([F, F * k[:, None]])

    w = np.linalg.lstsq(feats(Xtr), ytr, rcond=None)[0]
    poly = float(np.sqrt(np.mean((feats(Xte) @ w - yte) ** 2)))
    poly_curve = {str(fl): (feats(np.column_stack([np.log(sg), np.full_like(sg, 6 / 24), np.full_like(sg, float(fl))])) @ w)
                  .tolist() for fl in (0, 1)}
    # the labels' noise: the spread of a 3,000-path price, from repeated pricing of one note
    sn = load("snowball")
    reps = [X.snowball_price(sn["sigma"], coupon=sn["coupon"], S=0.9, elapsed_days=6 * DPM, n_paths=3000, seed=900 + i,
                             **TERMS) for i in range(40)]
    # Monte Carlo dots for the left panel, 40,000 paths, by the unit-path method
    U = _unit_note(sn["sigma"], 6 * DPM, 40000, 77)
    dots = {str(fl): [_note_value(U, S, bool(fl), sn["coupon"]) for S in sg[::4]] for fl in (0, 1)}
    from math import comb
    return _json({"steps": steps, "rmse": rmse, "checkpoints": checkpoints, "curves": curves, "spots": sg,
                  "poly_rmse": poly, "poly_curve": poly_curve, "label_noise": float(np.std(reps)), "dots": dots,
                  "dot_spots": sg[::4], "final": [r_[-1] for r_ in rmse],
                  "n_terms": {str(d): comb(d + 4, 4) for d in (3, 10, 30, 100)}})


def compute_pathwise_digital() -> dict:
    """A one-month digital call's delta (S = K = 100, 25% vol) by three Monte Carlo estimators as paths are added,
    five seeds each: pathwise (zero on every path), likelihood ratio, and pathwise plus the boundary term."""
    from scipy.stats import norm
    S, K, T, s = 100.0, 100.0, 21 / 252, 0.25
    exact = float(norm.pdf((np.log(S / K) - 0.5 * s * s * T) / (s * np.sqrt(T))) / (S * s * np.sqrt(T)))
    ns = np.unique(np.round(np.logspace(2, 5, 25)).astype(int))
    out = {"pathwise": [], "lr": [], "boundary": []}
    for seed in range(5):
        pw, lr, bd = X.digital_delta_estimators(S, K, T, s, int(ns[-1]), seed=seed)
        for nm, e in (("pathwise", pw), ("lr", lr), ("boundary", bd)):
            cs = np.cumsum(e)
            out[nm].append((cs[ns - 1] / ns).tolist())
    pw, lr, bd = X.digital_delta_estimators(S, K, T, s, 100000, seed=9)
    return _json({"n": ns, "exact": exact, **out, "sd_lr": float(lr.std()), "sd_bd": float(bd.std()),
                  "ratio": float((lr.std() / bd.std()) ** 2)})


def compute_dek() -> dict:
    """Derman, Ergener and Kani's static hedge of the down-and-out call (K = 100, H = 85, six months, 25% vol, 2%):
    the call, plus puts struck at the barrier with earlier and earlier expiries, each sized so the portfolio is worth
    zero on the barrier at one date, filled backward from expiry. The portfolio's value along S = H between the
    dates, and the hedge's cost against the closed form, for 3, 6, 12 and 24 dates."""
    K, H, T, s, r = 100.0, 85.0, 0.5, 0.25, 0.02
    out = {"K": K, "H": H, "T": T, "closed": float(X.down_out_call(100.0, K, H, T, s, r)), "rows": []}
    for n in (3, 6, 12, 24):
        dates = np.linspace(0, T, n + 1)  # t_0 = 0, ..., t_n = T
        legs = [(1.0, K, T, 1)]  # (weight, strike, expiry, call/put)

        def value(S, t, legs=legs):
            v = 0.0
            for w, k, e, cp in legs:
                if e > t + 1e-12:
                    v += w * float(bs.price(S, k, e - t, s, r, 0.0, cp))
            return v
        for i in range(n - 1, -1, -1):
            t = dates[i]
            e = dates[i + 1]
            p = float(bs.price(H, H, e - t, s, r, 0.0, -1))
            legs.append((-value(H, t) / p, H, e, -1))
        ts = np.linspace(0, T - 1e-3, 120)
        along = [value(H, t) for t in ts]
        out["rows"].append({"n": n, "cost": value(100.0, 0.0), "dates": dates, "t": ts, "along": along,
                            "weights": [w for w, _, _, _ in legs[1:]][::-1]})
    return _json(out)


ITEMS = {"market": compute_market, "barrier": compute_barrier, "digital": compute_digital, "asian": compute_asian,
         "snowball": compute_snowball, "surrogate": compute_surrogate, "book2024": compute_book2024,
         "korea": compute_korea, "worstof": compute_worstof, "uvm": compute_uvm, "envelope": compute_envelope,
         "decompose": compute_decompose, "buyers": compute_buyers, "barrier_surface": compute_barrier_surface,
         "static": compute_static, "digital_hedge": compute_digital_hedge, "onetouch": compute_onetouch,
         "digital_skew": compute_digital_skew, "asian_scatter": compute_asian_scatter, "outcomes": compute_outcomes,
         "coupon_q": compute_coupon_q, "greeks3d": compute_greeks3d, "bump_curve": compute_bump_curve,
         "korea2015": compute_korea2015, "corr_regimes": compute_corr_regimes, "worstof_ac": compute_worstof_ac,
         "cliquet": compute_cliquet, "uvm_book": compute_uvm_book, "uvm_film": compute_uvm_film,
         "modelrisk": compute_modelrisk, "robust": compute_robust, "book_vega": compute_book_vega,
         "surrogate_replay": compute_surrogate_replay, "pathwise_digital": compute_pathwise_digital,
         "dek": compute_dek}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
