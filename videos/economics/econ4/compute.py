"""Precompute every number in Part 4 of *Economics, Built* ("The Evidence").

    python -m videos.economics.econ4.compute            # everything missing (a few seconds)
    python -m videos.economics.econ4.compute --force season

Results are cached in ``.cache/econ4/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the draft lottery of 1 December 1969; the transcribed tables of Moore, Leamer, LaLonde
and Card) and the Museum of *Statistics, Built* (``explainer.stats.museum``: LaLonde's NSW data in Dehejia and
Wahba's subsample with the PSID comparison group; Card and Krueger's table 3).  Models: Agora's econometrician
(``agora.econometrician``), with the Island's Part 4 truths.  Every random draw is seeded.

Items:
    season        a season of the Island's fish market: 240 days of prices and quantities, feasts and storms, the
                  planted lines, the least-squares line and its probability limit, the four groups' means
    playit        the four candidate demand curves offered to the viewer
    instrument    the Wald estimates (storms trace demand, feasts trace supply), two-stage least squares, first stages
    schooling     the Island's school records: least squares, the omitted-variable bias, the new school as instrument
    lalonde       the NSW experiment and the PSID comparison: LaLonde's table 5, and the same comparisons recomputed on
                  Dehejia and Wahba's subsample
    draft         the draft lottery of 1969: ranks by birthday and month, the trend, a permutation test
    credibility   Card and Krueger's table 3 and its difference in differences
    experiment    the Island's apprenticeship, assigned by choice and by lottery: ability histograms and both
                  comparisons of means
    nit           a negative income tax's budget lines (the New Jersey experiment's guarantees and tax rates)
    lucas         Lucas's islands: the calm years' regression and what happens when the council exploits it
    phillips      US unemployment and CPI inflation, annual averages 1961-79 (FRED)
    power         the apprenticeship trial's power: the minimum detectable effect against the number of islanders
    dial          the return to schooling: Card's (2001) table of OLS and IV estimates
    villages      the apprenticeship scaled up: a two-level trial in the Island's villages, with spillovers
    weak          weak instruments on the Island's school records: two-stage least squares with K instruments of
                  pure noise (Bound, Jaeger and Baker's experiment), against the real instrument
    film          the intermission's data film: the capsules in the order drawn
    melody        the intermission's data melody: each capsule's birth month as a pitch, in the order drawn
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import econometrician as em
from explainer.economics.data import tables

CACHE = Cache("econ4")
load = CACHE.load
TRUTH = island.truths(4)


def _season() -> dict:
    return em.fish_season(**TRUTH["season"])


def compute_season() -> dict:
    t = TRUTH["season"]
    s = _season()
    o = em.ols(s["q"], s["p"])
    var_u = t["feast"][1] ** 2 * t["feast"][0] * (1 - t["feast"][0]) + t["noise"][0] ** 2
    var_v = t["storm"][1] ** 2 * t["storm"][0] * (1 - t["storm"][0]) + t["noise"][1] ** 2
    groups = {}
    for name, mask in (("ordinary", (s["feast"] == 0) & (s["storm"] == 0)), ("feast", (s["feast"] == 1) & (s["storm"] == 0)),
                       ("storm", (s["feast"] == 0) & (s["storm"] == 1)), ("both", (s["feast"] == 1) & (s["storm"] == 1))):
        groups[name] = {"n": int(mask.sum()), "p": float(s["p"][mask].mean()), "q": float(s["q"][mask].mean())}
    return {"p": s["p"], "q": s["q"], "feast": s["feast"], "storm": s["storm"],
            "a": t["a"], "b": t["b"], "c": t["c"], "d": t["d"], "F": t["feast"][1], "S": t["storm"][1],
            "ols_slope": o["slope"], "ols_intercept": float(o["beta"][0]), "ols_se": o["slope_se"],
            "plim": em.simultaneity_slope(t["b"], t["d"], var_u, var_v), "var_u": var_u, "var_v": var_v,
            "groups": groups, "days": t["days"],
            "n_feast": int(s["feast"].sum()), "n_storm": int(s["storm"].sum()),
            "p_mean": float(s["p"].mean()), "q_mean": float(s["q"].mean())}


def compute_playit() -> dict:
    s = compute_season()
    pm, qm = s["p_mean"], s["q_mean"]
    # four lines through the middle of the cloud, as slopes dq/dp: the least-squares line, a steep one (buyers barely
    # respond: on price-up axes a small dq/dp is steep), the planted
    # demand, a flat one
    cands = {"A": s["ols_slope"], "B": -25.0, "C": -s["b"], "D": -200.0}
    return {"p_mean": pm, "q_mean": qm, "candidates": cands, "answer": "C",
            "elasticity_at_mean": -s["b"] * pm / qm}


def compute_instrument() -> dict:
    s = _season()
    st = em.wald(s["q"], s["p"], s["storm"])
    fe = em.wald(s["q"], s["p"], s["feast"])
    ivs = em.iv(s["q"], s["p"], s["storm"])
    ivf = em.iv(s["q"], s["p"], s["feast"])
    # the first stage: does the storm move the price?
    fs = em.ols(s["p"], s["storm"])
    return {"storm": st, "feast": fe, "iv_storm": ivs, "iv_feast": ivf,
            "first_stage_storm": {"slope": fs["slope"], "se": fs["slope_se"]},
            "truth_demand": -TRUTH["season"]["b"], "truth_supply": TRUTH["season"]["d"]}


def compute_schooling() -> dict:
    sc = dict(TRUTH["schooling"])
    sc["return_"] = sc.pop("return")
    r = em.schooling_records(**sc)
    o = em.ols(r["logw"], r["school"])
    both = em.ols(r["logw"], np.column_stack([r["school"], r["ability"]]))
    ivr = em.iv(r["logw"], r["school"], r["near"])
    cov = float(np.cov(r["school"], r["ability"])[0, 1])
    bias = em.ovb(sc["ability_on_wage"], cov, float(r["school"].var(ddof=1)))
    w = em.wald(r["logw"], r["school"], r["near"])
    rng = np.random.default_rng(7)
    show = rng.choice(len(r["school"]), 300, replace=False)
    return {"school": r["school"][show], "logw": r["logw"][show], "ability": r["ability"][show],
            "near": r["near"][show], "ols": o["slope"], "ols_se": o["slope_se"],
            "with_ability": float(both["beta"][1]), "iv": ivr["estimate"], "iv_se": ivr["se"], "F": ivr["F"],
            "bias_formula": bias, "truth": sc["return_"], "gamma": sc["ability_on_wage"], "cov_sa": cov,
            "var_s": float(r["school"].var(ddof=1)), "wald": w, "n": sc["n"]}


def compute_lalonde() -> dict:
    from explainer.stats import museum

    t = tables.LALONDE_1986.data
    d = museum.nsw()
    exp = d["sample"] == "experiment"
    tr = exp & (d["treat"] == 1)
    ct = exp & (d["treat"] == 0)
    ps = d["sample"] == "psid"
    X_names = ("age", "educ", "black", "hisp", "married", "nodegree", "re74", "re75")

    def reg(mask_t, mask_c):
        m = mask_t | mask_c
        X = np.column_stack([np.where(mask_t[m], 1.0, 0.0)] + [d[k][m].astype(float) for k in X_names])
        return em.ols(d["re78"][m], X)

    experiment = float(d["re78"][tr].mean() - d["re78"][ct].mean())
    raw_psid = float(d["re78"][tr].mean() - d["re78"][ps].mean())
    adj_psid = reg(tr, ps)["slope"]
    adj_exp = reg(tr, ct)["slope"]
    pre = {k: (float(d[k][tr].mean()), float(d[k][ct].mean()), float(d[k][ps].mean()))
           for k in ("age", "educ", "black", "married", "nodegree", "re74", "re75")}
    return {"table5": {k: t[k] for k in ("experiment", "PSID-1", "CPS-SSA-1", "PSID-3", "CPS-SSA-3")},
            "experiment": experiment, "experiment_adj": adj_exp, "raw_psid": raw_psid, "adj_psid": adj_psid,
            "n": {"treated": int(tr.sum()), "control": int(ct.sum()), "psid": int(ps.sum())},
            "pre": pre, "earn78": {"treated": float(d["re78"][tr].mean()), "control": float(d["re78"][ct].mean()),
                                   "psid": float(d["re78"][ps].mean())}}


def compute_draft() -> dict:
    d = data.draft1970()
    rank = np.array(d["rank"])
    month = np.array(d["month"])
    day = np.array(d["day"])
    means = [float(rank[month == m].mean()) for m in range(1, 13)]
    rho = float(np.corrcoef(day, rank)[0, 1])
    # a permutation test: how often does a fair shuffle give a correlation this far from zero?
    rng = np.random.default_rng(1969)
    sims = np.array([np.corrcoef(day, rng.permutation(rank))[0, 1] for _ in range(20000)])
    p = float(np.mean(np.abs(sims) >= abs(rho)))
    order = np.argsort(rank)          # the days in the order their capsules were drawn
    return {"day": day, "rank": rank, "month": month, "monthly_mean": means, "rho": rho, "p_perm": p,
            "first": int(day[order[0]]), "draw_order_month": month[order].tolist(),
            "dec_in_first_100": int((month[order[:100]] == 12).sum()),
            "jan_in_first_100": int((month[order[:100]] == 1).sum())}


def compute_credibility() -> dict:
    from explainer.stats import museum

    ck = museum.CARD_KRUEGER
    return {"PA": ck["PA"], "NJ": ck["NJ"], "se_PA": ck["se_PA"], "se_NJ": ck["se_NJ"], "did": ck["did"],
            "se_did": ck["se_did"], "n_NJ": ck["n_NJ"], "n_PA": ck["n_PA"],
            "did_check": em.did(ck["NJ"][0], ck["NJ"][1], ck["PA"][0], ck["PA"][1])}


def compute_experiment() -> dict:
    r = em.apprenticeship(**TRUTH["apprentice"])
    edges = np.linspace(-3.0, 3.0, 25)

    def hist(mask):
        h, _ = np.histogram(np.clip(r["ability"][mask], -2.999, 2.999), bins=edges)
        return (h / mask.sum() / (edges[1] - edges[0])).tolist()

    out = {"edges": edges.tolist(), "effect": r["effect"], "bias": r["bias"], "n": int(len(r["ability"]))}
    for way in ("chose", "lottery"):
        d = r[way]
        out[way] = {"in": hist(d), "out": hist(~d), **r["by_choice" if way == "chose" else "by_lottery"]}
    return out


def compute_nit() -> dict:
    """Budget lines in units of the poverty line: income = max(earnings, G + (1 - t) earnings)."""
    G = [0.5, 0.75, 1.0, 1.25]
    t = [0.3, 0.5, 0.7]
    return {"guarantees": G, "tax_rates": t, "shown": {"G": 1.0, "t": 0.5, "breakeven": 1.0 / 0.5},
            "breakeven": {f"{g}_{r}": g / r for g in G for r in t}}


def compute_lucas() -> dict:
    L = em.lucas_islands(**TRUTH["lucas"])
    c = L["calm"]
    calm = em.ols(L["y"][c], L["pi"][c])
    after = em.ols(L["y"][~c], L["pi"][~c])
    return {"pi": L["pi"], "expected": L["expected"], "y": L["y"], "calm": c, "b": L["b"], "ystar": L["ystar"],
            "calm_slope": calm["slope"], "calm_intercept": float(calm["beta"][0]),
            "after_slope": after["slope"], "predicted_y_at_push": float(calm["beta"][0] + calm["slope"] *
                                                                        TRUTH["lucas"]["pi_push"]),
            "y_push_first": float(L["y"][~c][0]), "y_push_last": float(L["y"][~c][-10:].mean()),
            "years": TRUTH["lucas"]["years"], "pi_push": TRUTH["lucas"]["pi_push"]}


def compute_phillips() -> dict:
    def annual(series):
        d = data.fred(series)
        out: dict[int, list] = {}
        for dt, v in zip(d["date"], d["value"]):
            out.setdefault(int(dt[:4]), []).append(v)
        return {y: float(np.mean(v)) for y, v in out.items() if len(v) == 12}

    u, c = annual("UNRATE"), annual("CPIAUCSL")
    years = list(range(1961, 1980))
    return {"years": years, "u": [u[y] for y in years], "pi": [100 * (c[y] / c[y - 1] - 1) for y in years],
            "cite": data.fred_cite("UNRATE", "CPIAUCSL")}


def compute_power() -> dict:
    """Minimum detectable effect of a two-arm trial with half treated, 5% two-sided size and 80% power:
    MDE = (z_.975 + z_.8) * sigma * sqrt(1 / (p (1 - p) N)), with sigma the spread of log earnings in the
    apprenticeship's lottery sample; checked by simulation at three sizes."""
    from scipy.stats import norm

    r = em.apprenticeship(**TRUTH["apprentice"])
    sigma = float(np.std(r["y_lottery"][~r["lottery"]], ddof=1))
    m = float(norm.ppf(0.975) + norm.ppf(0.8))
    Ns = np.unique(np.round(np.geomspace(100, 20000, 80)).astype(int))
    mde = m * sigma * np.sqrt(1 / (0.25 * Ns))
    # simulated power at the planted effect, from the planted model with fresh draws
    sims = {}
    for N in (400, 1600, 6400):
        rng = np.random.default_rng(N)
        a = dict(TRUTH["apprentice"])
        hits = 0
        reps = 400
        for k in range(reps):
            a["seed"] = int(rng.integers(1 << 30))
            a["n"] = N
            res = em.apprenticeship(**a)["by_lottery"]
            hits += abs(res["diff"] / res["se"]) > norm.ppf(0.975)
        sims[str(N)] = hits / reps
    n_needed = float((m * sigma / TRUTH["apprentice"]["effect"]) ** 2 / 0.25)
    return {"N": Ns.tolist(), "mde": mde.tolist(), "sigma": sigma, "multiplier": m, "sim_power": sims,
            "n_needed": n_needed, "effect": TRUTH["apprentice"]["effect"]}


