"""Psyche's traits (Part 32): the positive manifold, the factor model that summarizes it, three different worlds that
produce it, the scales that turn a test into an IQ, and the matrix items that are the purest tests of reasoning.

* :func:`tetrads` and :func:`one_factor`: Spearman's tetrad differences, which vanish when one factor explains all the
  correlations, and a one-factor maximum-likelihood fit (``explainer.stats.kit.multi.factor_ml``) with its residuals.
* :func:`common_cause`, :func:`sampling` and :func:`mutualism`: three simulated populations that all show a positive
  manifold.  In the first a single latent g causes every score; in Thomson's (1916) each test draws on a random
  sample of many independent "bonds", and tests correlate because their samples overlap; in van der Maas and
  colleagues' (2006) abilities grow, each helping the others, from independent starting resources.  Factor analysis
  fits one factor to all three.
* :func:`ratio_iq`, :func:`deviation_iq`, :func:`sem_interval` and :func:`restriction_corrected`: Stern's mental quotient,
  Wechsler's deviation IQ, the standard error of a score from its reliability, and Thorndike's correction of a
  validity for range restriction (the point at issue between Schmidt and Hunter's .51 and Sackett's .31).
* :func:`matrix_item` and :func:`solve`: matrix items built from attribute rules (constant, progression, distribution
  of three), and a rule-inducing solver that can hold only so many rules at once (after Carpenter, Just and Shell,
  1990): its accuracy falls with the number of rules.
* :func:`below_cut`, :func:`kelley`, :func:`selection_gain` and :func:`impact_ratio`: what the numbers do in practice.
  The chance that a person whose true score sits near a cutoff scores below it; Kelley's estimate of a true score,
  pulled toward the mean by the test's unreliability; Brogden's expected performance of the people a test selects,
  the validity times the mean standardized score of those above the cut; and the ratio of two groups' selection rates
  at a cut, against the four-fifths rule.

Nothing here imports manim.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

from explainer.stats.kit import multi

__all__ = ["tetrads", "one_factor", "common_cause", "sampling", "mutualism", "corr", "ratio_iq", "deviation_iq",
           "sem_interval", "restriction_corrected", "ATTRS", "matrix_item", "solve", "solver_accuracy", "train_one",
           "overlap", "invariance_demo", "below_cut", "kelley", "selection_gain", "impact_ratio"]


# --------------------------------------------------------------------------------------------- the factor model
def corr(X) -> np.ndarray:
    """Correlation matrix of the columns of X."""
    return np.corrcoef(np.asarray(X, float), rowvar=False)


def tetrads(R) -> np.ndarray:
    """All tetrad differences r_ab r_cd - r_ac r_bd over distinct quadruples (three per quadruple).  Under one common
    factor every one is zero, because r_ab = l_a l_b."""
    R = np.asarray(R, float)
    out = []
    for a, b, c, d in combinations(range(len(R)), 4):
        out += [R[a, b] * R[c, d] - R[a, c] * R[b, d], R[a, b] * R[c, d] - R[a, d] * R[b, c],
                R[a, c] * R[b, d] - R[a, d] * R[b, c]]
    return np.array(out)


def one_factor(R, n: int | None = None) -> dict:
    """A one-factor maximum-likelihood fit: loadings (signed so that they are mostly positive), uniquenesses, the
    implied matrix L L' + Psi, the residual correlations, and the share of total variance the factor carries."""
    R = np.asarray(R, float)
    f = multi.factor_ml(R, 1, n=n)
    L = f["loadings"][:, 0]
    if L.sum() < 0:
        L = -L
    implied = np.outer(L, L) + np.diag(f["uniqueness"])
    resid = R - implied
    np.fill_diagonal(resid, 0.0)
    off = ~np.eye(len(R), dtype=bool)
    out = {"loadings": L, "uniqueness": f["uniqueness"], "implied": implied, "residual": resid,
           "rmsr": float(np.sqrt(np.mean(resid[off] ** 2))), "share": float(np.sum(L ** 2) / len(R))}
    for k in ("chi2", "df", "p"):
        if k in f:
            out[k] = f[k]
    return out


