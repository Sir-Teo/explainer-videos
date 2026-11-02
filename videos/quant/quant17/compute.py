"""Every number in Part 17 (Deep Pricing and Hedging), computed and cached in .cache/quant17/.

    python -m videos.quant.quant17.compute [items] [--force]

Items (minutes each on a CPU; ``calib_data`` is the long one, and two processes running it share the chunks):

* ``calib_data``  rough Bergomi Monte Carlo implied volatilities for 12,000 random parameter sets (80 points each),
                  in resumable chunks under .cache/quant17/calib/;
* ``calib``       the pointwise neural calibrator: training curve, held-out error, and the Surface calibrated through
                  it, checked by fresh Monte Carlo against Part 14's direct fit;
* ``calib_hist``  rough Bergomi through the network on Part 13's 100 weekly surfaces (2024-2025): H, eta, rho through
                  time, against Heston's weekly fits;
* ``hlp``         Hutchinson, Lo and Poggio (1994) redone: a network learns a call's price from simulated market data
                  and hedges it;
* ``dml``         differential machine learning on a basket option: price error against training-set size, with and
                  without the derivatives;
* ``bsde``        the deep BSDE solver on Han-Jentzen-E's 100-dimensional pricing equation with default risk;
* ``stopping``    deep optimal stopping for a Bermudan max-call on five assets;
* ``hedge``       the deep hedger: no costs (against Black-Scholes delta), proportional costs (the no-trade band
                  against Whalley-Wilmott), training snapshots, and indifference prices by cost;
* ``nsde``        a neural SDE calibrated to vanillas: robust lower and upper prices of an exotic;
* ``generator``   market generators for BTC's daily returns (GARCH, a signature-MMD generator and a small diffusion
                  model) scored on the stylized facts of Part 1;
* ``envelope``    registers nothing (no strategy is tested); the counter.
"""

from __future__ import annotations

import json
import os
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant.house import deep as D, pit

CACHE = Cache("quant17")
load = CACHE.load

N_SETS, CHUNK = 12000, 200


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


# ---------------------------------------------------------------------------
def compute_calib_data() -> dict:
    """Chunks of 200 parameter sets; a chunk is claimed by an exclusive lock file, so several processes can share the
    work and a restart resumes where it stopped."""
    out = CACHE.dir / "calib"
    out.mkdir(parents=True, exist_ok=True)
    n_chunks = N_SETS // CHUNK
    for c in range(n_chunks):
        f = out / f"chunk_{c:03d}.npz"
        lock = out / f"chunk_{c:03d}.lock"
        if f.exists():
            continue
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
        except FileExistsError:
            continue
        rng = np.random.default_rng(1000 + c)
        P = D._sample_params(rng, CHUNK)
        rows = []
        t0 = time.time()
        for i, th in enumerate(P):
            r = D.rbergomi_iv_samples(th, seed=100000 * c + 97 * i)
            rows.append(np.hstack([np.repeat(th[None], len(r), 0), r, np.full((len(r), 1), c * CHUNK + i)]))
        np.savez_compressed(f, rows=np.vstack(rows).astype(np.float32))
        lock.unlink(missing_ok=True)
        print(f"  chunk {c + 1}/{n_chunks} in {time.time() - t0:.0f}s", flush=True)
    while len(list(out.glob("chunk_*.npz"))) < n_chunks:  # another process is finishing its chunks
        time.sleep(30)
    n = sum(len(np.load(f)["rows"]) for f in out.glob("chunk_*.npz"))
    return {"sets": N_SETS, "points": int(n), "bounds": D.CALIB_BOUNDS, "paths_per_set": 10000}


def _calib_rows():
    return np.vstack([np.load(f)["rows"] for f in sorted((CACHE.dir / "calib").glob("chunk_*.npz"))])


