"""statkit.design: designed experiments written out (Part 13 of *Statistics, Built*).

    from explainer.stats.kit.design import Field, oneway, rcbd, latin_square, factorial_effects, fraction, tukey_hsd

``Field`` is the field-trial simulator: a rectangle of plots with a smooth, hidden fertility surface plus plot noise,
on which any allocation of treatments can be laid out and harvested.  ``Bakery`` is a hidden response surface (a
recipe's quality as a function of oven temperature and baking time) for response-surface methods.  The analysis
functions are checked against SciPy/statsmodels in ``tests/test_stats_kit_design.py``.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------------------------------------------
# The field-trial simulator
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class Field:
    """``rows x cols`` plots.  Fertility = a gentle east-west gradient + a smooth hump + plot noise (seeded)."""
    rows: int = 12
    cols: int = 12
    gradient: float = 6.0
    hump: float = 4.0
    noise: float = 2.0
    seed: int = 1843

    def __post_init__(self):
        g = np.random.Generator(np.random.PCG64(self.seed))
        r, c = np.meshgrid(np.linspace(0, 1, self.rows), np.linspace(0, 1, self.cols), indexing="ij")
        cx, cy = g.uniform(0.2, 0.8, 2)
        self.fertility = (50 + self.gradient * (c - 0.5) * 2 + self.hump * np.exp(-((r - cx) ** 2 + (c - cy) ** 2) / 0.08))
        self._g = g

    def harvest(self, effects: np.ndarray, rng: np.random.Generator | None = None) -> np.ndarray:
        """Yields for a ``rows x cols`` array of treatment effects: fertility + effect + fresh plot noise."""
        g = rng or self._g
        return self.fertility + effects + self.noise * g.standard_normal(self.fertility.shape)


@dataclass
class Bakery:
    """A hidden recipe surface: quality (0-100) as a function of oven temperature (C) and time (min): a quadratic hill
    with a tilted ridge (the two interact), floored at 0, plus noise.  The optimum is 85 at 205 C and 31 minutes."""
    noise: float = 2.0
    seed: int = 1951

    def __post_init__(self):
        self._g = np.random.Generator(np.random.PCG64(self.seed))

    @staticmethod
    def truth(temp, time):
        u = (np.asarray(temp, float) - 205) / 20
        v = (np.asarray(time, float) - 31) / 6
        return np.maximum(0.0, 85 - 9 * u ** 2 - 7 * v ** 2 - 10 * u * v)  # burnt or raw bread scores 0

    def bake(self, temp, time, rng=None):
        g = rng or self._g
        t = self.truth(temp, time)
        return t + self.noise * g.standard_normal(np.shape(t))


# ---------------------------------------------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------------------------------------------
def oneway(groups) -> dict:
    """One-way ANOVA: SST = SSB + SSW, F = (SSB/(k-1)) / (SSW/(N-k))."""
    groups = [np.asarray(gp, float) for gp in groups]
    allv = np.concatenate(groups)
    N, k = len(allv), len(groups)
    gm = allv.mean()
    ssb = sum(len(gp) * (gp.mean() - gm) ** 2 for gp in groups)
    ssw = sum(((gp - gp.mean()) ** 2).sum() for gp in groups)
    f = (ssb / (k - 1)) / (ssw / (N - k))
    return {"ssb": float(ssb), "ssw": float(ssw), "sst": float(ssb + ssw), "dfb": k - 1, "dfw": N - k, "F": float(f),
            "p": float(stats.f.sf(f, k - 1, N - k)), "mse": float(ssw / (N - k)), "means": [float(gp.mean()) for gp in groups]}


def rcbd(y) -> dict:
    """Randomized complete blocks: ``y[t, b]`` (treatment t in block b); two-way ANOVA without interaction."""
    y = np.asarray(y, float)
    t, b = y.shape
    gm = y.mean()
    ssb_ = t * ((y.mean(0) - gm) ** 2).sum()
    sstr = b * ((y.mean(1) - gm) ** 2).sum()
    sse = ((y - y.mean(1, keepdims=True) - y.mean(0, keepdims=True) + gm) ** 2).sum()
    dfe = (t - 1) * (b - 1)
    f = (sstr / (t - 1)) / (sse / dfe)
    return {"ss_treat": float(sstr), "ss_block": float(ssb_), "sse": float(sse), "dfe": dfe, "F": float(f),
            "p": float(stats.f.sf(f, t - 1, dfe)), "mse": float(sse / dfe)}


def latin_square(n: int, rng: np.random.Generator) -> np.ndarray:
    """A random n x n Latin square: the cyclic square with rows, columns and symbols permuted."""
    base = (np.arange(n)[:, None] + np.arange(n)[None, :]) % n
    base = base[rng.permutation(n)][:, rng.permutation(n)]
    return rng.permutation(n)[base]


def latin_anova(y, sq) -> dict:
    """Rows, columns and treatments in a Latin square."""
    y, sq = np.asarray(y, float), np.asarray(sq)
    n = y.shape[0]
    gm = y.mean()
    tm = np.array([y[sq == k].mean() for k in range(n)])
    ssr = n * ((y.mean(1) - gm) ** 2).sum()
    ssc = n * ((y.mean(0) - gm) ** 2).sum()
    sst = n * ((tm - gm) ** 2).sum()
    sse = ((y - gm) ** 2).sum() - ssr - ssc - sst
    dfe = (n - 1) * (n - 2)
    f = (sst / (n - 1)) / (sse / dfe)
    return {"ss_rows": float(ssr), "ss_cols": float(ssc), "ss_treat": float(sst), "sse": float(sse), "dfe": dfe, "F": float(f),
            "p": float(stats.f.sf(f, n - 1, dfe)), "mse": float(sse / dfe), "means": tm.tolist()}


def full_factorial(k: int) -> np.ndarray:
    """The 2^k design in standard (Yates) order, levels -1/+1; column 0 is factor A, the fastest-changing."""
    return np.array([[1 if (i >> j) & 1 else -1 for j in range(k)] for i in range(2 ** k)])


def factorial_effects(X: np.ndarray, y: np.ndarray, names: str = "ABCDEFG") -> dict:
    """Main effects and interactions of a two-level design: effect = mean(y at +) - mean(y at -) of each product column."""
    X = np.asarray(X)
    y = np.asarray(y, float)
    k = X.shape[1]
    out = {}
    for r in range(1, k + 1):
        for combo in itertools.combinations(range(k), r):
            col = np.prod(X[:, combo], axis=1)
            out["".join(names[i] for i in combo)] = float(y[col > 0].mean() - y[col < 0].mean())
    return out


def yates(y: np.ndarray) -> np.ndarray:
    """Yates' (1937) algorithm on responses in standard order: k passes of pairwise sums and differences.
    Returns [grand total, then contrasts in standard order (A, B, AB, C, AC, BC, ABC, ...)]."""
    y = np.asarray(y, float)
    k = int(round(np.log2(len(y))))
    col = y.copy()
    for _ in range(k):
        col = np.concatenate([col[0::2] + col[1::2], col[1::2] - col[0::2]])
    return col


def fraction(k: int, generators: dict[str, str]) -> np.ndarray:
    """A 2^(k-p) fractional factorial: the base factors in full, the others defined by ``generators`` like {"D": "ABC"}."""
    base = [c for c in "ABCDEFG"[:k] if c not in generators]
    X = full_factorial(len(base))
    cols = {c: X[:, i] for i, c in enumerate(base)}
    for c, gen in generators.items():
        cols[c] = np.prod([cols[g] for g in gen], axis=0)
    return np.column_stack([cols[c] for c in "ABCDEFG"[:k]])


def aliases(word: str, defining: list[str]) -> list[str]:
    """Aliases of an effect under a defining relation I = W1 = W2 = ... (multiplication: symmetric difference)."""
    out = []
    for w in defining:
        s = set(word) ^ set(w)
        out.append("".join(sorted(s)) or "I")
    return out


def tukey_hsd(groups, alpha=0.05) -> dict:
    """Tukey's honestly significant difference for equal-sized groups: |mean_i - mean_j| > q * sqrt(MSE/n)."""
    a = oneway(groups)
    k, n = len(groups), len(groups[0])
    q = float(stats.studentized_range.ppf(1 - alpha, k, a["dfw"]))
    hsd = q * np.sqrt(a["mse"] / n)
    return {"q": q, "hsd": float(hsd), "means": a["means"]}