# --------------------------------------------------------------------------------------------- three worlds
def common_cause(n: int = 2000, loadings=(0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45), seed: int = 0) -> np.ndarray:
    """Scores x_j = l_j g + sqrt(1 - l_j^2) e_j: one latent cause, g, and independent specifics."""
    rng = np.random.default_rng(seed)
    lam = np.asarray(loadings, float)
    g = rng.normal(size=(n, 1))
    return g * lam[None, :] + rng.normal(size=(n, len(lam))) * np.sqrt(1 - lam ** 2)[None, :]


def sampling(n: int = 2000, bonds: int = 3000, shares=(0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25), seed: int = 1,
             noise: float = 0.3) -> np.ndarray:
    """Thomson's sampling world: every person has ``bonds`` independent elementary abilities; test j sums a random
    subset of a share s_j of them, plus noise.  No ability is shared by all tests, and there is no g; tests correlate
    in proportion to the overlap of their samples, which is larger for tests that sample more."""
    rng = np.random.default_rng(seed)
    B = rng.normal(size=(n, bonds))
    X = np.empty((n, len(shares)))
    for j, s in enumerate(shares):
        idx = rng.choice(bonds, size=int(round(s * bonds)), replace=False)
        x = B[:, idx].sum(axis=1)
        x = x / x.std()
        X[:, j] = x + noise * rng.normal(size=n)
    return X


def mutualism(n: int = 2000, k: int = 8, coupling: float = 0.08, seed: int = 2, t_end: float = 60.0,
              dt: float = 0.05) -> np.ndarray:
    """van der Maas and colleagues' mutualism: abilities x_i grow logistically toward independent, person-specific
    limits K_i, and each ability's growth is helped by the others:
    dx_i/dt = a_i x_i (1 - x_i / K_i) + a_i x_i sum_{j != i} M x_j / K_i.
    The limits K are independent across abilities, so there is no common cause; the correlations come from the
    coupling M during growth."""
    rng = np.random.default_rng(seed)
    K = np.exp(rng.normal(0.0, 0.25, size=(n, k)))  # independent resources
    a = rng.uniform(0.2, 0.4, size=(n, k))
    x = np.full((n, k), 0.05)
    M = coupling
    for _ in range(int(t_end / dt)):
        help_ = M * (x.sum(axis=1, keepdims=True) - x)
        x = x + dt * a * x * (1 - x / K + help_ / K)
    return x


# --------------------------------------------------------------------------------------------- the scale
def ratio_iq(mental_age, chronological_age) -> np.ndarray:
    """Stern's (1912) quotient, times 100 as Terman (1916) wrote it."""
    return 100.0 * np.asarray(mental_age, float) / np.asarray(chronological_age, float)


def deviation_iq(raw, norm_mean: float, norm_sd: float) -> np.ndarray:
    """Wechsler's (1939) deviation IQ: a z-score against the norming sample of the same age, on mean 100, SD 15."""
    return 100.0 + 15.0 * (np.asarray(raw, float) - norm_mean) / norm_sd


def sem_interval(score: float, reliability: float, sd: float = 15.0, z: float = 1.96) -> dict:
    """The standard error of measurement sd sqrt(1 - r) and the interval score +- z SEM."""
    sem = sd * np.sqrt(1 - reliability)
    return {"sem": float(sem), "lo": float(score - z * sem), "hi": float(score + z * sem)}


def restriction_corrected(r: float, u: float) -> float:
    """Thorndike's case II: the correlation in the full population when the selected group's standard deviation on
    the predictor is u times the population's (u < 1): R = (r / u) / sqrt(1 - r^2 + r^2 / u^2)."""
    return float((r / u) / np.sqrt(1 - r ** 2 + r ** 2 / u ** 2))


# --------------------------------------------------------------------------------------------- matrix items
ATTRS = ("shape", "number", "shade", "size")  # each attribute takes the values 0, 1, 2


