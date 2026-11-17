"""Precompute every number in Part 46 of *Psychology, Built* ("Scaling, Surveys and Choice").

    python -m videos.psychology.psych46.compute            # everything missing (a minute)
    python -m videos.psychology.psych46.compute --force decoy

Results are cached in ``.cache/psych46/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.scaling``), tested in ``tests/psychology/test_scaling.py``.

Items:
    veg         Guilford's paired comparisons of nine vegetables: the proportions, Thurstone's Case V scale, the
                Bradley-Terry strengths by MM, and how well each model reproduces the proportions
    gumbel      random utility with Gumbel noise against the logit formula, for three options
    redbus      a car and a bus, then a second bus identical to the first: the logit's prediction against
                correlated noise (the truth when the buses are the same)
    decoy       the pairwise-comparison sampler: two options, then a decoy for each, then an extreme option for
                each, at short and long deliberation
    conjoint    a choice-based conjoint study of a phone (price, battery, camera, brand): 600 simulated people with
                varying part-worths, 12 tasks each; the conditional logit's part-worths and willingness to pay, and
                a market simulation
    points      the correlation of a rating with the latent attitude, by number of points
    acq         acquiescence: two unrelated traits, scales keyed all one way or balanced, with and without the style
    careless    straightlining: alpha and a correlation between scales as the share of careless respondents grows
    nps         the net promoter score's standard error by sample size, against the mean rating's, in comparable
                units; the information lost by collapsing 0-10 into three groups
    judges      Thurstone's scale recovered from 5 to 400 judges
    arena       a leaderboard of 20 entrants from 50 to 3,200 random votes, fitted by Bradley-Terry
    wtp_n       willingness to pay from conjoint studies of 50 to 800 people
    checks      instructed-response attention checks: random responders caught, attentive people excluded
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import scaling as Sc

CACHE = Cache("psych46")
load = CACHE.load


def compute_veg() -> dict:
    d = opendata.vegetables_guilford()
    P = d["P"]
    th = Sc.thurstone_scale(P * 100)
    bt = Sc.btl_fit(P * 100)
    from scipy import stats
    Pt = stats.norm.cdf(th[:, None] - th[None, :])
    Pb = Sc.btl_probs(bt["v"])
    off = ~np.eye(9, dtype=bool)
    return {"names": d["names"], "P": P, "thurstone": th, "btl": bt["log"] - bt["log"].mean(),
            "err_thurstone": float(np.abs(Pt - P)[off].mean()), "err_btl": float(np.abs(Pb - P)[off].mean()),
            "max_err_thurstone": float(np.abs(Pt - P)[off].max()), "btl_iters": bt["iters"],
            "corr": float(np.corrcoef(th, bt["log"])[0, 1]), "slope": float(np.polyfit(th, bt["log"], 1)[0])}


def compute_gumbel() -> dict:
    V = np.array([0.0, 0.5, 1.0])
    return {"V": V, "sim": Sc.gumbel_choice_shares(V, n=400_000, seed=46), "logit": Sc.logit_probs(V)}


def compute_redbus() -> dict:
    two = Sc.logit_probs([0.0, 0.0])
    three = Sc.logit_probs([0.0, 0.0, 0.0])
    truth = Sc.normal_choice_shares([0.0, 0.0, 0.0], [[1, 0, 0], [0, 1, 0.999], [0, 0.999, 1]], n=400_000, seed=47)
    return {"two": two, "logit3": three, "truth3": truth}


def compute_decoy() -> dict:
    A, B = [6, 4], [4, 6]
    sets = {"pair": [A, B], "decoy_A": [A, B, [5.5, 3.5]], "decoy_B": [A, B, [3.5, 5.5]],
            "extreme_A": [A, B, [2, 8]], "extreme_B": [A, B, [8, 2]]}
    out = {}
    for steps in (5, 40):
        for k, opts in sets.items():
            out[f"{k}_{steps}"] = Sc.pairwise_sampler(opts, steps=steps, n=60_000, noise=0.1, seed=48)
    out["steps_grid"] = np.array([2, 5, 10, 20, 40, 80])
    out["comp_by_steps"] = np.array([Sc.pairwise_sampler(sets["extreme_B"], steps=s, n=40_000, noise=0.1, seed=49)[0]
                                     for s in out["steps_grid"]])
    out["decoy_by_steps"] = np.array([Sc.pairwise_sampler(sets["decoy_A"], steps=s, n=40_000, noise=0.1, seed=50)[0]
                                      for s in out["steps_grid"]])
    return out


def compute_conjoint() -> dict:
    levels = [3, 2, 2, 3]  # price ($400, $600, $800), battery (1 day, 2 days), camera (good, great), brand (A, B, C)
    price = {0: [4.0, 6.0, 8.0]}  # in hundreds of dollars, linear
    design = Sc.conjoint_design(levels, 300, 3, seed=46)
    X = Sc.dummy_code(design, levels, numeric=price)
    names = [r"price (per \$100)", "two-day battery", "great camera", "brand B", "brand C"]
    beta = np.array([-0.6, 0.9, 0.5, 0.3, -0.2])
    sd = np.array([0.2, 0.5, 0.4, 0.4, 0.4])
    Xs, ys = Sc.simulate_conjoint(X, beta, sd, 600, seed=47)
    f = Sc.fit_clogit(Xs, ys)
    wtp = -100 * f["b"][1:] / f["b"][0]
    # a market: three products, shares under the fitted logit
    market = np.array([[6.0, 1, 0, 0, 0], [8.0, 1, 1, 1, 0], [4.0, 0, 0, 0, 1]])
    shares = Sc.logit_probs(market @ f["b"])
    market2 = market.copy()
    market2[0, 0] = 5.0  # the first product cut to $500
    shares2 = Sc.logit_probs(market2 @ f["b"])
    return {"names": names, "true": beta, "est": f["b"], "se": f["se"], "wtp": wtp, "wtp_true": -100 * beta[1:] / beta[0],
            "shares": shares, "shares_cut": shares2, "n_tasks": len(ys), "n_people": 600}


def compute_points() -> dict:
    rng = np.random.default_rng(46)
    z = rng.standard_normal(200_000)
    out = {}
    from scipy import stats
    for k in (2, 3, 4, 5, 7, 11):
        cuts = stats.norm.ppf(np.arange(1, k) / k)
        r = np.searchsorted(cuts, z)
        out[k] = float(np.corrcoef(r, z)[0, 1])
    return {"k": np.array(list(out)), "r": np.array(list(out.values()))}


def compute_acq() -> dict:
    rng = np.random.default_rng(47)
    n = 20_000
    t1, t2, style = rng.standard_normal((3, n))
    pos, bal = [1] * 6, [1, -1] * 3
    out = {}
    for name, keys in (("pos", pos), ("bal", bal)):
        for sl in (0.0, 0.4):
            a = Sc.styled_answers(t1, style, keys, style_loading=sl, seed=1).sum(1)
            b = Sc.styled_answers(t2, style, keys, style_loading=sl, seed=2).sum(1)
            out[f"{name}_{int(sl * 10)}"] = float(np.corrcoef(a, b)[0, 1])
    return out


def compute_careless() -> dict:
    rng = np.random.default_rng(48)
    n = 5000
    t1 = rng.standard_normal(n)
    t2 = 0.3 * t1 + np.sqrt(1 - 0.09) * rng.standard_normal(n)
    style = np.zeros(n)
    A = Sc.styled_answers(t1, style, [1] * 6, style_loading=0.0, seed=3)
    B = Sc.styled_answers(t2, style, [1] * 6, style_loading=0.0, seed=4)
    shares = np.array([0.0, 0.05, 0.1, 0.2, 0.3])
    alpha, r = [], []
    for sh in shares:
        AB = Sc.straightline(np.hstack([A, B]), sh, seed=5)
        a, b = AB[:, :6], AB[:, 6:]
        C = np.corrcoef(a.T)
        rb = C[np.triu_indices(6, 1)].mean()
        alpha.append(float(6 * rb / (1 + 5 * rb)))
        r.append(float(np.corrcoef(a.sum(1), b.sum(1))[0, 1]))
    return {"shares": shares, "alpha": np.array(alpha), "r": np.array(r), "true_r": 0.3}


def compute_nps() -> dict:
    rng = np.random.default_rng(49)
    # a population's 0-10 ratings: a latent satisfaction cut at fixed points
    z = rng.standard_normal(200_000)
    cuts = np.array([-2.3, -1.9, -1.5, -1.2, -0.9, -0.6, -0.2, 0.25, 0.75, 1.3])
    ratings = np.searchsorted(cuts, z)
    out = {"nps": Sc.nps(ratings), "mean": float(ratings.mean()), "sd": float(ratings.std()),
           "share_promoters": float(np.mean(ratings >= 9)), "share_detractors": float(np.mean(ratings <= 6)),
           "hist": np.bincount(ratings, minlength=11) / len(ratings)}
    ns = np.array([50, 100, 200, 400, 1000])
    se_nps = []
    for n in ns:
        se_nps.append(Sc.nps_se(ratings[:n * 50]) * np.sqrt(n * 50 / n))
    out["ns"], out["se_nps"] = ns, np.array(se_nps)
    # the same two products: how often does each summary rank them correctly from samples of 200?
    z2 = rng.standard_normal(200_000) + 0.15
    r2 = np.searchsorted(cuts, z2)
    wins_nps = wins_mean = 0
    reps = 2000
    for k in range(reps):
        a = ratings[rng.integers(0, len(ratings), 200)]
        b = r2[rng.integers(0, len(r2), 200)]
        wins_nps += Sc.nps(b) > Sc.nps(a)
        wins_mean += b.mean() > a.mean()
    out["right_nps"], out["right_mean"] = wins_nps / reps, wins_mean / reps
    out["nps_b"] = Sc.nps(r2)
    return out


def compute_judges() -> dict:
    """Thurstone's scale from 5 to 400 judges: how far the scale values fall from the truth (RMSE, 100 panels)."""
    s = np.linspace(-1.2, 1.2, 9)
    ns = np.array([5, 10, 25, 50, 100, 400])
    rmse = []
    for n in ns:
        e = []
        for r in range(100):
            W = Sc.simulate_pairs(s, int(n), seed=4600 + 1000 * int(n) + r)
            th = Sc.thurstone_scale(W) * np.sqrt(2)  # back to units of sigma
            e.append(np.sqrt(np.mean((th - (s - s.mean())) ** 2)))
        rmse.append(np.mean(e))
    return {"n": ns, "rmse": np.array(rmse), "spread": float(s.std())}


