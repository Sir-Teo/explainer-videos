"""Genes, families, and the designs that try to tell them apart (videos/psychology/SYLLABUS.md, Part 9).

**Many small genes.**  :func:`allele_sum` is the exact distribution of a trait that is the sum of L loci of
equal effect: one locus gives three classes, fifty give a bell curve (Fisher 1918).

**Families.**  Everyone here has a *breeding value* A (the sum of their alleles' effects), and a phenotype
P = A + D + C + E: additive genes, dominance, the environment a family shares, and everything else.  Children are
made under the infinitesimal model: a child's A is the mean of the parents' plus a segregation draw whose
variance is half the additive variance.  Identical twins share the draw; fraternal twins and siblings get one
each.  :func:`twin_study` simulates pairs reared together, with switches for each assumption the classical
design makes: equal environments (``mz_extra``), random mating (``assort``), additivity (``d2``), and genes
uncorrelated with the family environment (``rge``).  :func:`falconer` is the textbook estimate from the two
correlations, :func:`falconer_se` its standard error, and :func:`ace_fit` the maximum-likelihood version.
:func:`adoption_study` gives the three correlations an adoption design reads (adoptive siblings, a parent and
the child they did not raise, identical twins reared apart), and :func:`midparent_offspring` the regression of
children on their parents' average, whose slope is the heritability.

**What heritability is not.**  :func:`two_fields` is Lewontin's picture: seed from one sack, sown in a rich field
and a poor one.  Within each field the differences are genetic; between the fields they are not.

**Finding the genes.**  :func:`power_for_r2` and :func:`n_for_r2` say what a sample can detect when one variant
explains a few hundredths of a percent of a trait; :func:`candidate_gene_study` runs the flexible analysis of a
gene that does nothing.  :func:`simulate_genotypes`, :func:`polygenic_trait` and :func:`gwas` are a genome-wide
association study on unlinked variants; :func:`polygenic_score` adds up the estimated effects in new people, and
:func:`expected_r2` is the standard approximation to how well that works.

**Within and between families.**  :func:`sibling_design` gives children a score with a direct effect and
parents whose own scores shape the home ("genetic nurture"), optionally in a population with two strata; the
effect estimated across families is larger than the one estimated between siblings, which is the direct one.
:func:`stratified_association` is the bare stratification artefact.

**Selection and coincidence.**  :func:`embryo_gain` is the expected gain from choosing the top-scoring of k
embryos; :func:`coincidences` counts how many of a long list of traits two strangers share by chance.

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import integrate, optimize, stats

__all__ = [
    "allele_sum", "TwinData", "twin_study", "falconer", "falconer_se", "ace_fit", "adoption_study",
    "midparent_offspring", "two_fields", "power_for_r2", "n_for_r2", "candidate_gene_study",
    "simulate_genotypes", "polygenic_trait", "gwas", "polygenic_score", "expected_r2", "sibling_design",
    "stratified_association", "expected_max", "embryo_gain", "coincidences",
]


# ----------------------------------------------------------------------------------------- many small genes
def allele_sum(n_loci: int, p: float = 0.5) -> tuple[np.ndarray, np.ndarray]:
    """The distribution of the number of "plus" alleles at ``n_loci`` loci (two alleles each, frequency ``p``):
    the values 0..2L and their probabilities."""
    k = np.arange(2 * n_loci + 1)
    return k, stats.binom.pmf(k, 2 * n_loci, p)


# ----------------------------------------------------------------------------------------- families
def _mate(rng, pm, pf, m: float):
    """An order for the fathers such that spouses' phenotypes correlate about ``m`` (by rank)."""
    n = len(pm)
    if m <= 0:
        return rng.permutation(n)
    z = m * (pm - pm.mean()) / pm.std() + math.sqrt(1 - m * m) * rng.standard_normal(n)
    order = np.empty(n, int)
    order[np.argsort(z)] = np.argsort(pf)
    return order


def _parents(rng, n, a2, e_var, assort):
    """Mothers' and fathers' breeding values, paired (optionally assortatively on phenotype)."""
    am, af = math.sqrt(a2) * rng.standard_normal(n), math.sqrt(a2) * rng.standard_normal(n)
    pm = am + math.sqrt(e_var) * rng.standard_normal(n)
    pf = af + math.sqrt(e_var) * rng.standard_normal(n)
    o = _mate(rng, pm, pf, assort)
    return am, af[o], pm, pf[o]