def matrix_item(rng, n_rules: int, n_options: int = 8) -> dict:
    """A 3x3 matrix item.  ``n_rules`` of the four attributes vary by a rule, the rest are constant; each varying
    attribute follows either a progression along each row (v, v+1, v+2) or a distribution of three values (each
    row a permutation of 0, 1, 2).  Returns the grid (3 x 3 x 4 attribute values), the rules, the answer (the
    bottom-right cell) and ``n_options`` options, each wrong one differing from the answer in one attribute."""
    attrs = list(range(len(ATTRS)))
    varying = set(rng.choice(attrs, size=n_rules, replace=False).tolist()) if n_rules else set()
    grid = np.zeros((3, 3, len(ATTRS)), int)
    rules = {}
    for a in attrs:
        if a not in varying:
            v = int(rng.integers(3))
            grid[:, :, a] = v
            rules[ATTRS[a]] = "constant"
        elif rng.random() < 0.5:
            for r in range(3):
                grid[r, :, a] = [0, 1, 2]
            rules[ATTRS[a]] = "progression"
        else:
            base = rng.permutation(3)
            for r in range(3):
                grid[r, :, a] = np.roll(base, r)
            rules[ATTRS[a]] = "distribution"
    answer = grid[2, 2].copy()
    options = [answer.copy()]
    seen = {tuple(answer)}
    while len(options) < n_options:
        o = answer.copy()
        a = int(rng.integers(len(ATTRS)))
        o[a] = (o[a] + int(rng.integers(1, 3))) % 3
        if tuple(o) not in seen:
            seen.add(tuple(o))
            options.append(o)
    order = rng.permutation(n_options)
    options = [options[i] for i in order]
    return {"grid": grid, "rules": rules, "answer": answer, "options": options,
            "correct": int(np.where(order == 0)[0][0]), "n_rules": n_rules}


def _infer(row1, row2, cells):
    """Infer one attribute's value in the missing cell from the first two rows and the third row's first two
    cells: constant, progression or distribution."""
    if len(set(row1)) == 1 and len(set(row2)) == 1:
        return cells[0]
    if list(row1) == [0, 1, 2] and list(row2) == [0, 1, 2]:
        return cells[1] + 1
    return ({0, 1, 2} - set(cells[:2])).pop()


def solve(item, capacity: int, rng) -> int:
    """A rule-inducing solver that can keep track of ``capacity`` varying attributes.  It infers the missing value of
    the attributes it tracks, discards the options that disagree, and guesses among those left."""
    grid = item["grid"]
    varying = [a for a, name in enumerate(ATTRS) if item["rules"][name] != "constant"]
    constant = [a for a in range(len(ATTRS)) if a not in varying]
    tracked = constant + list(rng.permutation(varying)[:capacity]) if varying else constant
    keep = []
    for i, o in enumerate(item["options"]):
        ok = all(o[a] == _infer(grid[0, :, a], grid[1, :, a], grid[2, :2, a]) for a in tracked)
        if ok:
            keep.append(i)
    return int(rng.choice(keep)) if keep else int(rng.integers(len(item["options"])))


