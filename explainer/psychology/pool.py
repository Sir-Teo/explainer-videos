"""The Pool: the simulated participant pool of *Psychology, Built* (videos/psychology/SYLLABUS.md, §2.3).

A seeded population of 100,000 simulated people.  Each is a Psyche with its own parameters, drawn from a
generative model that is written down here, so that the truth behind every simulated study is known and a method
can be graded against it.  **It is never evidence about people**: every frame that shows it carries the tag
``simulated: the Pool``.

The Pool grows with the series; each part adds the block its models need.  So far:

``age``
    Whole years, 18 to 80 (the lifespan arrives in Parts 30 and 31).

Reaction time (Part 1; times in ms)
    Every person has four stage means, ``sense``, ``respond``, ``discriminate`` and ``choose_bit`` (the time to
    choose per bit of uncertainty, as in Hick's law).  They are built from one general speed factor and specific
    parts,

        log(stage_j) = log(m_j) + s_j ( lam_j g + sqrt(1 - lam_j^2) e_j ),      g, e_j ~ N(0, 1) independent,

    so ``lam_j`` is the stage's loading on general speed and ``s_j`` its spread on the log scale.  ``respond``
    also changes by ``AGE_SLOPE`` ms for each year of age away from ``AGE_REF``.  And ``gonogo_decides`` marks the people who treat a
    go/no-go trial as a choice (Wundt's objection to Donders' method c): for them method c contains the choice
    stage too, so their b - c difference is zero.

    The planted values are in :data:`TRUTH`; ``tests/psychology/test_pool.py`` checks that large samples recover
    them.

Sessions (Part 2; times in ms)
    A person measured twice does not give the same number twice.  ``practice`` is how much faster the person's
    simple reaction gets with repeated sessions (a gain that approaches its ceiling geometrically),
    ``PRACTICE_RATE`` the share of the remaining gain picked up at each session, ``DAY_SD`` the day-to-day wobble
    of a person's own mean, and ``keen`` a standardized eagerness to sign up for things, which goes with being
    young and quick.  :meth:`Pool.session_rt` returns one session's mean simple reaction time for each person;
    ``explainer.psychology.lab`` builds its designs, sound and unsound, on it.

Traits and how they show (Part 3; standardized)
    Three traits, ``conscientious``, ``neurotic`` and ``extravert``, with the correlations of :data:`TRAIT_R`, and
    ``grit``, which correlates :data:`GRIT_R` with conscientiousness (the corrected correlation of Crede, Tynan and
    Harms 2017: a second name for nearly the same thing).  A trait is never seen.  What is seen is an answer, and
    an answer also carries the way it was obtained: ``style`` holds one independent standardized quantity per
    method (:data:`METHODS`: how a person tends to answer questionnaires, how they come across to a friend, how
    they look in a record).  :meth:`Pool.items` returns item answers, on a rating scale or continuous, as

        y = loading * trait + method_loading * style[method] + rest * e,        e ~ N(0, 1) per item and occasion,

    and :meth:`Pool.scale` their sum.  Because the truth is stored, a score's reliability and validity are
    known exactly and not estimated; ``explainer.psychology.measure`` holds the estimators that are graded
    against them.

    ``conflict`` is a person's true interference effect in a conflict task of the Stroop or flanker kind, in ms:
    everyone has one (:data:`CONFLICT_MEAN`), and people differ in it only a little (:data:`CONFLICT_SD`).
    :meth:`Pool.conflict_task` runs a session.  It is the Pool's version of the reliability paradox (Hedge, Powell
    and Sumner 2018), and Battery task 3 will be built on it in Part 18.

Nothing here imports manim.
"""

from __future__ import annotations

import math

import numpy as np

from .battery import Trials
from .psyche.chronometry import Stage, StageModel

__all__ = ["Pool", "TRUTH", "SEED"]

SEED = 1850  # the year of Fechner's morning and of Helmholtz's report
AGE_SLOPE = 0.55  # ms of simple RT per year of age, on the response stage (Woods et al. 2015)
AGE_REF = 41.5  # the stage medians below are those of a person of this age (the middle of Woods et al.'s 18 to 65)

