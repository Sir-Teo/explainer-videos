"""Psyche's personality (Part 33): five traits, how they are found and scored, why one act says little and many acts
say a lot, what types throw away, how far two groups are apart in many dimensions, and what a trail of likes gives
away.

* :func:`score` and :data:`KEYS`: scale scores for the five factors from the 25 International Personality Item Pool
  items in the SAPA sample (``opendata.bfi``), with reverse-keyed items flipped on the six-point scale.
* :func:`parallel` : Horn's parallel analysis, the eigenvalues of the data against those of random data of the same
  size, the usual rule for how many factors to keep.
* :func:`act_world` and :func:`aggregate_curve`: a population whose behaviour in each situation is a stable trait, a
  situation's pull, a person-by-situation signature and noise.  One act predicts another weakly (Hartshorne and May,
  Mischel's .30); averages over many acts predict each other well (Epstein), as the Spearman-Brown formula says.
  :func:`components` splits the variance of behaviour into person, situation, signature and noise.
* :func:`type_agreement`: a continuous trait cut at the median into two "types", tested twice with a given
  reliability: the chance of the same type on one dimension, 1/2 + arcsin(r)/pi, and on four at once; and
  :func:`dichotomy_loss`, the share of a correlation a median split keeps, sqrt(2/pi) for normal data.
* :func:`mahalanobis` and :func:`overlap_d`: two groups' distance over several traits at once, and the overlap of two
  normal distributions that far apart, 2 Phi(-D/2); :func:`d_by_dimensions` shows D growing as variables are added
  even when each univariate difference stays small.
* :func:`besd`: Rosenthal and Rubin's binomial effect-size display: a correlation r as success rates 50 +- 50 r %.
* :func:`likes_world` and :func:`likes_accuracy`: simulated people whose many binary "likes" each lean a little on
  their traits; a ridge regression on the first k likes predicts a trait, and its accuracy grows with k.
* :func:`faking`: applicants who raise their conscientiousness answers, and what that does to who is hired.

Everything simulated here is labelled simulated; the scale scores use real, open data.  Nothing here imports manim.
"""

from __future__ import annotations

import numpy as np

__all__ = ["TRAITS", "NAMES", "KEYS", "score", "parallel", "act_world", "aggregate_curve", "components",
           "type_agreement", "dichotomy_loss", "mahalanobis", "overlap_d", "d_by_dimensions", "besd", "likes_world",
           "likes_accuracy", "faking"]

TRAITS = ("A", "C", "E", "N", "O")
NAMES = {"A": "agreeableness", "C": "conscientiousness", "E": "extraversion", "N": "neuroticism", "O": "openness"}
# item -> +1 or -1 for its trait (the SAPA/psychTools keying; neuroticism scored as neuroticism)
KEYS = {"A1": -1, "A2": 1, "A3": 1, "A4": 1, "A5": 1, "C1": 1, "C2": 1, "C3": 1, "C4": -1, "C5": -1,
        "E1": -1, "E2": -1, "E3": 1, "E4": 1, "E5": 1, "N1": 1, "N2": 1, "N3": 1, "N4": 1, "N5": 1,
        "O1": 1, "O2": -1, "O3": 1, "O4": 1, "O5": -1}


def _Phi(z):
    from scipy.stats import norm
    return norm.cdf(z)


def score(X, names, points: int = 6) -> dict:
    """Scale means for the five traits from item responses X (n x items, NaN for missing), reverse-keyed items flipped
    as (points + 1 - x).  A person's scale score is the mean of the items they answered."""
    X = np.asarray(X, float)
    out = {}
    for t in TRAITS:
        cols = [j for j, nm in enumerate(names) if nm in KEYS and nm[0] == t]
        Y = X[:, cols].copy()
        for k, j in enumerate(cols):
            if KEYS[names[j]] < 0:
                Y[:, k] = points + 1 - Y[:, k]
        with np.errstate(invalid="ignore"):
            out[t] = np.nanmean(Y, axis=1)
    return out


def parallel(X, n_iter: int = 50, seed: int = 0, q: float = 0.95) -> dict:
    """Horn's parallel analysis on the complete rows of X: eigenvalues of the correlation matrix against the q-quantile
    of eigenvalues from normal data of the same shape.  Factors to keep: the leading run above the threshold."""
    X = np.asarray(X, float)
    X = X[~np.isnan(X).any(axis=1)]
    n, p = X.shape
    ev = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    rng = np.random.default_rng(seed)
    sims = np.array([np.sort(np.linalg.eigvalsh(np.corrcoef(rng.normal(size=(n, p)), rowvar=False)))[::-1]
                     for _ in range(n_iter)])
    thr = np.quantile(sims, q, axis=0)
    keep = 0
    while keep < p and ev[keep] > thr[keep]:
        keep += 1
    return {"eigen": ev, "random": thr, "keep": keep, "n": n}


