"""Evidence: how big an effect is, how often a study finds it, and how a literature comes to mislead
(*Psychology, Built*, Part 4; videos/psychology/SYLLABUS.md).

The false-positive lab of the series.  Four groups of tools, all plain numpy and scipy:

* **Effect sizes.**  :func:`cohen_d`; what a ``d`` looks like (:func:`overlap`, :func:`superiority`); conversions
  (:func:`d_to_r`, :func:`r_to_d`); and :func:`p_for`, the p-value of a given ``d`` at a given sample size, which is
  why "significant" says so little about size.
* **One study.**  :func:`power` (two-group, normal approximation, as in ``lab.power_two_group``), :func:`n_for`,
  :func:`peeking` (the false-positive rate when a null study is tested after every batch and stopped at the first
  p < .05), :func:`forks` (one dataset, sixteen defensible analyses: the forking-paths exercise of the film and of
  the part's interactive), and :func:`flexibility` (Simmons, Nelson and Simonsohn's simulation, from
  ``explainer.stats.kit.multiple.phack``).
* **A literature.**  :func:`literature` runs ``k`` laboratories on one true effect and applies a publication
  filter; :func:`pcurve` bins the significant p-values; :func:`replicate` reruns the published studies as a
  replication project would; :func:`ppv` is the share of published findings that are true.
* **Claiming an absence.**  :func:`tost` (two one-sided tests against a smallest effect of interest) and
  :func:`bf01` (a Bayes factor for the null against a normal prior on the effect).

Nothing here imports manim.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import stats

from explainer.stats.kit import multiple as _multiple

__all__ = ["cohen_d", "overlap", "superiority", "d_to_r", "r_to_d", "p_for", "power", "n_for", "peeking",
           "FORKS", "forks", "flexibility", "literature", "pcurve", "replicate", "ppv", "tost", "bf01",
           "any_significant"]

Z975 = 1.959963984540054


# ---------------------------------------------------------------------------
# effect sizes
# ---------------------------------------------------------------------------
def cohen_d(a, b) -> float:
    """The difference between two group means in units of their pooled standard deviation."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / pooled)


def overlap(d: float) -> float:
    """The overlapping share of two unit-variance normal curves whose means differ by ``d``."""
    return float(2 * stats.norm.cdf(-abs(d) / 2))


def superiority(d: float) -> float:
    """The chance that a person drawn from the higher group scores above a person drawn from the lower one."""
    return float(stats.norm.cdf(d / math.sqrt(2)))


def d_to_r(d: float) -> float:
    """The correlation between group membership and the outcome, for two groups of equal size."""
    return d / math.sqrt(d * d + 4)


def r_to_d(r: float) -> float:
    return 2 * r / math.sqrt(1 - r * r)


def p_for(d: float, n: int) -> float:
    """The two-sided p-value of an observed difference of ``d`` standard deviations between two groups of ``n``."""
    return float(2 * stats.norm.sf(abs(d) * math.sqrt(n / 2)))


# ---------------------------------------------------------------------------
# one study
# ---------------------------------------------------------------------------
def power(d: float, n: int, alpha: float = 0.05) -> float:
    """The chance that a two-group study with ``n`` people in each group gives p < ``alpha`` (two-sided) when
    the true effect is ``d``."""
    z, ncp = stats.norm.isf(alpha / 2), abs(d) * math.sqrt(n / 2)
    return float(stats.norm.sf(z - ncp) + stats.norm.cdf(-z - ncp))


def n_for(d: float, target: float = 0.8, alpha: float = 0.05) -> int:
    """People needed in each of two groups for power ``target``."""
    return int(math.ceil(2 * ((stats.norm.isf(alpha / 2) + stats.norm.ppf(target)) / d) ** 2))


