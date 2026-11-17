"""Psyche's lifespan (Part 31): three clocks that cannot be told apart without an assumption, designs that each get
ageing wrong in their own way, growth curves for every child, windows that close, and the slow drift of cohorts.

* :func:`apc_equivalent`: the age-period-cohort identity.  Because age = period - cohort, any linear trend can be moved
  between the three clocks: (a, p, c) and (a + k, p - k, c + k) predict exactly the same scores, for every k.
* :func:`ability_world`: a simulated population, born 1900 to 1990 and tested 1956 to 2019.  A true ageing curve (flat
  to about 55, then falling, faster with age) is added to a cohort drift (later cohorts score higher, the Flynn effect)
  and noise.  :func:`cross_sectional` tests everyone once, in one year; :func:`longitudinal` follows one cohort, with
  practice gains on retesting and selective drop-out of the lowest scorers; :func:`cohort_sequential` follows several
  cohorts and separates age from cohort under the assumption of no period effect.
* :func:`growth_data` and :func:`fit_growth`: children measured on several occasions; a linear mixed model with a random
  intercept and a random slope, fitted by EM.  It returns the population line, the spread of children's lines, the
  correlation of starting point and growth, and each child's shrunken (BLUP) line beside its own least-squares line.
* :func:`plasticity`: a sensitive period as a window whose openness falls logistically with age.
* :func:`fluid_crystallized`: illustrative curves for processing speed, fluid reasoning and vocabulary across adulthood.
* :func:`flynn_norms`: what happens to an IQ measured against old norms when scores drift by about three points a decade.
* :func:`lexis`: a table of mean scores by age and period, made by a pure age, period or cohort effect: the three
  graphs of the part's "On you".
* :func:`dual_systems`: illustrative curves for sensation seeking (peaking at 19) and self-regulation (rising to a
  plateau in the mid-twenties), the shape reported by Steinberg and colleagues in eleven countries.
* :func:`sibling_correlations`: the correlations of identical twins, fraternal twins and adoptive siblings under an
  ACE model; an adoptive sibling's correlation is the shared environment alone.
* :func:`reserve`: the threshold model of cognitive reserve: pathology accumulates; symptoms begin when it exceeds the
  reserve; more reserve means later onset and, once past the threshold, a steeper decline to the same end.
* :func:`paf` and :func:`combined_paf`: Levin's population attributable fraction, and the share preventable if several
  independent causal risk factors were all removed.
* :func:`hour_sampling`: how well one recorded hour a month, against one whole day a month, estimates how much a
  family talks (the measurement behind the word gap).
* :func:`fade_out` and :func:`familywise`: an illustrative fade-out of test-score effects, and the chance of at least
  one false positive among many outcomes.

Nothing here imports manim.
"""

from __future__ import annotations

import numpy as np

__all__ = ["apc_equivalent", "true_ageing", "ability_world", "cross_sectional", "longitudinal", "cohort_sequential",
           "growth_data", "fit_growth", "plasticity", "fluid_crystallized", "flynn_norms", "lexis", "dual_systems",
           "sibling_correlations", "reserve", "paf", "combined_paf", "hour_sampling", "fade_out", "familywise"]


# --------------------------------------------------------------------------------------------- three clocks
def apc_equivalent(a: float, p: float, c: float, k: float, age, period) -> dict:
    """Linear age, period and cohort effects (a, p, c) and the shifted set (a + k, p - k, c + k): the two sets of
    predictions for people of the given ages, tested in the given periods (cohort = period - age)."""
    age, period = np.asarray(age, float), np.asarray(period, float)
    cohort = period - age
    y1 = a * age + p * period + c * cohort
    y2 = (a + k) * age + (p - k) * period + (c + k) * cohort
    return {"y1": y1, "y2": y2, "max_diff": float(np.max(np.abs(y1 - y2)))}


def true_ageing(age, start: float = 55.0, rate: float = 0.012, accel: float = 0.0009) -> np.ndarray:
    """The ageing curve in standard-deviation units: zero until ``start``, then falling, faster with age."""
    x = np.maximum(np.asarray(age, float) - start, 0.0)
    return -(rate * x + accel * x ** 2)


def ability_world(n: int = 40_000, seed: int = 0, cohort_gain: float = 0.02, born=(1900, 1990)) -> dict:
    """A population: birth year uniform over ``born``; a stable person effect; score at a test in year t is
    person + true_ageing(age) + cohort_gain x (birth - 1950) + occasion noise.  ``cohort_gain`` is in SD per year of
    birth (0.02 is about three IQ points a decade).  Returns birth years and person effects for the designs."""
    rng = np.random.default_rng(seed)
    birth = rng.uniform(*born, size=n)
    person = rng.normal(0, 0.9, size=n)
    return {"birth": birth, "person": person, "cohort_gain": cohort_gain, "seed": seed}


