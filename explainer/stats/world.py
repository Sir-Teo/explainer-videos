"""The World: a simulated population of one million people whose truth we know (videos/stats/SYLLABUS.md, §2).

    from explainer.stats.world import World
    w = World()                         # seed 1662, version 1
    w.height[w.adult]                   # every adult's height (cm)
    w.truth("mean_height")              # the population value, exactly
    idx = w.sample(100, among=w.adult, seed=7)   # a simple random sample of 100 adults

In real data the truth is hidden; here every parameter is a number we can compute, so every estimator, test and
interval in the series can be graded against it.  The population is finite: a "true mean" is the mean of the million
values, not of an abstract distribution (the distributions they were drawn from are documented with each block, and
are what later parts call the superpopulation).

**Reproducible and stable.**  Each block (geography, people, heights, ...) draws from its own random stream,
``SeedSequence([seed, crc32(block)])``, and is built on first use.  Adding a block in a later part never changes the
values of an existing one, so a number shown in Part 1 is still true in Part 40.  ``VERSION`` changes only if an
existing block's law changes; caches are keyed by it.

Everything on screen that comes from here is tagged ``simulated`` (``explainer.stats.simulated_tag``).
"""

from __future__ import annotations

import zlib
from functools import cached_property

import numpy as np

VERSION = 1
N = 1_000_000
N_TOWNS = 200
N_REGIONS = 10
ADULT_AGE = 18


