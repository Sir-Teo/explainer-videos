"""The Battery of *Psychology, Built*: twelve classic tasks and one questionnaire, fixed for the whole series
(videos/psychology/SYLLABUS.md, §2.4).

Every task has three columns in the films: the published human benchmark, Psyche's result, and the viewer's.  This
module holds what the three share: the list of tasks with the signature a model must reproduce, and the trial-level
data format, :class:`Trials`, which Psyche's models, the Pool and the open datasets of the Archive all use, so one
plotting and fitting pipeline serves them all.

A task is added to :data:`RUNNERS` by the part that first uses it.  So far:

* Task 1, reaction time (Part 1): Donders' methods a (simple), c (go/no-go) and b (choice among ``n``),
  ``run("rt_simple" | "rt_gonogo" | "rt_choice", model, n_trials, seed)``.

Nothing here imports manim.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

__all__ = ["Task", "TASKS", "Trials", "run", "RUNNERS"]


@dataclass(frozen=True)
class Task:
    key: str  # short name, used in code and on the site
    number: object  # 1..12, or "Q" for the questionnaire
    name: str
    first_part: int  # the part of the series that first uses it
    signature: str  # what a model must reproduce to be credited with the task


TASKS = (
    Task("rt", 1, "Simple and choice reaction time", 1,
         "the right-skewed RT distribution; Hick's logarithm"),
    Task("threshold", 2, "Two-alternative threshold (contrast or length)", 11,
         "a psychometric function; Weber's fraction"),
    Task("stroop", 3, "Stroop colour naming", 18, "interference larger than facilitation; the delta plot"),
    Task("search", 4, "Visual search", 18,
         "flat and sloped set-size functions; target-absent slopes about twice target-present"),
    Task("change", 5, "Change detection", 19, "capacity near three to four items; precision falling with load"),
    Task("recall", 6, "Free recall of a word list", 20, "primacy, recency, contiguity"),
    Task("dots", 7, "Random-dot motion", 25, "accuracy and RT against coherence; fast and slow errors"),
    Task("bandit", 8, "Two-armed bandit and the two-step task", 17,
         "win-stay lose-shift; model-based and model-free signatures"),
    Task("gambles", 9, "Risky and delayed choices", 26, "the fourfold pattern; framing; hyperbolic discounting"),
    Task("rotation", 10, "Mental rotation", 24, "RT linear in angle"),
    Task("reading", 11, "Lexical decision and self-paced reading", 23, "frequency and surprisal effects"),
    Task("matrices", 12, "Matrix reasoning (generated items)", 32, "item difficulty ordered by rule count"),
    Task("ipip", "Q", "A 50-item public-domain Big Five inventory (IPIP)", 33, "five factors"),
)
TASK = {t.key: t for t in TASKS}


@dataclass
class Trials:
    """Trial-level data of one task: equal-length arrays, one entry per trial.

    ``subject`` an integer id (0 for a single subject), ``condition`` a short string per trial, ``rt`` in
    milliseconds (NaN where no response was required or given), ``correct`` a boolean, and ``extra`` any further
    per-trial arrays a task needs (stimulus values, responses)."""

    task: str
    subject: np.ndarray
    condition: np.ndarray
    rt: np.ndarray
    correct: np.ndarray
    extra: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.rt)

    def where(self, condition: str | None = None, subject: int | None = None) -> np.ndarray:
        """Boolean mask of the trials in ``condition`` (and of ``subject``) that have a response."""
        m = np.isfinite(self.rt)
        if condition is not None:
            m &= self.condition == condition
        if subject is not None:
            m &= self.subject == subject
        return m

    def rts(self, condition: str | None = None, subject: int | None = None) -> np.ndarray:
        return self.rt[self.where(condition, subject)]

    def mean_rt(self, condition: str | None = None, subject: int | None = None) -> float:
        return float(self.rts(condition, subject).mean())

    @staticmethod
    def concat(parts: list) -> "Trials":
        first = parts[0]
        return Trials(first.task, *(np.concatenate([getattr(p, f) for p in parts])
                                    for f in ("subject", "condition", "rt", "correct")),
                      extra={k: np.concatenate([p.extra[k] for p in parts]) for k in first.extra})


def _rt_task(condition: str):
    def runner(model, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
        """``model`` is a :class:`explainer.psychology.psyche.chronometry.StageModel` for this method."""
        rng = np.random.default_rng(seed)
        rt = model.sample(n_trials, rng)
        return Trials("rt", np.full(n_trials, subject), np.full(n_trials, condition), rt,
                      np.ones(n_trials, dtype=bool))

    return runner


RUNNERS = {"rt_simple": _rt_task("a"), "rt_gonogo": _rt_task("c"), "rt_choice": _rt_task("b")}


def run(name: str, model, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Run a Battery task on a model: ``run("rt_choice", models["b"], 200, seed=1)``."""
    return RUNNERS[name](model, n_trials, seed=seed, subject=subject)