def compute_arena() -> dict:
    """A leaderboard from random pairwise votes: 20 entrants with Bradley-Terry strengths, votes on random pairs,
    fitted by MM (with half a pseudo-vote each way on every pair so sparse data stay finite); Spearman's rho between
    true and fitted order, and how often the true best is ranked first (100 boards each)."""
    from scipy import stats
    k = 20
    rng = np.random.default_rng(4601)
    logv = np.linspace(-1.5, 1.5, k)
    P = Sc.btl_probs(np.exp(logv))
    ms = np.array([50, 100, 200, 400, 800, 1600, 3200])
    rho, top = [], []
    for m in ms:
        rr, tt = [], []
        for r in range(100):
            W = np.full((k, k), 0.05)
            np.fill_diagonal(W, 0)
            i = rng.integers(0, k, m)
            j = (i + rng.integers(1, k, m)) % k
            win = rng.random(m) < P[i, j]
            np.add.at(W, (np.where(win, i, j), np.where(win, j, i)), 1)
            f = Sc.btl_fit(W, iters=3000, tol=1e-9)
            rr.append(stats.spearmanr(f["log"], logv)[0])
            tt.append(int(np.argmax(f["log"]) == k - 1))
        rho.append(np.mean(rr))
        top.append(np.mean(tt))
    return {"m": ms, "rho": np.array(rho), "top": np.array(top), "k": k}