# name: (median in ms, log-scale SD, loading on general speed)
RT_STAGES = {
    "sense": (131.0, 0.10, 0.60),  # Woods et al. (2015): stimulus detection time averaged 131 ms
    "respond": (82.0, 0.14, 0.60),  # 213 - 131: movement initiation
    "discriminate": (40.0, 0.30, 0.50),
    "choose_bit": (50.0, 0.30, 0.50),  # ms per bit of response uncertainty
}
PRACTICE_MEAN = 12.0  # ms: the mean total gain in simple RT from practice, over many sessions
PRACTICE_CV = 0.5
PRACTICE_RATE = 0.6  # the share of the remaining gain made at each new session
DAY_SD = 6.0  # ms: day-to-day standard deviation of one person's mean simple RT
KEEN_SPEED = -0.45  # loading of eagerness on general slowness (quick people sign up)
KEEN_AGE = -0.30  # ... and on standardized age (young people sign up)
# Part 3: traits, and the methods by which they are seen
TRAITS = ("conscientious", "neurotic", "extravert")
TRAIT_R = {("conscientious", "neurotic"): -0.25, ("conscientious", "extravert"): 0.10,
           ("neurotic", "extravert"): -0.20}
GRIT_R = 0.84  # grit with conscientiousness, corrected for unreliability (Crede, Tynan & Harms 2017)
METHODS = ("self", "peer", "record")  # a questionnaire, a friend's rating, a count from records
CUTS = {5: (-1.5, -0.5, 0.5, 1.5), 7: (-1.75, -1.05, -0.35, 0.35, 1.05, 1.75)}  # rating-scale thresholds
CONFLICT_MEAN, CONFLICT_SD = 60.0, 17.0  # ms: the interference effect, and how little people differ in it
CONFLICT_BASE, CONFLICT_BASE_S = 430.0, 0.15  # ms: median congruent RT, and its spread (log scale) with speed
CONFLICT_TRIAL_SD = 100.0  # ms: trial-to-trial standard deviation in both conditions
CONFLICT_DAY_SD = 15.0  # ms: a day's shift of a person's whole level (the same in both conditions)

TRUTH = {
    "rt_stages": RT_STAGES,
    "age_slope": AGE_SLOPE,
    "gonogo_decides": 0.5,  # the share of people for whom go/no-go includes the choice
    "cv_base": 0.12,  # trial-to-trial CV of sensing and responding
    "cv_stage": 0.60,  # trial-to-trial CV of the inserted stages
    "practice_mean": PRACTICE_MEAN,
    "practice_rate": PRACTICE_RATE,
    "day_sd": DAY_SD,
    "keen": {"speed": KEEN_SPEED, "age": KEEN_AGE},
    "trait_r": TRAIT_R,
    "grit_r": GRIT_R,
    "conflict": {"mean": CONFLICT_MEAN, "sd": CONFLICT_SD, "trial_sd": CONFLICT_TRIAL_SD},
}