def act_world(n: int = 4000, situations: int = 40, trait: float = 1.0, situation: float = 0.6, signature: float = 0.6,
              noise: float = 1.4, seed: int = 0) -> dict:
    """Behaviour B[i, s] = person_i + pull_s + signature_is + noise_is: a stable trait, a situation everyone responds
    to, a person's own if-then profile across situations (stable over repeated visits), and occasion noise.  Each
    situation is visited twice, so the same act can be compared on two occasions.  Returns both visits."""
    rng = np.random.default_rng(seed)
    person = rng.normal(0, trait, size=(n, 1))
    pull = rng.normal(0, situation, size=(1, situations))
    sig = rng.normal(0, signature, size=(n, situations))
    b1 = person + pull + sig + rng.normal(0, noise, size=(n, situations))
    b2 = person + pull + sig + rng.normal(0, noise, size=(n, situations))
    return {"b1": b1, "b2": b2, "person": person[:, 0], "pull": pull[0], "sd": (trait, situation, signature, noise)}


def aggregate_curve(world: dict, ks=(1, 2, 4, 8, 16), seed: int = 1) -> dict:
    """The correlation between a person's average over k situations and their average over k other situations (cross-
    situational consistency, aggregated), with the Spearman-Brown prediction from the single-act correlation; and the
    correlation of one act with the same situation on another occasion (retest of a single act)."""
    b1 = world["b1"]
    n, S = b1.shape
    rng = np.random.default_rng(seed)
    obs = []
    for k in ks:
        rs = []
        for _ in range(30):
            idx = rng.permutation(S)
            a, b = idx[:k], idx[k:2 * k]
            rs.append(np.corrcoef(b1[:, a].mean(1), b1[:, b].mean(1))[0, 1])
        obs.append(float(np.mean(rs)))
    r1 = obs[0]
    sb = [float(k * r1 / (1 + (k - 1) * r1)) for k in ks]
    same = float(np.mean([np.corrcoef(world["b1"][:, s], world["b2"][:, s])[0, 1] for s in range(S)]))
    return {"k": list(ks), "observed": obs, "spearman_brown": sb, "single": r1, "same_situation": same}


def components(sd) -> dict:
    """Shares of behavioural variance (one act, one occasion) due to the person, the situation, the person-by-situation
    signature and noise, from the generating SDs."""
    v = np.array(sd, float) ** 2
    v = v / v.sum()
    return dict(zip(("person", "situation", "signature", "noise"), (float(x) for x in v)))


def type_agreement(reliability: float, dims: int = 4, n: int = 200_000, seed: int = 0) -> dict:
    """Two administrations of `dims` independent traits, each measured with the given test-retest reliability and cut
    at the median: the share with the same type on one dimension (exact: 1/2 + arcsin(r)/pi) and on all of them
    (simulated, and exact for independent dimensions: the one-dimension share to the power dims)."""
    one = 0.5 + np.arcsin(reliability) / np.pi
    rng = np.random.default_rng(seed)
    t = rng.normal(size=(n, dims))
    e = np.sqrt((1 - reliability) / reliability)
    x1 = t + e * rng.normal(size=(n, dims))
    x2 = t + e * rng.normal(size=(n, dims))
    same = (x1 > 0) == (x2 > 0)
    return {"one": float(one), "one_sim": float(same[:, 0].mean()), "all": float(one ** dims),
            "all_sim": float(same.all(axis=1).mean())}


def dichotomy_loss() -> float:
    """The correlation of a median split of a normal variable with the variable itself, sqrt(2/pi): a type keeps this
    share of every correlation the trait has."""
    return float(np.sqrt(2 / np.pi))


def mahalanobis(X1, X2) -> dict:
    """Univariate d for each column and the multivariate Mahalanobis D between two groups, with the pooled covariance
    (rows with missing values dropped)."""
    X1 = np.asarray(X1, float)
    X2 = np.asarray(X2, float)
    X1 = X1[~np.isnan(X1).any(axis=1)]
    X2 = X2[~np.isnan(X2).any(axis=1)]
    n1, n2 = len(X1), len(X2)
    diff = X2.mean(0) - X1.mean(0)
    Sp = ((n1 - 1) * np.cov(X1, rowvar=False) + (n2 - 1) * np.cov(X2, rowvar=False)) / (n1 + n2 - 2)
    Sp = np.atleast_2d(Sp)
    d = diff / np.sqrt(np.diag(Sp))
    D = float(np.sqrt(diff @ np.linalg.solve(Sp, diff)))
    return {"d": d, "D": D, "n": (n1, n2)}