def compute_wtp_n() -> dict:
    """Willingness to pay for the two-day battery from conjoint studies of 50 to 800 people (12 tasks each): the
    spread of the estimate over 40 replicate studies."""
    levels = [3, 2, 2, 3]
    price = {0: [4.0, 6.0, 8.0]}
    design = Sc.conjoint_design(levels, 300, 3, seed=46)
    X = Sc.dummy_code(design, levels, numeric=price)
    beta = np.array([-0.6, 0.9, 0.5, 0.3, -0.2])
    sd = np.array([0.2, 0.5, 0.4, 0.4, 0.4])
    ns = np.array([50, 100, 200, 400, 800])
    lo, med, hi = [], [], []
    for n in ns:
        w = []
        for r in range(40):
            Xs, ys = Sc.simulate_conjoint(X, beta, sd, int(n), seed=46000 + 100 * int(n) + r)
            b = Sc.fit_clogit(Xs, ys)["b"]
            w.append(-100 * b[1] / b[0])
        w = np.array(w)
        lo.append(np.percentile(w, 10)); med.append(np.median(w)); hi.append(np.percentile(w, 90))
    return {"n": ns, "lo": np.array(lo), "med": np.array(med), "hi": np.array(hi), "true": -100 * beta[1] / beta[0]}


def compute_checks() -> dict:
    """Instructed-response checks ('choose agree') on a five-point item: a random responder passes each with
    probability 1/5, an attentive one fails each with probability 0.02; with k checks, the share of random responders
    caught and of attentive people wrongly excluded (failing any)."""
    k = np.arange(1, 6)
    return {"k": k, "caught": 1 - 0.2 ** k, "wrong": 1 - 0.98 ** k}


ITEMS = {"veg": compute_veg, "gumbel": compute_gumbel, "redbus": compute_redbus, "decoy": compute_decoy,
         "conjoint": compute_conjoint, "points": compute_points, "acq": compute_acq, "careless": compute_careless,
         "nps": compute_nps, "judges": compute_judges, "arena": compute_arena, "wtp_n": compute_wtp_n,
         "checks": compute_checks}

if __name__ == "__main__":
    CACHE.main(ITEMS)