def scheffe_multiplier(k: int, df: int, alpha=0.05) -> float:
    return float(np.sqrt((k - 1) * stats.f.ppf(1 - alpha, k - 1, df)))


def d_criterion(x, degree: int = 2) -> float:
    """det(X'X / n) for polynomial regression of the given degree at design points x (D-optimality)."""
    x = np.asarray(x, float)
    X = np.vander(x, degree + 1, increasing=True)
    return float(np.linalg.det(X.T @ X / len(x)))


def mde(n_per_arm: int, sigma: float, alpha=0.05, power=0.8) -> float:
    """The minimum detectable effect of a two-arm comparison: (z_{1-a/2} + z_power) sigma sqrt(2/n)."""
    return float((stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)) * sigma * np.sqrt(2 / n_per_arm))


def cuped(y, x_pre) -> tuple[np.ndarray, float]:
    """CUPED (Deng, Xu, Kohavi & Walker 2013): y - theta (x - mean x), theta = cov(y, x)/var(x)."""
    y, x = np.asarray(y, float), np.asarray(x_pre, float)
    theta = float(np.cov(y, x)[0, 1] / x.var(ddof=1))
    return y - theta * (x - x.mean()), theta


def srm_test(n_a: int, n_b: int, p_a: float = 0.5) -> float:
    """Sample-ratio mismatch: a chi-squared test that the arms got the intended split."""
    return float(stats.chisquare([n_a, n_b], [p_a * (n_a + n_b), (1 - p_a) * (n_a + n_b)]).pvalue)