def compute_villages() -> dict:
    t = TRUTH["villages"]
    r = em.village_trial(**t)
    return {k: r[k] for k in ("within", "within_se", "spill_hat", "total", "means", "truth_total")} | {
        "direct": t["direct"], "spill": t["spill"], "villages": t["villages"], "per_village": t["per_village"],
        "saturations": list(t["saturations"])}


WEAK_K, WEAK_REPS = 60, 400


def compute_weak() -> dict:
    sc = dict(TRUTH["schooling"])
    sc["return_"] = sc.pop("return")
    r = em.schooling_records(**sc)
    real = em.iv(r["logw"], r["school"], r["near"])
    ols = em.ols(r["logw"], r["school"])["slope"]
    rng = np.random.default_rng(1995)
    est, F = [], []
    for _ in range(WEAK_REPS):
        Z = (rng.random((len(r["school"]), WEAK_K)) < 0.5).astype(float)
        res = em.iv(r["logw"], r["school"], Z)
        est.append(res["estimate"])
        F.append(res["F"])
    est, F = np.array(est), np.array(F)
    edges = np.linspace(-0.05, 0.25, 31)
    h, _ = np.histogram(np.clip(est, edges[0] + 1e-9, edges[-1] - 1e-9), bins=edges)
    return {"K": WEAK_K, "reps": WEAK_REPS, "n": int(len(r["school"])), "estimates": est, "F": F,
            "median": float(np.median(est)), "mean": float(np.mean(est)), "F_median": float(np.median(F)),
            "edges": edges.tolist(), "hist": h.tolist(), "ols": ols, "truth": sc["return_"],
            "real": real}