def overlap_d(D: float) -> float:
    """Overlap of two normal distributions (equal covariance) a Mahalanobis distance D apart: 2 Phi(-D/2)."""
    return float(2 * _Phi(-abs(D) / 2))


def d_by_dimensions(X1, X2, sizes, reps: int = 40, seed: int = 0) -> dict:
    """Mean Mahalanobis D over random subsets of each size of the columns, and the mean absolute univariate d."""
    rng = np.random.default_rng(seed)
    p = np.asarray(X1).shape[1]
    out_D, out_d = [], []
    for k in sizes:
        Ds, ds = [], []
        for _ in range(reps if k < p else 1):
            cols = rng.choice(p, size=k, replace=False) if k < p else np.arange(p)
            m = mahalanobis(np.asarray(X1)[:, cols], np.asarray(X2)[:, cols])
            Ds.append(m["D"])
            ds.append(np.abs(m["d"]).mean())
        out_D.append(float(np.mean(Ds)))
        out_d.append(float(np.mean(ds)))
    return {"k": list(sizes), "D": out_D, "mean_abs_d": out_d}


def besd(r: float) -> tuple:
    """Rosenthal and Rubin's binomial effect-size display: the 'success' rates 50 + 50 r and 50 - 50 r percent."""
    return 0.5 + r / 2, 0.5 - r / 2


def likes_world(n: int = 6000, likes: int = 2000, strength: float = 0.18, density: float = 0.06, seed: int = 0) -> dict:
    """Simulated people with five standard-normal traits and binary 'likes': each like has a base rate around
    `density` and a small loading on one or two traits; P(like) = logistic(base + loadings . traits)."""
    rng = np.random.default_rng(seed)
    T = rng.normal(size=(n, 5))
    W = np.zeros((5, likes))
    for j in range(likes):
        ks = rng.choice(5, size=rng.integers(1, 3), replace=False)
        W[ks, j] = rng.normal(0, strength, size=len(ks)) * rng.choice([1, 2.5], p=[0.85, 0.15])
    base = np.log(density / (1 - density)) + rng.normal(0, 0.7, size=likes)
    P = 1 / (1 + np.exp(-(base + T @ W)))
    L = (rng.random((n, likes)) < P).astype(float)
    return {"T": T, "L": L, "W": W}


def likes_accuracy(world: dict, ks, trait: int = 4, train: float = 0.7, lam: float = 30.0, orders: int = 5,
                   seed: int = 0) -> dict:
    """Ridge regression of one trait on k likes (columns, in a random order), fitted on a training share and scored
    as the correlation of predicted and true trait in the held-out people, averaged over `orders` random orders of
    the likes; the trait's own measurement would add error, so this is the ceiling the likes alone reach."""
    T, L = world["T"], world["L"]
    n, m = L.shape
    cut = int(train * n)
    rng = np.random.default_rng(seed)
    perms = [rng.permutation(m) for _ in range(orders)]
    out = []
    for k in ks:
        rs = []
        for perm in perms:
            cols = perm[:k]
            Xtr, Xte = L[:cut][:, cols], L[cut:][:, cols]
            mu = Xtr.mean(0)
            A, B = Xtr - mu, Xte - mu
            y = T[:cut, trait] - T[:cut, trait].mean()
            beta = np.linalg.solve(A.T @ A + lam * np.eye(k), A.T @ y)
            rs.append(float(np.corrcoef(B @ beta, T[cut:, trait])[0, 1]))
        out.append(float(np.mean(rs)))
    return {"k": list(ks), "r": out}


def faking(n: int = 100_000, share: float = 0.3, lift: float = 0.8, validity: float = 0.25, select: float = 0.1,
           seed: int = 0) -> dict:
    """Applicants' honest conscientiousness predicts performance with the given validity; a share of them raise their
    answers by `lift` SD.  Hiring the top `select` on the reported score: the share of hires who faked, the hires'
    mean performance against hiring on honest scores, and the validity of reported scores."""
    rng = np.random.default_rng(seed)
    c = rng.normal(size=n)
    perf = validity * c + np.sqrt(1 - validity ** 2) * rng.normal(size=n)
    fakers = rng.random(n) < share
    reported = c + lift * fakers
    top = reported >= np.quantile(reported, 1 - select)
    honest_top = c >= np.quantile(c, 1 - select)
    return {"faker_share_hired": float(fakers[top].mean()), "faker_share_pool": float(fakers.mean()),
            "perf_hired": float(perf[top].mean()), "perf_honest": float(perf[honest_top].mean()),
            "validity_reported": float(np.corrcoef(reported, perf)[0, 1])}
