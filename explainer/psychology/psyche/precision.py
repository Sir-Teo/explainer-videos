"""Psyche's precision-psychiatry bench (Part 59): the measurement discipline computational psychiatry relearned.

The reliability paradox (a task effect everyone shows is a poor measure of who shows it more), the trade-off
between group sensitivity and individual reliability with the trials it costs, attenuation of a parameter-symptom
correlation, a clustering pipeline that finds "biotypes" in structureless data and a stability check that exposes
them, an outcome-prediction model trained on one simulated trial and tested on another, and the sample a
treatment-selection rule needs (the personalized advantage index).  numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


# ----------------------------------------------------------------------------------------------------------------
# Reliability
# ----------------------------------------------------------------------------------------------------------------
def difference_reliability(sd_between: float, sd_trial: float, trials: int) -> float:
    """Split-half style reliability of a person's difference score (condition B minus A, ``trials`` per condition):
    true between-person variance over observed variance."""
    err = 2 * sd_trial ** 2 / trials
    return sd_between ** 2 / (sd_between ** 2 + err)


def paradox(n_people: int = 60, trials: int = 60, mean_effect: float = 60.0, sd_between: float = 15.0,
            sd_trial: float = 120.0, seed: int = 0) -> dict:
    """A Stroop-like task simulated twice (test and retest): every person has a true effect drawn around a large
    mean; trial noise is large.  The group effect is enormous (t in the tens) while the test-retest correlation of
    the individual effects is modest: Hedge, Powell and Sumner's reliability paradox."""
    rng = np.random.default_rng(seed)
    true = rng.normal(mean_effect, sd_between, n_people)

    def session():
        a = rng.normal(0, sd_trial, (n_people, trials)).mean(1)
        b = (true[:, None] + rng.normal(0, sd_trial, (n_people, trials))).mean(1)
        return b - a

    s1, s2 = session(), session()
    t = s1.mean() / (s1.std(ddof=1) / np.sqrt(n_people))
    return {"s1": s1, "s2": s2, "t": float(t), "d_group": float(s1.mean() / s1.std(ddof=1)),
            "retest_r": float(np.corrcoef(s1, s2)[0, 1]),
            "expected_r": float(difference_reliability(sd_between, sd_trial, trials))}


def design_tradeoff(sd_total_effect: float = 60.0, sd_trial: float = 120.0, trials=(20, 50, 100, 200, 400, 800),
                    shares=np.linspace(0.05, 0.95, 19)) -> dict:
    """A task designer can make the effect larger and more uniform (good for showing it in a group) or more
    variable between people (good for measuring individuals).  With the effect's spread between people a share s
    of a fixed budget (sd_between = s x sd_total, mean = (1 - s) x sd_total), the group effect size falls as s
    rises while reliability rises; more trials raise reliability at any s."""
    shares = np.asarray(shares)
    rel = np.array([[difference_reliability(s * sd_total_effect, sd_trial, n) for s in shares] for n in trials])
    group_d = np.array([(1 - s) * sd_total_effect / np.sqrt((s * sd_total_effect) ** 2 + 2 * sd_trial ** 2 / trials[2])
                        for s in shares])
    return {"shares": shares, "trials": np.asarray(trials), "reliability": rel, "group_d": group_d}


def attenuated_r(true_r: float, rel_x: float, rel_y: float) -> float:
    """Spearman's attenuation (Part 3): the observed correlation is the true one times sqrt(rel_x rel_y)."""
    return true_r * np.sqrt(rel_x * rel_y)


# ----------------------------------------------------------------------------------------------------------------
# Biotypes
# ----------------------------------------------------------------------------------------------------------------
def kmeans(X: np.ndarray, k: int, seed: int = 0, iters: int = 100) -> np.ndarray:
    """Plain k-means with k-means++ starts; returns labels."""
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d2 = np.min([((X - c) ** 2).sum(1) for c in C], axis=0)
        C.append(X[rng.choice(len(X), p=d2 / d2.sum())])
    C = np.array(C)
    for _ in range(iters):
        lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(2), axis=1)
        newC = np.array([X[lab == j].mean(0) if np.any(lab == j) else C[j] for j in range(k)])
        if np.allclose(newC, C):
            break
        C = newC
    return lab


def adjusted_rand(a, b) -> float:
    """The adjusted Rand index between two labellings (1 = identical, about 0 = chance)."""
    a, b = np.asarray(a), np.asarray(b)
    ca, cb = np.unique(a), np.unique(b)
    M = np.array([[np.sum((a == i) & (b == j)) for j in cb] for i in ca])
    comb = lambda x: x * (x - 1) / 2
    sij = comb(M).sum()
    sa, sb = comb(M.sum(1)).sum(), comb(M.sum(0)).sum()
    n = comb(len(a))
    exp = sa * sb / n
    mx = (sa + sb) / 2
    return float((sij - exp) / (mx - exp)) if mx != exp else 1.0