def solver_accuracy(capacity: int, n_rules: int, trials: int = 400, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(trials):
        it = matrix_item(rng, n_rules)
        hits += solve(it, capacity, rng) == it["correct"]
    return hits / trials


# --------------------------------------------------------------------------------------------- interventions and groups
def train_one(world: str, n: int = 2000, k: int = 8, boost: float = 0.5, seed: int = 3) -> dict:
    """Raise one ability's resource (the first) by ``boost`` SD-like units and report the mean change in every
    ability.  In the common-cause world the other abilities do not move; in the mutualism world they rise too, through
    the coupling.  The two worlds have the same positive manifold but answer this experiment differently."""
    rng = np.random.default_rng(seed)
    if world == "common":
        lam = np.linspace(0.8, 0.45, k)
        g = rng.normal(size=(n, 1))
        e = rng.normal(size=(n, k))
        base = g * lam + e * np.sqrt(1 - lam ** 2)
        after = base.copy()
        after[:, 0] += boost
        return {"before": base.mean(0), "after": after.mean(0), "change": after.mean(0) - base.mean(0)}
    if world == "mutualism":
        K = np.exp(rng.normal(0.0, 0.25, size=(n, k)))
        a = rng.uniform(0.2, 0.4, size=(n, k))

        def grow(K):
            x = np.full((n, k), 0.05)
            for _ in range(1200):
                help_ = 0.08 * (x.sum(axis=1, keepdims=True) - x)
                x = x + 0.05 * a * x * (1 - x / K + help_ / K)
            return x

        b = grow(K)
        K2 = K.copy()
        K2[:, 0] *= np.exp(boost * 0.25)
        t = grow(K2)
        sd = b.std(0)
        return {"before": b.mean(0) / sd, "after": t.mean(0) / sd, "change": (t.mean(0) - b.mean(0)) / sd}
    raise ValueError(world)


def overlap(d: float) -> dict:
    """Two normal distributions with equal spread and means d SDs apart: the overlapping coefficient 2 Phi(-|d|/2),
    and the share of the lower group above the higher group's mean, Phi(-|d|)."""
    from scipy.stats import norm

    return {"overlap": float(2 * norm.cdf(-abs(d) / 2)), "above_mean": float(norm.cdf(-abs(d)))}


def invariance_demo(n: int = 4000, seed: int = 5, latent_gap: float = 0.0, biased: int = 2, bias: float = 0.6,
                    loadings=(0.8, 0.75, 0.7, 0.65, 0.6, 0.55)) -> dict:
    """Two groups measured with the same tests.  Either the groups differ on the latent ability (``latent_gap``),
    which moves every test's mean in proportion to its loading, or one test is biased against one group (an
    intercept shift ``bias`` on test ``biased``), which moves that test only.  Returns the standardized mean
    difference on each test and on the total score."""
    rng = np.random.default_rng(seed)
    lam = np.asarray(loadings, float)
    out = {}
    g1 = rng.normal(size=(n, 1))
    g2 = rng.normal(size=(n, 1)) - latent_gap
    X1 = g1 * lam + rng.normal(size=(n, len(lam))) * np.sqrt(1 - lam ** 2)
    X2 = g2 * lam + rng.normal(size=(n, len(lam))) * np.sqrt(1 - lam ** 2)
    X2[:, biased] -= bias
    sd = np.sqrt((X1.var(0) + X2.var(0)) / 2)
    out["d_tests"] = (X1.mean(0) - X2.mean(0)) / sd
    t1, t2 = X1.sum(1), X2.sum(1)
    out["d_total"] = float((t1.mean() - t2.mean()) / np.sqrt((t1.var() + t2.var()) / 2))
    out["loadings"] = lam
    return out


# ---------------------------------------------------------------------------------------------------- in practice
def _phi(z):
    return np.exp(-0.5 * np.asarray(z, float) ** 2) / np.sqrt(2 * np.pi)


def _Phi(z):
    from scipy.stats import norm
    return norm.cdf(z)


def _Phi_inv(p):
    from scipy.stats import norm
    return norm.ppf(p)


def below_cut(true_score, cut: float = 70.0, reliability: float = 0.95, sd: float = 15.0):
    """P(observed < cut | true score): the observed score is the true score plus normal error with the SEM."""
    sem = sd * np.sqrt(1 - reliability)
    return _Phi((cut - np.asarray(true_score, float)) / sem)


def kelley(observed, reliability: float, mean: float = 100.0):
    """Kelley's (1927) regressed true-score estimate: the mean plus the reliability times the deviation."""
    return mean + reliability * (np.asarray(observed, float) - mean)


def selection_gain(validity, ratio):
    """Brogden (1949): the mean standardized criterion of the top ``ratio`` on a normal test, r * phi(z) / ratio."""
    ratio = np.asarray(ratio, float)
    z = _Phi_inv(1 - ratio)
    return np.asarray(validity, float) * _phi(z) / ratio


def impact_ratio(d: float, ratio_ref):
    """Two normal groups, the second ``d`` SD lower; the cut selects ``ratio_ref`` of the first.  Returns the second
    group's selection rate and the ratio of the rates (the four-fifths rule compares it with 0.8)."""
    ratio_ref = np.asarray(ratio_ref, float)
    z = _Phi_inv(1 - ratio_ref)
    rate = 1 - _Phi(z + d)
    return {"rate": rate, "ratio": rate / ratio_ref}
