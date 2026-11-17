"""The Battery of *Psychology, Built*: twelve classic tasks and one questionnaire, fixed for the whole series
(videos/psychology/SYLLABUS.md, §2.4).

Every task has three columns in the films: the published human benchmark, Psyche's result, and the viewer's.  This
module holds what the three share: the list of tasks with the signature a model must reproduce, and the trial-level
data format, :class:`Trials`, which Psyche's models, the Pool and the open datasets of the Archive all use, so one
plotting and fitting pipeline serves them all.

A task is added to :data:`RUNNERS` by the part that first uses it.  So far:

* Task 1, reaction time (Part 1): Donders' methods a (simple), c (go/no-go) and b (choice among ``n``),
  ``run("rt_simple" | "rt_gonogo" | "rt_choice", model, n_trials, seed)``.
* Task 2, the two-alternative threshold (Part 11): which of two patches is brighter, by the method of constant
  stimuli, ``run("threshold", observer, n_trials, seed)`` with a :class:`explainer.psychology.psyche.psychophysics.
  Observer`; the increments are in ``extra["delta"]`` (a standard of 100, increments of 1 to 24).
* Task 3, Stroop colour naming (Part 18): congruent, neutral and incongruent trials in equal numbers, in random
  order, ``run("stroop", params, n_trials, seed)`` with ``params`` a dict of :func:`explainer.psychology.psyche.
  attention.stroop` keyword arguments (``{}`` for Psyche's defaults).
* Task 4, visual search (Part 18): feature and conjunction searches at set sizes 4, 8, 16 and 32, target present on
  half the trials, ``run("search", params, n_trials, seed)`` with ``params`` keyword arguments of
  :func:`explainer.psychology.psyche.attention.guided_search`; the set size and presence are in ``extra``.
* Task 5, change detection (Part 19): coloured squares at set sizes 2, 4, 6 and 8, one probed item changed on half
  the trials, ``run("change", params, n_trials, seed)`` with ``params`` keyword arguments of a slot observer
  (``K``, ``guess``); the set size and whether the probe changed are in ``extra``, and ``correct`` is whether the
  answer (same or different) was right.
* Task 6, free recall (Part 20): lists of sixteen words recalled at once by Psyche's context model,
  ``run("recall", params, n_lists, seed)`` with ``params`` overriding :data:`explainer.psychology.psyche.memory.
  CMR_DEFAULT`` (say, the values Part 20 fitted to PEERS); one trial is one list, with its recalls (serial positions
  in output order) in ``extra["recalls"]``.

* Task 9, risky and delayed choices (Part 26): sure amounts against "100 with probability p" for gains and
  losses (the fourfold pattern), the disease problem in both frames, and 100 sooner against 110 four weeks later
  at front-end delays from now to a year, ``run("gambles", params, n_trials, seed)`` with ``params`` overriding
  cumulative prospect theory's 1992 values, the choice sensitivities ``tau`` (gambles) and ``tau_t`` (delays) and
  the hyperbolic rate ``k`` per week; ``correct`` is whether the risky (or later) option was chosen, and the
  item is in ``extra`` (``p``, ``amount``, ``sure``, ``delay``).
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


THRESHOLD_STANDARD = 100.0
THRESHOLD_DELTAS = (1.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0)


def _threshold(model, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Two-alternative forced choice at fixed increments over a standard of 100, in random order; ``n_trials`` is
    rounded down to a multiple of the number of increments.  No response times are modelled (NaN)."""
    from explainer.psychology.psyche.psychophysics import two_afc

    rng = np.random.default_rng(seed)
    per = max(1, n_trials // len(THRESHOLD_DELTAS))
    t = two_afc(THRESHOLD_STANDARD, THRESHOLD_DELTAS, model, per, rng)
    n = len(t["delta"])
    return Trials("threshold", np.full(n, subject), np.full(n, "2afc"), np.full(n, np.nan), t["correct"],
                  extra={"delta": t["delta"], "standard": np.full(n, THRESHOLD_STANDARD)})


STROOP_CONDITIONS = ("congruent", "neutral", "incongruent")


def _stroop(params, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Colour naming on Psyche's two-pathway diffusion; conditions in equal numbers, shuffled."""
    from explainer.psychology.psyche.attention import stroop

    rng = np.random.default_rng(seed)
    cond = rng.permutation(np.resize(np.array(STROOP_CONDITIONS), n_trials))
    rt, ok = np.empty(n_trials), np.empty(n_trials, dtype=bool)
    for c in STROOP_CONDITIONS:
        m = cond == c
        r, k = stroop(c, "colour", n=int(m.sum()), rng=rng, **(params or {}))
        rt[m], ok[m] = r, k
    return Trials("stroop", np.full(n_trials, subject), cond, rt, ok)


SEARCH_SET_SIZES = (4, 8, 16, 32)


def _search(params, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Feature and conjunction search on Psyche's guided search: kind, set size and presence balanced and shuffled;
    the condition is ``"feature"`` or ``"conjunction"``."""
    from explainer.psychology.psyche.attention import guided_search, make_display

    rng = np.random.default_rng(seed)
    cells = [(k, s, p) for k in ("feature", "conjunction") for s in SEARCH_SET_SIZES for p in (True, False)]
    plan = [cells[i] for i in rng.permutation(np.resize(np.arange(len(cells)), n_trials))]
    rt, ok = np.empty(n_trials), np.empty(n_trials, dtype=bool)
    for i, (k, s, p) in enumerate(plan):
        rt[i], ok[i] = guided_search(make_display(s, k, p, rng), k, rng, **(params or {}))
    return Trials("search", np.full(n_trials, subject), np.array([c[0] for c in plan]), rt, ok,
                  extra={"set_size": np.array([c[1] for c in plan]), "present": np.array([c[2] for c in plan])})


CHANGE_SET_SIZES = (2, 4, 6, 8)


def _change(params, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Single-probe change detection by a slot observer: set size and change balanced and shuffled.  An observer
    stores ``min(K, N)`` items (a fractional K stores floor or ceiling); a stored probe is judged correctly, an
    unstored one is called "different" with probability ``guess``.  No RTs: ``rt`` is NaN."""
    p = {"K": 3.5, "guess": 0.45, **(params or {})}
    rng = np.random.default_rng(seed)
    cells = [(s, c) for s in CHANGE_SET_SIZES for c in (True, False)]
    plan = [cells[i] for i in rng.permutation(np.resize(np.arange(len(cells)), n_trials))]
    ok = np.empty(n_trials, dtype=bool)
    for i, (n, changed) in enumerate(plan):
        lo = np.floor(p["K"])
        stored = min(lo + (rng.random() < p["K"] - lo), n)
        if rng.random() < stored / n:
            ok[i] = True
        else:
            said_change = rng.random() < p["guess"]
            ok[i] = said_change == changed
    return Trials("change", np.full(n_trials, subject), np.array(["change"] * n_trials), np.full(n_trials, np.nan),
                  ok, extra={"set_size": np.array([c[0] for c in plan]), "changed": np.array([c[1] for c in plan])})


RECALL_LIST_LENGTH = 16


def _recall(params, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Immediate free recall of ``n_trials`` lists of sixteen words by Psyche's context model
    (:func:`explainer.psychology.psyche.memory.cmr_simulate`, ``params`` overriding its defaults).  One trial is one
    list: ``extra["recalls"]`` holds its recalls in output order as serial positions 1..16 (0 pads), ``correct`` is
    whether anything was recalled, and ``rt`` is NaN."""
    from explainer.psychology.psyche import memory

    R = memory.cmr_simulate(RECALL_LIST_LENGTH, n_trials, params or {}, np.random.default_rng(seed))
    return Trials("recall", np.full(n_trials, subject), np.array(["immediate"] * n_trials),
                  np.full(n_trials, np.nan), (R > 0).any(1), extra={"recalls": R})



GAMBLE_PROBS = (0.05, 0.25, 0.5, 0.75, 0.95)
GAMBLE_SURE = (5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0)
GAMBLE_DELAYS = (0.0, 1.0, 4.0, 12.0, 26.0, 52.0)  # weeks before the sooner reward


def _gamble_items() -> list:
    items = []
    for sign in (1.0, -1.0):
        for p in GAMBLE_PROBS:
            for s in GAMBLE_SURE:
                items.append(("gain" if sign > 0 else "loss", p, 100.0 * sign, s * sign, np.nan))
    items += [("frame_saved", 1 / 3, 600.0, 200.0, np.nan), ("frame_die", 2 / 3, -600.0, -400.0, np.nan)]
    items += [("delay", np.nan, 110.0, 100.0, d) for d in GAMBLE_DELAYS]
    return items


def _gambles(params, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Risky and delayed choices by Psyche's chooser (:mod:`explainer.psychology.psyche.choice`): a logistic rule
    on cumulative prospect theory's values for gambles, and on hyperbolically discounted amounts for delays.  The
    item list is cycled and shuffled."""
    from explainer.psychology.psyche import choice

    q = {**choice.TK92, "tau": 0.15, "tau_t": 0.3, "k": 0.05, **(params or {})}
    cpt = {k: q[k] for k in choice.TK92}
    rng = np.random.default_rng(seed)
    items = _gamble_items()
    plan = [items[i] for i in rng.permutation(np.resize(np.arange(len(items)), n_trials))]
    risky = np.empty(n_trials, dtype=bool)
    for t, (kind, p, amount, sure, delay) in enumerate(plan):
        if kind == "delay":
            d = amount * choice.discount(delay + 4.0, k=q["k"]) - sure * choice.discount(delay, k=q["k"])
            z = q["tau_t"] * d
        else:
            g = choice.cpt(choice.lottery((p, amount), (1 - p, 0.0)), **cpt)
            z = q["tau"] * (g - choice.cpt(choice.lottery((1.0, sure)), **cpt))
        risky[t] = rng.random() < 1 / (1 + np.exp(-np.clip(z, -60, 60)))
    return Trials("gambles", np.full(n_trials, subject), np.array([it[0] for it in plan]),
                  np.full(n_trials, np.nan), risky,
                  extra={"p": np.array([it[1] for it in plan]), "amount": np.array([it[2] for it in plan]),
                         "sure": np.array([it[3] for it in plan]), "delay": np.array([it[4] for it in plan])})


RUNNERS = {"rt_simple": _rt_task("a"), "rt_gonogo": _rt_task("c"), "rt_choice": _rt_task("b"), "threshold": _threshold,
           "stroop": _stroop, "search": _search, "change": _change, "recall": _recall, "gambles": _gambles}


def run(name: str, model, n_trials: int, seed: int = 0, subject: int = 0) -> Trials:
    """Run a Battery task on a model: ``run("rt_choice", models["b"], 200, seed=1)``."""
    return RUNNERS[name](model, n_trials, seed=seed, subject=subject)