@dataclass
class TwinData:
    """Phenotypes of twin pairs reared together: ``mz`` and ``dz`` are (pairs, 2)."""
    mz: np.ndarray
    dz: np.ndarray

    @staticmethod
    def _r(pairs: np.ndarray) -> float:
        """The intraclass correlation (twin order is arbitrary, so each pair is entered both ways)."""
        x = np.r_[pairs[:, 0], pairs[:, 1]]
        y = np.r_[pairs[:, 1], pairs[:, 0]]
        return float(np.corrcoef(x, y)[0, 1])

    @property
    def r_mz(self) -> float:
        return self._r(self.mz)

    @property
    def r_dz(self) -> float:
        return self._r(self.dz)


def twin_study(n_mz: int, n_dz: int, a2: float, c2: float, e2: float, *, d2: float = 0.0, mz_extra: float = 0.0,
               assort: float = 0.0, rge: float = 0.0, rng=None) -> TwinData:
    """Twin pairs reared together.  ``a2``, ``d2``, ``c2``, ``e2`` are the variances of the additive, dominance,
    shared-environment and unshared parts (they need not sum to one).

    * ``mz_extra``: a share of the unshared variance that identical twins, and only they, have in common (they are
      treated more alike): the equal-environments assumption fails.
    * ``assort``: the correlation between spouses' phenotypes (one generation of assortative mating).
    * ``rge``: the correlation between the family's environment and the parents' average breeding value (parents'
      genes shape the home).
    """
    rng = rng or np.random.default_rng(0)

    def make(n, identical):
        am, af, _, _ = _parents(rng, n, a2, d2 + c2 + e2, assort)
        mid = (am + af) / 2
        seg = math.sqrt(a2 / 2)
        s1 = seg * rng.standard_normal(n)
        s2 = s1 if identical else seg * rng.standard_normal(n)
        z = rng.standard_normal(n)
        home = math.sqrt(c2) * (rge * (mid - mid.mean()) / (mid.std() or 1.0) + math.sqrt(1 - rge * rge) * z)
        if identical:
            d1 = d2_ = math.sqrt(d2) * rng.standard_normal(n)
            shared_e = math.sqrt(mz_extra * e2) * rng.standard_normal(n)
            own = math.sqrt((1 - mz_extra) * e2)
        else:
            u = rng.standard_normal(n)
            d1 = math.sqrt(d2) * (0.5 * u + math.sqrt(0.75) * rng.standard_normal(n))
            d2_ = math.sqrt(d2) * (0.5 * u + math.sqrt(0.75) * rng.standard_normal(n))
            shared_e, own = 0.0, math.sqrt(e2)
        p1 = mid + s1 + d1 + home + shared_e + own * rng.standard_normal(n)
        p2 = mid + s2 + d2_ + home + shared_e + own * rng.standard_normal(n)
        return np.c_[p1, p2]

    return TwinData(make(n_mz, True), make(n_dz, False))


def falconer(r_mz: float, r_dz: float) -> dict:
    """The classical estimates from the two twin correlations: h2 = 2 (rMZ - rDZ), c2 = 2 rDZ - rMZ,
    e2 = 1 - rMZ.  They can fall outside [0, 1]; that is information about the assumptions."""
    return {"h2": 2 * (r_mz - r_dz), "c2": 2 * r_dz - r_mz, "e2": 1 - r_mz}


def falconer_se(r_mz: float, r_dz: float, n_mz: int, n_dz: int) -> float:
    """The standard error of Falconer's h2: twice the root of the two correlations' sampling variances,
    (1 - r^2)^2 / (n - 1) each."""
    v = (1 - r_mz ** 2) ** 2 / (n_mz - 1) + (1 - r_dz ** 2) ** 2 / (n_dz - 1)
    return 2 * math.sqrt(v)


def _sym_cov(pairs: np.ndarray) -> np.ndarray:
    x = np.r_[pairs[:, 0], pairs[:, 1]]
    y = np.r_[pairs[:, 1], pairs[:, 0]]
    v, c = float(np.var(x)), float(np.cov(x, y, bias=True)[0, 1])
    return np.array([[v, c], [c, v]])


