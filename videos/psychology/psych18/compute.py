"""Precompute every number in Part 18 of *Psychology, Built* ("Attention").

    python -m videos.psychology.psych18.compute            # everything missing (a minute or two)
    python -m videos.psychology.psych18.compute --force search

Results are cached in ``.cache/psych18/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.attention``); simulated studies are picked by rule (a fixed seed, or the mean
of many runs), never by their result.

Items:
    dichotic    who hears what in the unattended ear: a filter against an attenuator, and a sweep of attenuation
    load        flanker interference against perceptual load
    cueing      endogenous and exogenous cue effects against SOA; RTs at 400 ms
    search      set-size functions for feature, conjunction and spatial searches; three example displays
    saliency    a saliency map of a field of bars and its first five fixations
    prevalence  misses against target prevalence
    flicker     the flicker paradigm, fitted to Rensink's two means; the no-blank control
    notice      noticing an unexpected object against its similarity to the attended set
    blink       the attentional blink over lags 1 to 8
    prp         the psychological refractory period over SOAs
    stroop      Stroop RTs and errors, the word-reading control, the delta plot and the sequence effect
    switch      task-switching cost against the preparation interval
    normalize   the normalization model: contrast-response functions for two stimulus and attention-field sizes
    tva         whole report against exposure duration
    vigilance   hits and false alarms over a two-hour watch
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import attention as A

CACHE = Cache("psych18")
load = CACHE.load


def compute_dichotic() -> dict:
    att, flt = A.dichotic(), A.dichotic(model="filter")
    a = np.linspace(0, 1, 41)
    sweep = {w: np.array([A.dichotic(attenuation=x)[w][1] if x > 0 else 0.0 for x in a])
             for w in ("own name", "an ordinary word")}
    return {"words": list(att), "attended": [att[w][0] for w in att], "attenuate": [att[w][1] for w in att],
            "filter": [flt[w][1] for w in flt], "a": a, "sweep_name": sweep["own name"],
            "sweep_word": sweep["an ordinary word"]}


def compute_load() -> dict:
    load_ = np.arange(1, 7)
    return {"load": load_, "interference": A.flanker_interference(load_)}


def compute_cueing() -> dict:
    soa = np.linspace(0, 1000, 201)
    r = A.posner_rts(400, "endogenous", n=400, rng=np.random.default_rng(18))
    return {"soa": soa, "endogenous": A.cue_effect(soa, "endogenous"), "exogenous": A.cue_effect(soa, "exogenous"),
            "valid": float(r["valid"].mean()), "neutral": float(r["neutral"].mean()), "invalid": float(r["invalid"].mean())}


def compute_search() -> dict:
    out = {"set_sizes": np.array([4, 8, 16, 32])}
    for kind in ("feature", "conjunction", "spatial"):
        r = A.search_slopes(kind, n=400, rng=np.random.default_rng({"feature": 1, "conjunction": 2, "spatial": 3}[kind]))
        out[f"{kind}_present"], out[f"{kind}_absent"] = r["present"][0], r["absent"][0]
        out[f"{kind}_miss"] = r["present"][1]
        out[f"{kind}_slopes"] = np.array(r["slopes"])
        d = A.make_display(16, kind, True, np.random.default_rng(40))
        out[f"{kind}_display"] = np.c_[d.colour, d.orient, d.shape, d.xy]
        out[f"{kind}_target"] = d.target
    return out


def bar_field(h: int = 90, w: int = 160, rng=None):
    """A field of short bars on a grid: mostly green verticals; one red vertical, one green horizontal.  Returns
    feature maps (red-green, vertical, horizontal, luminance) and the bar list (row, col, colour, orientation)."""
    rng = rng or np.random.default_rng(7)
    maps = {k: np.zeros((h, w)) for k in ("red", "vertical", "horizontal", "luminance")}
    bars = []
    for i, r in enumerate(range(10, h - 5, 15)):
        for j, c in enumerate(range(10, w - 5, 16)):
            r0, c0 = r + int(rng.integers(-2, 3)), c + int(rng.integers(-2, 3))
            colour, orient = 0, 0
            if (i, j) == (2, 7):
                colour = 1
            if (i, j) == (4, 2):
                orient = 1
            bars.append((r0, c0, colour, orient))
            if orient == 0:
                sl = (slice(r0 - 4, r0 + 5), slice(c0 - 1, c0 + 2))
            else:
                sl = (slice(r0 - 1, r0 + 2), slice(c0 - 4, c0 + 5))
            maps["luminance"][sl] = 1.0
            maps["red" if colour else "vertical" if orient == 0 else "horizontal"][sl] = 1.0
            if colour:
                maps["vertical"][sl] = 1.0
    return maps, np.array(bars)


def compute_saliency() -> dict:
    maps, bars = bar_field()
    feats = {"colour": maps["red"], "orientation": maps["horizontal"] - 0.0 * maps["vertical"],
             "luminance": maps["luminance"]}
    sal = A.saliency_map(feats, centre=2.0, surround=10.0)
    path = A.scan_path(sal, k=5, ior_radius=9)
    return {"sal": sal, "path": np.array(path), "bars": bars, "shape": np.array(sal.shape)}


def compute_prevalence() -> dict:
    """Fit the criterion-shift model (d' and the share of the optimal shift) to Wolfe, Horowitz and Kenner's three
    miss rates by least squares on log odds."""
    from scipy.optimize import minimize
    from explainer.psychology import archive

    w = archive.WOLFE_2005.data
    pv, mv = np.array(w["prevalence"]), np.array(w["miss"])

    def loss(th):
        m = A.prevalence_misses(pv, d_prime=th[0], shift=th[1])
        return float(np.sum((np.log(m / (1 - m)) - np.log(mv / (1 - mv))) ** 2))

    res = minimize(loss, x0=(2.5, 0.7), bounds=((1.0, 5.0), (0.0, 1.5)))
    dp, sh = res.x
    p = np.logspace(np.log10(0.01), np.log10(0.5), 60)
    return {"p": p, "miss": A.prevalence_misses(p, d_prime=dp, shift=sh), "d_prime": float(dp), "shift": float(sh),
            "data_p": pv, "data_miss": mv,
            "fit": A.prevalence_misses(pv, d_prime=dp, shift=sh)}


def compute_flicker() -> dict:
    """Fit two numbers to Rensink et al.'s two means (7.3 alternations for central interests, 17.1 for marginal):
    how many items attention samples per alternation, and how much more an interesting item weighs.  A scene holds
    40 items, two of them central interests.  Each candidate is scored by 400 simulated observers per change."""
    n_items, ci_items = 40, 2
    best = None
    for per in (0.8, 1.0, 1.2, 1.5, 1.8, 2.2, 2.6, 3.0):
        for wci in (2.0, 3.0, 4.0, 6.0, 8.0, 12.0):
            w = np.ones(n_items)
            w[:ci_items] = wci
            rng = np.random.default_rng(int(per * 100 + wci))
            ci = np.mean([A.flicker(w, 0, per, rng=rng) for _ in range(400)])
            mi = np.mean([A.flicker(w, 20, per, rng=rng) for _ in range(400)])
            err = (np.log(ci / 7.3)) ** 2 + (np.log(mi / 17.1)) ** 2
            if best is None or err < best[0]:
                best = (err, per, wci, ci, mi)
    _, per, wci, ci, mi = best
    w = np.ones(n_items)
    w[:ci_items] = wci
    rng = np.random.default_rng(1997)
    dist_ci = np.array([A.flicker(w, 0, per, rng=rng) for _ in range(2000)])
    dist_mi = np.array([A.flicker(w, 20, per, rng=rng) for _ in range(2000)])
    return {"per": per, "w_ci": wci, "ci": float(dist_ci.mean()), "mi": float(dist_mi.mean()), "dist_ci": dist_ci,
            "dist_mi": dist_mi, "n_items": n_items, "cycle_s": 2 * (0.24 + 0.08) / 2 * 2}


def compute_notice() -> dict:
    s = np.linspace(0, 1, 101)
    return {"s": s, "low": A.notice_probability(s, load=0.35), "high": A.notice_probability(s, load=0.6)}


def compute_blink() -> dict:
    lags = np.arange(1, 9)
    return {"lags": lags, "p": A.attentional_blink(lags, n=20000, rng=np.random.default_rng(1992))}


def compute_prp() -> dict:
    soa = np.array([0, 50, 100, 150, 200, 300, 400, 600, 800, 1000])
    r = A.prp(soa, n=20000, rng=np.random.default_rng(1994))
    return {"soa": soa, "rt1": r["rt1"], "rt2": r["rt2"]}


def compute_stroop() -> dict:
    rng = np.random.default_rng(1935)
    out = {}
    for task in ("colour", "word"):
        for c in ("congruent", "neutral", "incongruent"):
            rt, ok = A.stroop(c, task, n=6000, rng=rng)
            out[f"{task}_{c}"] = float(rt[ok].mean())
            out[f"{task}_{c}_err"] = float(1 - ok.mean())
            if task == "colour" and c in ("congruent", "incongruent"):
                out[f"rts_{c}"] = rt[ok]
    out["dx"], out["dy"] = A.delta_plot(out["rts_congruent"], out["rts_incongruent"])
    conds = np.random.default_rng(2001).choice(["congruent", "incongruent"], 8000)
    rts, ok, _ = A.stroop_sequence(conds, rng=np.random.default_rng(1992))
    prev = np.concatenate([[""], conds[:-1]])
    for pc in ("congruent", "incongruent"):
        for c in ("congruent", "incongruent"):
            sel = (prev == pc) & (conds == c) & ok
            out[f"seq_{pc}_{c}"] = float(rts[sel].mean())
    return out


def compute_switch() -> dict:
    rsi = np.linspace(0, 1500, 151)
    return {"rsi": rsi, "cost": A.switch_cost(rsi)}


def compute_normalize() -> dict:
    c = np.logspace(-2, 0, 25)
    out = {"c": c}
    for name, sw, aw in (("small", 1.0, 8.0), ("large", 8.0, 1.0)):
        u, a = A.normalization_crf(c, sw, aw, False), A.normalization_crf(c, sw, aw, True)
        g = A.gain_type(c, u, a)
        out[f"{name}_u"], out[f"{name}_a"] = u, a
        out[f"{name}_rmax"], out[f"{name}_c50"] = g["rmax_ratio"], g["c50_ratio"]
    return out


def compute_tva() -> dict:
    e = np.linspace(0, 300, 61)
    return {"e": e, "six": A.tva_whole_report(e, 6, n=8000, rng=np.random.default_rng(1990)),
            "two": A.tva_whole_report(e, 2, n=8000, rng=np.random.default_rng(1991))}


def compute_vigilance() -> dict:
    t = np.linspace(0, 120, 121)
    v = A.vigilance(t)
    return {"t": t, "hits": v["hits"], "fas": v["fas"], "d": v["d"]}


ITEMS = {
    "dichotic": compute_dichotic,
    "load": compute_load,
    "cueing": compute_cueing,
    "search": compute_search,
    "saliency": compute_saliency,
    "prevalence": compute_prevalence,
    "flicker": compute_flicker,
    "notice": compute_notice,
    "blink": compute_blink,
    "prp": compute_prp,
    "stroop": compute_stroop,
    "switch": compute_switch,
    "normalize": compute_normalize,
    "tva": compute_tva,
    "vigilance": compute_vigilance,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
