"""Psyche's culture (Part 38): minds that learn from other minds, and measures that travel badly.

* :func:`conformist_step` and :func:`conformist_path`: Boyd and Richerson's conformist transmission.  A learner
  samples three models and adopts the majority variant with a bias D; the share p of a variant moves by
  D p (1 - p) (2p - 1) per generation, so the majority grows and the minority shrinks, and a population settles
  on whichever variant was ahead.  :func:`conformist_sim` does the same with finite learners.
* :func:`prestige_sim`: learners copy the most successful of a few models.  A second trait with no effect on
  success, carried by the successful, spreads with it (hitchhiking).
* :func:`skill_change` and :func:`tasmania`: Henrich's model of cumulative culture.  Each learner copies the most
  skilled member of the last generation and lands, on average, ``alpha`` below the model, with Gumbel noise of scale
  ``beta``; the best of N such copies gains beta (gamma + ln N) - alpha.  Below a critical population
  N* = exp(alpha / beta - gamma) a skill is lost, above it it accumulates.
* :func:`reference_group`: Heine and colleagues' reference-group effect.  People rate themselves on a Likert item
  relative to the people around them, so two cultures that differ in a trait can report the same mean, while a
  behavioural measure shows the difference.
* :func:`trolley`: a moral-judgment model.  The chance that a person in a country accepts a sacrifice is a logistic
  function of a case effect shared by all countries plus a country level; the order of the cases is universal and
  the levels vary.  :func:`fit_trolley` recovers both from simulated answers.
"""

from __future__ import annotations

import numpy as np

__all__ = ["conformist_step", "conformist_path", "conformist_sim", "prestige_sim", "skill_change",
           "critical_size", "tasmania", "reference_group", "TROLLEY_CASES", "trolley", "fit_trolley"]

EULER = 0.5772156649015329


def conformist_step(p, D: float = 0.3):
    """One generation of conformist transmission with three models: p + D p (1 - p) (2p - 1)."""
    p = np.asarray(p, float)
    return p + D * p * (1 - p) * (2 * p - 1)


def conformist_path(p0: float, D: float = 0.3, generations: int = 40) -> np.ndarray:
    out = [float(p0)]
    for _ in range(generations):
        out.append(float(conformist_step(out[-1], D)))
    return np.array(out)


def conformist_sim(n: int = 200, p0: float = 0.4, D: float = 0.3, generations: int = 40, seed: int = 0):
    """Finite learners, each sampling three models from the last generation.  With k of the three carrying the
    variant, a learner adopts it with chance 0, 1/3 - D/3, 2/3 + D/3 or 1, so that the expected share next
    generation is :func:`conformist_step`.  Returns the share carrying the variant by generation."""
    rng = np.random.default_rng(seed)
    x = rng.random(n) < p0
    out = [x.mean()]
    # adoption chance given k carriers among three, chosen so that E[adopt] = p + D p(1-p)(2p-1)
    adopt = np.array([0.0, 1 / 3 - D / 3, 2 / 3 + D / 3, 1.0])
    for _ in range(generations):
        k = x[rng.integers(0, n, size=(n, 3))].sum(axis=1)
        x = rng.random(n) < adopt[k]
        out.append(x.mean())
    return np.array(out)