def _score(w, idx, year, rng, practice: float = 0.0):
    age = year - w["birth"][idx]
    return (w["person"][idx] + true_ageing(age) + w["cohort_gain"] * (w["birth"][idx] - 1950)
            + practice + rng.normal(0, 0.44, size=len(idx)))


def cross_sectional(w, year: int = 1990, ages=range(20, 91, 5), per_age: int = 300, seed: int = 1) -> dict:
    """Everyone tested once, in ``year``: mean score by age band."""
    rng = np.random.default_rng(seed)
    out = []
    for a in ages:
        idx = np.where(np.abs((year - w["birth"]) - a) < 2.5)[0][:per_age]
        out.append(_score(w, idx, year, rng).mean())
    return {"age": np.array(list(ages), float), "mean": np.array(out)}


def longitudinal(w, birth_year: float = 1930, first: int = 1956, waves: int = 9, gap: int = 7, practice: float = 0.08,
                 dropout: float = 0.12, seed: int = 2) -> dict:
    """One cohort followed every ``gap`` years from ``first``: each retest adds ``practice`` (saturating), and before
    each wave a share ``dropout`` of the remaining people leave, the lowest scorers more often.  Returns mean scores of
    those still in the study, and of everyone (what full retention would show)."""
    rng = np.random.default_rng(seed)
    idx = np.where(np.abs(w["birth"] - birth_year) < 2.5)[0][:1500]
    stay = np.ones(len(idx), bool)
    ages, kept, everyone, n_left = [], [], [], []
    last = None
    for k in range(waves):
        year = first + gap * k
        prac = practice * (1 - 0.5 ** k) * 2
        s = _score(w, idx, year, rng, prac)
        if last is not None:
            # drop-out: probability rises as the last score falls
            z = (last - last[stay].mean()) / (last[stay].std() + 1e-9)
            p = dropout * 2 / (1 + np.exp(1.2 * z))
            stay &= rng.random(len(idx)) > p
        ages.append(year - birth_year)
        kept.append(s[stay].mean())
        everyone.append((s - prac).mean())
        n_left.append(int(stay.sum()))
        last = s
    return {"age": np.array(ages, float), "kept": np.array(kept), "everyone": np.array(everyone),
            "n": np.array(n_left)}


def cohort_sequential(w, cohorts=(1900, 1910, 1920, 1930, 1940, 1950, 1960), first: int = 1956, waves: int = 9,
                      gap: int = 7, seed: int = 3) -> dict:
    """Several cohorts, each followed (without practice or drop-out here); a regression of score on age dummies and
    birth year, assuming no period effect, recovers the ageing curve and the cohort drift."""
    rng = np.random.default_rng(seed)
    rows = []
    for c in cohorts:
        idx = np.where(np.abs(w["birth"] - c) < 2.5)[0][:300]
        for k in range(waves):
            year = first + gap * k
            age = year - c
            if age < 18 or age > 92:
                continue
            s = _score(w, idx, year, rng)
            rows.append((age, c, s.mean()))
    rows = np.array(rows)
    ages = np.unique(np.round(rows[:, 0] / 5) * 5)
    band = np.round(rows[:, 0] / 5) * 5
    X = np.column_stack([(band == a).astype(float) for a in ages] + [rows[:, 1] - 1950])
    beta, *_ = np.linalg.lstsq(X, rows[:, 2], rcond=None)
    curve = beta[:-1]
    curve = curve - curve[np.argmin(np.abs(ages - 40))]
    return {"age": ages, "curve": curve, "cohort_gain_hat": float(beta[-1]), "points": rows}


# --------------------------------------------------------------------------------------------- growth curves
def growth_data(n: int = 120, waves: int = 5, seed: int = 4, beta=(100.0, 6.0), sd_int: float = 8.0,
                sd_slope: float = 2.0, rho: float = 0.3, sd_e: float = 5.0) -> dict:
    """Children measured at ages 0..waves-1 (years from the first visit), with a random intercept and slope."""
    rng = np.random.default_rng(seed)
    cov = np.array([[sd_int ** 2, rho * sd_int * sd_slope], [rho * sd_int * sd_slope, sd_slope ** 2]])
    b = rng.multivariate_normal([0, 0], cov, size=n)
    t = np.arange(waves, dtype=float)
    y = (beta[0] + b[:, :1]) + (beta[1] + b[:, 1:]) * t[None, :] + rng.normal(0, sd_e, size=(n, waves))
    # some missed visits
    miss = rng.random((n, waves)) < 0.12
    miss[:, 0] = False
    y[miss] = np.nan
    return {"t": t, "y": y, "b_true": b, "beta": np.array(beta), "cov": cov, "sd_e": sd_e}