def ace_fit(data: TwinData) -> dict:
    """Maximum-likelihood ACE: variances a, c, e >= 0 with cov(MZ) = a + c and cov(DZ) = a / 2 + c, fitted to the
    two covariance matrices.  Returns the shares ``a2``, ``c2``, ``e2`` of the fitted variance, the variance
    ``total`` and the log-likelihood (up to a constant)."""
    s_mz, s_dz, n_mz, n_dz = _sym_cov(data.mz), _sym_cov(data.dz), len(data.mz), len(data.dz)

    def nll(theta):
        a, c, e = theta
        out = 0.0
        for s, n, g in ((s_mz, n_mz, 1.0), (s_dz, n_dz, 0.5)):
            v, cov = a + c + e, g * a + c
            sig = np.array([[v, cov], [cov, v]])
            sign, logdet = np.linalg.slogdet(sig)
            if sign <= 0:
                return 1e12
            out += 0.5 * n * (logdet + np.trace(np.linalg.solve(sig, s)))
        return out

    v0 = float(s_mz[0, 0] + s_dz[0, 0]) / 2
    best = None
    for start in ((0.4, 0.3, 0.3), (0.7, 0.05, 0.25), (0.1, 0.5, 0.4)):
        res = optimize.minimize(nll, np.array(start) * v0, method="L-BFGS-B", bounds=[(0, None), (0, None), (1e-6, None)])
        if best is None or res.fun < best.fun:
            best = res
    a, c, e = best.x
    tot = a + c + e
    return {"a2": float(a / tot), "c2": float(c / tot), "e2": float(e / tot), "total": float(tot), "loglik": float(-best.fun)}


def adoption_study(n: int, a2: float, c2: float, e2: float, *, placement: float = 0.0, rng=None) -> dict:
    """Three correlations an adoption design reads, simulated on ``n`` families each:

    * ``adoptive_siblings``: two unrelated children raised in one home: c2 (as a share of the variance);
    * ``parent_child_apart``: a biological parent and the child they did not raise: h2 / 2;
    * ``mz_apart``: identical twins raised in different homes: h2, the design of the Minnesota study.

    ``placement`` is the correlation between the two homes of separated twins (selective placement), which adds
    ``placement * c2`` to their resemblance."""
    rng = rng or np.random.default_rng(0)
    sa, sc, se = math.sqrt(a2), math.sqrt(c2), math.sqrt(e2)
    home = sc * rng.standard_normal(n)
    k1 = sa * rng.standard_normal(n) + home + se * rng.standard_normal(n)
    k2 = sa * rng.standard_normal(n) + home + se * rng.standard_normal(n)
    ap = sa * rng.standard_normal(n)
    parent = ap + sc * rng.standard_normal(n) + se * rng.standard_normal(n)
    child = ap / 2 + math.sqrt(0.75) * sa * rng.standard_normal(n) + sc * rng.standard_normal(n) + se * rng.standard_normal(n)
    at = sa * rng.standard_normal(n)
    h1 = rng.standard_normal(n)
    h2_ = placement * h1 + math.sqrt(1 - placement ** 2) * rng.standard_normal(n)
    t1 = at + sc * h1 + se * rng.standard_normal(n)
    t2 = at + sc * h2_ + se * rng.standard_normal(n)
    r = lambda x, y: float(np.corrcoef(x, y)[0, 1])  # noqa: E731
    return {"adoptive_siblings": r(k1, k2), "parent_child_apart": r(parent, child), "mz_apart": r(t1, t2)}


def midparent_offspring(n: int, a2: float, e2: float, rng=None) -> tuple[np.ndarray, np.ndarray]:
    """The parents' average phenotype and one child's, with no environment shared across the generations.  The
    regression slope of child on midparent is the heritability, a2 / (a2 + e2)."""
    rng = rng or np.random.default_rng(0)
    sa, se = math.sqrt(a2), math.sqrt(e2)
    am, af = sa * rng.standard_normal(n), sa * rng.standard_normal(n)
    mid = (am + se * rng.standard_normal(n) + af + se * rng.standard_normal(n)) / 2
    child = (am + af) / 2 + math.sqrt(a2 / 2) * rng.standard_normal(n) + se * rng.standard_normal(n)
    return mid, child


# ----------------------------------------------------------------------------------------- what it is not
def two_fields(n: int, h2_within: float = 0.9, gap: float = 3.0, rng=None) -> dict:
    """Seed from one sack sown in two fields.  Each plant's height is its genetic value plus its field's level
    plus a little noise.  Returns the heights and genetic values in each field, the heritability within each
    (``h2_within``, by construction) and the share of the gap between the fields that is genetic (zero)."""
    rng = rng or np.random.default_rng(0)
    sg, se = math.sqrt(h2_within), math.sqrt(1 - h2_within)
    g1, g2 = sg * rng.standard_normal(n), sg * rng.standard_normal(n)
    rich = gap + g1 + se * rng.standard_normal(n)
    poor = g2 + se * rng.standard_normal(n)
    return {"rich": rich, "poor": poor, "g_rich": g1, "g_poor": g2,
            "h2_rich": float(np.corrcoef(g1, rich)[0, 1] ** 2), "h2_poor": float(np.corrcoef(g2, poor)[0, 1] ** 2),
            "gap": float(rich.mean() - poor.mean()), "genetic_gap": float(g1.mean() - g2.mean())}