def prestige_sim(n: int = 300, models: int = 5, generations: int = 30, seed: int = 0) -> dict:
    """Each person has a useful skill (raising success) and a neutral marker (a style, say).  Learners copy both
    from the most successful of ``models`` people sampled from the last generation, with copying error.  The marker
    starts in 10% of the population, carried by people with slightly more skill; it spreads although it does
    nothing."""
    rng = np.random.default_rng(seed)
    skill = rng.normal(size=n)
    marker = np.zeros(n, bool)
    top = np.argsort(skill)[-n // 10:]
    marker[top[rng.random(len(top)) < 0.9]] = True
    share, mean_skill = [marker.mean()], [skill.mean()]
    for _ in range(generations):
        success = skill + rng.normal(scale=3.0, size=n)
        pick = rng.integers(0, n, size=(n, models))
        best = pick[np.arange(n), np.argmax(success[pick], axis=1)]
        skill = skill[best] + rng.normal(scale=0.5, size=n) - 0.3
        flip = rng.random(n) < 0.02
        marker = np.where(flip, ~marker[best], marker[best])
        share.append(marker.mean())
        mean_skill.append(skill.mean())
    return {"share": np.array(share), "skill": np.array(mean_skill)}


def skill_change(N, alpha: float = 4.5, beta: float = 1.0):
    """Expected change per generation in the best skill when N learners copy the best model (Henrich 2004):
    beta (gamma + ln N) - alpha."""
    return beta * (EULER + np.log(np.asarray(N, float))) - alpha


def critical_size(alpha: float = 4.5, beta: float = 1.0) -> float:
    return float(np.exp(alpha / beta - EULER))


def tasmania(N: int, alpha: float = 4.5, beta: float = 1.0, generations: int = 60, z0: float = 10.0,
             seed: int = 0) -> np.ndarray:
    """The best skill in a population of N learners over generations.  Each learner copies the best of the last
    generation and lands at z_best - alpha + Gumbel(0, beta)."""
    rng = np.random.default_rng(seed)
    best = [z0]
    for _ in range(generations):
        z = best[-1] - alpha + rng.gumbel(0.0, beta, size=N)
        best.append(float(z.max()))
    return np.array(best)


def reference_group(n: int = 2000, true_gap: float = 0.8, seed: int = 0) -> dict:
    """Two cultures, A and B, with B higher on a trait by ``true_gap`` SDs.  Each person rates "I am X" on a 1-7
    scale by comparing themselves with the people around them (their own culture), so the self-report means
    match; a behavioural measure, noisy but absolute, shows the gap.  Returns trait, self-report and behaviour by
    culture, and the two standardized gaps."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0.0, 1.0, n)
    b = rng.normal(true_gap, 1.0, n)

    def likert(x, ref):
        z = (x - ref.mean()) / ref.std()
        return np.clip(np.round(4 + 1.2 * z + rng.normal(0, 0.6, len(x))), 1, 7)

    ra, rb = likert(a, a), likert(b, b)
    ba, bb = a + rng.normal(0, 1.0, n), b + rng.normal(0, 1.0, n)

    def d(x, y):
        return float((y.mean() - x.mean()) / np.sqrt((x.var() + y.var()) / 2))

    return {"trait": (a, b), "report": (ra, rb), "behaviour": (ba, bb), "gap_report": d(ra, rb),
            "gap_behaviour": d(ba, bb), "gap_trait": d(a, b)}


#: the three classic cases with the case effects (log-odds) that put Awad et al.'s country-level averages at
#: about 81%, 72% and 51% when countries vary around a level of zero
TROLLEY_CASES = {"switch": 1.95, "loop": 1.3, "footbridge": 0.05}


def _sig(x):
    return 1 / (1 + np.exp(-x))


def trolley(countries: int = 42, per: int = 600, country_sd: float = 0.45, person_sd: float = 1.2,
            seed: int = 0) -> dict:
    """Simulated answers: person j in country c accepts the sacrifice in case k with chance
    sigmoid(case_k + level_c + u_j).  Returns the levels and each country's share accepting each case."""
    rng = np.random.default_rng(seed)
    cases = np.array(list(TROLLEY_CASES.values()))
    level = rng.normal(0, country_sd, countries)
    share = np.zeros((countries, len(cases)))
    for c in range(countries):
        u = rng.normal(0, person_sd, per)
        p = _sig(cases[None, :] + level[c] + u[:, None])
        share[c] = (rng.random(p.shape) < p).mean(axis=0)
    return {"cases": list(TROLLEY_CASES), "level": level, "share": share}


def fit_trolley(share, eps: float = 1e-3) -> dict:
    """Additive fit of logit(share) = case + country (two-way means), as a check that the case order is shared."""
    s = np.clip(np.asarray(share, float), eps, 1 - eps)
    L = np.log(s / (1 - s))
    case = L.mean(axis=0)
    country = L.mean(axis=1) - L.mean()
    resid = L - case[None, :] - country[:, None]
    order_same = float(np.mean(np.all(np.diff(s, axis=1) < 0, axis=1)))
    return {"case": case, "country": country, "resid_sd": float(resid.std()), "order_same": order_same}
