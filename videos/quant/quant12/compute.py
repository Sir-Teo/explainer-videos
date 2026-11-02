"""Every number in Part 12 (The Volatility Surface), computed and cached in .cache/quant12/.

    python -m videos.quant.quant12.compute [items] [--force]

Items (seconds to a few minutes on a CPU):

* ``surface``    the Surface (10 December 2025): quotes, per-expiry SVI, an SSVI fit, Gatheral's g on each, and the
                 next day's quotes for the sticky-strike / sticky-delta test;
* ``localvol``   Dupire's local volatility from the SSVI fit, and the forward smile it implies (Monte Carlo);
* ``varswap``    the variance-swap strike from the 30-day strip against at-the-money vol; our VIX on the Surface
                 against DVOL;
* ``history``    weekly surfaces from Deribit trades, January 2024 to November 2025: SSVI fits, the 30-day variance
                 swap rate, and the realized variance that followed (the variance risk premium); the SVIX bound;
* ``volmageddon`` the VIX around 5 February 2018 (FRED);
* ``vae``        a variational autoencoder over the weekly surfaces (an implied-vol grid), with a 2-d latent space;
* ``envelope``   registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import bs, paths, pit, smile, surface, volsurface as V

CACHE = Cache("quant12")
load = CACHE.load

KGRID = np.linspace(-0.4, 0.4, 17)
TGRID = np.array([7, 14, 30, 60, 90, 180]) / 365


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


def _fit_day(q):
    w = q["iv"] ** 2 * q["T"]
    ok = (np.abs(q["k"]) < 0.6) & (q["T"] > 2 / 365)
    fit = V.fit_ssvi(q["k"][ok], q["T"][ok], w[ok], weights=q["vega"][ok])
    return fit, ok


def _ssvi_iv(fit, k, T):
    th = V.theta_at(fit, T)
    return np.sqrt(V.ssvi_w(k, th, fit["rho"], fit["eta"], fit["gamma"]) / T)


# ---------------------------------------------------------------------------
def compute_surface() -> dict:
    q = surface.build(surface.DAYS[0])
    q1 = surface.build(surface.DAYS[1])
    fit, ok = _fit_day(q)
    model_iv = _ssvi_iv(fit, q["k"], q["T"])
    rmse_ssvi = surface.vega_rmse(model_iv[ok], q, ok)
    per = []
    for e in q["expiries"]:
        m = np.array([x == e["expiry"] for x in q["expiry"]])
        if m.sum() < 6:
            continue
        T = e["T"]
        p = smile.fit_svi(q["k"][m], q["iv"][m] ** 2 * T, weights=q["vega"][m])
        kk = np.linspace(-1.0, 1.0, 201)
        f = lambda k, t, p=p: smile.svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"])  # noqa: E731
        w, dw, d2w, _ = V.numeric_derivs(f, kk, T)
        per.append({"expiry": e["expiry"], "T": T, "n": int(m.sum()), "svi": p, "g_min": float(V.g_function(kk, w, dw, d2w).min()),
                    "k": q["k"][m], "iv": q["iv"][m], "F": e["F"]})
    # sticky strike vs sticky delta: predict day 2's vols from day 1's smile, holding strike or moneyness fixed
    errs = {"sticky strike": [], "sticky moneyness": []}
    S0, S1 = q["S"], q1["S"]
    for i in range(len(q1["k"])):
        T1 = q1["T"][i]
        K = q1["K"][i]
        F1 = q1["F"][i]
        if T1 < 5 / 365:
            continue
        # day-1 forward of the same horizon, approximately: scale by spot
        F0 = F1 * S0 / S1
        errs["sticky strike"].append(float(_ssvi_iv(fit, np.log(K / F0), T1 + 1 / 365)) - q1["iv"][i])
        errs["sticky moneyness"].append(float(_ssvi_iv(fit, np.log(K / F1), T1 + 1 / 365)) - q1["iv"][i])
    rm = {k: float(np.sqrt(np.mean(np.square(v))) * 100) for k, v in errs.items()}
    gk = np.linspace(-1, 1, 201)
    g_ssvi = [float(V.g_function(gk, *V.numeric_derivs(lambda k, t, th=th: V.ssvi_w(k, th, fit["rho"], fit["eta"], fit["gamma"]),
                                                         gk, 0.5)[:3]).min()) for th in fit["theta"]]
    return _json({"S": q["S"], "S_next": S1, "ssvi": fit, "rmse_ssvi": rmse_ssvi, "per": per, "n_quotes": int(len(q["k"])),
                  "sticky_rmse": rm, "g_ssvi_min": float(min(g_ssvi)), "K": q["K"], "T": q["T"], "k": q["k"], "iv": q["iv"],
                  "grid_k": KGRID, "grid_T": TGRID,
                  "grid_iv": np.array([[float(_ssvi_iv(fit, k, T)) for k in KGRID] for T in TGRID])})


def compute_localvol() -> dict:
    s = load("surface")
    fit = s["ssvi"]
    f = lambda k, T: V.ssvi_surface_w(fit, k, T)  # noqa: E731
    ks = np.linspace(-0.4, 0.4, 41)
    Ts = np.array([7, 14, 30, 60, 90, 180]) / 365
    lv = np.zeros((len(Ts), len(ks)))
    for i, T in enumerate(Ts):
        w, dw, d2w, dT = V.numeric_derivs(f, ks, T, h=2e-3, hT=2e-3)
        lv[i] = np.sqrt(np.maximum(V.dupire_local_var(ks, w, dw, d2w, dT), 1e-6))
    # forward smile under local vol: Monte Carlo of dS/S = sigma_loc(log S/F, t) dW, a 30-day option starting in 60 days
    # (the House's simulator, shared with Part 13's comparison of models)
    steps1, steps2 = 60, 30
    X = V.local_vol_paths(fit, steps1 + steps2, 40000, seed=7)
    x, x_start = X[-1], X[steps1]
    Rk = np.linspace(-0.25, 0.25, 11)
    ret = np.exp(x - x_start)
    T2 = steps2 / 365
    fwd_iv = []
    for k in Rk:  # out-of-the-money options, as quoted
        cp = 1 if k >= 0 else -1
        c = np.mean(np.maximum(cp * (ret - np.exp(k)), 0))
        fwd_iv.append(float(bs.implied_vol(c, 1.0, np.exp(k), T2, 0.0, 0.0, cp)))
    today_iv = [float(_ssvi_iv(fit, k, T2)) for k in Rk]
    return _json({"k": ks, "T": Ts, "lv": lv, "fwd_k": Rk, "fwd_iv": fwd_iv, "spot_iv_30d": today_iv,
                  "fwd_skew": float(fwd_iv[3] - fwd_iv[7]), "spot_skew": float(today_iv[3] - today_iv[7])})


def compute_varswap() -> dict:
    s = load("surface")
    fit = s["ssvi"]
    S = s["S"]
    out = {}
    T = 30 / 365
    F = S  # the 30-day forward, close to spot on this day (Part 9's basis is a few percent a year)
    K = np.linspace(0.3 * F, 2.5 * F, 2201)
    iv = _ssvi_iv(fit, np.log(K / F), T)
    otm = np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))
    kvar = V.var_swap_strike(K, otm, F, T)
    atm = float(_ssvi_iv(fit, 0.0, T))
    # the VIX recipe on strikes like Deribit's (every 1,000 or 2,000 dollars), interpolated to 30 days
    Kd = np.arange(round(0.5 * F, -3), round(1.6 * F, -3) + 1, 2000.0)
    vixs = []
    for TT in (21 / 365, 42 / 365):
        ivd = _ssvi_iv(fit, np.log(Kd / F), TT)
        vixs.append((TT, V.vix(Kd, bs.price(F, Kd, TT, ivd, cp=1), bs.price(F, Kd, TT, ivd, cp=-1), F, TT)))
    (T1, v1), (T2, v2) = vixs
    w30 = ((T2 - T) / (T2 - T1)) * T1 * v1 ** 2 + ((T - T1) / (T2 - T1)) * T2 * v2 ** 2
    our_vix = float(np.sqrt(w30 / T))
    dv = data.deribit_dvol("2025-12", "2025-12")
    ref = datetime(2025, 12, 10, 8, tzinfo=timezone.utc).timestamp()
    dvol = float(dv["close"][np.argmin(np.abs(np.asarray(dv["time"]) - ref))]) / 100
    weights = 1 / K ** 2
    out.update({"K": K, "weights": weights / weights.max(), "otm": otm, "kvar": float(np.sqrt(kvar)), "atm": atm,
                "our_vix": our_vix, "dvol": dvol, "F": F})
    return _json(out)


def _realized_after(ts, days=30):
    kl = data.binance_klines("BTCUSDT", "1h", "2024-01", "2025-12")
    t = np.asarray(kl["time"]) + 3600
    c = np.asarray(kl["close"])
    i = int(np.searchsorted(t, ts))
    j = i + days * 24
    if j >= len(c):
        return np.nan
    r = np.diff(np.log(c[i:j + 1]))
    return float(np.sum(r * r) * 365 / days)


def compute_history() -> dict:
    d = date(2024, 1, 3)
    rows = []
    while d <= date(2025, 11, 26):
        try:
            q = surface.build(d.isoformat())
            fit, ok = _fit_day(q)
            F = q["S"]
            T = 30 / 365
            K = np.linspace(0.3 * F, 2.5 * F, 1101)
            iv = _ssvi_iv(fit, np.log(K / F), T)
            otm = np.where(K < F, bs.price(F, K, T, iv, cp=-1), bs.price(F, K, T, iv, cp=1))
            kvar = V.var_swap_strike(K, otm, F, T)
            ref = datetime(d.year, d.month, d.day, 8, tzinfo=timezone.utc).timestamp()
            rv = _realized_after(ref)
            grid = np.array([[float(_ssvi_iv(fit, k, T_)) for k in KGRID] for T_ in TGRID])
            # Martin's SVIX: the lower bound on the expected return over 30 days, (risk-neutral variance of R)/R_f
            Kq = np.linspace(0.2 * F, 3.0 * F, 2801)
            ivq = _ssvi_iv(fit, np.log(Kq / F), T)
            otmq = np.where(Kq < F, bs.price(F, Kq, T, ivq, cp=-1), bs.price(F, Kq, T, ivq, cp=1))
            svix2 = float(2 / (T * F ** 2) * np.trapezoid(otmq, Kq))
            rows.append({"day": d.isoformat(), "S": F, "kvar": kvar, "rv": rv, "atm": float(_ssvi_iv(fit, 0.0, T)),
                         "skew": float(_ssvi_iv(fit, -0.1, T) - _ssvi_iv(fit, 0.1, T)), "grid": grid, "rmse": fit["rmse"],
                         "svix2": svix2, "n": int(ok.sum())})
        except Exception as e:  # a day without enough quotes is skipped, and said so
            rows.append({"day": d.isoformat(), "error": str(e)[:200]})
        d += timedelta(days=7)
    good = [r for r in rows if "kvar" in r]
    kv = np.array([r["kvar"] for r in good])
    rv = np.array([r["rv"] for r in good])
    m = np.isfinite(rv)
    vrp = kv[m] - rv[m]
    # weekly observations of 30-day windows overlap by about four: Newey-West with 4 lags
    mean = float(vrp.mean())
    dc = vrp - mean
    v = dc @ dc / len(dc)
    for L in range(1, 5):
        v += 2 * (1 - L / 5) * (dc[L:] @ dc[:-L]) / len(dc)
    t_nw = float(mean / np.sqrt(v / len(dc)))
    return _json({"rows": good, "skipped": [r["day"] for r in rows if "error" in r], "n": len(good),
                  "vrp_mean": mean, "vrp_t": t_nw, "share_positive": float((vrp > 0).mean()),
                  "kvar_vol_mean": float(np.sqrt(kv[m]).mean()), "rv_vol_mean": float(np.sqrt(rv[m]).mean()),
                  "svix_bound_mean": float(np.mean([r["svix2"] for r in good]) ), "grid_k": KGRID, "grid_T": TGRID})


def compute_volmageddon() -> dict:
    v = data.fred("VIXCLS", "2017-06-01", "2018-06-30")
    dd, x = np.asarray(v["date"]), np.asarray(v["value"])
    ok = np.isfinite(x)
    i = int(np.where(dd == 20180205)[0][0])
    return _json({"date": dd[ok], "vix": x[ok], "before": float(x[i - 1]), "after": float(x[i]),
                  "jump": float(x[i] / x[i - 1] - 1), "min_2017": float(np.nanmin(x[(dd >= 20170601) & (dd < 20180101)]))})


def compute_vae() -> dict:
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(0)
    h = load("history")
    X = np.array([np.asarray(r["grid"]).ravel() for r in h["rows"]])
    X = np.log(np.clip(X, 0.05, 5.0))
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = torch.tensor((X - mu) / sd, dtype=torch.float32)
    n_in, n_lat = Z.shape[1], 2
    enc = torch.nn.Sequential(torch.nn.Linear(n_in, 64), torch.nn.Tanh(), torch.nn.Linear(64, 2 * n_lat))
    dec = torch.nn.Sequential(torch.nn.Linear(n_lat, 64), torch.nn.Tanh(), torch.nn.Linear(64, n_in))
    opt = torch.optim.Adam(list(enc.parameters()) + list(dec.parameters()), lr=3e-3)
    for it in range(3000):
        e = enc(Z)
        m_, lv = e[:, :n_lat], e[:, n_lat:]
        z = m_ + torch.exp(0.5 * lv) * torch.randn_like(m_)
        rec = dec(z)
        kl = -0.5 * torch.mean(torch.sum(1 + lv - m_ ** 2 - torch.exp(lv), 1))
        loss = torch.mean((rec - Z) ** 2) + 0.01 * kl
        opt.zero_grad()
        loss.backward()
        opt.step()
    with torch.no_grad():
        m_ = enc(Z)[:, :n_lat].numpy()
        recon = dec(torch.tensor(m_)).numpy()
        err = float(np.sqrt(np.mean((np.exp(recon * sd + mu) - np.exp(X)) ** 2)) * 100)
        # walk the latent space: the surfaces at z = (a, 0) and (0, b)
        walk = {}
        for name, axis in (("z1", 0), ("z2", 1)):
            vals = np.linspace(-2, 2, 5)
            outs = []
            for v_ in vals:
                z = np.zeros((1, n_lat))
                z[0, axis] = v_
                outs.append(np.exp(dec(torch.tensor(z, dtype=torch.float32)).numpy()[0] * sd + mu).reshape(len(TGRID), len(KGRID)))
            walk[name] = np.array(outs)
    atm = np.array([np.asarray(r["grid"])[2, len(KGRID) // 2] for r in h["rows"]])
    skew = np.array([r["skew"] for r in h["rows"]])
    c1 = [float(np.corrcoef(m_[:, j], atm)[0, 1]) for j in range(n_lat)]
    c2 = [float(np.corrcoef(m_[:, j], skew)[0, 1]) for j in range(n_lat)]
    return _json({"latent": m_, "recon_rmse_volpts": err, "walk": walk, "corr_atm": c1, "corr_skew": c2,
                  "days": [r["day"] for r in h["rows"]], "atm": atm, "skew": skew})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


ITEMS = {"surface": compute_surface, "localvol": compute_localvol, "varswap": compute_varswap,
         "history": compute_history, "volmageddon": compute_volmageddon, "vae": compute_vae,
         "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