def biotypes(n: int = 220, dims: int = 20, k: int = 4, structure: float = 0.0, seed: int = 0) -> dict:
    """A biotype pipeline: select the connectivity features most correlated with symptoms (in the same sample),
    cluster patients on them, and report the clusters; then check stability by clustering two random halves and
    comparing the labels on the shared people.  With ``structure`` = 0 there are no subgroups at all; the pipeline
    still returns k clusters that differ in symptoms, because the features were chosen for that."""
    rng = np.random.default_rng(seed)
    centres = rng.normal(0, structure, (k, dims))
    g = rng.integers(0, k, n)
    X = rng.standard_normal((n, dims)) + centres[g]
    sym = X[:, :3].sum(1) * 0.3 + rng.standard_normal(n)
    r = np.array([abs(np.corrcoef(X[:, j], sym)[0, 1]) for j in range(dims)])
    feats = np.argsort(r)[-6:]
    lab = kmeans(X[:, feats], k, seed=seed)
    f = stats.f_oneway(*[sym[lab == j] for j in range(k) if np.sum(lab == j) > 1])
    aris = []
    for b in range(20):
        idx = rng.permutation(n)
        h1, h2 = idx[: n // 2], idx[n // 2:]
        l1 = kmeans(X[h1][:, feats], k, seed=b)
        l2 = kmeans(X[h2][:, feats], k, seed=b + 100)
        # assign the other half's points to each half's nearest centre and compare on everyone
        c1 = np.array([X[h1][l1 == j][:, feats].mean(0) for j in range(k)])
        c2 = np.array([X[h2][l2 == j][:, feats].mean(0) for j in range(k)])
        a1 = np.argmin(((X[:, feats][:, None] - c1[None]) ** 2).sum(2), 1)
        a2 = np.argmin(((X[:, feats][:, None] - c2[None]) ** 2).sum(2), 1)
        aris.append(adjusted_rand(a1, a2))
    return {"labels": lab, "symptom_F": float(f.statistic), "symptom_p": float(f.pvalue),
            "stability_ari": float(np.mean(aris)), "true_ari": float(adjusted_rand(lab, g)) if structure > 0 else 0.0}


# ----------------------------------------------------------------------------------------------------------------
# Prediction that does not travel; treatment selection
# ----------------------------------------------------------------------------------------------------------------
def trial_data(n: int = 300, p: int = 40, true_k: int = 3, site_shift: float = 0.0, drift: float = 0.0,
               seed: int = 0, beta=None) -> tuple:
    """A simulated trial: p baseline features, a binary outcome that truly depends on true_k of them weakly; a new
    trial can shift the features (site_shift) and change how the features relate to outcome (drift)."""
    rng = np.random.default_rng(seed)
    if beta is None:
        beta = np.zeros(p)
        beta[:true_k] = 0.35
    b = beta.copy()
    if drift:
        b = b + rng.normal(0, drift, p)
    X = rng.standard_normal((n, p)) + site_shift * rng.standard_normal(p)
    lp = X @ b
    y = rng.random(n) < 1 / (1 + np.exp(-lp))
    return X, y.astype(float), beta


def fit_logistic(X, y, ridge: float = 1.0, iters: int = 50) -> np.ndarray:
    """Ridge logistic regression by Newton's method (intercept unpenalized)."""
    Xa = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Xa.shape[1])
    R = ridge * np.eye(Xa.shape[1])
    R[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xa @ w))
        g = Xa.T @ (y - p) - R @ w
        H = Xa.T @ (Xa * (p * (1 - p))[:, None]) + R
        w += np.linalg.solve(H, g)
    return w


def auc(score, y) -> float:
    """Area under the ROC curve by the Mann-Whitney statistic."""
    s1, s0 = score[y == 1], score[y == 0]
    return float((np.sum(s1[:, None] > s0[None, :]) + 0.5 * np.sum(s1[:, None] == s0[None, :])) / (len(s1) * len(s0)))


def cross_trial(reps: int = 40, n: int = 300, p: int = 40, drift: float = 0.35, site_shift: float = 0.5,
                seed: int = 0) -> dict:
    """Train on trial A (with feature selection and tuning done on all of A, as many studies did); estimate AUC by
    resubstitution, by honest cross-validation inside A, and on an independent trial B from a different site whose
    feature-outcome relations drift (Chekroud et al. 2024's pattern)."""
    rng = np.random.default_rng(seed)
    res = {"apparent": [], "cv": [], "new_trial": []}
    for r in range(reps):
        XA, yA, beta = trial_data(n, p, seed=int(rng.integers(1 << 30)))
        XB, yB, _ = trial_data(n, p, beta=beta, drift=drift, site_shift=site_shift, seed=int(rng.integers(1 << 30)))
        rs = np.array([abs(np.corrcoef(XA[:, j], yA)[0, 1]) for j in range(p)])
        sel = np.argsort(rs)[-10:]  # selection on the whole of A
        w = fit_logistic(XA[:, sel], yA, ridge=0.1)
        res["apparent"].append(auc(np.column_stack([np.ones(n), XA[:, sel]]) @ w, yA))
        folds = np.array_split(rng.permutation(n), 5)
        sc = np.zeros(n)
        for f in folds:
            tr = np.setdiff1d(np.arange(n), f)
            rs_tr = np.array([abs(np.corrcoef(XA[tr, j], yA[tr])[0, 1]) for j in range(p)])
            s2 = np.argsort(rs_tr)[-10:]
            w2 = fit_logistic(XA[tr][:, s2], yA[tr], ridge=0.1)
            sc[f] = np.column_stack([np.ones(len(f)), XA[f][:, s2]]) @ w2
        res["cv"].append(auc(sc, yA))
        res["new_trial"].append(auc(np.column_stack([np.ones(n), XB[:, sel]]) @ w, yB))
    return {k: float(np.mean(v)) for k, v in res.items()}


def pai_sample(effect_interaction: float = 0.3, alpha: float = 0.05, power: float = 0.8) -> dict:
    """How many patients a trial needs to show that a selection rule helps (DeRubeis et al.'s personalized
    advantage index): the benefit of choosing by the rule is a treatment-by-moderator interaction, and detecting an
    interaction of standardized size d needs about four times the sample of a main effect of the same size."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    n_main = 2 * 2 * z ** 2 / effect_interaction ** 2  # total, two arms, d = effect
    n_inter = 4 * n_main
    return {"main_total": float(n_main), "interaction_total": float(n_inter)}
