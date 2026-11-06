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
    # The lake (Part 3): a fish population, for capture-recapture
    # ------------------------------------------------------------------
    @cached_property
    def lake(self) -> dict:
        """The island's lake and its fish: the number is the truth that capture-recapture estimates (about 8,000), with
        each fish's length in cm (log-normal, median 31)."""
        g = self.rng("lake")
        n = int(g.poisson(8000))
        return {"n_fish": n, "length": np.exp(g.normal(np.log(31.0), 0.18, n))}

    # ------------------------------------------------------------------
    # Surveys (Part 18): an election, a telephone-and-car frame, and who answers
    # ------------------------------------------------------------------
    @cached_property
    def survey(self) -> dict:
        """Adults only.  ``vote_blue``: support for the challenger, Blue, in a two-way election, likelier with income
        (logistic in log income), older age and some regions (38.2% overall).  ``listed``: on the island's
        telephone-and-car registers, likelier with income (the *Literary Digest*'s frame).  ``propensity``: the chance
        of returning a mailed ballot, higher for Blue voters and the well-off (as Squire, 1988, found in 1936).
        ``turnout``: an enthusiasm score used by the pollsters' likely-voter screens.  Children are False / NaN."""
        g = self.rng("survey")
        a = self.age.astype(float)
        li = np.log(np.where(self.adult, self.income, 20_000.0))
        reg_eff = np.array([0.35, -0.25, 0.1, -0.4, 0.2, 0.0, -0.15, 0.3, -0.3, 0.15])[self.region]
        z_vote = -0.78 + 0.9 * (li - np.log(30_000)) + 0.012 * (a - 45) + reg_eff
        vote = self.adult & (g.random(self.n) < 1 / (1 + np.exp(-z_vote)))
        z_list = -1.6 + 1.5 * (li - np.log(30_000)) + 0.02 * (a - 45)
        listed = self.adult & (g.random(self.n) < 1 / (1 + np.exp(-z_list)))
        z_resp = -2.1 + 0.45 * vote + 0.25 * (li - np.log(30_000)) + 0.01 * (a - 45)
        propensity = np.where(self.adult, 1 / (1 + np.exp(-z_resp)), np.nan)
        turnout = np.where(self.adult, 1 / (1 + np.exp(-(-0.2 + 0.03 * (a - 45) + 0.3 * (li - np.log(30_000))))), np.nan)
        return {"vote_blue": vote, "listed": listed, "propensity": propensity, "turnout": turnout}

    # ------------------------------------------------------------------
    # Health (Part 20): salt, blood pressure, and a dietary survey
    # ------------------------------------------------------------------
    SODIUM_EFFECT = 1.5  # mm Hg of systolic pressure per g/day of current sodium intake, for every adult
    MEDS_EFFECT = 12.0  # mm Hg lowered by blood-pressure medicine
    TOLD_CUT = 0.10  # the share of sodium cut by those told their pressure is high

    @cached_property
    def health(self) -> dict:
        """Adults only (NaN / False for children).  ``bmi`` (log-normal, median rising to about 28 in middle age);
        usual energy intake ``kcal`` (men 2,400, women 1,800, falling after 30); usual sodium ``na_usual`` in mg (about
        1.75 mg per kcal, times a log-normal taste factor, so it tracks energy).  Systolic pressure before any
        diagnosis rises with age (curving upward), BMI and sodium (``SODIUM_EFFECT`` mm Hg per g), lower for women
        under 60, plus person-level noise (SD 12).  Those with untreated pressure of 140+ are ``told_high`` with
        probability 0.75 (others 0.04); the told cut their sodium by 10% (``TOLD_CUT``; ``na_current``) and 60% of them take
        ``bp_meds`` (``MEDS_EFFECT`` mm Hg).  ``sbp`` is the pressure now, from current sodium and medicine.
        Measurements: ``sbp_read`` (3 readings, each with SD 5 of noise) and two 24-hour recalls ``na_day1``/
        ``na_day2`` and ``kcal_day1``/``kcal_day2``: current intake times day-to-day log-normal variation (SD 0.40 for
        sodium, 0.30 for energy, correlated 0.7 within a day, since the same foods carry both)."""
        g = self.rng("health")
        n, ad = self.n, self.adult
        a = self.age.astype(float)
        female = ~self.male
        bmi = np.exp(np.log(24.0) + 0.16 * (1 - np.exp(-(a - ADULT_AGE).clip(0) / 15.0)) + 0.19 * g.standard_normal(n))
        kcal = np.where(self.male, 2400.0, 1800.0) * np.exp(-0.004 * (a - 30).clip(0) + 0.18 * g.standard_normal(n))
        na_usual = 1.75 * kcal * np.exp(-0.02 + 0.2 * g.standard_normal(n))
        base = (112.0 + 0.25 * (a - ADULT_AGE) + 0.006 * (a - ADULT_AGE) ** 2 + 0.5 * (bmi - 27.0)
                - 5.0 * (female & (a < 60)) + 12.0 * g.standard_normal(n))
        sbp0 = base + self.SODIUM_EFFECT * (na_usual / 1000 - 3.4)
        told = ad & (g.random(n) < np.where(sbp0 >= 140, 0.75, 0.04))
        na_current = na_usual * np.where(told, 1 - self.TOLD_CUT, 1.0)
        meds = told & (g.random(n) < 0.6)
        sbp = base + self.SODIUM_EFFECT * (na_current / 1000 - 3.4) - self.MEDS_EFFECT * meds
        reads = sbp[:, None] + 5.0 * g.standard_normal((n, 3))
        days = {}
        for d in (1, 2):
            z1 = g.standard_normal(n)
            z2 = 0.7 * z1 + np.sqrt(1 - 0.7 ** 2) * g.standard_normal(n)
            days[f"na_day{d}"] = na_current * np.exp(-0.40 ** 2 / 2 + 0.40 * z1)
            days[f"kcal_day{d}"] = kcal * np.exp(-0.30 ** 2 / 2 + 0.30 * z2)
        nan = lambda v: np.where(ad, v, np.nan)  # noqa: E731
        out = {"bmi": nan(np.round(bmi, 1)), "kcal": nan(kcal), "na_usual": nan(na_usual), "na_current": nan(na_current),
               "sbp": nan(sbp), "told_high": told, "bp_meds": meds, "sbp_read": np.where(ad[:, None], np.round(reads), np.nan)}
        out.update({k: nan(np.round(v)) for k, v in days.items()})
        return out

    # ------------------------------------------------------------------
    # Schools: pupils clustered in schools, a school-level programme (Parts 23, 25, 26)
    # ------------------------------------------------------------------
    N_SCHOOLS = 400
    SCHOOL_SD = 0.35  # SD of the school effect, in pupil-score SD units (about 100 points)
    PUPIL_SD = 0.85  # SD of the pupil-level noise
    SES_SCHOOL_SD = 0.45  # SD of schools' mean home background (SES)
    SES_SLOPE = 0.30  # score per unit of a pupil's own SES
    SES_CONTEXT = 0.15  # extra score per unit of the school's mean SES (the contextual effect)
    PROGRAMME_EFFECT = 0.20  # the tutoring programme's effect, in score SD units

    @cached_property
    def schools(self) -> dict:
        """400 schools, each in a town (drawn by town size), with 20 + Poisson(40) pupils.  Each school has a mean home
        background ``ses_school`` ~ N(0, 0.45^2) and an effect u ~ N(0, 0.35^2); half the schools, chosen at random, run
        a tutoring ``programme``.  Pupil ``ses`` = school mean + N(0, 0.9^2); ``score`` = 500 + 100 x (0.30 ses + 0.15
        ses_school + u + 0.20 programme + N(0, 0.85^2)).  Pupil arrays are flat, with ``school`` giving each pupil's
        school; the intraclass correlation of the score given the covariates is 0.35^2 / (0.35^2 + 0.85^2) = 0.145."""
        g = self.rng("schools")
        k = self.N_SCHOOLS
        town = g.choice(N_TOWNS, size=k, p=self.towns["weight"])
        size = 20 + g.poisson(40, k)
        ses_school = self.SES_SCHOOL_SD * g.standard_normal(k)
        u = self.SCHOOL_SD * g.standard_normal(k)
        programme = np.zeros(k, bool)
        programme[g.choice(k, k // 2, replace=False)] = True
        school = np.repeat(np.arange(k), size)
        ses = ses_school[school] + 0.9 * g.standard_normal(len(school))
        z = (self.SES_SLOPE * ses + self.SES_CONTEXT * ses_school[school] + u[school]
             + self.PROGRAMME_EFFECT * programme[school] + self.PUPIL_SD * g.standard_normal(len(school)))
        return {"town": town, "size": size, "ses_school": ses_school, "u": u, "programme": programme,
                "school": school, "ses": ses, "score": 500 + 100 * z}

    # ------------------------------------------------------------------
    # Doctor visits: overdispersed counts with structural zeros (Part 24)
    # ------------------------------------------------------------------
    VISITS_NEVER = 0.15  # share of adults (more of the young) who never see a doctor in a year
    VISITS_K = 1.2  # negative-binomial shape among the others

    @cached_property
    def visits(self) -> dict:
        """Adults only (-1 for children).  Visits to a doctor last year: with probability ``never`` (about 15%, falling
        with age from 25% at 18 to 8% at 80) a structural zero; otherwise negative binomial (shape 1.2) with mean
        exp(0.2 + 0.012 (age - 18) + 0.05 (BMI - 27) + 0.6 told_high + 0.25 female)."""
        g = self.rng("visits")
        a = self.age.astype(float)
        h = self.health
        bmi = np.nan_to_num(h["bmi"], nan=27.0)
        female = ~self.male
        never_p = np.clip(0.25 - 0.17 * (a - ADULT_AGE) / 62, 0.05, 0.25)
        mu = np.exp(0.2 + 0.012 * (a - ADULT_AGE) + 0.05 * (bmi - 27) + 0.6 * h["told_high"] + 0.25 * female)
        k = self.VISITS_K
        y = g.negative_binomial(k, k / (k + mu))
        never = g.random(self.n) < never_p
        y = np.where(never, 0, y)
        return {"visits": np.where(self.adult, y, -1).astype(np.int32), "never": never & self.adult, "mu": mu}

    # ------------------------------------------------------------------
    # Hospitals: a league table of death rates (Part 25)
    # ------------------------------------------------------------------
    N_HOSPITALS = 60
    HOSPITAL_SD = 0.3  # SD of the hospital effects on the log odds of death
    HOSPITAL_LOGIT = -3.2  # the typical hospital: about 4% deaths

    @cached_property
    def hospitals(self) -> dict:
        """60 hospitals performing one operation: yearly volumes log-uniform from 15 to 900, true death probabilities
        expit(-3.2 + u), u ~ N(0, 0.3^2), and last year's deaths ~ Binomial(volume, p)."""
        g = self.rng("hospitals")
        H = self.N_HOSPITALS
        n = np.round(np.exp(g.uniform(np.log(15), np.log(900), H))).astype(int)
        u = g.normal(0, self.HOSPITAL_SD, H)
        p = 1 / (1 + np.exp(-(self.HOSPITAL_LOGIT + u)))
        return {"operations": n, "u": u, "p": p, "deaths": g.binomial(n, p)}

    N_GENES = 5000
    GENE_PATIENTS = 25  # per group
    GENE_NONNULL = 250
    GENE_BLOCK = 25  # genes per pathway
    GENE_RHO = 0.3  # within-pathway correlation

    @cached_property
    def genes(self) -> dict:
        """The World's gene-expression study (Part 33): 5,000 genes measured on 25 patients and 25 healthy controls.
        Genes come in 200 pathways of 25, correlated 0.3 within a pathway (one shared factor each).  250 genes, in 10
        pathways, are truly differentially expressed, with effects (in SD units) uniform on 0.5 to 1.5 and a random
        sign; the other 4,750 are null.  Returns the expression matrix x (50 x 5000), group (1 = patient), the true
        effects delta and the nonnull mask."""
        g = self.rng("genes")
        m, n, B = self.N_GENES, 2 * self.GENE_PATIENTS, self.GENE_BLOCK
        nb = m // B
        f = g.standard_normal((n, nb))
        x = np.sqrt(self.GENE_RHO) * np.repeat(f, B, axis=1) + np.sqrt(1 - self.GENE_RHO) * g.standard_normal((n, m))
        group = np.r_[np.ones(self.GENE_PATIENTS, int), np.zeros(self.GENE_PATIENTS, int)]
        blocks = g.choice(nb, self.GENE_NONNULL // B, replace=False)
        nonnull = np.zeros(m, bool)
        for b in blocks:
            nonnull[b * B:(b + 1) * B] = True
        delta = np.zeros(m)
        delta[nonnull] = g.uniform(0.5, 1.5, nonnull.sum()) * g.choice([-1.0, 1.0], nonnull.sum())
        x = x + group[:, None] * delta[None, :]
        return {"x": x, "group": group, "delta": delta, "nonnull": nonnull, "pathway": np.repeat(np.arange(nb), B)}

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
            "blue_share": lambda: float(self.survey["vote_blue"][self.adult].mean()),
            "sodium_effect": lambda: float(self.SODIUM_EFFECT),
            "mean_sbp": lambda: float(self.health["sbp"][self.adult].mean()),
            "corr_midparent_child": lambda: float(np.corrcoef((self.families["z_father"] + self.families["z_mother"]) / 2,
                                                              self.families["z_child"])[0, 1]),
        }
        return table[name]()