# ----------------------------------------------------------------------------------------- finding the genes
def power_for_r2(n: int, r2: float, alpha: float = 0.05) -> float:
    """The chance that a sample of ``n`` detects, at two-sided level ``alpha``, a variant that explains the share
    ``r2`` of a trait's variance (normal approximation to the test of a correlation)."""
    crit = stats.norm.isf(alpha / 2)
    ncp = math.sqrt(n * r2 / (1 - r2))
    return float(stats.norm.sf(crit - ncp) + stats.norm.cdf(-crit - ncp))


def n_for_r2(r2: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """The sample needed for that chance to be ``power``."""
    z = stats.norm.isf(alpha / 2) + stats.norm.isf(1 - power)
    return int(math.ceil(z * z * (1 - r2) / r2))


def candidate_gene_study(n: int, rng, *, maf: float = 0.4, outcomes: int = 2, r2: float = 0.0) -> dict:
    """One study of one candidate gene, analysed flexibly: a genotype (0, 1 or 2 copies), ``outcomes`` correlated
    measures of the trait, three genetic models (additive, dominant, recessive) and three samples (everyone, men,
    women).  Returns every p-value (``p``), the planned one (additive, everyone, first outcome) and the smallest.
    With ``r2 = 0`` the gene does nothing."""
    g = rng.binomial(2, maf, n).astype(float)
    sex = rng.integers(0, 2, n)
    base = rng.standard_normal(n)
    gs = (g - g.mean()) / g.std()
    ys = [math.sqrt(r2) * gs + math.sqrt(1 - r2) * (0.7 * base + math.sqrt(0.51) * rng.standard_normal(n))
          for _ in range(outcomes)]
    codings = [g, (g > 0).astype(float), (g > 1).astype(float)]
    ps = []
    for y in ys:
        for x in codings:
            for mask in (np.ones(n, bool), sex == 0, sex == 1):
                if x[mask].std() == 0:
                    ps.append(1.0)
                    continue
                ps.append(float(stats.pearsonr(x[mask], y[mask])[1]))
    return {"p": np.array(ps), "planned": ps[0], "smallest": float(min(ps))}


def simulate_genotypes(n: int, m: int, rng, maf_range=(0.05, 0.5)) -> np.ndarray:
    """Allele counts (0, 1, 2) for ``n`` unrelated people at ``m`` unlinked variants: (n, m) int8."""
    f = rng.uniform(*maf_range, m)
    return rng.binomial(2, f, (n, m)).astype(np.int8)


def _standardise(G: np.ndarray) -> np.ndarray:
    X = G.astype(np.float32)
    X -= X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    X /= sd
    return X


def polygenic_trait(G: np.ndarray, h2: float, n_causal: int, rng) -> tuple[np.ndarray, np.ndarray]:
    """A standardised trait in which ``n_causal`` of the variants (chosen at random) together explain ``h2``.
    Returns the trait and the true effect of each standardised variant (zero for the rest)."""
    n, m = G.shape
    beta = np.zeros(m)
    idx = rng.choice(m, n_causal, replace=False)
    beta[idx] = rng.standard_normal(n_causal) * math.sqrt(h2 / n_causal)
    g = _standardise(G) @ beta.astype(np.float32)
    g = (g - g.mean()) / g.std() * math.sqrt(h2)
    y = g + math.sqrt(1 - h2) * rng.standard_normal(n)
    return (y - y.mean()) / y.std(), beta


def gwas(G: np.ndarray, y: np.ndarray) -> dict:
    """One regression per variant: the estimated effect of each standardised variant on the standardised trait,
    its z statistic and two-sided p-value."""
    n = len(y)
    ys = (y - y.mean()) / y.std()
    beta = (_standardise(G).T @ ys.astype(np.float32)).astype(float) / n
    z = beta * math.sqrt(n - 2) / np.sqrt(np.clip(1 - beta ** 2, 1e-12, None))
    return {"beta": beta, "z": z, "p": 2 * stats.norm.sf(np.abs(z))}


def polygenic_score(G: np.ndarray, beta_hat: np.ndarray, p=None, threshold: float = 1.0) -> np.ndarray:
    """The sum of each person's standardised genotypes weighted by estimated effects, using the variants whose
    discovery p-value is below ``threshold`` (all of them by default)."""
    w = np.asarray(beta_hat, float).copy()
    if p is not None:
        w[np.asarray(p) > threshold] = 0.0
    return (_standardise(G) @ w.astype(np.float32)).astype(float)


def expected_r2(n: int, m: int, h2: float) -> float:
    """The share of a trait's variance a score should predict in new people when ``m`` independent variants carry
    a heritability ``h2`` and the effects were estimated on ``n`` people: h2 * n h2 / (n h2 + m)."""
    return h2 * n * h2 / (n * h2 + m)


# ----------------------------------------------------------------------------------------- within and between
def sibling_design(n_families: int, rng, *, direct: float = 0.3, nurture: float = 0.2, strata_gap: float = 0.0,
                   strata_env: float = 0.0) -> dict:
    """Two siblings a family.  Each child has a genetic score g (variance one in the population); the trait is
    ``direct * g`` plus ``nurture`` times the parents' average score (the home their genes helped make) plus
    noise.  With ``strata_gap`` the families come from two groups whose mean scores differ by that much and whose
    environments differ by ``strata_env``.  Returns the slope of the trait on the score across families
    (``population``), the slope of sibling differences on sibling score differences (``within``), and their
    ratio."""
    group = rng.integers(0, 2, n_families)
    shift = strata_gap * (group - 0.5)
    gm, gf = rng.standard_normal(n_families) + shift, rng.standard_normal(n_families) + shift
    mid = (gm + gf) / 2
    g1 = mid + math.sqrt(0.5) * rng.standard_normal(n_families)
    g2 = mid + math.sqrt(0.5) * rng.standard_normal(n_families)
    home = nurture * mid + strata_env * (group - 0.5)
    y1 = direct * g1 + home + rng.standard_normal(n_families)
    y2 = direct * g2 + home + rng.standard_normal(n_families)
    pop = float(np.polyfit(np.r_[g1, g2], np.r_[y1, y2], 1)[0])
    within = float(np.polyfit(g1 - g2, y1 - y2, 1)[0])
    return {"population": pop, "within": within, "ratio": within / pop, "g": np.c_[g1, g2], "y": np.c_[y1, y2]}


def stratified_association(n: int, rng, *, f_a: float = 0.2, f_b: float = 0.6, env_gap: float = 1.0) -> dict:
    """A variant that does nothing, in a sample drawn half from each of two groups that differ in the variant's
    frequency and, for unrelated reasons, in the trait.  Returns the p-value of the association in the pooled
    sample and within each group."""
    grp = rng.integers(0, 2, n)
    g = rng.binomial(2, np.where(grp == 0, f_a, f_b)).astype(float)
    y = env_gap * grp + rng.standard_normal(n)
    return {"pooled": float(stats.pearsonr(g, y)[1]), "within_a": float(stats.pearsonr(g[grp == 0], y[grp == 0])[1]),
            "within_b": float(stats.pearsonr(g[grp == 1], y[grp == 1])[1]),
            "r_pooled": float(np.corrcoef(g, y)[0, 1])}


# ----------------------------------------------------------------------------------------- selection, coincidence
def expected_max(k: int) -> float:
    """The expected value of the largest of ``k`` independent standard normal draws."""
    f = lambda x: x * k * stats.norm.pdf(x) * stats.norm.cdf(x) ** (k - 1)  # noqa: E731
    return float(integrate.quad(f, -10, 10)[0])


def embryo_gain(k: int, r2: float, sd: float = 15.0) -> float:
    """The expected gain, in trait units, from choosing the top-scoring of ``k`` embryos of one couple when the
    score predicts the share ``r2`` of the trait's variance in the population.  Siblings share half of the score's
    variance, so the spread to choose from is sd * sqrt(r2 / 2)."""
    return expected_max(k) * sd * math.sqrt(r2 / 2)


def coincidences(probs, n_pairs: int, rng) -> dict:
    """Two unrelated people compared on a list of traits, the chance of a match on trait i being ``probs[i]``.
    Returns the expected number of matches and the simulated numbers for ``n_pairs`` pairs of strangers."""
    p = np.asarray(probs, float)
    hits = (rng.random((n_pairs, len(p))) < p).sum(axis=1)
    return {"expected": float(p.sum()), "matches": hits}
