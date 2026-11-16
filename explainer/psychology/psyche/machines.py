"""Psyche's machine-psychology bench (Part 60): psychology's methods applied to artificial minds, and to people
using them.

No language model is run here (the series' machines have no network and no GPU); each function simulates the
method problem it is named for, with the truth known, so that the trap can be seen:

* contamination: a test-taker that has memorized published items against one that reasons, on the original items
  and on perturbed variants;
* prompt sensitivity: one model asked one question in many phrasings is one subject measured many times, not a
  sample of subjects;
* item response theory for benchmarks: which items separate models, and how stable a leaderboard's ranking is
  under resampling of items;
* silicon samples: simulated respondents that reproduce group averages but shrink the spread within groups and the
  differences of small groups;
* reliance on advice: the accuracy of a person with an aid, for every policy of reliance, and algorithm aversion
  after a visible error;
* a specification curve for screen time and well-being: many defensible analyses of one simulated data set.

numpy and scipy only.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy import stats


# ----------------------------------------------------------------------------------------------------------------
# Method traps
# ----------------------------------------------------------------------------------------------------------------
def contamination(n_items: int = 200, memorized: float = 0.8, reason_acc: float = 0.55, seed: int = 0) -> dict:
    """Two test-takers on a published problem set.  The memorizer saw a share ``memorized`` of the items during
    training and answers those from memory (right), the rest at chance among 4 options; the reasoner answers every
    item correctly with probability ``reason_acc``.  On perturbed variants (same logic, new surface), memory no
    longer helps.  The memorizer looks better on the originals and collapses on the variants."""
    rng = np.random.default_rng(seed)
    seen = rng.random(n_items) < memorized
    mem_orig = np.where(seen, 1.0, rng.random(n_items) < 0.25)
    mem_var = (rng.random(n_items) < 0.25).astype(float)
    rea_orig = (rng.random(n_items) < reason_acc).astype(float)
    rea_var = (rng.random(n_items) < reason_acc).astype(float)
    return {"memorizer": [float(mem_orig.mean()), float(mem_var.mean())],
            "reasoner": [float(rea_orig.mean()), float(rea_var.mean())]}


def prompt_sample(n_prompts: int = 100, n_models: int = 1, model_sd: float = 0.15, prompt_sd: float = 0.08,
                  mean: float = 0.6, seed: int = 0) -> dict:
    """The share of "human-like" answers when a model is asked in ``n_prompts`` phrasings.  Each model has its own
    true rate (spread ``model_sd`` between models); each phrasing moves it by ``prompt_sd``.  A confidence interval
    that treats the phrasings as independent subjects is far too narrow for a claim about models in general."""
    rng = np.random.default_rng(seed)
    model_rates = np.clip(rng.normal(mean, model_sd, n_models), 0.01, 0.99)
    rates = np.clip(model_rates[:, None] + rng.normal(0, prompt_sd, (n_models, n_prompts)), 0, 1)
    est = rates.mean()
    naive_se = rates.std(ddof=1) / np.sqrt(rates.size)
    honest_se = np.sqrt(model_sd ** 2 / n_models + prompt_sd ** 2 / rates.size)
    return {"estimate": float(est), "naive_ci": [float(est - 1.96 * naive_se), float(est + 1.96 * naive_se)],
            "honest_ci": [float(est - 1.96 * honest_se), float(est + 1.96 * honest_se)],
            "model_rates": model_rates}


def benchmark_irt(n_items: int = 300, n_models: int = 12, seed: int = 0, boot: int = 400) -> dict:
    """A benchmark as a test (Part 45): 2PL items with discriminations from 0.2 to 2.5 and difficulties spread
    widely; models with abilities from -1.5 to 1.5.  Returns the accuracy of each model, each item's information
    at the models' abilities, and how often a bootstrap over items reproduces the leaderboard's order."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.2, 2.5, n_items)
    b = rng.normal(0, 1.5, n_items)
    theta = np.sort(np.linspace(-1.5, 1.5, n_models) + rng.normal(0, 0.05, n_models))
    P = 1 / (1 + np.exp(-a[None, :] * (theta[:, None] - b[None, :])))
    X = (rng.random(P.shape) < P).astype(float)
    acc = X.mean(1)
    info = (a[None, :] ** 2 * P * (1 - P)).mean(0)
    order = np.argsort(-acc)
    same_top, kendall = 0, []
    for _ in range(boot):
        idx = rng.integers(0, n_items, n_items)
        acc_b = X[:, idx].mean(1)
        same_top += int(np.argmax(acc_b) == order[0])
        kendall.append(stats.kendalltau(acc, acc_b)[0])
    useful = np.argsort(-info)[: n_items // 5]
    return {"theta": theta, "accuracy": acc, "info": info, "a": a, "b": b, "top_stable": same_top / boot,
            "kendall": float(np.mean(kendall)), "useful_share_info": float(info[useful].sum() / info.sum())}


def items_to_separate(delta_acc: float = 0.03, acc: float = 0.7, power: float = 0.8, alpha: float = 0.05,
                      paired_corr: float = 0.5) -> dict:
    """How many items a benchmark needs to show that two models differ by ``delta_acc`` in accuracy: independent
    item scores, or paired scores on the same items (correlation ``paired_corr``), which need fewer."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    var = acc * (1 - acc)
    n_ind = 2 * var * z ** 2 / delta_acc ** 2
    n_pair = 2 * var * (1 - paired_corr) * z ** 2 / delta_acc ** 2
    return {"independent": float(n_ind), "paired": float(n_pair)}


# ----------------------------------------------------------------------------------------------------------------
# Silicon samples
# ----------------------------------------------------------------------------------------------------------------
def silicon(n: int = 5000, shares=(0.45, 0.30, 0.15, 0.07, 0.03), means=(5.0, 5.6, 4.4, 6.2, 3.0),
            sd: float = 1.6, shrink: float = 0.35, minority_pull: float = 0.6, seed: int = 0) -> dict:
    """A survey answer on a 1-to-9 scale in five groups.  "Silicon" respondents are generated from the group means
    a language model has absorbed: their spread within a group is shrunk by ``shrink`` and small groups' means are
    pulled toward the overall mean by ``minority_pull`` times (1 - share) (the majority's view dominates the
    training text).  Aggregates nearly match; spreads and minority differences do not."""
    rng = np.random.default_rng(seed)
    shares = np.asarray(shares) / np.sum(shares)
    means = np.asarray(means, float)
    g = rng.choice(len(shares), n, p=shares)
    human = np.clip(rng.normal(means[g], sd), 1, 9)
    overall = float(np.sum(shares * means))
    sil_means = means + minority_pull * (1 - shares) ** 4 * (overall - means)
    sil = np.clip(rng.normal(sil_means[g], sd * shrink), 1, 9)
    out = {"shares": shares, "human_mean": float(human.mean()), "silicon_mean": float(sil.mean()),
           "human_sd": float(human.std()), "silicon_sd": float(sil.std()),
           "human_group": np.array([human[g == k].mean() for k in range(len(shares))]),
           "silicon_group": np.array([sil[g == k].mean() for k in range(len(shares))])}
    out["group_error"] = out["silicon_group"] - out["human_group"]
    return out


# ----------------------------------------------------------------------------------------------------------------
# People relying on machines
# ----------------------------------------------------------------------------------------------------------------
def reliance(aid_acc: float = 0.8, human_acc: float = 0.7, shares=np.linspace(0, 1, 21)) -> dict:
    """The accuracy of a person who follows an aid on a share of decisions chosen at random, and of one who
    follows it exactly when it is more likely right (here always, since aid_acc > human_acc)."""
    shares = np.asarray(shares)
    acc = shares * aid_acc + (1 - shares) * human_acc
    return {"shares": shares, "accuracy": acc, "best": float(max(aid_acc, human_acc))}


def aversion(trials: int = 40, aid_acc: float = 0.8, human_acc: float = 0.7, drop: float = 0.5, recover: float = 0.03,
             start: float = 0.7, n_people: int = 2000, seed: int = 0) -> dict:
    """Algorithm aversion as a learning rule (Dietvorst et al.'s pattern): people rely on the aid with probability
    r; seeing the aid err when they relied on it cuts r by ``drop`` (a person's own errors are forgiven); r creeps
    back by ``recover`` a trial.  Reliance settles far below the accuracy-maximizing 1."""
    rng = np.random.default_rng(seed)
    r = np.full(n_people, start)
    rel, acc = [], []
    for _ in range(trials):
        use = rng.random(n_people) < r
        aid_right = rng.random(n_people) < aid_acc
        own_right = rng.random(n_people) < human_acc
        right = np.where(use, aid_right, own_right)
        r = np.where(use & ~aid_right, r * (1 - drop), np.minimum(r + recover, 1.0))
        rel.append(float(use.mean()))
        acc.append(float(right.mean()))
    return {"reliance": np.array(rel), "accuracy": np.array(acc), "best": float(max(aid_acc, human_acc))}


# ----------------------------------------------------------------------------------------------------------------
# Screens and well-being: a specification curve
# ----------------------------------------------------------------------------------------------------------------
def screen_data(n: int = 10000, true_beta: float = -0.03, seed: int = 0) -> dict:
    """A simulated adolescent survey: screen time (three measures of it), well-being (three measures), and four
    confounders (sleep, family income, school engagement, sex) that affect both.  The causal effect of screen time
    on well-being is ``true_beta`` standard deviations per standard deviation."""
    rng = np.random.default_rng(seed)
    C = rng.standard_normal((n, 4))
    screen_true = C @ np.array([-0.25, -0.15, -0.2, 0.1]) + rng.standard_normal(n)
    screen_true = screen_true / screen_true.std()
    wb_true = true_beta * screen_true + C @ np.array([0.25, 0.15, 0.3, -0.1]) + rng.standard_normal(n)
    wb_true = wb_true / wb_true.std()
    screens = [screen_true + rng.normal(0, s, n) for s in (0.5, 0.8, 1.2)]
    wbs = [wb_true + rng.normal(0, s, n) for s in (0.4, 0.7, 1.0)]
    return {"C": C, "screens": screens, "wbs": wbs}


def specification_curve(data: dict) -> dict:
    """Every combination of screen measure (3), well-being measure (3), confounder set (16 subsets of 4) and
    sample (all, or one sex): 288 regressions.  Returns the standardized coefficient, its p-value and the share of
    variance in well-being that screen time explains, for each."""
    C = data["C"]
    sex = C[:, 3] > 0
    rows = []
    for si, s in enumerate(data["screens"]):
        for wi, w in enumerate(data["wbs"]):
            for k in range(5):
                for subset in itertools.combinations(range(4), k):
                    for sample in ("all", "one sex"):
                        m = np.ones(len(s), bool) if sample == "all" else sex
                        xs = (s[m] - s[m].mean()) / s[m].std()
                        y = (w[m] - w[m].mean()) / w[m].std()
                        X = np.column_stack([np.ones(m.sum()), xs] + [C[m, j] for j in subset])
                        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
                        res = y - X @ coef
                        sig2 = res @ res / (len(y) - X.shape[1])
                        se = np.sqrt(sig2 * np.linalg.inv(X.T @ X)[1, 1])
                        p = 2 * stats.norm.sf(abs(coef[1] / se))
                        rows.append((coef[1], p, float(np.corrcoef(xs, y)[0, 1] ** 2), si, wi, len(subset), sample))
    beta = np.array([r[0] for r in rows])
    order = np.argsort(beta)
    return {"beta": beta[order], "p": np.array([r[1] for r in rows])[order],
            "r2": np.array([r[2] for r in rows])[order], "n_controls": np.array([r[5] for r in rows])[order],
            "median_beta": float(np.median(beta)), "share_sig": float(np.mean(np.array([r[1] for r in rows]) < 0.05)),
            "median_r2": float(np.median([r[2] for r in rows]))}