class Pool:
    """The simulated population.  ``Pool()`` is the series' Pool; other seeds and sizes are for tests."""

    def __init__(self, n: int = 100_000, seed: int = SEED):
        self.n, self.seed = n, seed
        rng = np.random.Generator(np.random.PCG64(seed))
        self.age = rng.integers(18, 81, size=n)
        # --- reaction time (Part 1) ---
        self.speed = rng.standard_normal(n)  # g: general speed (positive = slower, as it multiplies durations)
        for name, (median, s, lam) in RT_STAGES.items():
            z = lam * self.speed + math.sqrt(1 - lam ** 2) * rng.standard_normal(n)
            setattr(self, name, median * np.exp(s * z))
        self.respond = self.respond + AGE_SLOPE * (self.age - AGE_REF)
        self.gonogo_decides = rng.random(n) < TRUTH["gonogo_decides"]
        # --- sessions (Part 2): drawn after everything above, so Part 1's people are unchanged ---
        self.practice = rng.gamma(1 / PRACTICE_CV ** 2, PRACTICE_MEAN * PRACTICE_CV ** 2, size=n)
        z_age = (self.age - self.age.mean()) / self.age.std()
        rest = math.sqrt(1 - KEEN_SPEED ** 2 - KEEN_AGE ** 2)
        self.keen = KEEN_SPEED * self.speed + KEEN_AGE * z_age + rest * rng.standard_normal(n)
        # --- traits and methods (Part 3): drawn after everything above ---
        corr = np.eye(len(TRAITS))
        for (a, b), r in TRAIT_R.items():
            i, j = TRAITS.index(a), TRAITS.index(b)
            corr[i, j] = corr[j, i] = r
        z = rng.standard_normal((n, len(TRAITS))) @ np.linalg.cholesky(corr).T
        for k, name in enumerate(TRAITS):
            setattr(self, name, z[:, k])
        self.grit = GRIT_R * self.conscientious + math.sqrt(1 - GRIT_R ** 2) * rng.standard_normal(n)
        self.style = {m: rng.standard_normal(n) for m in METHODS}
        s2 = math.log(1 + (CONFLICT_SD / CONFLICT_MEAN) ** 2)  # a lognormal with the stated mean and SD
        self.conflict = CONFLICT_MEAN * np.exp(math.sqrt(s2) * rng.standard_normal(n) - s2 / 2)

    # ------------------------------------------------------------------
    def sample(self, k: int, seed: int = 0, among=None) -> np.ndarray:
        """``k`` distinct people (indices), at random; ``among`` restricts to a boolean mask."""
        rng = np.random.Generator(np.random.PCG64([self.seed, 7, seed]))
        ids = np.arange(self.n) if among is None else np.flatnonzero(among)
        return rng.choice(ids, size=k, replace=False)

    # ------------------------------------------------------------------
    # Reaction time
    # ------------------------------------------------------------------
    def true_stage(self, ids, n_alternatives: int = 5) -> dict:
        """The planted stage means of the people ``ids`` (ms): what Donders' subtraction is trying to estimate.
        ``choose`` is the choice among ``n_alternatives``; ``c_minus_a`` and ``b_minus_c`` are the true
        differences of mean RT between the methods, which equal the stage means only for people who do not
        decide in go/no-go."""
        ids = np.asarray(ids)
        choose = self.choose_bit[ids] * math.log2(n_alternatives)
        dec = self.gonogo_decides[ids]
        return {"sense": self.sense[ids], "respond": self.respond[ids], "discriminate": self.discriminate[ids],
                "choose": choose, "c_minus_a": self.discriminate[ids] + np.where(dec, choose, 0.0),
                "b_minus_c": np.where(dec, 0.0, choose)}

    def rt_models(self, i: int, n_alternatives: int = 5) -> dict:
        """Person ``i``'s stage models for Donders' methods a, b and c."""
        base, stg = TRUTH["cv_base"], TRUTH["cv_stage"]
        sense, respond = Stage("sense", float(self.sense[i]), base), Stage("respond", float(self.respond[i]), base)
        disc = Stage("discriminate", float(self.discriminate[i]), stg)
        choose = Stage("choose", float(self.choose_bit[i]) * math.log2(n_alternatives), stg)
        a = StageModel((sense, respond))
        b = StageModel((sense, disc, choose, respond))
        c = b if self.gonogo_decides[i] else StageModel((sense, disc, respond))
        return {"a": a, "b": b, "c": c}

    def run_rt(self, ids, n_trials: int, seed: int = 0, n_alternatives: int = 5) -> Trials:
        """Donders' three methods on the people ``ids``: ``n_trials`` trials of each method for each person."""
        ids = np.asarray(ids)
        rng = np.random.Generator(np.random.PCG64([self.seed, 11, seed]))
        base, stg = TRUTH["cv_base"], TRUTH["cv_stage"]

        def draw(mean, cv):  # (people, trials) gamma durations with the given per-person means
            return rng.gamma(1 / cv ** 2, (mean * cv ** 2)[:, None], size=(len(ids), n_trials))

        t = self.true_stage(ids, n_alternatives)
        out = []
        for method in "abc":
            rt = draw(t["sense"], base) + draw(t["respond"], base)
            if method in "bc":
                rt = rt + draw(t["discriminate"], stg)
            ch = draw(t["choose"], stg)
            if method == "b":
                rt = rt + ch
            elif method == "c":
                rt = rt + ch * self.gonogo_decides[ids][:, None]
            out.append(Trials("rt", np.repeat(ids, n_trials), np.full(rt.size, method), rt.ravel(),
                              np.ones(rt.size, dtype=bool)))
        return Trials.concat(out)

    # ------------------------------------------------------------------
    # Sessions (Part 2)
    # ------------------------------------------------------------------
    def simple_mean(self, ids) -> np.ndarray:
        """Each person's own long-run mean simple reaction time before any practice (ms)."""
        ids = np.asarray(ids)
        return self.sense[ids] + self.respond[ids]

    def practice_gain(self, ids, session: int) -> np.ndarray:
        """How much faster (ms) each person is at session ``session`` (0 is the first) than at session 0."""
        ids = np.asarray(ids)
        return self.practice[ids] * (1 - (1 - PRACTICE_RATE) ** session)

    def session_rt(self, ids, session: int = 0, n_trials: int = 20, seed: int = 0, shift=0.0) -> np.ndarray:
        """The mean simple reaction time (ms) of each person in ``ids`` over ``n_trials`` trials of one session.

        ``session`` counts the person's earlier sessions (practice makes later ones faster); ``shift`` is added
        to everyone (or, as an array, to each person): a treatment effect, or something that happened to the
        whole laboratory.  The same ``seed`` and ``session`` give the same numbers.
        """
        ids = np.asarray(ids)
        rng = np.random.Generator(np.random.PCG64([self.seed, 23, seed, session]))
        cv = TRUTH["cv_base"]
        trial_sd = cv * np.sqrt(self.sense[ids] ** 2 + self.respond[ids] ** 2)
        mean = self.simple_mean(ids) - self.practice_gain(ids, session) + np.asarray(shift, dtype=float)
        day = DAY_SD * rng.standard_normal(len(ids))
        return mean + day + trial_sd / math.sqrt(n_trials) * rng.standard_normal(len(ids))

    # ------------------------------------------------------------------
    # Part 3: answers, scales, and a conflict task
    # ------------------------------------------------------------------
    def items(self, trait: str, ids, k: int, seed: int = 0, loading=0.6, method: str | None = None,
              method_loading: float = 0.0, points: int | None = 5) -> np.ndarray:
        """Answers of the people ``ids`` to ``k`` items that tap ``trait`` (any standardized attribute of the
        Pool).  ``loading`` is one number or one per item; ``method`` adds that method's style with
        ``method_loading``.  ``points`` cuts the answer into a rating scale of 5 or 7 (1 is lowest); ``None``
        leaves it continuous.  ``seed`` is the occasion: the same seed gives the same answers."""
        ids = np.asarray(ids)
        lam = np.broadcast_to(np.asarray(loading, dtype=float), (k,))
        rest = 1 - lam ** 2 - method_loading ** 2
        if np.any(rest < 0):
            raise ValueError("loading and method_loading leave no room for error")
        rng = np.random.Generator(np.random.PCG64([self.seed, 303, seed]))
        y = lam * getattr(self, trait)[ids, None] + np.sqrt(rest) * rng.standard_normal((len(ids), k))
        if method is not None:
            y = y + method_loading * self.style[method][ids, None]
        if points is None:
            return y
        return 1 + np.searchsorted(np.asarray(CUTS[points]), y)

    def scale(self, trait: str, ids, k: int, seed: int = 0, **kw) -> np.ndarray:
        """The sum score of a ``k``-item scale (see :meth:`items`)."""
        return self.items(trait, ids, k, seed, **kw).sum(axis=1).astype(float)

    def conflict_task(self, ids, n_trials: int = 120, seed: int = 0) -> dict:
        """One session of a conflict task for the people ``ids``: mean RT (ms) over ``n_trials`` congruent and
        ``n_trials`` incongruent trials, and their difference, the ``cost``.  A person's level shifts from day to
        day, the same in both conditions, so the shift cancels in the cost."""
        ids = np.asarray(ids)
        rng = np.random.Generator(np.random.PCG64([self.seed, 304, seed]))
        base = CONFLICT_BASE * np.exp(CONFLICT_BASE_S * self.speed[ids]) + CONFLICT_DAY_SD * rng.standard_normal(len(ids))
        noise = CONFLICT_TRIAL_SD / math.sqrt(n_trials)
        congruent = base + noise * rng.standard_normal(len(ids))
        incongruent = base + self.conflict[ids] + noise * rng.standard_normal(len(ids))
        return {"congruent": congruent, "incongruent": incongruent, "cost": incongruent - congruent}
