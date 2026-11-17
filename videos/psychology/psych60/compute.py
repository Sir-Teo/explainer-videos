"""Precompute every number in Part 60 of *Psychology, Built* ("Minds and Machines").

    python -m videos.psychology.psych60.compute            # everything missing (seconds)

Results are cached in ``.cache/psych60/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.machines``); no language model is run.

Items:
    contam      a memorizer and a reasoner on published items and perturbed variants
    prompts     one model asked in 100 phrasings, against twelve models: naive and honest intervals
    irt         a 300-item benchmark as a test: accuracies, item information, leaderboard stability
    separate    items needed to separate two models by 3 points, independent and paired
    silicon     silicon respondents against human ones: means, spreads, small groups
    reliance    accuracy against reliance on an aid, and algorithm aversion over 40 trials
    spec        a specification curve for screen time and well-being (288 analyses)
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import machines as M

CACHE = Cache("psych60")
load = CACHE.load


def compute_contam() -> dict:
    runs = [M.contamination(seed=6000 + r) for r in range(20)]
    return {"memorizer": np.mean([r["memorizer"] for r in runs], 0), "reasoner": np.mean([r["reasoner"] for r in runs], 0)}


def compute_prompts() -> dict:
    one = M.prompt_sample(n_prompts=100, n_models=1, seed=6001)
    many = M.prompt_sample(n_prompts=100, n_models=12, seed=6002)
    return {"one_est": one["estimate"], "one_naive": one["naive_ci"], "one_honest": one["honest_ci"],
            "many_est": many["estimate"], "many_naive": many["naive_ci"], "many_honest": many["honest_ci"],
            "model_rates": many["model_rates"]}


def compute_irt() -> dict:
    return M.benchmark_irt(seed=6003)


def compute_separate() -> dict:
    return M.items_to_separate(delta_acc=0.03, acc=0.7)


def compute_silicon() -> dict:
    return M.silicon(seed=6004)


def compute_reliance() -> dict:
    r = M.reliance()
    a = M.aversion(seed=6005)
    return {"shares": r["shares"], "accuracy": r["accuracy"], "reliance_t": a["reliance"], "acc_t": a["accuracy"],
            "best": r["best"]}


def compute_spec() -> dict:
    return M.specification_curve(M.screen_data(seed=6006))


ITEMS = {"contam": compute_contam, "prompts": compute_prompts, "irt": compute_irt, "separate": compute_separate,
         "silicon": compute_silicon, "reliance": compute_reliance, "spec": compute_spec}

if __name__ == "__main__":
    CACHE.main(ITEMS)