class World:
    def __init__(self, seed: int = 1662, n: int = N):
        self.seed, self.n = seed, n

    def rng(self, block: str) -> np.random.Generator:
        """The random stream of one block: independent of every other block, the same on every machine."""
        return np.random.Generator(np.random.PCG64(np.random.SeedSequence([self.seed, zlib.crc32(block.encode())])))

    # ------------------------------------------------------------------
    # Geography: an island of 200 towns in 10 regions
    # ------------------------------------------------------------------
    @cached_property
    def towns(self) -> dict:
        """Town centres on an island (a noisy superellipse, 10 units across), their regions (nearest of 10 region
        seats), and their sizes (Zipf, exponent 1.05: a few cities, many villages)."""
        g = self.rng("geography")
        pts = []
        while len(pts) < N_TOWNS:
            x, y = g.uniform(-5, 5), g.uniform(-3.4, 3.4)
            r = (abs(x / 5) ** 2.6 + abs(y / 3.4) ** 2.6) ** (1 / 2.6)
            wobble = 0.86 + 0.1 * np.sin(3 * np.arctan2(y, x) + 0.7) + 0.05 * np.cos(5 * np.arctan2(y, x))
            if r < wobble:
                pts.append((x, y))
        xy = np.array(pts)
        seats = xy[g.choice(N_TOWNS, N_REGIONS, replace=False)]
        for _ in range(20):  # a few Lloyd steps so the regions are compact
            region = np.argmin(((xy[:, None, :] - seats[None]) ** 2).sum(-1), 1)
            seats = np.array([xy[region == k].mean(0) if np.any(region == k) else seats[k] for k in range(N_REGIONS)])
        region = np.argmin(((xy[:, None, :] - seats[None]) ** 2).sum(-1), 1)
        rank = g.permutation(N_TOWNS) + 1
        weight = rank ** -1.05
        return {"xy": xy, "region": region, "weight": weight / weight.sum(), "seats": seats}

    @cached_property
    def town(self) -> np.ndarray:
        """Each resident's town (0-199)."""
        g = self.rng("residence")
        return g.choice(N_TOWNS, size=self.n, p=self.towns["weight"]).astype(np.int16)

    @cached_property
    def region(self) -> np.ndarray:
        return self.towns["region"][self.town].astype(np.int8)

    # ------------------------------------------------------------------
    # People: age and sex
    # ------------------------------------------------------------------
    @cached_property
    def age(self) -> np.ndarray:
        """Whole years, 0-99: a gently ageing pyramid (births slowly falling, mortality rising after 60)."""
        g = self.rng("age")
        a = np.arange(100)
        w = np.exp(-0.004 * a) / (1 + np.exp((a - 78) / 6.5))
        return g.choice(100, size=self.n, p=w / w.sum()).astype(np.int8)

    @cached_property
    def male(self) -> np.ndarray:
        g = self.rng("sex")
        return g.random(self.n) < 0.5

    @cached_property
    def adult(self) -> np.ndarray:
        return self.age >= ADULT_AGE

    # ------------------------------------------------------------------
    # Heights (cm)
    # ------------------------------------------------------------------
    HEIGHT_MEAN = {True: 176.0, False: 163.0}  # adult means, men and women
    HEIGHT_SD = {True: 7.1, False: 6.4}

    @cached_property
    def height(self) -> np.ndarray:
        """Adult height ~ N(176, 7.1^2) for men and N(163, 6.4^2) for women; children are the same target scaled
        by a growth curve (50% of adult height at birth's first year, full height at 18)."""
        g = self.rng("height")
        z = g.standard_normal(self.n)
        target = np.where(self.male, self.HEIGHT_MEAN[True] + self.HEIGHT_SD[True] * z,
                          self.HEIGHT_MEAN[False] + self.HEIGHT_SD[False] * z)
        a = self.age.astype(float)
        growth = np.where(a >= ADULT_AGE, 1.0, 0.30 + 0.70 * (1 - np.exp(-a / 5.5)) / (1 - np.exp(-ADULT_AGE / 5.5)))
        return target * growth

    # ------------------------------------------------------------------
    # Incomes (per year, adults)
    # ------------------------------------------------------------------
    PARETO_ALPHA = 2.1
    PARETO_XMIN = 110_000.0
    PARETO_SHARE = 0.025

    @cached_property
    def income(self) -> np.ndarray:
        """Adults only (NaN for children).  A log-normal body whose centre follows a career (rising to the mid-50s,
        falling at retirement), sigma 0.55; and a Pareto tail: 2.5% of adults draw instead from Pareto(110,000,
        alpha = 2.1), so the top of the distribution follows a power law, as Pareto (1896) found."""
        g = self.rng("income")
        a = self.age.astype(float)
        career = np.log(21_000) + 0.85 * (1 - np.exp(-(a - ADULT_AGE).clip(0) / 11.0)) - 0.45 * (a >= 67)
        body = np.exp(career + 0.55 * g.standard_normal(self.n))
        tail = self.PARETO_XMIN * g.random(self.n) ** (-1 / self.PARETO_ALPHA)
        y = np.where(g.random(self.n) < self.PARETO_SHARE, tail, body)
        return np.where(self.adult, np.round(y, -1), np.nan)

    # ------------------------------------------------------------------
    # Families: parents' and adult children's heights (Galton's question)
    # ------------------------------------------------------------------
    N_FAMILIES = 50_000
    ASSORTATIVE = 0.10  # correlation of the two parents' standardized heights
    HERITABLE = 0.70  # a child's standardized height regresses on the standardized mid-parent with this slope

    @cached_property
    def families(self) -> dict:
        """50,000 households: father, mother and one adult child.  Standardized heights: parents correlated 0.10;
        child = 0.70 * midparent + noise (unit variance), so corr(child, midparent) = 0.70 * sqrt(0.55) ~ 0.52, near
        what Galton (1886) measured.  Heights in cm use each person's sex's mean and SD."""
        g = self.rng("families")
        n = self.N_FAMILIES
        c = np.array([[1, self.ASSORTATIVE], [self.ASSORTATIVE, 1]])
        zf, zm = (g.standard_normal((n, 2)) @ np.linalg.cholesky(c).T).T
        zmid = (zf + zm) / 2
        b, v = self.HERITABLE, (1 + self.ASSORTATIVE) / 2
        zc = b * zmid + np.sqrt(1 - b * b * v) * g.standard_normal(n)
        son = g.random(n) < 0.5
        cm = lambda z, male: np.where(male, self.HEIGHT_MEAN[True] + self.HEIGHT_SD[True] * z,  # noqa: E731
                                      self.HEIGHT_MEAN[False] + self.HEIGHT_SD[False] * z)
        return {"father": cm(zf, True), "mother": cm(zm, False), "child": cm(zc, son), "son": son,
                "z_father": zf, "z_mother": zm, "z_child": zc}

    # ------------------------------------------------------------------
    # The clinic: a treatment, a severity, a recovery (Simpson's paradox)
    # ------------------------------------------------------------------
    CLINIC_N = 20_000
    CLINIC_SEVERE = 0.35  # share of patients with severe illness
    CLINIC_TREATED = {False: 0.25, True: 0.75}  # P(treated | severe?): doctors treat the sicker patients
    CLINIC_RECOVER = {(False, False): 0.80, (False, True): 0.87, (True, False): 0.40, (True, True): 0.48}

    @cached_property
    def clinic(self) -> dict:
        """20,000 patients.  Severe illness (35%) makes treatment likelier (75% vs 25%) and recovery rarer.  Within
        each severity the treatment raises recovery by 7-8 points (``CLINIC_RECOVER[(severe, treated)]``), yet the
        treated, being sicker, recover less often overall."""
        g = self.rng("clinic")
        n = self.CLINIC_N
        severe = g.random(n) < self.CLINIC_SEVERE
        treated = g.random(n) < np.where(severe, self.CLINIC_TREATED[True], self.CLINIC_TREATED[False])
        p = np.select([~severe & ~treated, ~severe & treated, severe & ~treated, severe & treated],
                      [self.CLINIC_RECOVER[(False, False)], self.CLINIC_RECOVER[(False, True)],
                       self.CLINIC_RECOVER[(True, False)], self.CLINIC_RECOVER[(True, True)]])
        return {"severe": severe, "treated": treated, "recovered": g.random(n) < p}

    # ------------------------------------------------------------------
    # Screening (Part 2): a condition and two tests
    # ------------------------------------------------------------------
    SCREEN_SENS = 0.90  # P(test positive | condition)
    SCREEN_SPEC = 0.95  # P(test negative | no condition)

    @cached_property
    def screening(self) -> dict:
        """A silent condition among adults whose risk rises with age (logistic in age; about 1% of adults overall),
        and two screening tests, each positive with probability 0.90 for those with the condition and 0.05 for those
        without, the two tests independent *given* the condition.  Children are never affected or tested
        (``tested`` marks the adults)."""
        g = self.rng("screening")
        age = self.age.astype(float)
        risk = 1.0 / (1.0 + np.exp(-(-6.3 + 0.045 * (age - ADULT_AGE))))
        sick = self.adult & (g.random(self.n) < risk)
        pos = [np.where(sick, g.random(self.n) < self.SCREEN_SENS, g.random(self.n) < 1 - self.SCREEN_SPEC) & self.adult
               for _ in range(2)]
        return {"sick": sick, "test_a": pos[0], "test_b": pos[1], "tested": self.adult.copy()}

    # ------------------------------------------------------------------
    # Sampling and the truth
    # ------------------------------------------------------------------
    def sample(self, n: int, among: np.ndarray | None = None, seed: int = 0) -> np.ndarray:
        """Indices of a simple random sample of ``n`` residents (without replacement), from those in ``among``."""
        pool = np.arange(self.n) if among is None else np.flatnonzero(among)
        g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([self.seed, zlib.crc32(b"sample"), seed])))
        return np.sort(g.choice(pool, size=n, replace=False))

    def truth(self, name: str) -> float:
        """The exact population value of a named quantity (the finite population of the World)."""
        h, y = self.height[self.adult], self.income[self.adult]
        table = {
            "mean_height": lambda: float(h.mean()),
            "sd_height": lambda: float(h.std()),
            "median_height": lambda: float(np.median(h)),
            "mean_income": lambda: float(y.mean()),
            "median_income": lambda: float(np.median(y)),
            "sd_income": lambda: float(y.std()),
            "n_adults": lambda: float(self.adult.sum()),
            "corr_midparent_child": lambda: float(np.corrcoef((self.families["z_father"] + self.families["z_mother"]) / 2,
                                                              self.families["z_child"])[0, 1]),
        }
        return table[name]()
