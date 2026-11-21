"""Precompute every number in Part 56 of *Economics, Built* ("The Core Exam").

    python -m videos.economics.econ56.compute            # everything missing (about five minutes)
    python -m videos.economics.econ56.compute --force micro1

Results are cached in ``.cache/econ56/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
``exam`` module, which solves each question twice, by the formula and by brute force, over Part 52's Aiyagari economy
(``hetero``), Part 54's GMM (``estimate``) and statkit's difference-in-differences (``quasi``).  Data, via FRED: the
median duration of unemployment with the NBER's recession months (the intermission).

Items:
    micro1      a consumer with a kinked budget: demand, the Slutsky decomposition, the compensating variation
    micro2      an exchange economy with an externality: equilibrium, the Pareto set, the Pigouvian tax
    micro3      a first-price auction with a reserve: the bid function, revenue by formula and by simulation
    micro4      screening: two types, then a continuum
    macro1      the Ramsey model with a tax on capital: the steady states and the saddle-path transition
    macro2      a McCall worker whose benefits expire: reservation wages by periods of benefit left
    macro3      the three-equation model under discretion and under commitment
    macro4      Aiyagari's economy: capital supply and demand, and why r lies below the rate of time preference
    metrics1    a supply-and-demand system on simulated days: OLS against the Wald estimator
    metrics2    GMM for the consumption Euler equation, with the objective over a grid
    metrics3    two-way fixed effects with staggered adoption: the Goodman-Bacon decomposition and cell weights
    metrics4    a bivariate VAR with a long-run restriction, in population and in 200 samples
    film        the intermission's data film: the median duration of unemployment, 1967-2026, with recessions
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, score
from explainer.economics.agora import exam

CACHE = Cache("econ56")
load = CACHE.load
TRUTH: dict = {}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _series(name: str) -> dict:
    d = data.fred(name)
    return {k: v for k, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


def compute_micro1() -> dict:
    out = exam.kinked_budget()
    # the picture: budget, virtual budget, and indifference curves through each optimum
    a, m, xbar = out["alpha"], out["m"], out["xbar"]
    xs = np.linspace(2, 60, 300)

    def icurve(alpha, x0, y0):
        u = alpha * np.log(x0) + (1 - alpha) * np.log(y0)
        return np.exp((u - alpha * np.log(xs)) / (1 - alpha))

    out["xs"] = xs.tolist()
    out["ic"] = icurve(a, out["x"], out["y"]).tolist()
    k = out["kink_case"]
    out["ic_kink"] = icurve(k["alpha"], xbar, m - xbar).tolist()
    return _jsonable(out)


def compute_micro2() -> dict:
    out = exam.externality_box()
    X, Y = out["X"], out["Y"]
    p = out["p_tax"]
    out["ya_tax"] = Y / 2 + p * (X / 2 - out["xa_po"])
    out["yb_tax"] = Y - out["ya_tax"]
    return _jsonable(out)


def compute_micro3() -> dict:
    return _jsonable(exam.reserve_auction())


def compute_micro4() -> dict:
    return _jsonable(exam.screening())


def compute_macro1() -> dict:
    out = exam.ramsey_tax()
    k, c = np.array(out["path_k"]), np.array(out["path_c"])
    keep = np.unique(np.linspace(0, len(k) - 1, 400).astype(int))
    out["path_k"], out["path_c"] = k[keep].tolist(), c[keep].tolist()
    out["path_t"] = (keep * out["dt"]).tolist()
    return _jsonable(out)


def compute_macro2() -> dict:
    return _jsonable(exam.mccall_expiring())


def compute_macro3() -> dict:
    return _jsonable(exam.discretion())


def compute_macro4() -> dict:
    return _jsonable(exam.aiyagari_gap())


def compute_metrics1() -> dict:
    return _jsonable(exam.supply_demand())


def compute_metrics2() -> dict:
    from explainer.economics.agora import estimate

    out = exam.euler_gmm()
    two = out["two"]
    dat = estimate.euler_data(T=out["T"], beta=out["beta"], gamma=out["gamma"], seed=56)
    f = estimate.euler_moments(dat)
    W = np.asarray(two["W"])
    bs = np.linspace(two["theta"][0] - 0.012, two["theta"][0] + 0.012, 61)
    gs = np.linspace(two["theta"][1] - 0.6, two["theta"][1] + 0.6, 61)
    T = f(np.array(two["theta"])).shape[0]
    J = np.array([[T * float(f(np.array([b, g])).mean(0) @ W @ f(np.array([b, g])).mean(0)) for b in bs]
                  for g in gs])
    keep = ("theta", "se", "J", "df", "p_J", "n")
    return _jsonable({"T": out["T"], "beta": out["beta"], "gamma": out["gamma"], "m": out["m"], "k": out["k"],
                      "df": out["df"], "one": {k: out["one"][k] for k in keep if k in out["one"]},
                      "two": {k: two[k] for k in keep if k in two}, "grid_b": bs, "grid_g": gs, "Jgrid": J})


def compute_metrics3() -> dict:
    out = exam.staggered_did()
    out["twfe_no_never"] = exam.staggered_did(never=False)["twfe"]
    return _jsonable(out)


def compute_metrics4() -> dict:
    return _jsonable(exam.long_run_var())


def film_time(t: float, first: float = 1967.0, last: float = 2026.85) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    med, rec = _series("UEMPMED"), _series("USREC")
    ds = sorted(med)
    t = [_t(d) for d in ds]
    v = [med[d] for d in ds]
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
    k = int(np.argmax(v))
    pre = [x for d, x in zip(ds, v) if d < "2008-01-01"]
    return {"t": t, "weeks": v, "times": [film_time(x) for x in t], "recessions": spans, "first": ds[0],
            "last": ds[-1], "max": float(v[k]), "max_date": ds[k], "max_before_2008": float(max(pre)),
            "last_value": float(v[-1])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["weeks"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=10, log=True, low=40, high=86)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f} weeks"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the median duration of unemployment in the United States, month by month, "
                               "1967-2026 (BLS via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ56").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "micro1": compute_micro1,
    "micro2": compute_micro2,
    "micro3": compute_micro3,
    "micro4": compute_micro4,
    "macro1": compute_macro1,
    "macro2": compute_macro2,
    "macro3": compute_macro3,
    "macro4": compute_macro4,
    "metrics1": compute_metrics1,
    "metrics2": compute_metrics2,
    "metrics3": compute_metrics3,
    "metrics4": compute_metrics4,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
