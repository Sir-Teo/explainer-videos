"""Precompute every number in Part 55 of *Economics, Built* ("Identifying Macro").

    python -m videos.economics.econ55.compute            # everything missing (about eight minutes)
    python -m videos.economics.econ55.compute --force puzzle

Results are cached in ``.cache/econ55/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
macro-econometrics (``agora.macrometrics``) with the Island's Part 55 truths, Part 31's monetary history
(``agora.cb``) and Part 32's regions (``agora.fiscal``).  Data, via FRED: industrial production, the CPI, the federal
funds rate and the producer price index for all commodities (the hook's vector autoregressions), and the 10-year and
3-month Treasury yields with the NBER's recession months (the intermission).

Items:
    puzzle      Sims's price puzzle on American data, 1965-1995: a recursive VAR with and without commodity prices,
                with bootstrap bands
    rotations   one Island history and three impact matrices that fit it equally well
    playit      the true responses to the Island's three shocks, for the Play it
    schemes     every identification scheme on one Island history, against the truth
    schemes_mc  the point-identified schemes on many histories
    lpvar       local projections against VARs with too few and enough lags
    instruments Part 31's identification Monte Carlo, re-run: the price puzzle and its cures on the Island
    dsge        the small New Keynesian model estimated by Metropolis-Hastings, with all three series observed
    dsge_weak   the same with the rate left out: priors against posteriors
    profile     the likelihood profile of sigma, with and without the rate observed
    irfmatch    impulse-response matching
    regions     a currency union's regions: the relative multiplier and the missing intercept
    forecasts   two forecasts at the turns, against what happened: the professional forecasters' August 2008 forecast
                for 2009 (Part 1) and the Federal Reserve's June 2021 projection for 2022's inflation (Part 28)
    film        the intermission's data film: the yield curve's slope, 1953-2026, with recessions
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import cb, fiscal
from explainer.economics.agora import macrometrics as MM

CACHE = Cache("econ55")
load = CACHE.load
TRUTH = island.truths(55)
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _series(name: str) -> dict:
    d = data.fred(name)
    return {k: v for k, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


# ---------------------------------------------------------------------------------------------------------------
# the hook: Sims's price puzzle on American data


def compute_puzzle() -> dict:
    """Monthly VARs with 12 lags, 1965-1995: 100 x log industrial production, 100 x log CPI, (100 x log producer
    prices of all commodities,) and the federal funds rate, ordered so, with the funds rate last. Responses to a
    one-point funds-rate shock over 48 months, with residual-bootstrap 16-84% bands."""
    ip, cpi, ff, ppi = (_series(s) for s in ("INDPRO", "CPIAUCSL", "FEDFUNDS", "PPIACO"))
    dates = [d for d in sorted(ff) if "1965-01" <= d[:7] <= "1995-12" and d in ip and d in cpi and d in ppi]
    cols = {"ip": [100 * np.log(ip[d]) for d in dates], "cpi": [100 * np.log(cpi[d]) for d in dates],
            "ppi": [100 * np.log(ppi[d]) for d in dates], "ff": [ff[d] for d in dates]}
    out = {"first": dates[0], "last": dates[-1], "n": len(dates), "h": 48}
    for name, keys in (("plain", ("ip", "cpi", "ff")), ("commod", ("ip", "cpi", "ppi", "ff"))):
        X = np.column_stack([cols[k] for k in keys])
        k = keys.index("ff")
        b = MM.bootstrap_irf(X, 12, k, 48, reps=300, seed=55)
        res = {}
        for v in ("ip", "cpi"):
            j = keys.index(v)
            res[v] = {q: b[q][:, j].tolist() for q in ("point", "lo", "hi")}
        res["ff"] = b["point"][:, k].tolist()
        out[name] = res
    cp = np.array(out["plain"]["cpi"]["point"])
    out["peak_rise"] = float(cp.max())
    out["peak_month"] = int(cp.argmax())
    out["months_above_zero"] = int((cp > 0).sum())
    cc = np.array(out["commod"]["cpi"]["point"])
    out["commod_48"] = float(cc[-1])
    out["commod_cross"] = int(np.argmax((cc < 0) & (np.arange(len(cc)) > 0)))
    return out


# ---------------------------------------------------------------------------------------------------------------
# what a VAR identifies


def island_history() -> dict:
    S = TRUTH["svar"]
    return MM.svar_simulate(S["T"], S["seed"])


def compute_rotations() -> dict:
    """The reduced-form VAR fits the Island's history; any impact matrix B = chol(Sigma) Q with Q orthonormal
    reproduces the same Sigma. Three rotations of the last two Cholesky columns, each read as 'the monetary shock'
    (scaled to a one-point rise in the rate)."""
    S = TRUTH["svar"]
    H = island_history()
    fit = MM.var_fit(H["X"], S["p"])
    L = np.linalg.cholesky(fit["Sigma"])
    out = []
    for deg in (0.0, 40.0, -40.0):
        a = np.radians(deg)
        Q = np.eye(3)
        Q[1:, 1:] = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
        B = L @ Q
        r = MM.irf_from_impact(fit, B[:, 2], S["h"])
        r = r / r[0, 2]
        out.append({"deg": deg, "y": np.cumsum(r[:, 0]).tolist(), "pi": r[:, 1].tolist(), "i": r[:, 2].tolist(),
                    "BBt_err": float(np.abs(B @ B.T - fit["Sigma"]).max())})
    return {"rotations": out, "Sigma": fit["Sigma"].tolist(), "T": S["T"], "p": S["p"],
            "truth": MM.svar_true_irf(S["h"])["monetary"]}


def compute_playit() -> dict:
    tr = MM.svar_true_irf(12)
    # the panels in the order shown: demand, monetary, supply
    order = ["demand", "monetary", "supply"]
    return {"order": order, "panels": [tr[k] for k in order], "answer": order.index("monetary")}


# ---------------------------------------------------------------------------------------------------------------
# five schemes on the Island


def compute_schemes() -> dict:
    S = TRUTH["svar"]
    return MM.schemes_one(S["T"], S["seed"], S["p"], S["h"])


def compute_schemes_mc() -> dict:
    S = TRUTH["svar"]
    return MM.schemes_mc(S["reps"], S["T"], S["p"], S["h"], seed=1000)


def compute_lpvar() -> dict:
    L = TRUTH["lp"]
    return MM.lp_var_mc(L["reps"], L["T"], TRUTH["svar"]["h"], L["seed"])


def compute_instruments() -> dict:
    return cb.identification_mc(reps=200, T=240, h=16, seed=0)


# ---------------------------------------------------------------------------------------------------------------
# a DSGE model estimated


def nk_data() -> dict:
    N = TRUTH["nk"]
    return MM.nk_simulate(T=N["T"], seed=N["seed"])


def _posterior(obs) -> dict:
    N = TRUTH["nk"]
    D = nk_data()
    r = MM.nk_mh(D["Y"], draws=N["draws"], burn=N["burn"], seed=1, obs=obs)
    ch = r["chain"]
    out = {"names": r["names"], "truth": r["truth"], "accept": r["accept"], "mode": r["mode"], "params": {}}
    for j, n in enumerate(r["names"]):
        pr = MM.prior_draws(n, 40000, seed=j)
        lo = min(np.percentile(pr, 0.5), ch[:, j].min())
        hi = max(np.percentile(pr, 99.5), ch[:, j].max())
        edges = np.linspace(lo, hi, 41)
        hp = np.histogram(pr, edges, density=True)[0]
        hc = np.histogram(ch[:, j], edges, density=True)[0]
        out["params"][n] = {"edges": edges.tolist(), "prior": hp.tolist(), "post": hc.tolist(),
                            "post_mean": float(ch[:, j].mean()), "post_sd": float(ch[:, j].std()),
                            "prior_mean": float(pr.mean()), "prior_sd": float(pr.std()),
                            "ratio": float(ch[:, j].std() / pr.std()),
                            "q05": float(np.percentile(ch[:, j], 5)), "q95": float(np.percentile(ch[:, j], 95))}
    return out


def compute_dsge() -> dict:
    D = nk_data()
    out = _posterior((0, 1, 2))
    out["Y"] = D["Y"][:120].tolist()
    out["T"] = len(D["Y"])
    out["Gamma"] = MM.nk_solve(MM.NK_DEFAULT).tolist()
    return out


def compute_dsge_weak() -> dict:
    return _posterior((0, 1))


def compute_profile() -> dict:
    D = nk_data()
    grid = np.linspace(0.6, 3.0, 13)
    full = MM.nk_profile(D["Y"], "sigma", grid)
    two = MM.nk_profile(D["Y"], "sigma", grid, obs=(0, 1))
    full = np.array(full) - max(full)
    two = np.array(two) - max(two)
    return {"grid": grid.tolist(), "full": full.tolist(), "two": two.tolist(), "truth": MM.NK_DEFAULT["sigma"]}


def compute_irfmatch() -> dict:
    """An Island economy like the estimated one but whose central bank surprises more often (the monetary shock's
    s.d. 1 rather than 0.25), simulated for 400 quarters, with a market-surprise proxy for the monetary innovation.
    Local projections give the responses of the output gap, inflation and the rate to it, per point of the rate on
    impact; their sampling standard deviation comes from 60 more histories, each also matched, for the spread of
    the estimates. Then kappa and sigma are chosen to match (the rest at the truth)."""
    h = 12
    par = {**MM.NK_DEFAULT, "sd_v": 1.0}

    def one(seed):
        D = MM.nk_simulate(par, T=400, seed=seed)
        S = D["S"]
        v = S[1:, 2] - par["rho_v"] * S[:-1, 2]
        rng = np.random.default_rng(seed + 7)
        z = np.concatenate([[0.0], v + 0.5 * par["sd_v"] * rng.standard_normal(len(v))])
        return np.column_stack([MM.lp_iv(D["Y"], z, k, h, lags=4, unit=2) for k in range(3)])

    target = one(500)
    sims = np.array([one(600 + r) for r in range(60)])
    se = sims.std(0)
    m = MM.irf_match(target, se, h=h, free=("kappa", "sigma"), start=(0.3, 0.8))
    spread = [MM.irf_match(sims[r], se, h=h, free=("kappa", "sigma"), start=(0.3, 0.8))["estimate"]
              for r in range(len(sims))]
    ks = np.array([e["kappa"] for e in spread])
    ss = np.array([e["sigma"] for e in spread])
    tr = MM.nk_irf(par, h)
    tr = tr / tr[0, 2]
    return {"target": target.tolist(), "se": se.tolist(), **m, "truth_irf": tr.tolist(),
            "truth": {"kappa": par["kappa"], "sigma": par["sigma"]}, "start": {"kappa": 0.3, "sigma": 0.8}, "h": h,
            "kappa_5_95": [float(np.percentile(ks, 5)), float(np.percentile(ks, 95))],
            "sigma_5_95": [float(np.percentile(ss, 5)), float(np.percentile(ss, 95))],
            "kappa_median": float(np.median(ks)), "sigma_median": float(np.median(ss)), "sd_v": par["sd_v"]}


def compute_regions() -> dict:
    return fiscal.regions(**TRUTH["regions"])


# ---------------------------------------------------------------------------------------------------------------
# the intermission


def film_time(t: float, first: float = 1953.25, last: float = 2026.85) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_forecasts() -> dict:
    from videos.economics.econ1.compute import compute_spf
    from videos.economics.econ28.compute import compute_transitory

    s, t = compute_spf(), compute_transitory()
    return {"g_forecast": 100 * s["aug_2009"], "g_actual": 100 * s["actual_2009"],
            "pi_forecast": t["projected_2022"], "pi_actual": t["actual_2022"]}


def compute_film() -> dict:
    g10, tb, rec = _series("GS10"), _series("TB3MS"), _series("USREC")
    ds = [d for d in sorted(g10) if d in tb]
    t = [_t(d) for d in ds]
    spread = [g10[d] - tb[d] for d in ds]
    spans, start = [], None
    for d in sorted(rec):
        if d < ds[0]:
            continue
        if rec[d] > 0.5 and start is None:
            start = _t(d)
        if rec[d] <= 0.5 and start is not None:
            spans.append((start, _t(d)))
            start = None
    if start is not None:
        spans.append((start, _t(sorted(rec)[-1])))
    # inversions: months with a negative spread, grouped into episodes
    inv, cur = [], None
    for tt, sp in zip(t, spread):
        if sp < 0 and cur is None:
            cur = [tt, tt]
        elif sp < 0:
            cur[1] = tt
        elif cur is not None:
            inv.append(cur)
            cur = None
    if cur is not None:
        inv.append(cur)
    inv = [e for e in inv if e[1] - e[0] >= 2 / 12]
    followed = []
    for a, b in inv:
        nxt = [s for s in spans if s[0] >= a]
        followed.append(round(nxt[0][0] - a, 2) if nxt and nxt[0][0] - a <= 2.5 else None)
    return {"t": t, "spread": spread, "times": [film_time(x) for x in t], "recessions": spans, "first": ds[0],
            "last": ds[-1], "inversions": inv, "lead": followed, "min": float(min(spread)),
            "min_t": t[int(np.argmin(spread))]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["spread"])
    times = f["times"]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=40, high=86)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.2f} points"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the 10-year Treasury yield minus the 3-month bill rate, month by month, 1953-2026 "
                               "(via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ55").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "puzzle": compute_puzzle,
    "rotations": compute_rotations,
    "playit": compute_playit,
    "schemes": compute_schemes,
    "schemes_mc": compute_schemes_mc,
    "lpvar": compute_lpvar,
    "instruments": compute_instruments,
    "dsge": compute_dsge,
    "dsge_weak": compute_dsge_weak,
    "profile": compute_profile,
    "irfmatch": compute_irfmatch,
    "regions": compute_regions,
    "forecasts": compute_forecasts,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
