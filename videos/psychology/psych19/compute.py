"""Precompute every number in Part 19 of *Psychology, Built* ("Working Memory").

    python -m videos.psychology.psych19.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych19.compute --force bays

Results are cached in ``.cache/psych19/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.wm``); the open data are Bays, Catalao and Husain's (2009), fetched by
``explainer.psychology.opendata``.  Simulated studies are picked by rule (a fixed seed, or the mean of many runs),
never by their result.

Items:
    judgment    information transmitted by absolute judgments against the number of categories
    recode      Miller's recoding arithmetic: binary digits held at each grouping
    loop        the phonological loop: list recall against length for short and long words, with and without
                articulatory suppression; span against speech rate
    sperling    letters available in partial report against the cue's delay
    forgetting  Brown-Peterson recall against delay on trials 1, 2 and 3 and late in a session (SIMPLE)
    sternberg   memory-scanning RTs for serial, self-terminating, parallel and limited-capacity models
    change      change detection by a slot observer at set sizes 1 to 8; Cowan's K
    bays        the open data: error histograms, mixture and swap fits by set size, four process models fitted
                to each observer, AIC differences, and the winning model's predicted densities
    mimic       the mixture model fitted to a variable-precision observer who never guesses
    ring        a ring attractor: one trial's bump, its drift, and the memory's variance against delay
    training    simulated brain-training trials against passive and active controls
    budget      a fixed information budget shared among items, fitted to the open data's error spread
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import wm

CACHE = Cache("psych19")
load = CACHE.load

SET_SIZES = (1, 2, 4, 6)
MODELS = ("slots", "averaging", "equal", "variable")


def compute_judgment() -> dict:
    n = np.arange(2, 31)
    return {"n": n, "bits": wm.absolute_judgment(n), "input": np.log2(n)}


def compute_recode() -> dict:
    groups = np.arange(1, 6)
    return {"group": groups, "ideal": np.array([wm.recoded_span(g) for g in groups]),
            "binary": "101000100111001110", "octal": "504716"}


def compute_loop() -> dict:
    rng = np.random.default_rng(1975)
    out = {}
    for name, dur in (("short", 0.3), ("long", 0.8)):
        for sup in (False, True):
            r = wm.loop_span(dur, suppress=sup, n=20000, rng=rng)
            key = f"{name}_{'suppressed' if sup else 'loop'}"
            out[key] = r["p"]
            out[key + "_span"] = r["span"]
    out["lengths"] = np.arange(1, 13)
    rate = np.linspace(1.0, 4.0, 13)  # words per second
    out["rate"] = rate
    out["rate_span"] = np.array([wm.loop_span(1 / r, n=20000, rng=rng)["span"] for r in rate])
    return out


def compute_sperling() -> dict:
    t = np.linspace(0, 1000, 101)
    r = wm.partial_report(t)
    return {"delay": t, "available": r["available"], "whole": r["whole"]}


def compute_forgetting() -> dict:
    d = np.linspace(1, 18, 69)
    late = np.mean([wm.brown_peterson(d, t) for t in range(5, 21)], 0)
    marks = np.array([3, 6, 9, 12, 15, 18.0])
    return {"delay": d, "trial1": wm.brown_peterson(d, 1), "trial2": wm.brown_peterson(d, 2),
            "trial3": wm.brown_peterson(d, 3), "late": late, "marks": marks,
            "late_marks": np.mean([wm.brown_peterson(marks, t) for t in range(5, 21)], 0),
            "p18_by_trial": np.array([wm.brown_peterson([18.0], t)[0] for t in range(1, 9)]),
            "p3_by_trial": np.array([wm.brown_peterson([3.0], t)[0] for t in range(1, 9)])}


def compute_sternberg() -> dict:
    rng = np.random.default_rng(1966)
    k = np.arange(1, 7)
    out = {"k": k}
    for m in ("serial", "self", "parallel", "limited"):
        for pos in (True, False):
            out[f"{m}_{'yes' if pos else 'no'}"] = np.array(
                [wm.sternberg_rts(int(s), pos, m, n=20000, rng=rng).mean() for s in k])
    a = wm.sternberg_rts(4, True, "serial", n=40000, rng=rng)
    b = wm.sternberg_rts(4, True, "limited", n=40000, rng=rng)
    edges = np.linspace(200, 1200, 51)
    out["edges"] = edges
    out["hist_serial"] = np.histogram(a, edges, density=True)[0]
    out["hist_limited"] = np.histogram(b, edges, density=True)[0]
    out["slope_yes"], out["intercept_yes"] = np.polyfit(k, out["serial_yes"], 1)
    return out


def compute_change() -> dict:
    rng = np.random.default_rng(1997)
    N = np.arange(1, 9)
    H, FA = [], []
    for n in N:
        r = wm.change_detection(int(n), K=3.5, guess=0.45, n=4000, rng=rng)
        H.append(r["H"])
        FA.append(r["FA"])
    H, FA = np.array(H), np.array(FA)
    acc = (H + (1 - FA)) / 2
    return {"N": N, "H": H, "FA": FA, "accuracy": acc, "K": wm.k_cowan(H, FA, N)}


def _hist(e, bins=36):
    edges = np.linspace(-np.pi, np.pi, bins + 1)
    h, _ = np.histogram(wm.wrap(e), edges, density=True)
    return edges, h


def compute_bays() -> dict:
    d = opendata.bays_2009()
    e, N, s, dur = d["error"], d["set_size"], d["subject"], d["duration"]
    out = {"set_sizes": np.array(SET_SIZES), "trials": len(e), "observers": len(np.unique(s))}
    x = np.linspace(-np.pi, np.pi, 361)
    out["x"] = x
    for n in SET_SIZES:
        m = N == n
        edges, h = _hist(e[m])
        out[f"hist_{n}"] = h
        f = wm.fit_mixture(e[m])
        out[f"mix_{n}"] = np.array([f["g"], f["sd"], f["kappa"]])
        sw = wm.fit_swap(e[m], d["nontarget_error"][m]) if n > 1 else None
        out[f"swap_{n}"] = np.array([sw["pT"], sw["pN"], sw["pU"], sw["sd"]]) if sw else np.array([1, 0, 0, f["sd"]])
        out[f"sd_{n}"] = np.array([_circ_sd(e[m & (dur == t)]) for t in (100, 500, 2000)])
    out["edges"] = edges
    # four process models, fitted to each observer separately
    subs = np.unique(s)
    aic = np.zeros((len(subs), len(MODELS)))
    params = {mo: [] for mo in MODELS}
    for i, sub in enumerate(subs):
        k = s == sub
        for j, mo in enumerate(MODELS):
            f = wm.fit_model(mo, e[k], N[k])
            aic[i, j] = f["aic"]
            params[mo].append(f["params"])
    out["aic"] = aic
    out["daic"] = aic - aic.min(1, keepdims=True)
    out["daic_total"] = aic.sum(0) - aic.sum(0).min()
    out["wins"] = np.array([(aic.argmin(1) == j).sum() for j in range(len(MODELS))])
    for mo in MODELS:
        out[f"params_{mo}"] = np.array(params[mo])
    # predicted pooled densities: each observer's fitted model, averaged over observers
    for mo in ("slots", "variable"):
        for n in SET_SIZES:
            out[f"pred_{mo}_{n}"] = np.mean([wm.model_pdf(mo, p, x, np.full(len(x), n)) for p in params[mo]], 0)
    return out


def _circ_sd(e) -> float:
    """The circular standard deviation of errors, in radians."""
    return float(np.sqrt(-2 * np.log(abs(np.mean(np.exp(1j * np.asarray(e)))))))


def compute_mimic() -> dict:
    b = load("bays")
    vp = b["params_variable"]
    i = int(np.argsort(vp[:, 0])[len(vp) // 2])  # the median observer, by J1: picked by rule
    p = tuple(vp[i])
    rng = np.random.default_rng(2012)
    out = {"params": np.array(p), "set_sizes": np.array(SET_SIZES)}
    g, sd = [], []
    for n in SET_SIZES:
        e = wm.simulate_report("variable", p, np.full(20000, n), rng)
        f = wm.fit_mixture(e)
        g.append(f["g"])
        sd.append(f["sd"])
        edges, h = _hist(e)
        out[f"hist_{n}"] = h
    out["g"], out["sd"], out["edges"] = np.array(g), np.array(sd), edges
    out["K"] = np.array(SET_SIZES) * (1 - np.array(g))
    return out


def compute_ring() -> dict:
    r = wm.ring_attractor(delay=4000, trials=300, rng=np.random.default_rng(1989))
    t, a = r["t"], r["angle"]
    var = np.var(a, 0)
    slope = float(np.polyfit(t / 1000, var, 1)[0])
    one = wm.ring_attractor(delay=4000, trials=1, rng=np.random.default_rng(3))
    return {"t": t, "var": var, "sd_deg": np.degrees(np.sqrt(var)), "slope": slope,
            "paths": np.degrees(a[:12]), "theta": r["theta"], "rates": one["rates"], "path1": np.degrees(one["angle"][0])}


def compute_training() -> dict:
    rng = np.random.default_rng(2008)
    out = {}
    for control in ("passive", "active"):
        runs = [wm.training_trial(40, control=control, rng=rng) for _ in range(400)]
        out[f"{control}_near"] = np.array([r["near"] for r in runs])
        out[f"{control}_far"] = np.array([r["far"] for r in runs])
    return out


def compute_budget() -> dict:
    from scipy.optimize import least_squares

    b = load("bays")
    N = np.array(SET_SIZES, float)
    sd = np.degrees([np.mean(b[f"sd_{n}"]) for n in SET_SIZES])  # averaged over the three durations
    r = least_squares(lambda th: np.log(wm.budget_sd(N, th[0], th[1])) - np.log(sd), x0=(2.0, 15.0),
                      bounds=([0, 1], [10, 90]))
    bits, sd1 = r.x
    n = np.linspace(1, 8, 71)
    return {"N": N, "sd": sd, "bits": float(bits), "sd1": float(sd1), "n": n, "fit": wm.budget_sd(n, bits, sd1)}


ITEMS = {
    "judgment": compute_judgment,
    "recode": compute_recode,
    "loop": compute_loop,
    "sperling": compute_sperling,
    "forgetting": compute_forgetting,
    "sternberg": compute_sternberg,
    "change": compute_change,
    "bays": compute_bays,
    "mimic": compute_mimic,
    "ring": compute_ring,
    "training": compute_training,
    "budget": compute_budget,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