def compute_dial() -> dict:
    rows = tables.CARD_2001.data["rows"]
    return {"rows": [list(r) for r in rows], "ols_range": [min(r[2] for r in rows), max(r[2] for r in rows)],
            "iv_range": [min(r[3] for r in rows), max(r[3] for r in rows)],
            "iv_above": sum(1 for r in rows if r[3] > r[2]), "n": len(rows),
            "mean_ratio": float(np.mean([r[3] / r[2] for r in rows]))}


FILM_SECONDS = 36.0
MELODY_SECONDS = 46.0


def film_time(k: int) -> float:
    """When the data film reaches the k-th capsule drawn (0-based)."""
    return 1.5 + FILM_SECONDS * k / 366


def compute_film() -> dict:
    d = compute_draft()
    order = np.argsort(d["rank"])
    return {"order_day": d["day"][order], "order_month": d["month"][order], "times": [film_time(k) for k in range(366)],
            "monthly_mean": d["monthly_mean"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    months = np.array(f["order_month"], float)
    times = f["times"]
    mel = score.data_melody(months, MELODY_SECONDS, times=times, act=1, log=False, low=55, high=79)
    events = {"film_end": film_time(365) + 1.5, "first": times[0], "hundredth": times[99]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.15, "hz": score.hz(n), "name": str(int(m))}
                       for t, n, m in zip(times, mel["notes"], months)],
                meta={"label": "the 1969 draft lottery as a tune: each birthday drawn, its month as a pitch (computed)",
                      "kind": "synthesized"})
    ClipStore("econ4").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS, "film_seconds": FILM_SECONDS}


ITEMS = {
    "season": compute_season,
    "playit": compute_playit,
    "instrument": compute_instrument,
    "schooling": compute_schooling,
    "lalonde": compute_lalonde,
    "draft": compute_draft,
    "credibility": compute_credibility,
    "experiment": compute_experiment,
    "nit": compute_nit,
    "lucas": compute_lucas,
    "phillips": compute_phillips,
    "dial": compute_dial,
    "weak": compute_weak,
    "power": compute_power,
    "villages": compute_villages,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