def peeking(looks: int, batch: int = 10, reps: int = 4000, rng=None, alpha: float = 0.05) -> dict:
    """A study of nothing, tested after every ``batch`` people per group and stopped at the first p < alpha.
    Returns the share of studies that ever "find" the effect, and one example path of p-values (the median study
    by its smallest p)."""
    rng = rng or np.random.default_rng(0)
    n = looks * batch
    a, b = rng.standard_normal((reps, n)), rng.standard_normal((reps, n))
    ks = batch * np.arange(1, looks + 1)
    ca, cb = np.cumsum(a, axis=1)[:, ks - 1], np.cumsum(b, axis=1)[:, ks - 1]
    qa, qb = np.cumsum(a * a, axis=1)[:, ks - 1], np.cumsum(b * b, axis=1)[:, ks - 1]
    va, vb = (qa - ca ** 2 / ks) / (ks - 1), (qb - cb ** 2 / ks) / (ks - 1)
    t = (ca / ks - cb / ks) / np.sqrt((va + vb) / ks)
    p = 2 * stats.t.sf(np.abs(t), 2 * ks - 2)
    ever = (p < alpha).any(axis=1)
    order = np.argsort(p.min(axis=1))
    return {"rate": float(ever.mean()), "n": ks, "example": p[order[reps // 2]], "lucky": p[order[reps // 20]],
            "looks": looks, "batch": batch}


# the four choices of the forking-paths exercise: (key, the two options, the first being the plan)
FORKS = (
    ("measure", ("reaction time", "error rate")),
    ("outliers", ("keep everyone", "drop anyone beyond 2.5 SD")),
    ("covariate", ("no adjustment", "adjust for age")),
    ("more", ("stop at 20 per group", "add 10 more per group")),
)


def _fork_data(seed: int, n: int = 20, extra: int = 10, trials: int = 12) -> dict:
    """One study of a game that does nothing: ``n + extra`` people in each of two groups, each with a mean
    reaction time over ``trials`` trials (ms; age slows it a little) and an error rate (%), which goes with being
    slow (the two outcomes correlate about 0.5)."""
    rng = np.random.default_rng([4, seed])
    m = n + extra
    age = rng.integers(18, 66, (2, m)).astype(float)
    z = rng.standard_normal((2, m))
    rt = 300 + 0.6 * (age - 40) + 24 * z + rng.gamma(2.0, 30.0, (2, m, trials)).mean(axis=2) - 60.0
    errors = 6 + 2 * (0.55 * z + math.sqrt(1 - 0.55 ** 2) * rng.standard_normal((2, m)))
    return {"age": age, "rt": rt, "errors": errors, "n": n, "extra": extra}


def _fork_p(data: dict, choice) -> tuple:
    """(p, difference in SD units) for one of the sixteen analyses; ``choice`` is four 0/1 switches in the order of
    :data:`FORKS`."""
    measure, outliers, covariate, more = choice
    k = data["n"] + (data["extra"] if more else 0)
    score = (data["errors"] if measure else data["rt"])[:, :k]
    age = data["age"][:, :k]
    keep = np.ones_like(score, dtype=bool)
    if outliers:
        pooled = score.ravel()
        keep = np.abs(score - pooled.mean()) < 2.5 * pooled.std(ddof=1)
    y = np.concatenate([score[0][keep[0]], score[1][keep[1]]])
    g = np.concatenate([np.ones(keep[0].sum()), np.zeros(keep[1].sum())])
    cols = [np.ones_like(y), g] + ([np.concatenate([age[0][keep[0]], age[1][keep[1]]])] if covariate else [])
    X = np.column_stack(cols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    se = math.sqrt(resid @ resid / df * np.linalg.inv(X.T @ X)[1, 1])
    return float(2 * stats.t.sf(abs(beta[1] / se), df)), float(beta[1] / y.std(ddof=1))


def forks(seed: int) -> dict:
    """The forking-paths exercise on dataset ``seed``: the p-value of each of the sixteen analyses (keyed by the
    four switches), the planned one (all switches off), and the smallest."""
    data = _fork_data(seed)
    table = {c: _fork_p(data, c) for c in itertools.product((0, 1), repeat=4)}
    best = min(table, key=lambda c: table[c][0])
    return {"table": table, "planned": table[(0, 0, 0, 0)], "best": best, "best_p": table[best][0]}


def any_significant(seeds, alpha: float = 0.05) -> dict:
    """Over many null datasets: how often the planned analysis is significant, how often at least one of the
    sixteen is, and the same for each single switch (the plan against the plan with that switch on)."""
    planned = best = 0
    single = np.zeros(4)
    for s in seeds:
        f = forks(s)
        planned += f["planned"][0] < alpha
        best += f["best_p"] < alpha
        for i in range(4):
            on = tuple(int(j == i) for j in range(4))
            single[i] += min(f["planned"][0], f["table"][on][0]) < alpha
    k = len(list(seeds))
    return {"planned": planned / k, "any": best / k, "single": (single / k).tolist(), "datasets": k}


def flexibility(reps: int = 3000, rng=None) -> dict:
    """Simmons, Nelson and Simonsohn's four flexibilities, simulated with no true effect (statkit's ``phack``):
    false-positive rates of the planned analysis, of each flexibility alone, and of all four together."""
    return _multiple.phack(reps, rng or np.random.default_rng(0))


# ---------------------------------------------------------------------------
# a literature
# ---------------------------------------------------------------------------
def literature(k: int, d: float, n, rng=None, publish_null: float = 0.0, hack: float = 0.0) -> dict:
    """``k`` laboratories each run one two-group study of a true effect ``d`` with ``n`` people per group (a
    number, or one per laboratory).  A study that is significant in the expected direction is published; any other
    is published with probability ``publish_null`` (the file drawer keeps the rest).  ``hack`` is the chance that a
    non-significant study is pushed to p just under .05 by flexible analysis (its estimate moved to the
    threshold).  Returns per-study estimates, standard errors, p-values, and what was published."""
    rng = rng or np.random.default_rng(0)
    n = np.broadcast_to(np.asarray(n), (k,)).astype(float)
    se = np.sqrt(2 / n)
    est = d + se * rng.standard_normal(k)
    hacked = (est / se < Z975) & (rng.random(k) < hack)
    est = np.where(hacked, se * (Z975 + 0.09 * rng.random(k)), est)
    p = 2 * stats.norm.sf(np.abs(est / se))
    sig = (p < 0.05) & (est > 0)
    published = sig | (rng.random(k) < publish_null)
    return {"est": est, "se": se, "p": p, "n": n, "significant": sig, "published": published, "hacked": hacked,
            "d": d}


def pcurve(p, bins: int = 5) -> np.ndarray:
    """The shares of the significant p-values (p < .05) falling in ``bins`` equal bins from 0 to .05: flat when
    there is nothing there, piled up near zero when there is, and piled up near .05 when results were pushed."""
    p = np.asarray(p, float)
    p = p[p < 0.05]
    return np.histogram(p, bins=bins, range=(0, 0.05))[0] / max(len(p), 1)


def replicate(lit: dict, rng=None, power_target: float = 0.9, cap: int = 2000) -> dict:
    """Rerun every published, significant study of ``lit`` once, with enough people for ``power_target`` to
    detect the effect the original reported (as a replication project plans its samples).  Returns the share of
    replications that are significant in the same direction, and the mean replication effect over the mean
    original effect."""
    rng = rng or np.random.default_rng(1)
    pick = lit["published"] & lit["significant"]
    orig = lit["est"][pick]
    n = np.minimum(np.array([n_for(max(o, 0.05), power_target) for o in orig]), cap)
    se = np.sqrt(2 / n)
    truth = np.broadcast_to(np.asarray(lit.get("truth", lit["d"]), float), lit["est"].shape)[pick]
    rep = truth + se * rng.standard_normal(len(orig))
    sig = rep / se > Z975
    return {"rate": float(sig.mean()), "ratio": float(rep.mean() / orig.mean()), "originals": int(len(orig)),
            "orig": orig, "rep": rep, "n": n}


def ppv(prior: float, power_: float, alpha: float = 0.05) -> float:
    """Of the findings that reach p < alpha, the share that are true, when a share ``prior`` of the hypotheses
    tested are true and true ones are detected with probability ``power_``."""
    return prior * power_ / (prior * power_ + (1 - prior) * alpha)


# ---------------------------------------------------------------------------
# claiming an absence
# ---------------------------------------------------------------------------
def tost(est: float, se: float, bound: float) -> dict:
    """Two one-sided tests: is the effect inside (-bound, bound)?  The p-value is the larger of the two; the
    effect is declared smaller than ``bound`` in size when it is below alpha."""
    p_lo, p_hi = stats.norm.sf((est + bound) / se), stats.norm.cdf((est - bound) / se)
    return {"p": float(max(p_lo, p_hi)), "ci90": (est - 1.6448536 * se, est + 1.6448536 * se)}


def bf01(est: float, se: float, prior_sd: float = 0.5) -> float:
    """The Bayes factor for "no effect" against "an effect drawn from a normal prior with standard deviation
    ``prior_sd``": how many times better the null predicts the estimate that was observed."""
    return float(stats.norm.pdf(est, 0, se) / stats.norm.pdf(est, 0, math.sqrt(se * se + prior_sd * prior_sd)))
