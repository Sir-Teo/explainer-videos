"""Precompute every number in Part 50 of *Psychology, Built* ("The Weight of Evidence").

    python -m videos.psychology.psych50.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych50.compute --force grade

Results are cached in ``.cache/psych50/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.meta``).

Items:
    piles       a simulated drug literature: every registered trial against the published ones
    forest      fifteen simulated studies pooled: fixed and random effects, tau, I-squared, the prediction interval
    moderator   the power of a meta-regression to find a moderator, by number of studies
    funnel      a filtered literature's funnel, Egger's test, PET and PEESE
    grade       every correction method on simulated literatures with a known truth
    kvarven     naive meta-analysis of a filtered literature against a large preregistered replication
    grim        GRIM on five reported means; a SPRITE search
    statcheck   recomputed p-values for six reported tests
    mileage     real-looking against fabricated odometer readings
    specs       a specification curve: 96 analyses of one dataset
    crud        Meehl's paradox: directional predictions confirmed by sample size when everything correlates a little
    audit       the Ledger, by status, act and decade
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import ledger
from explainer.psychology.psyche import meta as M

CACHE = Cache("psych50")
load = CACHE.load


def compute_piles() -> dict:
    lit = M.literature(k=74, true_d=0.3, tau=0.1, n_lo=40, n_hi=160, publish_null=0.35, seed=50)
    pub = lit["published"]
    allre = M.random_effects(lit["d"], lit["v"])
    pubre = M.random_effects(lit["d"][pub], lit["v"][pub])
    return {"d": lit["d"], "se": lit["se"], "sig": lit["significant"].astype(int), "pub": pub.astype(int),
            "k": 74, "k_sig": int(lit["significant"].sum()), "k_pub": int(pub.sum()),
            "k_pub_sig": int((pub & lit["significant"]).sum()), "all_mu": allre["mu"], "pub_mu": pubre["mu"]}


def compute_forest() -> dict:
    lit = M.literature(k=15, true_d=0.4, tau=0.15, n_lo=20, n_hi=120, publish_null=1.0, seed=5001)
    re = M.random_effects(lit["d"], lit["v"])
    hk = M.random_effects(lit["d"], lit["v"], hk=True)
    return {"d": lit["d"], "se": lit["se"], "n": lit["n"], **{k: re[k] for k in ("mu", "lo", "hi", "tau", "I2",
                                                                                   "fixed", "pi_lo", "pi_hi")},
            "se_re": re["se"], "hk_lo": hk["lo"], "hk_hi": hk["hi"]}


def compute_moderator() -> dict:
    ks = np.array([10, 20, 40, 80, 160])
    return {"k": ks, "power": np.array([M.moderator_power(int(k), 0.2, reps=300, seed=5002 + int(k)) for k in ks])}


def compute_funnel() -> dict:
    lit = M.literature(k=300, true_d=0.2, tau=0.1, publish_null=0.15, hack=0.3, seed=5003)
    pub = lit["published"]
    y, se = lit["d"][pub], lit["se"][pub]
    e = M.egger(y, se)
    p = M.pet(y, se)
    return {"y": y, "se": se, "all_y": lit["d"], "all_se": lit["se"], "egger_p": e["p"], "egger_int": e["intercept"],
            "pet": p["est"], "peese": M.peese(y, se)["est"], "naive": M.random_effects(y, lit["v"][pub])["mu"],
            "k": int(pub.sum()), "true": 0.2}


def compute_grade() -> dict:
    scen = [(0.0, 0.0, 0.1, 0.0), (0.2, 0.1, 0.1, 0.0), (0.5, 0.1, 0.1, 0.0), (0.2, 0.3, 0.1, 0.0),
            (0.0, 0.0, 0.1, 0.5), (0.2, 0.1, 1.0, 0.0)]
    g = M.grade(scen, reps=50, k=150, seed=5004)
    names = ["no effect, filter", "small effect, filter", "medium effect, filter", "small, heterogeneous, filter",
             "no effect, filter + p-hacking", "small effect, no filter"]
    means = np.array([[r[m][0] for m in g["methods"]] for r in g["rows"]])
    rmse = np.array([[r[m][1] for m in g["methods"]] for r in g["rows"]])
    return {"methods": g["methods"], "scenarios": names, "true": np.array([s[0] for s in scen]), "mean": means,
            "rmse": rmse}


def compute_kvarven() -> dict:
    """Ten effects, each with a filtered literature (true d drawn small) and a large preregistered replication."""
    rng = np.random.default_rng(5005)
    true = rng.uniform(0.0, 0.25, 10)
    meta, rep = [], []
    for i, d in enumerate(true):
        lit = M.literature(k=60, true_d=float(d), tau=0.1, publish_null=0.1, seed=5100 + i)
        pub = lit["published"]
        meta.append(M.random_effects(lit["d"][pub], lit["v"][pub])["mu"])
        n = 1500
        rep.append(rng.normal(d, np.sqrt(2 / n)))
    meta, rep = np.array(meta), np.array(rep)
    return {"true": true, "meta": meta, "rep": rep, "ratio": float(meta.mean() / rep.mean())}


def compute_grim() -> dict:
    reports = [(5.19, 28), (3.45, 20), (4.68, 15), (2.17, 12), (6.33, 21)]
    ok = [M.grim(m, n) for m, n in reports]
    sp = M.sprite(3.5, 1.5, 20, 1, 7, tries=20000, seed=1)
    sp2 = M.sprite(3.5, 1.0, 20, 1, 7, tries=20000, seed=1)
    return {"means": np.array([r[0] for r in reports]), "ns": np.array([r[1] for r in reports]),
            "ok": np.array(ok, int), "sprite": sp if sp is not None else np.zeros(20),
            "sprite2": sp2 if sp2 is not None else np.zeros(20)}


def compute_statcheck() -> dict:
    reports = [(2.10, 28, 0.04, "="), (1.80, 30, 0.04, "="), (2.50, 40, 0.05, "<"), (3.20, 18, 0.005, "="),
               (2.02, 60, 0.048, "="), (1.70, 25, 0.10, "=")]
    out = M.statcheck(reports)
    return {"t": np.array([r[0] for r in reports]), "df": np.array([r[1] for r in reports]),
            "reported": np.array([r[2] for r in reports]), "rel": [r[3] for r in reports],
            "recomputed": np.array([o["recomputed"] for o in out]), "consistent": np.array([o["consistent"] for o in out], int),
            "gross": np.array([o["gross"] for o in out], int)}


def compute_mileage() -> dict:
    """Odometer differences between two readings: real driving gives a right-skewed spread with few very large
    values; numbers drawn uniformly between 0 and 50,000 give a flat histogram with a hard edge."""
    rng = np.random.default_rng(5006)
    real = rng.gamma(2.0, 6500, 6000)
    fake = rng.uniform(0, 50000, 6000)
    edges = np.linspace(0, 60000, 25)
    return {"edges": edges, "real": np.histogram(real, edges)[0], "fake": np.histogram(fake, edges)[0],
            "real_over": float(np.mean(real > 50000)), "fake_over": float(np.mean(fake > 50000))}


def compute_specs() -> dict:
    return M.spec_curve(seed=5007)


def compute_crud() -> dict:
    """Meehl's paradox: every pair of variables correlates a little (r ~ N(0, 0.15)); a weak theory predicts only a
    direction, right half the time by luck.  Share of 'confirmed' predictions (significant in the predicted
    direction) by sample size."""
    rng = np.random.default_rng(5008)
    ns = np.array([30, 100, 300, 1000, 3000, 10000])
    out = []
    for n in ns:
        r = rng.normal(0, 0.15, 4000)
        pred = rng.choice([-1, 1], 4000)
        z = np.arctanh(r) + rng.normal(0, 1 / np.sqrt(n - 3), 4000)
        out.append(float(np.mean((np.abs(z) * np.sqrt(n - 3) > 1.96) & (np.sign(z) == pred))))
    return {"n": ns, "confirmed": np.array(out)}


def compute_audit() -> dict:
    rows = ledger.rows(upto=49)
    a = M.ledger_audit(rows)
    statuses = list(a["total"])
    acts = [x[2] for x in M.ACTS if x[2] in a["by_act"]]
    decs = [d for d in a["by_decade"] if d >= 1850]
    return {"statuses": statuses, "total": np.array([a["total"][s] for s in statuses]), "n": a["n"], "acts": acts,
            "by_act": np.array([[a["by_act"][x][s] for s in statuses] for x in acts]), "decades": np.array(decs),
            "by_decade": np.array([[a["by_decade"][d][s] for s in statuses] for d in decs])}


ITEMS = {"piles": compute_piles, "forest": compute_forest, "moderator": compute_moderator, "funnel": compute_funnel,
         "grade": compute_grade, "kvarven": compute_kvarven, "grim": compute_grim, "statcheck": compute_statcheck,
         "mileage": compute_mileage, "specs": compute_specs, "crud": compute_crud, "audit": compute_audit}

if __name__ == "__main__":
    CACHE.main(ITEMS)