def _mc_iv_quotes(theta, T, k, n_paths=40000, seed=0):
    """Fresh rough Bergomi Monte Carlo implied vols at quotes (T, k): the check on the network's answer."""
    from explainer.quant.house import bs, rough as R

    H, eta, rho, v0, v1 = theta
    days = int(np.ceil(T.max() * 365)) + 1
    S = np.hstack([R.rbergomi_paths(H, eta, rho, D.xi_ramp(v0, v1), days / 365, days, 20000, seed=seed + j)
                   for j in range(n_paths // 20000)])
    out = np.full(len(T), np.nan)
    for i, (t, kk) in enumerate(zip(T, k)):
        x = S[int(round(t * 365))]
        cp = 1 if kk >= 0 else -1
        p = float(np.mean(np.maximum(cp * (x - np.exp(kk)), 0)))
        out[i] = bs.implied_vol(p, 1.0, float(np.exp(kk)), float(t), 0.0, 0.0, cp)
    return out


def _surface_quotes(day=None, min_T=6 / 365):
    from videos.quant.quant13 import compute as Q13

    Q = Q13._quotes(day, min_T=min_T) if day else Q13._quotes(min_T=min_T)
    m = (Q["T"] <= D.T_MAX) & (np.abs(Q["k"]) < 0.5)
    return {k: (v[m] if isinstance(v, np.ndarray) and len(v) == len(m) else v) for k, v in Q.items()}


def _calib_net():
    import torch

    net = D.calib_net()
    net.load_state_dict(torch.load(CACHE.dir / "calib_net.pt"))
    net.eval()
    return net


def compute_calib() -> dict:
    import torch

    torch.set_num_threads(2)
    rows = _calib_rows()
    sets = rows[:, -1].astype(int)
    held = (sets % 20) == 0  # 5% of parameter sets never seen in training
    X = D.calib_features(rows[:, :5], rows[:, 5], rows[:, 6])
    y = rows[:, 7]
    t0 = time.time()
    net, hist = D.train_calib_net(X[~held], y[~held], epochs=40, val=(X[held], y[held]),
                                  log=lambda r: print("   ", r, flush=True))
    train_s = time.time() - t0
    torch.save(net.state_dict(), CACHE.dir / "calib_net.pt")
    net.eval()
    # Monte Carlo noise of the labels themselves: the same parameter sets simulated again with other random numbers
    rng = np.random.default_rng(5)
    noise = []
    for j in rng.choice(np.unique(sets[held]), 12, replace=False):
        r = rows[sets == j]
        th = r[0, :5].astype(float)
        again = _mc_iv_quotes(th, r[:, 5].astype(float), r[:, 6].astype(float), n_paths=20000, seed=777 + int(j))
        ok = np.isfinite(again)
        noise.append((again[ok] - r[ok, 7]) * 100)
    noise = np.concatenate(noise)
    with torch.no_grad():
        pred = net(torch.from_numpy(X[held])).numpy()[:, 0]
    err = (pred - y[held]) * 100
    # the Surface, through the network, then checked by fresh Monte Carlo
    Q = _surface_quotes()
    w = Q["vega"] / Q["vega"].mean()  # vega-weighted squared errors, as Part 13 and 14 score fits
    fit = D.calibrate_neural(net, Q["T"], Q["k"], Q["iv"], w=w, starts=12)
    mc = _mc_iv_quotes(np.array(fit["x"]), Q["T"], Q["k"], n_paths=60000, seed=41)
    ok = np.isfinite(mc)
    mc_rmse = float(np.sqrt(np.average((mc[ok] - Q["iv"][ok]) ** 2 * 1e4, weights=Q["vega"][ok])))
    # one evaluation of the network for the whole surface, for the speed comparison
    feats = torch.from_numpy(D.calib_features(np.array(fit["x"]), Q["T"], Q["k"]))
    with torch.no_grad():
        t1 = time.perf_counter()
        for _ in range(100):
            net(feats)
        t_eval = (time.perf_counter() - t1) / 100
    t1 = time.perf_counter()
    _mc_iv_quotes(np.array(fit["x"]), Q["T"], Q["k"], n_paths=20000, seed=3)
    t_mc = time.perf_counter() - t1
    from videos.quant.quant14 import compute as Q14
    rb = Q14.load("rbergomi")
    # a smile slice for the picture: market, network and Monte Carlo at three expiries
    Ts = np.unique(Q["T"])
    pick = [Ts[np.argmin(np.abs(Ts - t))] for t in (14 / 365, 45 / 365, 120 / 365)]
    slices = []
    for t in pick:
        m = Q["T"] == t
        kk = np.linspace(Q["k"][m].min(), Q["k"][m].max(), 40)
        with torch.no_grad():
            curve = net(torch.from_numpy(D.calib_features(np.array(fit["x"]), np.full(40, t), kk))).numpy()[:, 0]
        slices.append({"T": float(t), "k": Q["k"][m], "iv": Q["iv"][m], "mc": mc[m], "kk": kk, "net": curve})
    return _json({"history": hist, "train_seconds": train_s, "n_train": int((~held).sum()), "n_held": int(held.sum()),
                  "held_rmse": float(np.sqrt(np.mean(err ** 2))), "held_err_q": np.percentile(np.abs(err), [50, 90, 99]),
                  "label_noise_rmse": float(np.sqrt(np.mean(noise ** 2))),
                  "surface": {"params": fit["params"], "net_rmse": fit["rmse"], "mc_rmse": mc_rmse,
                              "seconds": fit["seconds"], "n": int(len(Q["K"]))},
                  "t_net_surface": t_eval, "t_mc_surface": t_mc, "part14": {"params": rb["params"], "rmse": rb["rmse"]},
                  "slices": slices})


def compute_calib_hist() -> dict:
    import torch

    torch.set_num_threads(2)
    from explainer.quant.house import stochvol as sv
    from videos.quant.quant13 import compute as Q13
    net = _calib_net()
    hist = Q13.load("history")
    out = []
    for r in hist["rows"]:
        try:
            Q = _surface_quotes(r["day"])
        except Exception as e:  # a day without enough quotes
            print("   skip", r["day"], str(e)[:80])
            continue
        if len(Q["K"]) < 20:
            continue
        w = Q["vega"] / Q["vega"].mean()  # vega-weighted squared errors, as Part 13 and 14 score fits
        f = D.calibrate_neural(net, Q["T"], Q["k"], Q["iv"], w=w, starts=4, iters=150)
        # Heston refitted to exactly these quotes, starting from Part 13's weekly fit (which used every expiry)
        hf = sv.calibrate("Heston", Q, x0=r["x"], max_nfev=80)
        h_rmse = float(hf["rmse"])
        out.append({"day": r["day"], **f["params"], "rmse": f["rmse"], "heston_rmse": h_rmse, "heston_rmse_all": r["rmse"],
                    "heston_rho": r["x"][4], "n": int(len(Q["K"])), "seconds": f["seconds"]})
        print("   ", r["day"], {k: round(v, 3) for k, v in f["params"].items()}, round(f["rmse"], 2), flush=True)
    H = np.array([o["H"] for o in out])
    # spot checks: every tenth week re-priced by fresh Monte Carlo at the network's parameters
    checks = []
    for o in out[::10]:
        Q = _surface_quotes(o["day"])
        mc = _mc_iv_quotes(np.array([o[n] for n in D.CALIB_NAMES]), Q["T"], Q["k"], n_paths=40000, seed=9)
        ok = np.isfinite(mc)
        checks.append({"day": o["day"], "net_rmse": o["rmse"],
                       "mc_rmse": float(np.sqrt(np.average((mc[ok] - Q["iv"][ok]) ** 2 * 1e4, weights=Q["vega"][ok])))})
    return _json({"rows": out, "H_median": float(np.median(H)), "H_q": np.percentile(H, [10, 25, 75, 90]),
                  "share_H_below_0_15": float(np.mean(H < 0.15)), "rmse_median": float(np.median([o["rmse"] for o in out])),
                  "heston_rmse_median": float(np.median([o["heston_rmse"] for o in out])), "checks": checks,
                  "seconds_median": float(np.median([o["seconds"] for o in out]))})


def compute_hlp() -> dict:
    """HLP's experiment: a network learns C/K = f(S/K, T) from two years of simulated option prices, then delta-hedges
    fresh options with its own derivative; its tracking error is set against the Black-Scholes delta's."""
    import torch

    from explainer.quant.house import bs

    torch.set_num_threads(2)
    sig = 0.2
    tr = D.hlp_dataset(10, seed=1)
    # inputs scaled to order one: (S/K - 1) / 0.1 and T / 0.25
    sc = np.array([[1.0, 0.0], [0.1, 0.25]])
    core = D.train_mlp_regressor((tr[:, :2] - sc[0]) / sc[1], tr[:, 2:] * 10, width=64, depth=3, epochs=200)

    def net(x):
        return core((x - torch.tensor(sc[0], dtype=torch.float32)) / torch.tensor(sc[1], dtype=torch.float32)) / 10
    rng = np.random.default_rng(7)
    errs = {"net": [], "bs": []}
    for _ in range(200):  # fresh options: 63 trading days, struck at the money, daily rebalancing
        S = 50 * np.exp(np.cumsum(np.r_[0, sig * np.sqrt(1 / 252) * rng.standard_normal(63) - 0.5 * sig ** 2 / 252]))
        K = 50.0
        T = (63 - np.arange(64)) / 252
        x = torch.tensor(np.c_[S[:-1] / K, T[:-1]], dtype=torch.float32, requires_grad=True)
        out = net(x)
        g, = torch.autograd.grad(out.sum(), x)
        d_net = g[:, 0].numpy()
        d_bs = bs.greeks(S[:-1], K, T[:-1], sig, 0.0, 0.0, 1)["delta"]
        c0_net = float(out[0, 0].detach()) * K
        c0 = float(bs.price(S[0], K, T[0], sig, 0.0, 0.0, 1))
        payoff = max(S[-1] - K, 0)
        for name, d, c in (("net", d_net, c0_net), ("bs", d_bs, c0)):
            errs[name].append(c + float(np.sum(d * np.diff(S))) - payoff)
    xs = np.linspace(0.8, 1.2, 41)
    with torch.no_grad():
        curve = net(torch.tensor(np.c_[xs, np.full(41, 0.125)], dtype=torch.float32)).numpy()[:, 0]
    return _json({"n_train": len(tr), "network": "3 x 64, SiLU", "tracking_rmse": {k: float(np.sqrt(np.mean(np.square(v)))) for k, v in errs.items()},
                  "tracking_mean_abs": {k: float(np.mean(np.abs(v))) for k, v in errs.items()},
                  "curve": {"x": xs, "net": curve, "bs": bs.price(xs, 1.0, 0.125, sig, 0.0, 0.0, 1)}})


def compute_dml() -> dict:
    import torch

    torch.set_num_threads(2)
    mkt = D.bachelier_basket(7, seed=0)
    Xte = 100 + 1.0 * np.random.default_rng(5).standard_normal((4096, 7)) @ mkt["chol"].T
    pe, de = D.bachelier_price(mkt, Xte)
    rows = []
    fits = {}
    for n in (256, 1024, 4096, 16384):
        X, Y, dY = D.bachelier_samples(mkt, n, seed=n)
        for use in (False, True):
            t0 = time.time()
            f = D.train_differential(X, Y, dY if use else None, seed=1)
            p, dd = f(Xte)
            rows.append({"n": n, "differential": use, "price_rmse": float(np.sqrt(np.mean((p - pe) ** 2))),
                         "delta_rmse": float(np.sqrt(np.mean((dd - de) ** 2))), "seconds": time.time() - t0})
            print("   ", rows[-1], flush=True)
            if n == 1024:
                fits[use] = f
    u = np.linspace(-30, 30, 61)
    Xs = 100 + u[:, None] * np.ones((1, 7))
    X, Y, _ = D.bachelier_samples(mkt, 1024, seed=1024)
    B = X @ mkt["w"]
    sl = {"u": u, "exact": D.bachelier_price(mkt, Xs)[0], "plain": fits[False](Xs)[0], "diff": fits[True](Xs)[0],
          "scatter_B": B[:300] - 100, "scatter_Y": Y[:300]}
    return _json({"rows": rows, "slice": sl, "basket_vol": mkt["bvol"], "d": 7})


def compute_bsde() -> dict:
    import torch

    torch.set_num_threads(2)
    t0 = time.time()
    r = D.deep_bsde(iters=4000, log=lambda c: print("   ", c, flush=True) if c["iter"] % 500 == 0 else None)
    secs = time.time() - t0
    nd, se = D.no_default_price()
    p = D.DEFAULT_RISK
    return _json({"u0": r["u0"], "curve": r["curve"], "seconds": secs, "reference": p["reference"],
                  "rel_error": abs(r["u0"] - p["reference"]) / p["reference"], "no_default_mc": nd, "no_default_se": se,
                  "paper_no_default": p["no_default"], "params": p})


def compute_stopping() -> dict:
    import torch

    torch.set_num_threads(2)
    out = {}
    for d, ref in ((2, {"binomial": 13.902}), (5, D.MAX_CALL["paper"])):
        p = dict(D.MAX_CALL, d=d)
        t0 = time.time()
        r = D.deep_stopping(p, steps=500, log=lambda n, v: print("    date", n, round(v, 3), flush=True))
        out[str(d)] = {"lower": r["lower"], "se": r["se"], "seconds": time.time() - t0, "reference": ref,
                       "curves": {str(k): v for k, v in r["curves"].items()}}
        # the learned exercise region at date 4, in two dimensions: S1 and S2 with the other assets held at 100
        if d == 2:
            net = r["nets"][4]
            net.eval()
            g = np.linspace(60, 180, 61)
            G1, G2 = np.meshgrid(g, g)
            S = torch.tensor(np.c_[G1.ravel(), G2.ravel()] / 100, dtype=torch.float32)
            pay = torch.clamp(torch.maximum(S[:, 0], S[:, 1]) * 100 - 100, min=0) * float(np.exp(-0.05 * 4 / 3))
            with torch.no_grad():
                stop = net(torch.cat([S, pay[:, None] / 100], 1))[:, 0].numpy() > 0
            out["region"] = {"grid": g, "stop": stop.reshape(61, 61).astype(int)}
        print("   d =", d, out[str(d)]["lower"], flush=True)
    return _json(out)


HEDGE = {"sigma": 0.2, "T": 30 / 365, "steps": 30, "K": 100.0, "gamma": 1.0}


def compute_hedge() -> dict:
    import torch

    from explainer.quant.house import bs, quoting

    torch.set_num_threads(2)
    h = HEDGE
    out = {"setup": h}
    # 1. no costs: the network against Black-Scholes delta
    pg = np.linspace(0, 1, 51)
    S_sl = (95.0, 100.0, 105.0)

    def slices(p):
        """The trade (new holding minus old) against the holding already held, at three prices, 15 days left."""
        out = {}
        for s_ in S_sl:
            x = torch.full((51,), float(np.log(s_ / 100)))
            out[str(int(s_))] = (p(x, torch.full((51,), tau), torch.tensor(pg, dtype=torch.float32)).numpy() - pg)
        return out
    tau = 0.5
    pol, curve, _ = D.train_hedger("mlp", cost=0.0, iters=2500, batch=4096, seed=1,
                                   log=lambda i, l: print("    nocost", i, round(l, 4), flush=True))
    ev = D.evaluate_hedger(pol, 0.0)
    bsd = D.evaluate_hedger(D.delta_hedger(h["sigma"], h["T"]), 0.0)
    Sg = np.linspace(85, 115, 61)
    with torch.no_grad():
        nocost_slices = slices(pol)
    with torch.no_grad():
        prev = torch.tensor(bs.greeks(Sg, 100, tau * h["T"], h["sigma"], 0, 0, 1)["delta"], dtype=torch.float32)
        learned = pol(torch.log(torch.tensor(Sg / 100, dtype=torch.float32)), torch.full((61,), tau), prev).numpy()
    out["nocost"] = {"curve": curve[::10], "eval": ev, "bs_eval": bsd, "bs_price": float(bs.price(100, 100, h["T"], h["sigma"], 0, 0, 1)),
                     "S": Sg, "learned": learned, "bs_delta": prev.numpy(),
                     "slices": nocost_slices}
    # 2. costs 0.5%: the plain network, with snapshots of its trade map at 15 days to expiry
    SS, PP = np.meshgrid(Sg, pg)

    def snap(p):
        x = torch.log(torch.tensor(SS.ravel() / 100, dtype=torch.float32))
        new = p(x, torch.full((SS.size,), tau), torch.tensor(PP.ravel(), dtype=torch.float32)).numpy()
        return {"map": (new - PP.ravel()).reshape(PP.shape), "slices": slices(p)}
    cost = 0.005
    pol2, curve2, snaps = D.train_hedger("mlp", cost=cost, iters=3000, batch=4096, seed=1,
                                         snap_at=(0, 100, 300, 1000, 3000), snap_fn=snap,
                                         log=lambda i, l: print("    mlp cost", i, round(l, 4), flush=True))
    ww = quoting.ww_band(Sg, 100, tau * h["T"], h["sigma"], cost, gamma_risk=h["gamma"])
    wws = {str(int(s_)): quoting.ww_band(s_, 100, tau * h["T"], h["sigma"], cost, gamma_risk=h["gamma"]) for s_ in S_sl}
    flat = {}
    for key, sl in (("nocost", nocost_slices), ("cost", snaps[3000]["slices"])):
        z = np.asarray(sl["100"])
        w = pg[np.abs(z) < 0.02]
        flat[key] = [float(w.min()), float(w.max())] if len(w) else None
    out["mlp_cost"] = {"cost": cost, "curve": curve2[::10], "snaps": {str(k): v["map"] for k, v in snaps.items()},
                       "snap_slices": {str(k): v["slices"] for k, v in snaps.items()}, "S": Sg, "prev": pg,
                       "slice_S": S_sl, "ww_slices": {k: [float(v["lo"]), float(v["hi"]), float(v["delta"])] for k, v in wws.items()},
                       "flat_atm": flat, "ww_lo": ww["lo"], "ww_hi": ww["hi"], "delta": ww["delta"],
                       "eval": D.evaluate_hedger(pol2, cost)}
    # 3. the band network by cost: indifference price, turnover; Whalley-Wilmott and plain delta on the same paths
    rows = []
    surf = None
    for c in (0.0, 0.001, 0.0025, 0.005, 0.01):
        polb, _, _ = D.train_hedger("band", cost=c, iters=1200, batch=4096, seed=2,
                                    log=lambda i, l: print("    band", c, i, round(l, 4), flush=True))
        e = D.evaluate_hedger(polb, c)
        e_bs = D.evaluate_hedger(D.delta_hedger(h["sigma"], h["T"]), c)
        e_ww = D.evaluate_hedger(D.delta_hedger(h["sigma"], h["T"], band=(c, h["gamma"])), c) if c > 0 else e_bs
        rows.append({"cost": c, "deep": e, "delta": e_bs, "ww": e_ww})
        if c == cost:
            ts = np.linspace(0.05, 1.0, 20)
            lo = np.zeros((20, 61))
            hi = np.zeros((20, 61))
            wl = np.zeros((20, 61))
            wh = np.zeros((20, 61))
            with torch.no_grad():
                x = torch.log(torch.tensor(Sg / 100, dtype=torch.float32))
                for i, tt in enumerate(ts):
                    bl, bh = polb.band(x, torch.full((61,), float(tt)))
                    lo[i], hi[i] = bl.numpy(), bh.numpy()
                    b = quoting.ww_band(Sg, 100, tt * h["T"], h["sigma"], c, gamma_risk=h["gamma"])
                    wl[i], wh[i] = b["lo"], b["hi"]
            surf = {"tau": ts, "S": Sg, "lo": lo, "hi": hi, "ww_lo": wl, "ww_hi": wh}
    out["band"] = {"rows": rows, "surface": surf}
    return _json(out)


def compute_nsde() -> dict:
    """A neural SDE fitted to 36 Heston call prices (4 expiries x 9 strikes), then pushed to the lowest and highest
    price of a down-and-out call that stays consistent with the same vanillas. Heston's own price must lie inside."""
    import torch

    from explainer.quant.house import bs, stochvol as sv

    torch.set_num_threads(2)
    hes = (0.04, 1.5, 0.04, 0.5, -0.7)
    mats = [0.25, 0.5, 0.75, 1.0]
    strikes = np.round(np.linspace(0.8, 1.2, 9), 3)
    cf = lambda u, TT: sv.heston_cf(u, TT, *hes)  # noqa: E731
    target = np.array([sv.cos_price(cf, 1.0, strikes, T, 1, N=1024) for T in mats])
    tgt = torch.tensor(target, dtype=torch.float32)
    steps, T = 50, 1.0
    gen = torch.Generator().manual_seed(0)

    def calib_loss(m, n=16384):
        S = m.paths(n, T, steps, gen)
        return ((D.nsde_prices(S, mats, strikes, steps, T) - tgt) * 100).pow(2).mean(), S

    def ivs(m):
        g2 = torch.Generator().manual_seed(123)
        with torch.no_grad():
            S = m.paths(200000, T, steps, g2)
            P = D.nsde_prices(S, mats, strikes, steps, T).numpy()
            doc = float(D.down_out_call(S))
        iv = np.array([[bs.implied_vol(P[i, j], 1.0, strikes[j], mats[i], 0, 0, 1) for j in range(9)] for i in range(4)])
        return iv, doc
    tiv = np.array([[bs.implied_vol(target[i, j], 1.0, strikes[j], mats[i], 0, 0, 1) for j in range(9)] for i in range(4)])
    m = D.NeuralSV(seed=0)
    opt = torch.optim.Adam(m.parameters(), lr=3e-3)
    for it in range(800):
        loss, _ = calib_loss(m)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if it % 100 == 0:
            print("    calib", it, float(loss.detach()), flush=True)
    base = m.state_dict()
    iv0, doc0 = ivs(m)
    res = {"calibrated": {"iv_rmse": float(np.sqrt(np.mean((iv0 - tiv) ** 2)) * 100), "doc": doc0}}
    base_cl = float(calib_loss(m)[0].detach())
    for side, sgn in (("low", 1.0), ("high", -1.0)):
        mm = D.NeuralSV(seed=0)
        mm.load(base)
        opt = torch.optim.Adam(mm.parameters(), lr=5e-4)
        best = None
        for it in range(600):
            cl, S = calib_loss(mm)
            doc_ = D.down_out_call(S)
            loss = sgn * doc_ * 100 + 50.0 * cl
            if not torch.isfinite(loss):
                mm.load(best[1] if best else base)  # back to the last good state
                continue
            # keep the most extreme state that still reprices the vanillas about as well as the first calibration
            if float(cl) <= max(3 * base_cl, 0.004) and (best is None or sgn * float(doc_) < sgn * best[0]):
                best = (float(doc_), mm.state_dict())
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(mm.parameters(), 1.0)
            opt.step()
            if it % 100 == 0:
                print("    ", side, it, float(cl.detach()), float(doc_.detach()), flush=True)
        if best is not None:
            mm.load(best[1])
        iv, doc = ivs(mm)
        res[side] = {"iv_rmse": float(np.sqrt(np.mean((iv - tiv) ** 2)) * 100), "doc": doc, "iv": iv}
    # Heston's own down-and-out price, monitored at the same 50 dates
    P = sv.heston_qe(1.0, *hes, T, steps, 400000, seed=5)
    alive = P.min(0) > 0.8
    res["heston_doc"] = float(np.mean(alive * np.maximum(P[-1] - 1.0, 0)))
    res["target_iv"] = tiv
    res["setup"] = {"mats": mats, "strikes": strikes, "barrier": 0.8, "heston": hes, "steps": steps}
    return _json(res)


def compute_generator() -> dict:
    """BTC's daily log returns (Binance, Aug 2017 - Dec 2025) in 32-day windows: the first 80% of days train, the last
    20% are held out. Generators: i.i.d. normal and i.i.d. bootstrap (no memory), GARCH(1,1) with bootstrapped
    residuals, a signature-matching LSTM, and a small diffusion model; each scored on Part 1's stylized facts and on
    the signature distance to the held-out windows."""
    import torch

    from explainer.quant import data
    from explainer.quant.house import vol

    torch.set_num_threads(2)
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    close = np.asarray(b["close"], float)
    r = np.diff(np.log(close))
    cut = int(0.8 * len(r))
    sd = r[:cut].std()
    z = (r - r[:cut].mean()) / sd
    L = 32

    def windows(x, stride):
        return np.array([x[i:i + L] for i in range(0, len(x) - L + 1, stride)])
    train, test = windows(z[:cut], 2), windows(z[cut:], 8)
    rng = np.random.default_rng(0)
    n = 4000
    gens = {}
    gens["i.i.d. normal"] = rng.standard_normal((n, L))
    gens["i.i.d. bootstrap"] = rng.choice(z[:cut], (n, L))
    g = vol.garch_fit(z[:cut], "gjr")
    w_, a_, gm_, b_ = g["params"]
    res = z[:cut] / np.sqrt(g["h"])
    sim = np.zeros((n, L))
    hstart = rng.choice(g["h"], n)
    for i in range(n):
        h = hstart[i]
        for t in range(L):
            e = rng.choice(res) * np.sqrt(h)
            sim[i, t] = e
            h = w_ + (a_ + gm_ * (e < 0)) * e ** 2 + b_ * h
    gens["GJR-GARCH"] = sim
    t0 = time.time()
    G, curve_sig = D.train_sig_generator(train, L, iters=1500, log=lambda i, l: print("    sig", i, round(l, 4), flush=True))
    with torch.no_grad():
        gens["signature LSTM"] = G.sample(n, torch.Generator().manual_seed(3)).numpy()
    t_sig = time.time() - t0
    t0 = time.time()
    sampler, curve_dd = D.train_ddpm(train, iters=4000, log=lambda i, l: print("    ddpm", i, round(l, 4), flush=True))
    gens["diffusion"] = sampler(n, seed=4)
    t_dd = time.time() - t0
    # the signature distance reads fourth powers of returns, so a handful of explosive windows would dominate it:
    # every set is winsorized at the training data's 0.1% and 99.9% quantiles before it is compared
    lo_q, hi_q = np.quantile(z[:cut], [0.001, 0.999])

    def T_(w):
        return torch.tensor(np.clip(w, lo_q, hi_q), dtype=torch.float32)
    Ttr, Tte = T_(train), T_(test)
    scores = {"real (train)": D.stylized_facts(train), "real (held out)": D.stylized_facts(test)}
    scores["real (train)"].update(sig_train=0.0, sig_dist=D.sig_mmd(Ttr, Tte))
    scores["real (held out)"].update(sig_train=D.sig_mmd(Tte, Ttr), sig_dist=0.0)
    for k, v in gens.items():
        scores[k] = D.stylized_facts(v)
        scores[k]["sig_train"] = D.sig_mmd(T_(v), Ttr)
        scores[k]["sig_dist"] = D.sig_mmd(T_(v), Tte)
    lineup = {"real": test[rng.choice(len(test), 4, replace=False)] * sd,
              "diffusion": gens["diffusion"][:4] * sd, "signature LSTM": gens["signature LSTM"][:4] * sd,
              "GJR-GARCH": gens["GJR-GARCH"][:4] * sd}
    return _json({"scores": scores, "lineup": lineup, "daily_sd": sd, "n_train": len(train), "n_test": len(test),
                  "split_time": float(b["time"][cut + 1]), "seconds": {"sig": t_sig, "ddpm": t_dd},
                  "curves": {"sig": curve_sig[::10], "ddpm": curve_dd[::20]}})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


# ---------------------------------------------------------------------------
# The expansion: every network shown learning (checkpoints, seeds), and the experiments that close the syllabus.
# Each long item saves its finished pieces (CACHE.partial) and its trained weights under .cache/quant17/weights/.
# ---------------------------------------------------------------------------
def _threads():
    import torch

    torch.set_num_threads(1)


def _wdir():
    d = CACHE.dir / "weights"
    d.mkdir(parents=True, exist_ok=True)
    return d


HLP_SC = np.array([[1.0, 0.0], [0.1, 0.25]])


def _hlp_wrap(core):
    import torch

    def net(x):
        return core((x - torch.tensor(HLP_SC[0], dtype=torch.float32)) / torch.tensor(HLP_SC[1], dtype=torch.float32)) / 10
    return net


def _hlp_slice(net, T=0.125, xs=None):
    """Price, delta and gamma of the learned C/K at expiry T on a grid of S/K (autograd, twice)."""
    import torch

    xs = np.linspace(0.8, 1.2, 41) if xs is None else xs
    x = torch.tensor(np.c_[xs, np.full(len(xs), T)], dtype=torch.float32, requires_grad=True)
    out = net(x)
    g, = torch.autograd.grad(out.sum(), x, create_graph=True)
    gg, = torch.autograd.grad(g[:, 0].sum(), x)
    return out.detach().numpy()[:, 0], g[:, 0].detach().numpy(), gg[:, 0].numpy()


def _hlp_tracking(net, sig=0.2, n=200, keep_first=False):
    """compute_hlp's hedge test (the same 200 fresh options, rng 7): tracking errors of the net's delta and BS's."""
    import torch

    from explainer.quant.house import bs
    rng = np.random.default_rng(7)
    errs = {"net": [], "bs": []}
    first = None
    for i in range(n):
        S = 50 * np.exp(np.cumsum(np.r_[0, sig * np.sqrt(1 / 252) * rng.standard_normal(63) - 0.5 * sig ** 2 / 252]))
        K = 50.0
        T = (63 - np.arange(64)) / 252
        x = torch.tensor(np.c_[S[:-1] / K, T[:-1]], dtype=torch.float32, requires_grad=True)
        out = net(x)
        g, = torch.autograd.grad(out.sum(), x)
        d_net = g[:, 0].numpy()
        d_bs = bs.greeks(S[:-1], K, T[:-1], sig, 0.0, 0.0, 1)["delta"]
        c0_net = float(out[0, 0].detach()) * K
        c0 = float(bs.price(S[0], K, T[0], sig, 0.0, 0.0, 1))
        payoff = max(S[-1] - K, 0)
        for name, d, c in (("net", d_net, c0_net), ("bs", d_bs, c0)):
            errs[name].append(c + float(np.sum(d * np.diff(S))) - payoff)
        if i == 0 and keep_first:
            first = {"S": S, "d_net": d_net, "d_bs": d_bs, "c0_net": c0_net, "c0_bs": c0,
                     "val_net": c0_net + np.r_[0, np.cumsum(d_net * np.diff(S))],
                     "val_bs": c0 + np.r_[0, np.cumsum(d_bs * np.diff(S))],
                     "opt": np.array([bs.price(S[j], K, max(T[j], 1e-9), sig, 0, 0, 1) for j in range(64)])}
    rm = {k: float(np.sqrt(np.mean(np.square(v)))) for k, v in errs.items()}
    return rm, first


def compute_hlp_replay() -> dict:
    """HLP's network trained three times (seeds 0-2; seed 0 is the cached one), with the training curve every 5
    epochs, the learned slice at T = 0.125 every 20, the error over (S/K, T) at the end, and each seed's hedge test."""
    import torch

    from explainer.quant.house import bs
    _threads()
    tr = D.hlp_dataset(10, seed=1)
    X = (tr[:, :2] - HLP_SC[0]) / HLP_SC[1]
    part = CACHE.partial("hlp_replay", {"seeds": [0, 1, 2], "epochs": 200})
    xs = np.linspace(0.8, 1.2, 41)
    for s in (0, 1, 2):
        if str(s) in part:
            continue
        t0 = time.time()

        def snap(core):
            return _hlp_slice(_hlp_wrap(core), xs=xs)[0]
        core, curve, snaps = D.train_mlp_trace(X, tr[:, 2:] * 10, width=64, depth=3, epochs=200, seed=s, every=5,
                                               snap_every=20, snap_fn=snap)
        torch.save(core.state_dict(), _wdir() / f"hlp_s{s}.pt")
        net = _hlp_wrap(core)
        rm, first = _hlp_tracking(net, keep_first=(s == 0))
        sx, sT = np.linspace(0.8, 1.2, 31), np.linspace(5 / 252, 0.25, 21)
        GX, GT = np.meshgrid(sx, sT)
        with torch.no_grad():
            surf = net(torch.tensor(np.c_[GX.ravel(), GT.ravel()], dtype=torch.float32)).numpy()[:, 0].reshape(GX.shape)
        exact = bs.price(GX, 1.0, GT, 0.2, 0.0, 0.0, 1)
        p, d, g = _hlp_slice(net, xs=xs)
        part[str(s)] = _json({"curve": curve, "snaps": {str(k): v for k, v in snaps.items()}, "tracking": rm,
                              "first": first, "surf": surf, "surf_err": surf - exact, "seconds": time.time() - t0,
                              "slice_err_atm": float(abs(p[20] - bs.price(1.0, 1.0, 0.125, 0.2, 0, 0, 1)) * 100)})
        print(f"   hlp seed {s}: tracking {rm} ({time.time() - t0:.0f}s)", flush=True)
    sx, sT = np.linspace(0.8, 1.2, 31), np.linspace(5 / 252, 0.25, 21)
    return _json({"seeds": {s: part[s] for s in ("0", "1", "2")}, "xs": xs, "grid_x": sx, "grid_T": sT,
                  "bs_slice": bs.price(xs, 1.0, 0.125, 0.2, 0.0, 0.0, 1), "n_train": len(tr)})


def compute_greeks_act() -> dict:
    """The same HLP data fitted by three activations (SiLU, ReLU, softplus; seeds 0-1, 100 epochs each): the price,
    delta and gamma at T = 0.125 against Black-Scholes, and the butterfly test across 41 strikes at S = 1."""
    import torch
    import torch.nn as nn

    from explainer.quant.house import bs
    _threads()
    tr = D.hlp_dataset(10, seed=1)
    X = (tr[:, :2] - HLP_SC[0]) / HLP_SC[1]
    acts = {"SiLU": nn.SiLU, "ReLU": nn.ReLU, "softplus": nn.Softplus}
    part = CACHE.partial("greeks_act", {"acts": list(acts), "seeds": [0, 1], "epochs": 100})
    xs = np.linspace(0.8, 1.2, 81)
    T = 0.125
    g_bs = bs.greeks(xs, 1.0, T, 0.2, 0.0, 0.0, 1)
    p_bs = bs.price(xs, 1.0, T, 0.2, 0.0, 0.0, 1)
    Ks = np.linspace(0.8, 1.2, 41)
    for name, act in acts.items():
        for s in (0, 1):
            key = f"{name}_{s}"
            if key in part:
                continue
            t0 = time.time()
            core, curve, _ = D.train_mlp_trace(X, tr[:, 2:] * 10, width=64, depth=3, epochs=100, seed=s, act=act)
            torch.save(core.state_dict(), _wdir() / f"greeks_{key}.pt")
            net = _hlp_wrap(core)
            p, d, g = _hlp_slice(net, T, xs)
            with torch.no_grad():  # C(K) = K c(S/K) at S = 1: a butterfly's price is its second difference
                C = Ks * net(torch.tensor(np.c_[1 / Ks, np.full(41, T)], dtype=torch.float32)).numpy()[:, 0]
            fly = C[:-2] - 2 * C[1:-1] + C[2:]
            part[key] = _json({"price": p, "delta": d, "gamma": g, "fly": fly, "curve": curve,
                               "price_rmse": float(np.sqrt(np.mean((p - p_bs) ** 2))) * 100,
                               "delta_rmse": float(np.sqrt(np.mean((d - g_bs["delta"]) ** 2))),
                               "gamma_rmse": float(np.sqrt(np.mean((g - g_bs["gamma"]) ** 2))),
                               "neg_fly": float(np.mean(fly < 0)), "seconds": time.time() - t0})
            print(f"   {key}: price {part[key]['price_rmse']:.4f}% gamma {part[key]['gamma_rmse']:.3f} "
                  f"neg fly {part[key]['neg_fly']:.2f} ({time.time() - t0:.0f}s)", flush=True)
    C_bs = Ks * bs.price(1 / Ks, 1.0, T, 0.2, 0, 0, 1)
    return _json({"runs": {k: part[k] for k in part.done}, "xs": xs, "T": T, "bs": {"price": p_bs, "delta": g_bs["delta"],
                  "gamma": g_bs["gamma"], "fly": C_bs[:-2] - 2 * C_bs[1:-1] + C_bs[2:]}, "Ks": Ks})


def _held_split():
    rows = _calib_rows()
    sets = rows[:, -1].astype(int)
    return rows, sets, (sets % 20) == 0


def compute_calib_ckpt() -> dict:
    """The calibrator trained again (seed 1, the same 40 epochs), saving its state every epoch (it resumes), with the
    Surface's three smiles at the calibrated parameters as the network sees them after epochs 0, 1, 5, 10, 20, 40."""
    import torch

    _threads()
    c = load("calib")
    rows, sets, held = _held_split()
    X = D.calib_features(rows[:, :5], rows[:, 5], rows[:, 6])
    y = rows[:, 7]
    th = np.array([c["surface"]["params"][n] for n in D.CALIB_NAMES])

    def snap(net):
        net.eval()
        with torch.no_grad():
            out = [net(torch.from_numpy(D.calib_features(th, np.full(len(s["kk"]), s["T"]), np.asarray(s["kk"])))).numpy()[:, 0]
                   for s in c["slices"]]
        net.train()
        return np.array(out)
    t0 = time.time()
    net, hist, snaps = D.train_calib_net_ckpt(X[~held], y[~held], epochs=40, seed=1, val=(X[held], y[held]),
                                              ckpt=str(_wdir() / "calib_s1.ckpt"), snap_at=(0, 1, 5, 10, 20, 40),
                                              snap_fn=snap, log=lambda r: print("   ", r, flush=True))
    torch.save(net.state_dict(), _wdir() / "calib_net_s1.pt")
    seed0 = _calib_net()
    snap0 = snap(seed0)
    return _json({"history": hist, "snaps": {str(k): v for k, v in snaps.items()}, "seed0_final": snap0,
                  "seconds": time.time() - t0, "params": th})


def compute_calib_noise() -> dict:
    """The label-noise question done right: 200 held-out parameter sets simulated again with 20,000 fresh paths.
    Three RMSEs (vol points): network vs its 10k-path label, network vs the fresh simulation, label vs fresh."""
    import torch

    _threads()
    rows, sets, held = _held_split()
    net = _calib_net()
    ids = np.random.default_rng(11).choice(np.unique(sets[held]), 200, replace=False)
    part = CACHE.partial("calib_noise", {"n": 200, "paths": 20000})
    for c0 in range(0, 200, 20):
        key = str(c0)
        if key in part:
            continue
        t0 = time.time()
        out = []
        for j in ids[c0:c0 + 20]:
            r = rows[sets == j]
            th = r[0, :5].astype(float)
            fresh = _mc_iv_quotes(th, r[:, 5].astype(float), r[:, 6].astype(float), n_paths=20000, seed=5000 + int(j))
            with torch.no_grad():
                pred = net(torch.from_numpy(D.calib_features(th, r[:, 5], r[:, 6]))).numpy()[:, 0]
            ok = np.isfinite(fresh)
            out.append(np.c_[pred[ok], r[ok, 7], fresh[ok]])
        part[key] = np.vstack(out)
        print(f"   calib_noise {c0 + 20}/200 ({time.time() - t0:.0f}s)", flush=True)
    A = np.vstack([np.asarray(part[str(c)]) for c in range(0, 200, 20)]) * 100
    net_, lab, fr = A[:, 0], A[:, 1], A[:, 2]

    def stats(a, b):
        e = a - b
        return {"rmse": float(np.sqrt(np.mean(e ** 2))), "median_abs": float(np.median(np.abs(e)))}
    hist_e = {k: np.histogram(np.clip(v, -6, 6), bins=48, range=(-6, 6))[0] for k, v in
              (("net_fresh", net_ - fr), ("label_fresh", lab - fr))}
    return _json({"n_sets": 200, "n_points": int(len(A)), "net_label": stats(net_, lab), "net_fresh": stats(net_, fr),
                  "label_fresh": stats(lab, fr), "hist": hist_e, "bins": np.linspace(-6, 6, 49)})


def compute_calib_trace() -> dict:
    """calibrate_neural on the Surface again (the same 12 starts), with every start's iterates, and the network's
    implied-volatility surface on a (k, T) grid at ten iterates of the best start."""
    import torch

    _threads()
    net = _calib_net()
    Q = _surface_quotes()
    w = Q["vega"] / Q["vega"].mean()
    fit = D.calibrate_neural_trace(net, Q["T"], Q["k"], Q["iv"], w=w, starts=12)
    tr = fit["traces"][fit["best"]]
    kk = np.linspace(-0.45, 0.35, 30)
    TT = np.linspace(7 / 365, 180 / 365, 20)
    GK, GT = np.meshgrid(kk, TT)
    picks = np.unique(np.r_[0, np.round(np.geomspace(1, len(tr["step"]) - 1, 9)).astype(int)])
    surfs = []
    with torch.no_grad():
        for i in picks:
            f = net(torch.from_numpy(D.calib_features(np.array(tr["params"][i]), GT.ravel(), GK.ravel()))).numpy()[:, 0]
            surfs.append(f.reshape(GT.shape))
    return _json({"params": fit["params"], "rmse": fit["rmse"], "seconds": fit["seconds"], "traces": fit["traces"],
                  "best": fit["best"], "picks": picks, "surfs": surfs, "kk": kk, "TT": TT,
                  "quotes": {"k": Q["k"], "T": Q["T"], "iv": Q["iv"]}})


def _dml_slice_fn(mkt):
    u = np.linspace(-30, 30, 61)
    Xs = 100 + u[:, None] * np.ones((1, mkt["d"]))
    return u, Xs


def compute_dml_seeds() -> dict:
    """Differential ML's table again with two more seeds (fresh data and initialization) at n = 256, 1,024, 4,096."""
    _threads()
    mkt = D.bachelier_basket(7, seed=0)
    Xte = 100 + 1.0 * np.random.default_rng(5).standard_normal((4096, 7)) @ mkt["chol"].T
    pe, de = D.bachelier_price(mkt, Xte)
    part = CACHE.partial("dml_seeds", {"seeds": [2, 3], "n": [256, 1024, 4096]})
    for s in (2, 3):
        for n in (256, 1024, 4096):
            X, Y, dY = D.bachelier_samples(mkt, n, seed=10 * n + s)
            for use in (False, True):
                key = f"{s}_{n}_{int(use)}"
                if key in part:
                    continue
                t0 = time.time()
                f, curve, _ = D.train_differential_trace(X, Y, dY if use else None, seed=s)
                p, dd = f(Xte)
                part[key] = {"seed": s, "n": n, "differential": use, "price_rmse": float(np.sqrt(np.mean((p - pe) ** 2))),
                             "delta_rmse": float(np.sqrt(np.mean((dd - de) ** 2))), "curve": curve,
                             "seconds": time.time() - t0}
                print("   ", key, round(part[key]["price_rmse"], 3), round(part[key]["delta_rmse"], 4), flush=True)
    return _json({"rows": [part[k] for k in sorted(part.done)]})


def compute_dml_replay() -> dict:
    """The cached n = 1,024 runs (seed 1) replayed: the 1-D slice of the fit at six checkpoints, plain and
    differential, with the value loss curve."""
    _threads()
    mkt = D.bachelier_basket(7, seed=0)
    u, Xs = _dml_slice_fn(mkt)
    X, Y, dY = D.bachelier_samples(mkt, 1024, seed=1024)
    ck = (0, 5, 20, 60, 150, 390)
    out = {}
    for use in (False, True):
        _, curve, snaps = D.train_differential_trace(X, Y, dY if use else None, seed=1, snap_at=ck,
                                                     snap_fn=lambda f: f(Xs)[0])
        out["diff" if use else "plain"] = {"curve": curve, "snaps": {str(k): v for k, v in snaps.items()}}
    B = X @ mkt["w"]
    dB = dY @ np.ones(7)  # the pathwise slope along the diagonal direction (all assets move together)
    return _json({**out, "u": u, "exact": D.bachelier_price(mkt, Xs)[0], "checkpoints": ck,
                  "scatter_B": B[:300] - 100, "scatter_Y": Y[:300], "scatter_dY": dB[:300]})


def compute_dml2d() -> dict:
    """Two assets, 64 samples, three seeds: a plain network, a differential network, and a Gaussian process with
    gradient observations (the classical twin), each scored on a 41 x 41 grid against the exact Bachelier price."""
    _threads()
    mkt = D.bachelier_basket(2, seed=0)
    sd = np.sqrt(np.diag(mkt["cov"]))
    g1 = np.linspace(100 - 2.5 * sd[0], 100 + 2.5 * sd[0], 41)
    g2 = np.linspace(100 - 2.5 * sd[1], 100 + 2.5 * sd[1], 41)
    G1, G2 = np.meshgrid(g1, g2)
    Xg = np.c_[G1.ravel(), G2.ravel()]
    pe, _ = D.bachelier_price(mkt, Xg)
    out = {"g1": g1, "g2": g2, "exact": pe.reshape(41, 41), "seeds": {}}
    for s in (0, 1, 2):
        X, Y, dY = D.bachelier_samples(mkt, 64, seed=700 + s)
        res = {}
        for name, use in (("plain", False), ("diff", True)):
            f = D.train_differential(X, Y, dY if use else None, seed=s)
            p, _ = f(Xg)
            res[name] = p
        # the GP's length scale chosen on the training data alone: 4-fold cross-validation on the noisy payoffs
        noise_y = 0.5 * mkt["bvol"] ** 2 * mkt["T"]
        best = None
        for ls in (10.0, 20.0, 40.0):
            e = []
            for k in range(4):
                te = np.arange(64) % 4 == k
                m, _ = D.gp_with_gradients(X[~te], Y[~te], dY[~te], X[te], ls=ls, sf=float(np.std(Y)) * 2,
                                           noise_y=noise_y, noise_d=0.25 * 0.25)
                e.append(np.mean((m - Y[te]) ** 2))
            if best is None or np.mean(e) < best[1]:
                best = (ls, np.mean(e))
        m, sdv = D.gp_with_gradients(X, Y, dY, Xg, ls=best[0], sf=float(np.std(Y)) * 2, noise_y=noise_y,
                                     noise_d=0.25 * 0.25)
        res["gp"] = m
        row = {k: float(np.sqrt(np.mean((v - pe) ** 2))) for k, v in res.items()}
        row["gp_ls"] = best[0]
        out["seeds"][str(s)] = row
        if s == 0:
            out["surfs"] = {k: v.reshape(41, 41) for k, v in res.items()}
            out["gp_sd"] = sdv.reshape(41, 41)
            out["samples"] = {"X": X, "Y": Y, "dY": dY}
        print("   dml2d seed", s, row, flush=True)
    return _json(out)


def compute_bsde_seeds() -> dict:
    """Deep BSDE: seed 1 (2,000 iterations) with the shooting picture (terminal values against targets at five
    iterations, 32 paths of Y), the linear check (delta = 1, no default) against plain Monte Carlo, and the cached
    seed 0's tail average."""
    _threads()
    part = CACHE.partial("bsde_seeds", {"seed1": 2000, "linear": 1500})
    if "seed1" not in part:
        t0 = time.time()
        r = D.deep_bsde_snap(iters=2000, seed=1, snap_at=(0, 100, 300, 1000, 2000),
                             log=lambda c: print("    s1", c, flush=True) if c["iter"] % 250 == 0 else None)
        r["seconds"] = time.time() - t0
        part["seed1"] = _json(r)
    if "linear" not in part:
        t0 = time.time()
        r = D.deep_bsde_snap(dict(D.DEFAULT_RISK, delta=1.0), iters=1500, seed=2,
                             log=lambda c: print("    lin", c, flush=True) if c["iter"] % 250 == 0 else None)
        r["seconds"] = time.time() - t0
        part["linear"] = _json(r)
    b = load("bsde")

    def tail(curve, a, z):
        u = np.array([c["u0"] for c in curve if a <= c["iter"] <= z])
        return {"mean": float(u.mean()), "sd": float(u.std()), "n": int(len(u))}
    s1, lin = part["seed1"], part["linear"]
    return _json({"seed1": s1, "linear": lin, "tail0": tail(b["curve"], 3000, 4000), "tail1": tail(s1["curve"], 1000, 2000),
                  "tail_lin": tail(lin["curve"], 1000, 1500), "reference": b["reference"],
                  "no_default_mc": b["no_default_mc"], "no_default_se": b["no_default_se"]})


def compute_stopping_region() -> dict:
    """Deep stopping on two assets again (250 steps a date), keeping every date's exercise region on a 61 x 61 grid:
    the exercise tunnel."""
    _threads()
    p = dict(D.MAX_CALL, d=2)
    t0 = time.time()
    r = D.deep_stopping(p, steps=250, n_eval=300000, seed=1, log=lambda n, v: print("    date", n, round(v, 3), flush=True))
    grid, reg = D.stopping_regions(r["nets"], p)
    return _json({"grid": grid, "regions": {str(k): v for k, v in reg.items()}, "lower": r["lower"], "se": r["se"],
                  "curves": {str(k): v for k, v in r["curves"].items()}, "seconds": time.time() - t0, "steps": 250})


def _hold_curve(pol, Sg, tau=0.5):
    import torch

    from explainer.quant.house import bs
    h = HEDGE
    prev = torch.tensor(bs.greeks(Sg, 100, tau * h["T"], h["sigma"], 0, 0, 1)["delta"], dtype=torch.float32)
    with torch.no_grad():
        return pol(torch.log(torch.tensor(Sg / 100, dtype=torch.float32)), torch.full((len(Sg),), tau), prev).numpy()


def _save_pol(pol, name):
    import torch

    torch.save(pol.net.state_dict(), _wdir() / f"{name}.pt")


def _load_pol(kind, name, cls=None, **kw):
    import torch

    pol = cls(**kw) if cls else D.Hedger(kind)
    pol.net.load_state_dict(torch.load(_wdir() / f"{name}.pt"))
    return pol


def compute_hedge_replay() -> dict:
    """The deep hedger watched: no costs (3 seeds, 800 steps of 2,048 paths, the holding curve at 16 checkpoints,
    converging onto delta), and 0.5% costs (3 seeds, 1,500 steps, the trade map every 100 steps: the band opening)."""
    import torch

    from explainer.quant.house import bs
    _threads()
    h = HEDGE
    Sg = np.linspace(85, 115, 61)
    pg = np.linspace(0, 1, 51)
    SS, PP = np.meshgrid(Sg, pg)
    part = CACHE.partial("hedge_replay", {"nocost": [800, 2048], "cost": [1500, 2048, 0.005], "seeds": [0, 1, 2]})
    ck0 = [0, 5, 10, 20, 30, 45, 60, 80, 100, 150, 200, 300, 400, 500, 650, 800]
    for s in (0, 1, 2):
        key = f"nocost_{s}"
        if key not in part:
            t0 = time.time()
            pol, curve, snaps = D.train_hedger("mlp", 0.0, iters=800, batch=2048, seed=s, snap_at=ck0,
                                               snap_fn=lambda p: _hold_curve(p, Sg))
            _save_pol(pol, f"nocost_s{s}")
            part[key] = _json({"curve": curve, "snaps": {str(k): v for k, v in snaps.items()},
                               "eval": D.evaluate_hedger(pol, 0.0, n=100000), "seconds": time.time() - t0})
            print("   ", key, part[key]["eval"]["price"], f"{time.time() - t0:.0f}s", flush=True)
    ck1 = list(range(0, 1501, 100))
    for s in (0, 1, 2):
        key = f"cost_{s}"
        if key not in part:
            t0 = time.time()

            def snap(p):
                x = torch.log(torch.tensor(SS.ravel() / 100, dtype=torch.float32))
                new = p(x, torch.full((SS.size,), 0.5), torch.tensor(PP.ravel(), dtype=torch.float32)).numpy()
                return (new - PP.ravel()).reshape(PP.shape)
            pol, curve, snaps = D.train_hedger("mlp", 0.005, iters=1500, batch=2048, seed=s, snap_at=ck1, snap_fn=snap)
            _save_pol(pol, f"cost_s{s}")
            flat = {}
            for k, m in snaps.items():  # the do-nothing holdings at the money (|trade| < 0.02)
                z = m[:, 30]
                w = pg[np.abs(z) < 0.02]
                flat[str(k)] = [float(w.min()), float(w.max())] if len(w) else None
            part[key] = _json({"curve": curve, "maps": {str(k): v for k, v in snaps.items()} if s == 0 else {},
                               "flat": flat, "eval": D.evaluate_hedger(pol, 0.005, n=100000),
                               "seconds": time.time() - t0})
            print("   ", key, part[key]["eval"]["price"], f"{time.time() - t0:.0f}s", flush=True)
    # one path hedged live by the no-cost network (seed 0) and by delta
    pol = _load_pol("mlp", "nocost_s0")
    gen = torch.Generator().manual_seed(2024)
    S = D.gbm_torch(1, h["steps"], h["T"], h["sigma"], 100.0, gen)
    with torch.no_grad():
        _, _, hn = D.hedge_pnl(pol, S, 100.0, h["T"])
        _, _, hd = D.hedge_pnl(D.delta_hedger(h["sigma"], h["T"]), S, 100.0, h["T"])
    return _json({**{k: part[k] for k in part.done}, "S": Sg, "prev": pg, "ck_nocost": ck0, "ck_cost": ck1,
                  "bs_delta": bs.greeks(Sg, 100, 0.5 * h["T"], h["sigma"], 0, 0, 1)["delta"],
                  "live": {"S": S[0].numpy(), "net": hn[0].numpy(), "delta": hd[0].numpy()}})


def compute_risk_measures() -> dict:
    """The band network at 0.5% costs trained under two risk measures (entropic; CVaR 50% in Rockafellar-Uryasev
    form, its threshold trained alongside), 3 seeds each: tails, bands, and the threshold against the empirical VaR."""
    import torch

    _threads()
    h = HEDGE
    cost = 0.005
    part = CACHE.partial("risk_measures", {"iters": 1000, "batch": 4096, "seeds": [0, 1, 2]})
    bins = np.linspace(-9, 3, 61)
    for risk in ("entropic", "cvar_ru"):
        for s in (0, 1, 2):
            key = f"{risk}_{s}"
            if key in part:
                continue
            t0 = time.time()
            pol = D.Hedger("band", seed=s)
            curve, _, w = D.train_hedger_on(lambda b, g: D.gbm_torch(b, h["steps"], h["T"], h["sigma"], h["K"], g), pol,
                                            cost, risk=risk, iters=1000, batch=4096, seed=s)
            _save_pol(pol, f"risk_{key}")
            gen = torch.Generator().manual_seed(99)
            with torch.no_grad():
                S = D.gbm_torch(200000, h["steps"], h["T"], h["sigma"], h["K"], gen)
                X, c, _ = D.hedge_pnl(pol, S, h["K"], h["T"], cost)
                lo, hi = pol.band(torch.zeros(1), torch.full((1,), 0.5))
            Xn = X.numpy()
            part[key] = _json({"curve": curve[::10], "w": w, "var50": float(np.quantile(-Xn, 0.5)),
                               "price": float(D.entropic(X)), "cvar50": float(D.cvar(X, 0.5)), "cvar05": float(D.cvar(X, 0.05)),
                               "sd": float(Xn.std()), "mean": float(Xn.mean()), "cost": float(c.mean()),
                               "band_atm": [float(lo), float(hi)], "hist": np.histogram(np.clip(Xn, -9, 3), bins)[0],
                               "seconds": time.time() - t0})
            print("   ", key, {k: round(v, 3) for k, v in part[key].items() if isinstance(v, float)}, flush=True)
    return _json({"runs": {k: part[k] for k in part.done}, "bins": bins, "cost": cost})


def compute_drift() -> dict:
    """The drift trap: the no-cost hedger trained on paths drifting at 30% a year (3 seeds), against the driftless
    hedgers of hedge_replay: its holding sits above delta by Merton's mu / (gamma sigma^2 S); priced on drifted and on
    driftless paths."""
    import torch

    from explainer.quant.house import bs
    _threads()
    hr = load("hedge_replay")
    h = HEDGE
    mu = 0.3
    Sg = np.linspace(85, 115, 61)
    ck = [0, 20, 50, 100, 200, 400, 800]
    part = CACHE.partial("drift", {"mu": mu, "iters": 800, "batch": 2048, "seeds": [0, 1, 2]})
    for s in (0, 1, 2):
        key = str(s)
        if key in part:
            continue
        t0 = time.time()
        pol, curve, snaps = D.train_hedger_p("mlp", mu=mu, iters=800, batch=2048, seed=s, snap_at=ck,
                                             snap_fn=lambda p: _hold_curve(p, Sg))
        _save_pol(pol, f"drift_s{s}")
        part[key] = _json({"curve": curve, "snaps": {str(k): v for k, v in snaps.items()}, "seconds": time.time() - t0})
        print("   drift seed", s, f"{time.time() - t0:.0f}s", flush=True)

    def price_on(pol, m, n=100000):
        gen = torch.Generator().manual_seed(77)
        with torch.no_grad():
            S = D.gbm_torch_mu(n, h["steps"], h["T"], h["sigma"], m, h["K"], gen)
            X, _, _ = D.hedge_pnl(pol, S, h["K"], h["T"], 0.0)
        return {"price": float(D.entropic(X)), "mean": float(X.mean()), "sd": float(X.std())}
    bsd = bs.greeks(Sg, 100, 0.5 * h["T"], h["sigma"], 0, 0, 1)["delta"]
    merton = D.merton_hedge(Sg, h["sigma"], mu, h["gamma"])
    m = (Sg >= 90) & (Sg <= 110)
    rows = []
    for s in (0, 1, 2):
        pd_ = _load_pol("mlp", f"drift_s{s}")
        p0 = _load_pol("mlp", f"nocost_s{s}")
        hold = _hold_curve(pd_, Sg)
        rows.append({"seed": s, "hold": hold, "dev": float(np.mean((hold - bsd)[m])),
                     "drifted_on_P": price_on(pd_, mu), "drifted_on_Q": price_on(pd_, 0.0),
                     "plain_on_P": price_on(p0, mu), "plain_on_Q": price_on(p0, 0.0)})
        print("   ", {k: v for k, v in rows[-1].items() if k != "hold"}, flush=True)
    return _json({"mu": mu, "S": Sg, "bs_delta": bsd, "merton": bsd + merton, "merton_atm": float(D.merton_hedge(100, h["sigma"], mu)),
                  "runs": {k: part[k] for k in part.done}, "rows": rows, "ck": ck,
                  "nocost_curves": [hr[f"nocost_{s}"]["curve"] for s in range(3)]})


def compute_leland() -> dict:
    """Leland's hedge (delta at an inflated volatility) by cost, on compute_hedge's paths (200,000, seed 99), next
    to the cached daily delta, Whalley-Wilmott and band network."""
    from explainer.quant.house import bs
    _threads()
    h = HEDGE
    rows = []
    for r in load("hedge")["band"]["rows"]:
        c = r["cost"]
        if c == 0:
            continue
        sl = D.leland_sigma(h["sigma"], c, h["T"] / h["steps"])
        e = D.evaluate_hedger(D.delta_hedger(sl, h["T"]), c)
        rows.append({"cost": c, "sigma_leland": sl, "leland": e, "delta": r["delta"], "ww": r["ww"], "deep": r["deep"],
                     "bs_at_leland": float(bs.price(100, 100, h["T"], sl, 0, 0, 1))})
        print("   leland", c, round(sl, 4), round(e["price"], 3), flush=True)
    return _json({"rows": rows, "sigma_sqrt_dt": h["sigma"] * np.sqrt(h["T"] / h["steps"])})


def compute_hedge_seeds() -> dict:
    """The band network at 0.1%, 0.5% and 1% costs, seeds 3 and 4 (the cached run is seed 2), the policies saved:
    prices on the cached paths, the band at the money, and seed 3's band surface at 0.5% over (time, price)."""
    import torch

    from explainer.quant.house import quoting
    _threads()
    h = HEDGE
    part = CACHE.partial("hedge_seeds", {"iters": 1200, "batch": 4096, "seeds": [3, 4], "costs": [0.001, 0.005, 0.01]})
    Sg = np.linspace(85, 115, 61)
    for c in (0.001, 0.005, 0.01):
        for s in (3, 4):
            key = f"{c}_{s}"
            if key in part:
                continue
            t0 = time.time()
            pol, curve, _ = D.train_hedger("band", cost=c, iters=1200, batch=4096, seed=s)
            _save_pol(pol, f"band_{c}_s{s}")
            with torch.no_grad():
                lo, hi = pol.band(torch.zeros(1), torch.full((1,), 0.5))
            part[key] = _json({"eval": D.evaluate_hedger(pol, c), "band_atm": [float(lo), float(hi)],
                               "curve": curve[::10], "seconds": time.time() - t0})
            print("   band", key, round(part[key]["eval"]["price"], 3), f"{time.time() - t0:.0f}s", flush=True)
    pol = _load_pol("band", "band_0.005_s3")
    ts = np.linspace(0.05, 1.0, 20)
    lo, hi = np.zeros((20, 61)), np.zeros((20, 61))
    with torch.no_grad():
        x = torch.log(torch.tensor(Sg / 100, dtype=torch.float32))
        for i, tt in enumerate(ts):
            a, b = pol.band(x, torch.full((61,), float(tt)))
            lo[i], hi[i] = a.numpy(), b.numpy()
    ww = {str(c): quoting.ww_band(100.0, 100, 0.5 * h["T"], h["sigma"], c, gamma_risk=h["gamma"])["half_width"]
          for c in (0.001, 0.005, 0.01)}
    return _json({"runs": {k: part[k] for k in part.done}, "surface": {"tau": ts, "S": Sg, "lo": lo, "hi": hi},
                  "ww_half_atm": ww})


def compute_hedge_live() -> dict:
    """One path, hedged live by the band network (seed 3, 0.5%) and by daily delta: holdings, band edges, costs."""
    import torch

    _threads()
    load("hedge_seeds")
    h = HEDGE
    pol = _load_pol("band", "band_0.005_s3")
    gen = torch.Generator().manual_seed(31)
    S = D.gbm_torch(1, h["steps"], h["T"], h["sigma"], 100.0, gen)
    c = 0.005
    with torch.no_grad():
        _, cb, hb = D.hedge_pnl(pol, S, 100.0, h["T"], c)
        _, cd, hd = D.hedge_pnl(D.delta_hedger(h["sigma"], h["T"]), S, 100.0, h["T"], c)
        tau = torch.tensor([(h["T"] - k * h["T"] / h["steps"]) / h["T"] for k in range(h["steps"])], dtype=torch.float32)
        lo, hi = pol.band(torch.log(S[0, :-1] / 100), tau)
    hb, hd = hb[0].numpy(), hd[0].numpy()
    Sx = S[0].numpy()
    cum = lambda hh: np.cumsum(c * np.abs(np.diff(np.r_[0, hh])) * Sx[:-1])  # noqa: E731
    return _json({"S": Sx, "band": hb, "delta": hd, "lo": lo.numpy(), "hi": hi.numpy(), "cost_band": cum(hb),
                  "cost_delta": cum(hd), "trades_band": int(np.sum(np.abs(np.diff(np.r_[0, hb])) > 1e-6)),
                  "trades_delta": int(np.sum(np.abs(np.diff(np.r_[0, hd])) > 1e-6))})


def compute_band_prior() -> dict:
    """Arzel and Lehdili's prior: the band network started at Whalley-Wilmott's band against the default narrow
    start, 0.5% costs, 2 seeds each, 600 steps: the loss curves and the prices reached."""
    _threads()
    h = HEDGE
    c = 0.005
    part = CACHE.partial("band_prior", {"iters": 600, "batch": 4096, "seeds": [0, 1]})
    for name in ("default", "ww"):
        for s in (0, 1):
            key = f"{name}_{s}"
            if key in part:
                continue
            t0 = time.time()
            pol = D.WWBandHedger(c, seed=s) if name == "ww" else D.Hedger("band", seed=s)
            curve, _, _ = D.train_hedger_on(lambda b, g: D.gbm_torch(b, h["steps"], h["T"], h["sigma"], h["K"], g),
                                            pol, c, iters=600, batch=4096, seed=s)
            _save_pol(pol, f"prior_{key}")
            part[key] = _json({"curve": curve, "eval": D.evaluate_hedger(pol, c, n=100000), "seconds": time.time() - t0})
            print("   prior", key, round(part[key]["eval"]["price"], 3), f"{time.time() - t0:.0f}s", flush=True)
    return _json({"runs": {k: part[k] for k in part.done}})


def compute_nsde_trace() -> dict:
    """compute_nsde's run again (seed 0), traced: the 36 model implied vols every 20 calibration steps, and the push's
    (vanilla error, barrier price) every 10 steps for both sides, plus a few sample paths of the low and high models."""
    import torch

    from explainer.quant.house import bs, stochvol as sv
    _threads()
    hes = (0.04, 1.5, 0.04, 0.5, -0.7)
    mats = [0.25, 0.5, 0.75, 1.0]
    strikes = np.round(np.linspace(0.8, 1.2, 9), 3)
    cf = lambda u, TT: sv.heston_cf(u, TT, *hes)  # noqa: E731
    target = np.array([sv.cos_price(cf, 1.0, strikes, T, 1, N=1024) for T in mats])
    tgt = torch.tensor(target, dtype=torch.float32)
    steps, T = 50, 1.0
    gen = torch.Generator().manual_seed(0)

    def calib_loss(m, n=16384):
        S = m.paths(n, T, steps, gen)
        return ((D.nsde_prices(S, mats, strikes, steps, T) - tgt) * 100).pow(2).mean(), S

    def iv_of(P):
        return np.array([[bs.implied_vol(float(P[i, j]), 1.0, strikes[j], mats[i], 0, 0, 1) for j in range(9)]
                         for i in range(4)])

    def ivs(m):
        g2 = torch.Generator().manual_seed(123)
        with torch.no_grad():
            S = m.paths(200000, T, steps, g2)
            P = D.nsde_prices(S, mats, strikes, steps, T).numpy()
            doc = float(D.down_out_call(S))
        return iv_of(P), doc
    tiv = iv_of(target)
    part = CACHE.partial("nsde_trace", {"seed": 0})
    if "calib" not in part:
        m = D.NeuralSV(seed=0)
        opt = torch.optim.Adam(m.parameters(), lr=3e-3)
        tr = {"step": [], "loss": [], "iv": []}
        for it in range(800):
            loss, S = calib_loss(m)
            if it % 20 == 0 or it == 799:
                with torch.no_grad():
                    tr["step"].append(it)
                    tr["loss"].append(float(loss))
                    tr["iv"].append(iv_of(D.nsde_prices(S, mats, strikes, steps, T).numpy()))
            opt.zero_grad()
            loss.backward()
            opt.step()
            if it % 100 == 0:
                print("    calib", it, float(loss.detach()), flush=True)
        torch.save({"sd": m.state_dict(), "gen": gen.get_state()}, _wdir() / "nsde_base.pt")
        part["calib"] = _json(tr)
    st = torch.load(_wdir() / "nsde_base.pt", weights_only=False)
    base = st["sd"]
    gen.set_state(st["gen"])
    m = D.NeuralSV(seed=0)
    m.load(base)
    base_cl = float(calib_loss(m)[0].detach())
    iv0, doc0 = ivs(m)
    for side, sgn in (("low", 1.0), ("high", -1.0)):
        if side in part:
            continue
        mm = D.NeuralSV(seed=0)
        mm.load(base)
        opt = torch.optim.Adam(mm.parameters(), lr=5e-4)
        best = None
        tr = {"step": [], "cl": [], "doc": [], "ok": []}
        for it in range(600):
            cl, S = calib_loss(mm)
            doc_ = D.down_out_call(S)
            loss = sgn * doc_ * 100 + 50.0 * cl
            if not torch.isfinite(loss):
                mm.load(best[1] if best else base)
                continue
            ok = float(cl) <= max(3 * base_cl, 0.004)
            if ok and (best is None or sgn * float(doc_) < sgn * best[0]):
                best = (float(doc_), mm.state_dict())
            if it % 10 == 0:
                tr["step"].append(it)
                tr["cl"].append(float(cl))
                tr["doc"].append(float(doc_))
                tr["ok"].append(int(ok))
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(mm.parameters(), 1.0)
            opt.step()
        if best is not None:
            mm.load(best[1])
        iv, doc = ivs(mm)
        with torch.no_grad():
            P = torch.exp(mm.paths(400, T, steps, torch.Generator().manual_seed(8)))
        knocked = float((P.min(1).values <= 0.8).float().mean())
        part[side] = _json({"trace": tr, "iv": iv, "doc": doc, "iv_rmse": float(np.sqrt(np.mean((iv - tiv) ** 2)) * 100),
                            "paths": P[:12].numpy(), "knocked": knocked, "best": best[0] if best else None})
        print("   ", side, doc, part[side]["iv_rmse"], flush=True)
    return _json({"calib": part["calib"], "low": part["low"], "high": part["high"], "target_iv": tiv,
                  "calibrated": {"iv": iv0, "doc": doc0, "iv_rmse": float(np.sqrt(np.mean((iv0 - tiv) ** 2)) * 100)},
                  "base_cl": base_cl, "ceiling": max(3 * base_cl, 0.004),
                  "setup": {"mats": mats, "strikes": strikes, "barrier": 0.8}})


def _btc():
    """compute_generator's data: BTC daily log returns standardized on the first 80%, and its 32-day windows."""
    from explainer.quant import data

    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    close = np.asarray(b["close"], float)
    r = np.diff(np.log(close))
    cut = int(0.8 * len(r))
    sd = r[:cut].std()
    z = (r - r[:cut].mean()) / sd
    L = 32

    def windows(x, stride, L=L):
        return np.array([x[i:i + L] for i in range(0, len(x) - L + 1, stride)])
    return {"z": z, "cut": cut, "sd": sd, "train": windows(z[:cut], 2), "test": windows(z[cut:], 8), "windows": windows}


def compute_ddpm_reverse() -> dict:
    """The diffusion generator trained three times (seed 0 reproduces the cached one), its reverse process kept at
    seven steps for 24 windows, and the forward process on one real window."""
    import torch

    _threads()
    B = _btc()
    train, test = B["train"], B["test"]
    lo_q, hi_q = np.quantile(B["z"][:B["cut"]], [0.001, 0.999])
    Tte = torch.tensor(np.clip(test, lo_q, hi_q), dtype=torch.float32)
    ts = (200, 150, 100, 60, 30, 10, 0)
    part = CACHE.partial("ddpm_reverse", {"seeds": [0, 1, 2], "iters": 4000})
    for s in (0, 1, 2):
        if str(s) in part:
            continue
        t0 = time.time()
        sample, curve, abar = D.train_ddpm_snap(train, iters=4000, seed=s)
        x, snaps = sample(4000, seed=4, snap_at=ts)
        sf = D.stylized_facts(x)
        res = {"curve": curve[::20], "kurtosis": sf["kurtosis"], "acf_abs_mean": sf["acf_abs_mean"],
               "leverage": sf["leverage"], "sig_dist": D.sig_mmd(torch.tensor(np.clip(x, lo_q, hi_q), dtype=torch.float32), Tte),
               "seconds": time.time() - t0}
        if s == 0:
            res["snaps"] = {str(k): v[:24] for k, v in snaps.items()}
            x0 = test[3]
            eps = np.random.default_rng(1).standard_normal(len(x0))
            res["forward"] = {str(t): (np.sqrt(abar[t - 1]) * x0 + np.sqrt(1 - abar[t - 1]) * eps) if t > 0 else x0
                              for t in ts}
        part[str(s)] = _json(res)
        print("   ddpm seed", s, round(sf["kurtosis"], 2), f"{time.time() - t0:.0f}s", flush=True)
    return _json({"seeds": {k: part[k] for k in ("0", "1", "2")}, "ts": ts, "daily_sd": B["sd"],
                  "real_kurtosis_test": D.stylized_facts(test)["kurtosis"],
                  "real_kurtosis_train": D.stylized_facts(train)["kurtosis"]})


def compute_crossgen() -> dict:
    """Rule 17 tested: band hedgers (0.5% costs) trained on GBM (hedge_seeds, seed 3) and on GJR-GARCH paths fitted
    to BTC (rescaled to 20% a year), with daily delta and Whalley-Wilmott, each priced on GBM paths, GARCH paths and
    real BTC 30-day windows (2017-2025, rescaled alike): indifference prices in a 3 x 4 table."""
    import torch

    from explainer.quant.house import vol
    _threads()
    load("hedge_seeds")
    h = HEDGE
    c = 0.005
    B = _btc()
    z, cut = B["z"], B["cut"]
    g = vol.garch_fit(z[:cut], "gjr")
    res = z[:cut] / np.sqrt(g["h"])
    res = (res - res.mean()) / res.std()
    scale = h["sigma"] * np.sqrt(h["T"] / h["steps"])
    hstart = np.asarray(g["h"], float)

    def garch(n, gen):
        idx = torch.randint(len(hstart), (n,), generator=gen)
        S, _ = D.garch_paths_torch(g["params"], res, n, h["steps"], scale=scale, S0=h["K"],
                                   h0=torch.as_tensor(hstart, dtype=torch.float32)[idx], gen=gen)
        return S
    part = CACHE.partial("crossgen", {"iters": 1200, "batch": 4096, "seed": 3})
    if "garch_trained" not in part:
        t0 = time.time()
        pol = D.Hedger("band", seed=3)
        curve, _, _ = D.train_hedger_on(garch, pol, c, iters=1200, batch=4096, seed=3)
        _save_pol(pol, "band_garch_s3")
        part["garch_trained"] = {"curve": curve[::10], "seconds": time.time() - t0}
    W = B["windows"](z, 3, L=h["steps"])
    real = torch.tensor(h["K"] * np.exp(np.c_[np.zeros(len(W)), np.cumsum(scale * W - 0.5 * scale ** 2, 1)]),
                        dtype=torch.float32)
    tests = {"GBM": D.gbm_torch(100000, h["steps"], h["T"], h["sigma"], h["K"], torch.Generator().manual_seed(99)),
             "GJR-GARCH": garch(100000, torch.Generator().manual_seed(98)), "BTC history": real}
    hedgers = {"delta daily": D.delta_hedger(h["sigma"], h["T"]),
               "Whalley--Wilmott": D.delta_hedger(h["sigma"], h["T"], band=(c, h["gamma"])),
               "net (GBM-trained)": _load_pol("band", "band_0.005_s3"),
               "net (GARCH-trained)": _load_pol("band", "band_garch_s3")}
    table = {}
    for tn, S in tests.items():
        table[tn] = {}
        for hn, pol in hedgers.items():
            with torch.no_grad():
                X, cc, _ = D.hedge_pnl(pol, S, h["K"], h["T"], c)
            table[tn][hn] = {"price": float(D.entropic(X)), "cvar50": float(D.cvar(X, 0.5)), "sd": float(X.std()),
                             "cost": float(cc.mean())}
        print("   ", tn, {k: round(v["price"], 3) for k, v in table[tn].items()}, flush=True)
    return _json({"table": table, "garch": {"params": g["params"]}, "n_real": int(len(W)),
                  "train": part["garch_trained"], "tests": list(tests), "hedgers": list(hedgers)})


ITEMS = {"calib_data": compute_calib_data, "calib": compute_calib, "calib_hist": compute_calib_hist, "hlp": compute_hlp,
         "dml": compute_dml, "bsde": compute_bsde, "stopping": compute_stopping, "hedge": compute_hedge,
         "nsde": compute_nsde, "generator": compute_generator, "envelope": compute_envelope,
         # the expansion (cheapest and most needed first)
         "hlp_replay": compute_hlp_replay, "greeks_act": compute_greeks_act, "calib_trace": compute_calib_trace,
         "calib_noise": compute_calib_noise, "dml_replay": compute_dml_replay, "dml_seeds": compute_dml_seeds,
         "dml2d": compute_dml2d, "leland": compute_leland, "hedge_replay": compute_hedge_replay,
         "drift": compute_drift, "risk_measures": compute_risk_measures, "hedge_seeds": compute_hedge_seeds,
         "hedge_live": compute_hedge_live, "band_prior": compute_band_prior, "ddpm_reverse": compute_ddpm_reverse,
         "crossgen": compute_crossgen, "stopping_region": compute_stopping_region, "bsde_seeds": compute_bsde_seeds,
         "nsde_trace": compute_nsde_trace, "calib_ckpt": compute_calib_ckpt}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