def fit_growth(t, y, iters: int = 300) -> dict:
    """Linear mixed model y_ij = (b0 + u0i) + (b1 + u1i) t_j + e_ij by EM (missing values allowed).  Returns the fixed
    effects, the random-effect covariance D, the residual variance, BLUPs, and per-child least-squares lines."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    n = len(y)
    obs = [~np.isnan(y[i]) for i in range(n)]
    Zs = [np.column_stack([np.ones(m.sum()), t[m]]) for m in obs]
    ys = [y[i][obs[i]] for i in range(n)]
    beta = np.linalg.lstsq(np.vstack(Zs), np.concatenate(ys), rcond=None)[0]
    D = np.eye(2)
    s2 = 1.0
    for _ in range(iters):
        bh, Vb = [], []
        XtVX = np.zeros((2, 2))
        XtVy = np.zeros(2)
        for Z, yi in zip(Zs, ys):
            V = Z @ D @ Z.T + s2 * np.eye(len(yi))
            Vi = np.linalg.inv(V)
            XtVX += Z.T @ Vi @ Z
            XtVy += Z.T @ Vi @ yi
        beta = np.linalg.solve(XtVX, XtVy)
        D_new = np.zeros((2, 2))
        s2_num, m_tot = 0.0, 0
        for Z, yi in zip(Zs, ys):
            V = Z @ D @ Z.T + s2 * np.eye(len(yi))
            Vi = np.linalg.inv(V)
            r = yi - Z @ beta
            b = D @ Z.T @ Vi @ r
            Vbi = D - D @ Z.T @ Vi @ Z @ D
            bh.append(b)
            Vb.append(Vbi)
            D_new += np.outer(b, b) + Vbi
            e = r - Z @ b
            s2_num += e @ e + np.trace(Z @ Vbi @ Z.T)
            m_tot += len(yi)
        D = D_new / n
        s2 = s2_num / m_tot
    ols = np.array([np.linalg.lstsq(Z, yi, rcond=None)[0] if len(yi) >= 2 else [np.nan, np.nan]
                    for Z, yi in zip(Zs, ys)])
    blup = beta[None, :] + np.array(bh)
    corr = D[0, 1] / np.sqrt(D[0, 0] * D[1, 1])
    return {"beta": beta, "D": D, "sd_int": float(np.sqrt(D[0, 0])), "sd_slope": float(np.sqrt(D[1, 1])),
            "rho": float(corr), "sd_e": float(np.sqrt(s2)), "blup": blup, "ols": ols}


# --------------------------------------------------------------------------------------------- windows and ageing
def plasticity(age, close: float = 2.0, width: float = 0.5, floor: float = 0.15) -> np.ndarray:
    """Openness of a sensitive period: about 1 early, falling to ``floor`` around ``close`` (logistic in age)."""
    a = np.asarray(age, float)
    return floor + (1 - floor) / (1 + np.exp((a - close) / width))


def fluid_crystallized(age) -> dict:
    """Illustrative adult curves in SD units relative to age 25: processing speed falls steadily from the twenties;
    fluid reasoning holds a little longer then falls; vocabulary rises into the sixties and declines late."""
    a = np.asarray(age, float)
    speed = -0.025 * np.maximum(a - 25, 0)
    fluid = -0.008 * np.maximum(a - 25, 0) - 0.0006 * np.maximum(a - 45, 0) ** 2
    vocab = 0.03 * np.minimum(np.maximum(a - 25, 0), 40) - 0.0012 * np.maximum(a - 65, 0) ** 2
    return {"speed": speed, "fluid": fluid, "vocab": vocab}


def flynn_norms(years_since_norming, points_per_decade: float = 3.0) -> np.ndarray:
    """The inflation of an IQ scored against norms ``years_since_norming`` old, if scores drift by
    ``points_per_decade``: the average person scores 100 + drift."""
    return 100.0 + points_per_decade * np.asarray(years_since_norming, float) / 10.0


# --------------------------------------------------------------------------------------------- three graphs, and more
def lexis(kind: str, ages=range(20, 81, 10), periods=range(1960, 2021, 10), size: float = 1.0) -> dict:
    """Mean scores on a grid of ages (rows) by test years (columns) when only one clock matters: ``"age"`` (decline
    after 50), ``"period"`` (a rise for everyone tested after 1990) or ``"cohort"`` (later birth, higher score).
    Returns the table and, for plotting, curves by age at each period (a cross-section per year)."""
    A = np.array(list(ages), float)[:, None]
    P = np.array(list(periods), float)[None, :]
    C = P - A
    if kind == "age":
        y = -size * np.maximum(A - 50, 0) / 30 + 0 * P
    elif kind == "period":
        y = size * np.clip((P - 1985) / 20, 0, 1) + 0 * A
    elif kind == "cohort":
        y = size * (C - 1940) / 60
    else:
        raise ValueError(kind)
    return {"ages": A[:, 0], "periods": P[0], "table": y}


def dual_systems(age) -> dict:
    """Illustrative curves on a 0-1 scale: sensation seeking rises to a peak at 19 and falls; self-regulation rises and
    levels off at about 24.  The gap between them is widest in mid-to-late adolescence."""
    a = np.asarray(age, float)
    seeking = 0.25 + 0.75 * np.exp(-((a - 19) / 6.5) ** 2)
    regulation = 0.2 + 0.75 / (1 + np.exp(-(a - 15.5) / 2.6))
    return {"seeking": seeking, "regulation": regulation, "gap": seeking - regulation}


def sibling_correlations(h2: float, c2: float) -> dict:
    """ACE model: identical twins share h2 + c2, fraternal twins h2/2 + c2, adoptive siblings c2 only."""
    return {"mz": h2 + c2, "dz": h2 / 2 + c2, "adoptive": c2, "e2": 1 - h2 - c2}


def reserve(age, reserve: float = 1.0, start: float = 50.0, rate: float = 0.0025, power: float = 2.0,
            end: float = 95.0, floor: float = -4.0) -> dict:
    """Pathology p(t) = rate (t - start)^power accumulates from ``start``; cognition stays at 0 until p exceeds the
    reserve, then falls linearly in pathology to ``floor`` at the pathology reached by age ``end``, whatever the
    reserve.  More reserve: a later onset and a steeper fall to the same end (Stern's account).  Returns pathology,
    cognition and the age at which symptoms begin."""
    a = np.asarray(age, float)
    path = rate * np.maximum(a - start, 0) ** power
    p_end = rate * (end - start) ** power
    cog = floor * np.clip((path - reserve) / (p_end - reserve), 0, 1)
    onset = start + (reserve / rate) ** (1 / power)
    return {"pathology": path, "cognition": cog, "onset": float(onset)}


def paf(p: float, rr: float) -> float:
    """Levin's population attributable fraction: p (RR - 1) / (1 + p (RR - 1)), valid only if the factor is causal."""
    x = p * (rr - 1)
    return float(x / (1 + x))


def combined_paf(pafs) -> float:
    """If independent causal factors were all removed: 1 - prod(1 - PAF_i).  Less than the sum, because one case can
    be attributed to several factors."""
    return float(1 - np.prod(1 - np.asarray(pafs, float)))


def hour_sampling(n_families: int = 40, seed: int = 6, months: int = 12, hours_per_day: int = 12) -> dict:
    """How well one recorded hour a month estimates a family's talk.  Each family has a mean rate of words per hour
    (lognormal across families); hours within a day vary widely (gamma, coefficient of variation about 0.9) and with
    the time of day.  Returns each family's true yearly mean rate, the estimate from one random hour per month, and
    the estimate from one whole day per month, with their correlations with the truth."""
    rng = np.random.default_rng(seed)
    mu = rng.lognormal(np.log(1200), 0.45, size=n_families)
    shape = 1.2
    tod = 0.6 + 0.8 * np.sin(np.linspace(0.2, np.pi - 0.2, hours_per_day))
    tod = tod / tod.mean()
    true = mu
    one_hour = np.empty(n_families)
    one_day = np.empty(n_families)
    for f in range(n_families):
        hrs = rng.gamma(shape, mu[f] * tod[None, :] / shape, size=(months, hours_per_day))
        pick = rng.integers(0, hours_per_day, size=months)
        one_hour[f] = hrs[np.arange(months), pick].mean()
        one_day[f] = hrs.mean()
    r_hour = float(np.corrcoef(np.log(true), np.log(one_hour))[0, 1])
    r_day = float(np.corrcoef(np.log(true), np.log(one_day))[0, 1])
    return {"true": true, "one_hour": one_hour, "one_day": one_day, "r_hour": r_hour, "r_day": r_day}


def fade_out(years, end_effect: float = 0.6, half_life: float = 1.2, floor: float = 0.0) -> np.ndarray:
    """Illustrative fade-out of a programme's effect on test scores: ``end_effect`` (SD) when it ends, halving every
    ``half_life`` years toward ``floor``."""
    t = np.asarray(years, float)
    return floor + (end_effect - floor) * 0.5 ** (np.maximum(t, 0) / half_life)


def familywise(m, alpha: float = 0.05) -> np.ndarray:
    """The chance of at least one p below ``alpha`` among m independent tests of true nulls."""
    return 1 - (1 - alpha) ** np.asarray(m, float)
