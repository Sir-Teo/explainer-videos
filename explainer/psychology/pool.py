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
TRUTH = {
    "rt_stages": RT_STAGES,
    "age_slope": AGE_SLOPE,
    "gonogo_decides": 0.5,  # the share of people for whom go/no-go includes the choice
    "cv_base": 0.12,  # trial-to-trial CV of sensing and responding
    "cv_stage": 0.60,  # trial-to-trial CV of the inserted stages
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
