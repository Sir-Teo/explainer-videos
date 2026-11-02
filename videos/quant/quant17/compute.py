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
    w = np.sqrt(Q["vega"] / Q["vega"].mean())
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
        w = np.sqrt(Q["vega"] / Q["vega"].mean())
        f = D.calibrate_neural(net, Q["T"], Q["k"], Q["iv"], w=w, starts=4, iters=150)
        out.append({"day": r["day"], **f["params"], "rmse": f["rmse"], "heston_rmse": r["rmse"],
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
    pol, curve, _ = D.train_hedger("mlp", cost=0.0, iters=1200, batch=4096, seed=0,
                                   log=lambda i, l: print("    nocost", i, round(l, 4), flush=True))
    ev = D.evaluate_hedger(pol, 0.0)
    bsd = D.evaluate_hedger(D.delta_hedger(h["sigma"], h["T"]), 0.0)
    Sg = np.linspace(85, 115, 61)
    tau = 0.5
    with torch.no_grad():
        prev = torch.tensor(bs.greeks(Sg, 100, tau * h["T"], h["sigma"], 0, 0, 1)["delta"], dtype=torch.float32)
        learned = pol(torch.log(torch.tensor(Sg / 100, dtype=torch.float32)), torch.full((61,), tau), prev).numpy()
    out["nocost"] = {"curve": curve[::10], "eval": ev, "bs_eval": bsd, "bs_price": float(bs.price(100, 100, h["T"], h["sigma"], 0, 0, 1)),
                     "S": Sg, "learned": learned, "bs_delta": prev.numpy()}
    # 2. costs 0.5%: the plain network, with snapshots of its trade map at 15 days to expiry
    pg = np.linspace(0, 1, 51)
    SS, PP = np.meshgrid(Sg, pg)

    def snap(p):
        x = torch.log(torch.tensor(SS.ravel() / 100, dtype=torch.float32))
        new = p(x, torch.full((SS.size,), tau), torch.tensor(PP.ravel(), dtype=torch.float32)).numpy()
        return (new - PP.ravel()).reshape(PP.shape)
    cost = 0.005
    pol2, curve2, snaps = D.train_hedger("mlp", cost=cost, iters=1500, batch=4096, seed=1,
                                         snap_at=(0, 50, 150, 400, 1500), snap_fn=snap,
                                         log=lambda i, l: print("    mlp cost", i, round(l, 4), flush=True))
    ww = quoting.ww_band(Sg, 100, tau * h["T"], h["sigma"], cost, gamma_risk=h["gamma"])
    out["mlp_cost"] = {"cost": cost, "curve": curve2[::10], "snaps": {str(k): v for k, v in snaps.items()}, "S": Sg,
                       "prev": pg, "ww_lo": ww["lo"], "ww_hi": ww["hi"], "delta": ww["delta"], "eval": D.evaluate_hedger(pol2, cost)}
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
                    o = polb.net(torch.stack([x, torch.full((61,), float(tt))], -1))
                    lo[i] = o[:, 0].numpy()
                    hi[i] = (o[:, 0] + torch.nn.functional.softplus(o[:, 1])).numpy()
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
    for side, sgn in (("low", 1.0), ("high", -1.0)):
        mm = D.NeuralSV(seed=0)
        mm.load(base)
        opt = torch.optim.Adam(mm.parameters(), lr=1e-3)
        for it in range(500):
            cl, S = calib_loss(mm)
            loss = sgn * D.down_out_call(S) * 100 + 20.0 * cl
            opt.zero_grad()
            loss.backward()
            opt.step()
            if it % 100 == 0:
                print("    ", side, it, float(cl.detach()), float(D.down_out_call(S).detach()), flush=True)
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
    Tt = torch.tensor(test, dtype=torch.float32)
    scores = {"real (train)": D.stylized_facts(train), "real (held out)": D.stylized_facts(test)}
    scores["real (train)"]["sig_dist"] = D.sig_mmd(torch.tensor(train, dtype=torch.float32), Tt)
    scores["real (held out)"]["sig_dist"] = 0.0
    for k, v in gens.items():
        scores[k] = D.stylized_facts(v)
        scores[k]["sig_dist"] = D.sig_mmd(torch.tensor(v, dtype=torch.float32), Tt)
    lineup = {"real": test[rng.choice(len(test), 4, replace=False)] * sd,
              "diffusion": gens["diffusion"][:4] * sd, "signature LSTM": gens["signature LSTM"][:4] * sd,
              "GJR-GARCH": gens["GJR-GARCH"][:4] * sd}
    return _json({"scores": scores, "lineup": lineup, "daily_sd": sd, "n_train": len(train), "n_test": len(test),
                  "split_time": float(b["time"][cut + 1]), "seconds": {"sig": t_sig, "ddpm": t_dd},
                  "curves": {"sig": curve_sig[::10], "ddpm": curve_dd[::20]}})


def compute_envelope() -> dict:
    return {"trials": pit.trials_so_far(), "registered": {}}


ITEMS = {"calib_data": compute_calib_data, "calib": compute_calib, "calib_hist": compute_calib_hist, "hlp": compute_hlp,
         "dml": compute_dml, "bsde": compute_bsde, "stopping": compute_stopping, "hedge": compute_hedge,
         "nsde": compute_nsde, "generator": compute_generator, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
