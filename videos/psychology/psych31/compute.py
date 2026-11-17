"""Precompute every number in Part 31 of *Psychology, Built* ("The Lifespan").

    python -m videos.psychology.psych31.compute            # everything missing (under a minute)
    python -m videos.psychology.psych31.compute --force growth

Results are cached in ``.cache/psych31/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.lifespan``).  Published numbers are quoted in the scenes with their sources; curves
marked illustrative have the published shape, not fitted values.  Simulations use fixed seeds.

Items:
    apc         the identity age = period - cohort: two sets of linear effects that predict the same scores; the
                three Lexis tables of the part's "On you"
    designs     one simulated population, three designs: cross-sectional, longitudinal with practice and
                drop-out, and cohort-sequential, against the true ageing curve
    growth      120 children on five visits: the mixed model's fixed line, spreads, correlation, BLUPs
    windows     illustrative plasticity curves for a window that closes in infancy and one that closes at 17
    adolescence the dual-systems curves; chronotype's latest point from the archive
    parents     ACE correlations in childhood and adulthood, and simulated sibling pairs
    wordgap     one hour a month against a whole day: how well each estimates a family's talk
    programmes  an illustrative fade-out, Perry's age-40 numbers, and the familywise error of many outcomes
    ageing      illustrative adult curves for speed, reasoning and vocabulary; the longitudinal masking of decline
    reserve     the threshold model of reserve for three reserves; attributable fractions
    flynn       the inflation of IQ scored on old norms
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import lifespan as L

CACHE = Cache("psych31")
load = CACHE.load


def compute_apc() -> dict:
    ages = np.arange(20.0, 81.0, 5.0)
    period = 1950.0 + ages  # one cohort, born 1950, followed through life
    out = {"ages": ages}
    for k in (0.0, 0.01, -0.01):
        r = L.apc_equivalent(0.0, 0.01, 0.0, k, ages, period)
        out[f"y_{k:+.2f}"] = r["y2"] - r["y1"][0]
        out[f"diff_{k:+.2f}"] = r["max_diff"]
    for kind in ("age", "period", "cohort"):
        t = L.lexis(kind)
        out[f"lexis_{kind}"] = t["table"]
    t = L.lexis("age")
    out["lexis_ages"], out["lexis_periods"] = t["ages"], t["periods"]
    return out


def compute_designs() -> dict:
    w = L.ability_world(n=40_000)
    cs = L.cross_sectional(w)
    lo = L.longitudinal(w)
    cq = L.cohort_sequential(w)
    grid = np.arange(20, 91, 1.0)
    return {"cs_age": cs["age"], "cs_mean": cs["mean"] - cs["mean"][0],
            "lo_age": lo["age"], "lo_kept": lo["kept"] - lo["kept"][0], "lo_every": lo["everyone"] - lo["everyone"][0],
            "lo_n": lo["n"], "cq_age": cq["age"], "cq_curve": cq["curve"], "cq_gain": cq["cohort_gain_hat"],
            "grid": grid, "truth": L.true_ageing(grid), "gain": w["cohort_gain"]}


def compute_growth() -> dict:
    g = L.growth_data(n=120, seed=4)
    f = L.fit_growth(g["t"], g["y"], iters=300)
    pick = np.arange(12)
    return {"t": g["t"], "y": g["y"][pick], "beta": f["beta"], "sd_int": f["sd_int"], "sd_slope": f["sd_slope"],
            "rho": f["rho"], "sd_e": f["sd_e"], "blup": f["blup"], "ols": f["ols"], "true": g["b_true"] + g["beta"],
            "n_children": 120, "n_obs": int(np.sum(~np.isnan(g["y"]))),
            "sd_ols": float(np.nanstd(f["ols"][:, 1])), "sd_blup": float(np.std(f["blup"][:, 1])),
            "sd_true": float(np.std(g["b_true"][:, 1]))}


def compute_windows() -> dict:
    weeks = np.linspace(0, 20, 201)
    early = (weeks / 4.5) ** 2 * np.exp(-(weeks - 4.5) / 2.25)  # illustrative: peak in week 4 to 5, gone by ~15
    t_lang = np.linspace(0, 40, 161)
    lang = L.plasticity(t_lang, close=21.0, width=1.5, floor=0.35)  # near its peak to about 17, then down
    return {"weeks": weeks, "early": early / early.max(), "t_lang": t_lang, "lang": lang}


def compute_adolescence() -> dict:
    a = np.linspace(10, 30, 201)
    d = L.dual_systems(a)
    r = archive.ROENNEBERG_2004.data
    return {"age": a, "seeking": d["seeking"], "regulation": d["regulation"], "gap": d["gap"],
            "gap_peak": float(a[np.argmax(d["gap"])]), "late_women": r["latest_women"], "late_men": r["latest_men"]}


def compute_parents() -> dict:
    rng = np.random.default_rng(31)
    out = {}
    for stage, (h2, c2) in {"child": (0.4, 0.3), "adult": (0.6, 0.0)}.items():
        th = L.sibling_correlations(h2, c2)
        out[f"{stage}_theory"] = [th["mz"], th["dz"], th["adoptive"]]
        sims = []
        for share in (1.0, 0.5, 0.0):
            n = 300
            a = rng.normal(size=n)
            g1 = np.sqrt(h2) * a
            g2 = np.sqrt(h2) * (share * a + np.sqrt(1 - share ** 2) * rng.normal(size=n))
            c = rng.normal(size=n) * np.sqrt(c2)
            e = np.sqrt(1 - h2 - c2)
            x1 = g1 + c + e * rng.normal(size=n)
            x2 = g2 + c + e * rng.normal(size=n)
            sims.append(float(np.corrcoef(x1, x2)[0, 1]))
        out[f"{stage}_sim"] = sims
        out[f"{stage}_h2"], out[f"{stage}_c2"] = h2, c2
    return out


def compute_wordgap() -> dict:
    h = L.hour_sampling(n_families=42, seed=6)
    return {k: h[k] for k in ("true", "one_hour", "one_day", "r_hour", "r_day")}


def compute_programmes() -> dict:
    yrs = np.linspace(0, 6, 61)
    m = np.arange(1, 61)
    return {"years": yrs, "fade": L.fade_out(yrs), "m": m, "fwer": L.familywise(m),
            "fwer10": float(L.familywise(10)), "fwer30": float(L.familywise(30))}


def compute_ageing() -> dict:
    a = np.linspace(20, 90, 141)
    f = L.fluid_crystallized(a)
    return {"age": a, **f}


def compute_reserve() -> dict:
    a = np.linspace(50, 95, 181)
    out = {"age": a}
    for i, r in enumerate((0.5, 1.0, 2.0)):
        x = L.reserve(a, r)
        out[f"cog{i}"], out[f"onset{i}"] = x["cognition"], x["onset"]
        out["pathology"] = x["pathology"]
    out["reserves"] = [0.5, 1.0, 2.0]
    out["paf_example"] = L.paf(0.3, 1.9)
    out["paf_sum"] = 0.07 + 0.07 + 0.05 + 0.05
    out["paf_combined"] = L.combined_paf([0.07, 0.07, 0.05, 0.05])
    return out


def compute_flynn() -> dict:
    y = np.linspace(0, 30, 31)
    return {"years": y, "score": L.flynn_norms(y), "at15": float(L.flynn_norms(15))}


ITEMS = {"apc": compute_apc, "designs": compute_designs, "growth": compute_growth, "windows": compute_windows,
         "adolescence": compute_adolescence, "parents": compute_parents, "wordgap": compute_wordgap,
         "programmes": compute_programmes, "ageing": compute_ageing, "reserve": compute_reserve,
         "flynn": compute_flynn}


if __name__ == "__main__":
    CACHE.main(ITEMS)
