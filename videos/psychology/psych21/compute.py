"""Precompute every number in Part 21 of *Psychology, Built* ("Memory II: Forgetting and Inventing").

    python -m videos.psychology.psych21.compute            # everything missing (about a minute; fetches open data once)
    python -m videos.psychology.psych21.compute --force spacing

Results are cached in ``.cache/psych21/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.memory``); the replication data are the Archive's (Murre and Dros's table of
savings) and the verbal-overshadowing Registered Replication Report's per-lab counts, fetched by
``explainer.psychology.opendata``.  Simulated studies use a fixed seed, chosen before the result was seen.

Items:
    laws         four forgetting laws fitted to Ebbinghaus and three replications, with AIC
    jost         Jost's law under the power law and under the exponential
    mixture      a gamma mixture of exponentials, averaged, is a power function: the averaging artefact
    interference retroactive interference in a linear associator, against the overlap of the second list's cues
    penguin      a network trained on Rumelhart's semantic items learns the penguin, focused or interleaved
    spacing      Pavlik and Anderson's model: recall against gap for four retention intervals, and the ridge
    consolidate  a two-store model of systems consolidation: retrieval strength by age, intact and after a lesion
    testing      the bifurcation model fitted to Roediger and Karpicke's first experiment
    adjust       the category adjustment model: bias toward the prototype, and the error it saves, by trace noise
    drm          the DRM illusion by global matching
    overshadow   the verbal-overshadowing replication: each lab's difference, pooled, against the original
    lineup       lineups by signal detection: the confidence-accuracy characteristic for three memory strengths
    hlr          half-life regression fitted to simulated practice data, against two simpler schedulers
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M

CACHE = Cache("psych21")
load = CACHE.load

T_MIN = np.array([20.0, 64.0, 526.0, 1440.0, 2880.0, 8640.0, 44640.0])


def compute_laws() -> dict:
    s = archive.SAVINGS_REPLICATIONS.data
    out = {"t": T_MIN, "tt": np.geomspace(15, 60000, 200), "names": np.array(list(M.LAWS))}
    for who in ("ebbinghaus", "mack", "seitz", "dros"):
        y = np.array(s[who])
        fits = {law: M.fit_law(law, T_MIN, y) for law in M.LAWS}
        out[who] = y
        out[who + "_aic"] = np.array([fits[law]["aic"] for law in M.LAWS])
        for law in M.LAWS:
            out[f"{who}_{law}"] = M.law_curve(law, fits[law]["params"], out["tt"])
            out[f"{who}_{law}_params"] = fits[law]["params"]
    return out


def compute_jost() -> dict:
    d = load("laws")
    h = np.linspace(0, 20000, 200)
    pw = d["ebbinghaus_power_params"]
    ex = d["ebbinghaus_exponential_params"]
    young, old = 60.0, 2880.0  # one hour old, and two days old but rehearsed to the same strength
    py, po = M.jost("power", pw, young, old, h)
    ey, eo = M.jost("exponential", ex, young, old, h)
    return {"h": h, "power_young": py, "power_old": po, "exp_young": ey, "exp_old": eo}


def compute_mixture() -> dict:
    t = np.linspace(0, 30, 300)
    rng = np.random.default_rng(1885)
    shape, scale = 1.5, 0.4
    rates = rng.gamma(shape, scale, 12)
    each = np.exp(-np.outer(rates, t))
    many = rng.gamma(shape, scale, 20000)
    avg = np.exp(-np.outer(many, t)).mean(0)
    return {"t": t, "each": each, "average": avg, "power": M.gamma_mixture(t, shape, scale), "shape": shape,
            "scale": scale}


def compute_interference() -> dict:
    ov = np.linspace(0, 1, 11)
    rng = np.random.default_rng(1924)
    both = [np.mean([M.associator_interference(overlap=o, rng=rng)["both"] for _ in range(20)]) for o in ov]
    first = M.associator_interference(rng=np.random.default_rng(1))["first"]
    return {"overlap": ov, "both": np.array(both), "first": first}


def compute_penguin() -> dict:
    r = M.penguin_experiment()
    out = {"base_error": r["base_error"]}
    for k in ("focused", "interleaved"):
        out[k + "_old"] = r[k]["old"]
        out[k + "_new"] = r[k]["new"]
        out[k + "_robin"] = np.array([r[k]["robin_can"][a] for a in ("grow", "move", "fly", "swim")])
    return out


def compute_spacing() -> dict:
    gaps = np.unique(np.r_[np.linspace(0, 2, 9), np.geomspace(2, 120, 40)])
    ri = np.array([7.0, 35.0, 70.0, 350.0])
    R = M.spacing_ridge(gaps, ri, c=1.0, a=0.1)
    best = gaps[R.argmax(1)]
    return {"gaps": gaps, "ri": ri, "recall": R, "best": best, "ratio": best / ri}


def compute_consolidate() -> dict:
    age = np.linspace(0, 400, 401)
    intact = M.two_store(age)
    lesion = M.two_store(age, lesion=True)
    return {"age": age, "intact": intact, "lesion": lesion, "hippo": np.exp(-0.3 * age),
            "spared": np.where(intact > 0, lesion / np.maximum(intact, 1e-12), 0.0),
            "peak_age": float(age[lesion.argmax()])}


def compute_testing() -> dict:
    r = archive.ROEDIGER_KARPICKE_2006.data
    f = M.fit_bifurcation({"restudy": r["exp1_restudy"], "test": r["exp1_test"]})
    p = f["params"]
    fine = M.bifurcation(p, delays=np.r_[5 / 1440, np.linspace(0.25, 7, 40)])
    return {"params": np.array([p[k] for k in ("restudy", "gain", "theta_test", "loss", "tau")]), "sse": f["sse"],
            "restudy": f["model"]["restudy"], "test": f["model"]["test"], "initial_test": f["model"]["initial_test"],
            "fine_delays": fine["delays"], "fine_restudy": fine["restudy"], "fine_test": fine["test"],
            "s_restudy": fine["restudy_strength"], "s_test": fine["test_strength"]}


def compute_adjust() -> dict:
    pos = np.linspace(2, 88, 44)
    out = {"positions": pos, "noise": np.array([4.0, 10.0, 20.0]), "cat_sd": 22.0}
    for k, sd in enumerate(out["noise"]):
        r = M.category_adjustment(pos, sd, out["cat_sd"], rng=np.random.default_rng(1991))
        out[f"bias{k}"] = r["bias"]
        out[f"lambda{k}"] = r["lambda"]
        out[f"rmse{k}"] = float(r["rmse"].mean())
        out[f"rmse_trace{k}"] = float(r["rmse_trace"].mean())
    return out


def compute_drm() -> dict:
    d = M.drm_global_matching(lists=200, assoc=0.095, rng=np.random.default_rng(1995))
    fam = d["familiarity"]
    crit = float(np.quantile(fam["studied"], 0.14))
    return {"studied": fam["studied"], "lure": fam["lure"], "unrelated": fam["unrelated"], "criterion": crit,
            "yes_studied": float(np.mean(fam["studied"] > crit)), "yes_lure": float(np.mean(fam["lure"] > crit)),
            "yes_unrelated": float(np.mean(fam["unrelated"] > crit))}


def compute_overshadow() -> dict:
    out = {}
    for study in (1, 2):
        d = opendata.overshadowing_rrr(study)
        v, c = d["verbal"], d["control"]  # (labs, 2): correct, included
        pv, pc = v[:, 0] / v[:, 1], c[:, 0] / c[:, 1]
        diff = pv - pc
        se = np.sqrt(pv * (1 - pv) / v[:, 1] + pc * (1 - pc) / c[:, 1])
        w = 1 / se ** 2
        pooled = float(np.sum(w * diff) / np.sum(w))
        tau2 = max(0.0, (np.sum(w * (diff - pooled) ** 2) - (len(diff) - 1)) /
                   (np.sum(w) - np.sum(w ** 2) / np.sum(w)))  # DerSimonian-Laird
        wr = 1 / (se ** 2 + tau2)
        rand = float(np.sum(wr * diff) / np.sum(wr))
        out[f"s{study}_diff"] = diff
        out[f"s{study}_se"] = se
        out[f"s{study}_pooled"] = rand
        out[f"s{study}_pooled_se"] = float(np.sqrt(1 / np.sum(wr)))
        out[f"s{study}_tau"] = float(np.sqrt(tau2))
        out[f"s{study}_n"] = int(v[:, 1].sum() + c[:, 1].sum())
        out[f"s{study}_labs"] = len(diff)
        o = d["original"]
        out[f"s{study}_original"] = float(o[0, 0] / o[0, 1] - o[1, 0] / o[1, 1])
        on = d["online"]
        out[f"s{study}_online"] = float(on[0, 0] / on[0, 1] - on[1, 0] / on[1, 1])
        out[f"s{study}_verbal_rate"] = float(v[:, 0].sum() / v[:, 1].sum())
        out[f"s{study}_control_rate"] = float(c[:, 0].sum() / c[:, 1].sum())
    return out


def compute_lineup() -> dict:
    out = {"d": np.array([1.0, 1.5, 2.0])}
    for k, d in enumerate(out["d"]):
        r = M.lineup_cac(d, rng=np.random.default_rng(2017))
        out[f"cac{k}"] = r["cac"]
        out[f"overall{k}"] = r["overall"]
        out[f"present{k}"] = r["present_suspect"]
        out[f"absent{k}"] = r["absent_suspect"]
        out[f"present_filler{k}"] = r["present_filler"]
        out[f"absent_filler{k}"] = r["absent_filler"]
    out["levels"] = np.arange(1, 6)
    return out


def compute_hlr() -> dict:
    s = M.hlr_simulate(rng=np.random.default_rng(2016))
    n = len(s["gap"])
    train = np.arange(n) % 5 != 0  # every fifth row held out
    f = M.fit_hlr(s["x"][train], s["gap"][train], s["recalled"][train])
    th = f["theta"]
    test = ~train
    y = s["recalled"][test]
    gap = s["gap"][test]
    p_hlr = 2.0 ** (-gap / 2.0 ** (s["x"][test] @ th))
    p_const = np.full(test.sum(), s["recalled"][train].mean())
    # Leitner's boxes: the half-life doubles with each box; a right answer moves the word up, a wrong one to the start
    right, wrong = s["x"][test, 0] ** 2, s["x"][test, 1] ** 2
    box = np.maximum(right - wrong, 0)
    p_leit = 2.0 ** (-gap / 2.0 ** box)
    mae = {k: float(np.mean(np.abs(y - p))) for k, p in (("const", p_const), ("leitner", p_leit), ("hlr", p_hlr))}
    edges = np.linspace(0, 1, 11)
    idx = np.clip(np.digitize(p_hlr, edges) - 1, 0, 9)
    pred = np.array([p_hlr[idx == b].mean() if np.any(idx == b) else np.nan for b in range(10)])
    obs = np.array([y[idx == b].mean() if np.any(idx == b) else np.nan for b in range(10)])
    cnt = np.array([np.sum(idx == b) for b in range(10)])
    gaps = np.linspace(0, 14, 141)
    curves = {f"curve_right{r}": 2.0 ** (-gaps / 2.0 ** (np.array([np.sqrt(r), 0.0, 1.0]) @ th)) for r in (0, 2, 6)}
    return {"theta": th, "true_theta": s["theta"], "rows": n, "test_rows": int(test.sum()),
            "mae_const": mae["const"], "mae_leitner": mae["leitner"], "mae_hlr": mae["hlr"],
            "cal_pred": pred, "cal_obs": obs, "cal_n": cnt, "gaps": gaps, **curves}


ITEMS = {
    "laws": compute_laws,
    "jost": compute_jost,
    "mixture": compute_mixture,
    "interference": compute_interference,
    "penguin": compute_penguin,
    "spacing": compute_spacing,
    "consolidate": compute_consolidate,
    "testing": compute_testing,
    "adjust": compute_adjust,
    "drm": compute_drm,
    "overshadow": compute_overshadow,
    "lineup": compute_lineup,
    "hlr": compute_hlr,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
