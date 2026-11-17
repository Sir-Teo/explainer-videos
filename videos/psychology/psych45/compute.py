"""Precompute every number in Part 45 of *Psychology, Built* ("Item Response Theory").

    python -m videos.psychology.psych45.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych45.compute --force cat

Results are cached in ``.cache/psych45/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.irt``), checked against ltm's published fits in ``tests/psychology/test_irt.py``.

Items:
    classical   one set of 10 items given to a weaker and a stronger group (2,000 simulated people each): the items'
                proportions correct in each group against their fixed difficulties; two people of equal ability
                taking an easy and a hard form; the classical SE (one number) against the IRT SE by ability
    lsat        the LSAT's five items, 1,000 people: Rasch and 2PL fits by marginal ML (EM), the likelihood-ratio
                test, the conditional ML difficulties, and the probability of each 2-correct pattern given its
                score at three abilities
    em          EM's log-likelihood on the LSAT by cycle; ability by sum score (EAP, posterior SD, ML)
    info        item and test information of the LSAT's 2PL items, and the standard error by ability
    cat         a bank of 300 simulated 2PL items and 1,000 simulated people: an adaptive test stopping at SE 0.3,
                against fixed forms of 5 to 60 items; one example path
    grm         four attitude items (1992 Eurobarometer, British sample, 392 people): the graded response model
    dif         15 items, two groups of 3,000 differing in mean ability by 0.8 SD: Mantel-Haenszel on an item with
                no DIF and on one made 0.8 harder for the focal group
    linking     two 30-item forms sharing 10 anchors, each calibrated in its own sample: mean-sigma linking, and
                true-score equating through the two test characteristic curves
    pv          a survey of 4,000 students, 4 booklets of 6 items from a pool of 24: EAP, plausible values and the
                truth, for the population's SD and a group gap
    bkt         Bayesian knowledge tracing: 500 simulated students, 10 practice steps; the fitted parameters; one
                student's P(known); Elo for learners and items on the same data
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import irt as I

CACHE = Cache("psych45")
load = CACHE.load


def compute_classical() -> dict:
    rng = np.random.default_rng(45)
    b = np.linspace(-2.0, 2.0, 10)
    weak, strong = rng.normal(-0.7, 1, 2000), rng.normal(0.7, 1, 2000)
    pw = I.simulate(weak, 1.0, b, seed=1).mean(0)
    ps = I.simulate(strong, 1.0, b, seed=2).mean(0)
    easy, hard = np.linspace(-2.5, 0.0, 10), np.linspace(0.0, 2.5, 10)
    exp_easy = float(I.prob(0.5, 1.0, easy).sum())
    exp_hard = float(I.prob(0.5, 1.0, hard).sum())
    th = np.linspace(-3, 3, 61)
    se_irt = I.fixed_form_se(th, 1.0, b)
    X = I.simulate(rng.normal(size=4000), 1.0, b, seed=3)
    s = X.sum(1)
    k = len(b)
    pq = X.mean(0) * (1 - X.mean(0))
    alpha = k / (k - 1) * (1 - pq.sum() / s.var())
    sem_raw = s.std() * np.sqrt(1 - alpha)
    return {"b": b, "p_weak": pw, "p_strong": ps, "exp_easy": exp_easy, "exp_hard": exp_hard, "th": th,
            "se_irt": se_irt, "alpha": float(alpha), "sem_raw": float(sem_raw), "sd_raw": float(s.std())}


def compute_lsat() -> dict:
    X = opendata.lsat_1000()["X"]
    r = I.fit_mml(X, "rasch")
    t = I.fit_mml(X, "2pl")
    c = I.fit_cml(X)
    lr = 2 * (t["loglik"] - r["loglik"])
    from scipy import stats
    pats = [np.array(p) for p in ([1, 1, 0, 0, 0], [0, 0, 1, 1, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0])]
    bc = c["b"]
    pg = {}
    for th in (-2.0, 0.0, 2.0):
        P = I.prob(th, 1.0, bc)[0]
        # all patterns with two right
        import itertools
        allp = [np.array(q) for q in itertools.product([0, 1], repeat=5) if sum(q) == 2]
        L = np.array([np.prod(np.where(q == 1, P, 1 - P)) for q in allp])
        pg[th] = [float(np.prod(np.where(p == 1, P, 1 - P)) / L.sum()) for p in pats]
    return {"p": X.mean(0), "n": len(X), "rasch_a": r["a"][0], "rasch_b": r["b"], "rasch_ll": r["loglik"],
            "twopl_a": t["a"], "twopl_b": t["b"], "twopl_ll": t["loglik"], "lr": float(lr),
            "lr_p": float(stats.chi2.sf(lr, 4)), "cml_b": bc, "cml_n": c["n_used"],
            "pg_m2": np.array(pg[-2.0]), "pg_0": np.array(pg[0.0]), "pg_2": np.array(pg[2.0]),
            "scores": np.bincount(X.sum(1).astype(int), minlength=6)}


def compute_em() -> dict:
    """EM's climb on the LSAT (two-parameter model): the log-likelihood after 1 to 40 cycles; and ability by sum
    score under the Rasch fit: EAP, posterior SD and the maximum-likelihood estimate (infinite at 0 and 5)."""
    X = opendata.lsat_1000()["X"]
    trace = [I.fit_mml(X, "2pl", iters=k, tol=-1)["loglik"] for k in range(1, 41)]
    d = load("lsat")
    pats = np.array([[1] * r + [0] * (5 - r) for r in range(6)], float)
    e = I.eap(pats, d["rasch_a"], d["rasch_b"])
    mle = [I.mle_theta(p, d["rasch_a"], d["rasch_b"], lo=-8, hi=8) for p in pats]
    W = e["W"]
    return {"trace": np.array(trace), "eap": e["theta"], "sd": e["sd"], "mle": np.array(mle), "post": W,
            "nodes": I.NODES}


def compute_info() -> dict:
    d = load("lsat")
    th = np.linspace(-6, 4, 201)
    Ii = I.info(th, d["twopl_a"], d["twopl_b"])
    return {"th": th, "item": Ii, "test": Ii.sum(1), "se": 1 / np.sqrt(Ii.sum(1))}


def _bank(seed=45, n=300):
    rng = np.random.default_rng(seed)
    return np.exp(rng.normal(0.2, 0.25, n)), rng.uniform(-3, 3, n)


def compute_cat() -> dict:
    a, b = _bank()
    rng = np.random.default_rng(46)
    people = rng.normal(size=1000)
    n_items, est, se = [], [], []
    for i, t in enumerate(people):
        r = I.cat(float(t), a, b, stop_se=0.3, max_items=60, seed=1000 + i)
        n_items.append(len(r["items"]))
        est.append(r["theta"])
        se.append(r["se"])
    n_items, est = np.array(n_items), np.array(est)
    # fixed forms: the k items most informative at 0 (the best fixed form for an average person), and a random form
    lengths = np.arange(5, 61, 5)
    best = np.argsort(-I.info(0.0, a, b)[0])
    fixed_best, fixed_rand = [], []
    order_rand = np.random.default_rng(47).permutation(len(b))
    for k in lengths:
        for idx, out in ((best[:k], fixed_best), (order_rand[:k], fixed_rand)):
            X = I.simulate(people, a[idx], b[idx], seed=int(k))
            e = I.eap(X, a[idx], b[idx])
            out.append(float(np.sqrt(np.mean((e["theta"] - people) ** 2))))
    cat_rmse = float(np.sqrt(np.mean((est - people) ** 2)))
    ex = I.cat(1.3, a, b, stop_se=0.3, max_items=60, seed=7)
    return {"a": a, "b": b, "people": people, "n_items": n_items, "mean_items": float(n_items.mean()),
            "cat_rmse": cat_rmse, "lengths": lengths, "fixed_best": np.array(fixed_best),
            "fixed_rand": np.array(fixed_rand), "ex_items": np.array(ex["items"]), "ex_path": ex["path"],
            "ex_ses": ex["ses"], "ex_resp": ex["responses"], "ex_true": 1.3,
            "max_exposure": float(np.bincount(np.concatenate([I.cat(float(t), a, b, 0.0, 0.3, 60, seed=2000 + i)["items"]
                                                              for i, t in enumerate(people[:200])]),
                                              minlength=len(b)).max() / 200)}


def compute_grm() -> dict:
    s = opendata.science_attitudes()
    cols = [0, 2, 3, 6]
    Y = s["Y"][:, cols]
    g = I.fit_grm(Y, 4)
    th = np.linspace(-4, 4, 161)
    curves = np.stack([I.grm_prob(th, g["a"][j], g["B"][j]) for j in range(len(cols))])
    return {"names": [s["names"][c] for c in cols], "levels": s["levels"], "a": g["a"], "B": g["B"],
            "loglik": g["loglik"], "th": th, "curves": curves, "n": len(Y),
            "counts": np.stack([np.bincount(Y[:, j], minlength=4) for j in range(len(cols))])}


def compute_dif() -> dict:
    rng = np.random.default_rng(48)
    g = np.repeat([0, 1], 3000)
    th = rng.normal(size=6000) - 0.8 * g
    b = np.linspace(-1.5, 1.5, 15)
    X = I.simulate(th, 1.0, b, seed=49)
    j = 7
    X2 = X.copy()
    bj = np.where(g == 1, b[j] + 0.8, b[j])
    X2[:, j] = rng.random(6000) < 1 / (1 + np.exp(-(th - bj)))
    none, dif = I.mantel_haenszel(X, g, j), I.mantel_haenszel(X2, g, j)
    # proportion correct by total score, in each group, for the DIF item
    sc = X2.sum(1)
    by = np.array([[X2[(sc == s) & (g == gg), j].mean() if np.sum((sc == s) & (g == gg)) > 20 else np.nan
                    for s in range(16)] for gg in (0, 1)])
    by0 = np.array([[X[(X.sum(1) == s) & (g == gg), j].mean() if np.sum((X.sum(1) == s) & (g == gg)) > 20 else np.nan
                     for s in range(16)] for gg in (0, 1)])
    return {"none": none, "dif": dif, "gap_none": I.raw_gap(X, g, j), "gap_dif": I.raw_gap(X2, g, j),
            "by_score_dif": by, "by_score_none": by0, "impact": 0.8, "shift": 0.8}


def compute_linking() -> dict:
    rng = np.random.default_rng(50)
    b_all = rng.uniform(-2.5, 2.5, 50)
    anchors = np.arange(10)
    form_x = np.concatenate([anchors, np.arange(10, 30)])
    form_y = np.concatenate([anchors, np.arange(30, 50)])
    th_x, th_y = rng.normal(0, 1, 2000), rng.normal(0.5, 1.2, 2000)  # this year's group is abler and more varied
    fx = I.fit_mml(I.simulate(th_x, 1.0, b_all[form_x], seed=51), "rasch")
    fy = I.fit_mml(I.simulate(th_y, 1.0, b_all[form_y], seed=52), "rasch")
    bx, by = fx["b"] * fx["a"][0], fy["b"] * fy["a"][0]  # on each sample's own N(0, 1)-of-ability scale, times a
    bx_raw, by_raw = fx["b"], fy["b"]
    A, B = I.mean_sigma(by_raw[:10], bx_raw[:10])
    linked = A * by_raw + B
    # true-score equating: each form's test characteristic curve on last year's scale (Rasch, slope a_x)
    ax = fx["a"][0]
    th = np.linspace(-4, 4, 401)
    tcc_x = I.prob(th, ax, bx_raw).sum(1)
    tcc_y = I.prob(th, ax, linked).sum(1)
    scores = np.array([6, 10, 15, 20, 24])
    eq = np.interp(np.interp(scores, tcc_y, th), th, tcc_x)
    return {"b_true": b_all, "bx": bx_raw, "by": by_raw, "A": A, "B": B, "linked": linked, "th": th,
            "tcc_x": tcc_x, "tcc_y": tcc_y, "scores": scores, "equated": eq,
            "err_before": float(np.sqrt(np.mean((by_raw[10:] - b_all[30:] - (bx_raw[:10] - b_all[:10]).mean()) ** 2))),
            "err_after": float(np.sqrt(np.mean((linked[10:] - (bx_raw[:10] - b_all[:10]).mean() - b_all[30:]) ** 2))),
            "anchor_x": bx_raw[:10], "anchor_y": by_raw[:10], "true_shift": 0.5, "true_scale": 1.2}


def compute_pv() -> dict:
    rng = np.random.default_rng(53)
    n = 4000
    grp = rng.integers(0, 2, n)
    th = rng.normal(0, 1, n) + 0.4 * (grp - 0.5)
    b = np.linspace(-2, 2, 24)
    X = I.simulate(th, 1.0, b, seed=54)
    booklet = rng.integers(0, 4, n)
    mask = np.zeros_like(X, bool)
    for k in range(4):
        mask[booklet == k, k::4] = True
    Xs = np.where(mask, X, np.nan)
    e = I.eap(Xs, 1.0, b)
    pv = I.plausible_values(Xs, 1.0, b, m=5, seed=55)
    cm = I.latent_em(Xs, 1.0, b, grp)
    pvc = I.plausible_values(Xs, 1.0, b, m=5, seed=56, mu=cm["mu"][grp], sd=cm["sd"][grp])
    gap = lambda v: float(v[grp == 1].mean() - v[grp == 0].mean())  # noqa: E731
    return {"true_sd": float(th.std()), "eap_sd": float(e["theta"].std()), "pv_sd": float(pv.std(0).mean()),
            "pvc_sd": float(pvc.std(0).mean()), "pvc_gap": float(np.mean([gap(pvc[:, m]) for m in range(5)])),
            "cond_mu": cm["mu"], "cond_sd": cm["sd"],
            "true_gap": gap(th), "eap_gap": gap(e["theta"]), "pv_gap": float(np.mean([gap(pv[:, m]) for m in range(5)])),
            "eap_hist": np.histogram(e["theta"], bins=np.linspace(-4, 4, 33))[0],
            "pv_hist": np.histogram(pv[:, 0], bins=np.linspace(-4, 4, 33))[0],
            "true_hist": np.histogram(th, bins=np.linspace(-4, 4, 33))[0], "items_each": 6, "pool": 24}


def compute_bkt() -> dict:
    truth = {"L0": 0.2, "T": 0.15, "G": 0.2, "S": 0.1}
    Y, K = I.bkt_simulate(500, 10, **truth, seed=56)
    f = I.bkt_fit(Y)
    i = 3
    y = Y[i]
    filt = I.bkt_filter(y, f["L0"], f["T"], f["G"], f["S"])
    # Elo on the same answers: every student meets items of one skill; item difficulty from step
    person = np.repeat(np.arange(500), 10)
    item = np.tile(np.arange(10), 500)
    th, bb = I.elo_learn(person, item, Y.ravel(), 500, 10, k=0.3)
    return {"truth": truth, "fit": f, "y": y, "known_true": K[i].astype(float), "p_known": filt["known"],
            "p_correct": filt["correct"], "acc_by_step": Y.mean(0), "elo_items": bb,
            "known_by_step": K.mean(0)}


ITEMS = {"classical": compute_classical, "lsat": compute_lsat, "em": compute_em, "info": compute_info, "cat": compute_cat,
         "grm": compute_grm, "dif": compute_dif, "linking": compute_linking, "pv": compute_pv, "bkt": compute_bkt}

if __name__ == "__main__":
    CACHE.main(ITEMS)
