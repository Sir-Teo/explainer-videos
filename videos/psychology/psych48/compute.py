"""Precompute every number in Part 48 of *Psychology, Built* ("Modelling Behaviour").

    python -m videos.psychology.psych48.compute            # everything missing (several minutes)
    python -m videos.psychology.psych48.compute --force confusion

Results are cached in ``.cache/psych48/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.fit``, with Part 17's Q-learner from ``psyche.rl``).

Items:
    jump        Estes: 200 learners who each jump from guessing to knowing on one trial; their average
    practice    60 people whose response times fall exponentially at their own rates: who is better fitted by an
                exponential, and what fits the average
    example     one simulated participant in a reversal bandit, fitted by the four models
    recovery    parameter recovery for the Q-learner over a grid of learning rates and inverse temperatures
    surface     the log-likelihood over (alpha, beta) for one participant: the trade-off ridge
    confusion   model recovery: data from each of four models, the model chosen by BIC
    group       30 people, 60 trials each: individual estimates against empirical-Bayes (hierarchical) estimates
    ppc         a posterior predictive check: perseverating data fitted with and without perseveration
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import fit as F

CACHE = Cache("psych48")
load = CACHE.load


def compute_jump() -> dict:
    j = F.jump_learners(seed=48)
    return {"t": j["t"], "mean": j["mean"], "each": j["each"][:8], "smooth": j["smooth"]}


def compute_practice() -> dict:
    p = F.practice_curves(seed=0)
    return {"t": p["t"], "mean": p["mean"], "some": p["Y"][:6], "avg_exp": p["avg_exp"], "avg_pow": p["avg_pow"],
            "exp_wins": p["exp_wins_individual"], "rss_exp": p["avg_rss_exp"], "rss_pow": p["avg_rss_pow"]}


def compute_example() -> dict:
    C, R = F.simulate("q", (0.3, 5.0), seed=48)
    fits = {m: F.fit(m, C, R) for m in F.MODELS}
    return {"choices": C, "rewards": R, **{f"{m}_bic": fits[m]["bic"] for m in F.MODELS},
            **{f"{m}_ll": fits[m]["ll"] for m in F.MODELS}, "q_params": fits["q"]["params"],
            "q_persev_params": fits["q_persev"]["params"]}


def compute_recovery() -> dict:
    return F.recovery([0.1, 0.25, 0.4, 0.6, 0.8], [1.0, 2.5, 5.0, 8.0, 12.0], reps=3, seed=4800)


def compute_surface() -> dict:
    C, R = F.simulate("q", (0.3, 5.0), seed=48)
    a = np.linspace(0.02, 1.0, 40)
    b = np.linspace(0.5, 15, 40)
    return {"alpha": a, "beta": b, "ll": F.tradeoff_surface(C, R, a, b)}


def compute_confusion() -> dict:
    return F.model_confusion(reps=25, seed=4801)


def compute_group() -> dict:
    return F.group_fit(seed=48)


def compute_ppc() -> dict:
    a = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q", n=30, seed=4802)
    b = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q_persev", n=30, seed=4802)
    return {"obs": a["obs"], "pred_q": a["pred"], "pred_persev": b["pred"]}


def compute_signatures() -> dict:
    """Each model's signature before any fit: stay-after-win and stay-after-loss, 40 simulated players each."""
    params = {"random": (0.5,), "wsls": (0.1,), "q": (0.3, 5.0), "q_persev": (0.3, 5.0, 1.5)}
    out = {}
    for k, (m, p) in enumerate(params.items()):
        st = [list(F.stay_after(*F.simulate(m, p, seed=4810 + 100 * k + i)).values()) for i in range(40)]
        out[m] = np.mean(st, 0)
    return {"models": list(params), "win": np.array([out[m][0] for m in params]),
            "loss": np.array([out[m][1] for m in params])}


def compute_starts() -> dict:
    """A slow, decisive perseverator (alpha 0.05, beta 15, kappa 0.5) over 80 trials, fitted from 40 random starting
    points: the final negative log-likelihoods, the share that reach the best, and the parameters at the best and at
    the other optimum."""
    from scipy import optimize
    C, R = F.simulate("q_persev", (0.05, 15.0, 0.5), trials=80, reversal=40, seed=3)
    rng = np.random.default_rng(3)
    finals, xs = [], []
    for i in range(40):
        x0 = [rng.uniform(0.01, 1.0), rng.uniform(0.1, 20.0), rng.uniform(-3, 3)]
        r = optimize.minimize(lambda p: -F.loglik("q_persev", p, C, R), x0=x0, method="L-BFGS-B",
                              bounds=F.BOUNDS["q_persev"])
        finals.append(r.fun); xs.append(r.x)
    finals, xs = np.array(finals), np.array(xs)
    best = finals.min()
    other = finals > best + 0.5
    return {"nll": np.sort(finals), "best": float(best), "share_best": float(np.mean(~other)),
            "best_params": xs[np.argmin(finals)], "other_params": xs[other][np.argmin(finals[other])] if other.any() else xs[0],
            "other_nll": float(finals[other].min()) if other.any() else float(best)}


def compute_trials() -> dict:
    """Parameter recovery for the Q-learner by number of trials: correlations of true and fitted alpha and beta."""
    ts = np.array([50, 100, 200, 400])
    ra, rb = [], []
    for t in ts:
        r = F.recovery([0.15, 0.4, 0.7], [2.0, 5.0, 10.0], reps=8, trials=int(t), seed=4830 + int(t))
        ra.append(r["r_alpha"]); rb.append(r["r_beta"])
    return {"trials": ts, "r_alpha": np.array(ra), "r_beta": np.array(rb)}


def compute_tradeoff() -> dict:
    """The correlation between fitted alpha and fitted beta across repeated simulations of one learner."""
    a, b = [], []
    for i in range(40):
        C, R = F.simulate("q", (0.3, 5.0), seed=4840 + i)
        f = F.fit("q", C, R)
        a.append(f["params"][0]); b.append(f["params"][1])
    a, b = np.array(a), np.array(b)
    return {"alpha": a, "beta": b, "r": float(np.corrcoef(a, b)[0, 1]), "r_log": float(np.corrcoef(np.log(a), np.log(b))[0, 1])}


def compute_crossval() -> dict:
    """Thirty perseverating learners, each playing two sessions: fit every model to session one and score it on
    session two (log-likelihood per choice); against the share of learners for whom BIC picks each model."""
    models = list(F.MODELS)
    held, bic_pick = np.zeros(len(models)), np.zeros(len(models))
    n = 30
    for i in range(n):
        C1, R1 = F.simulate("q_persev", (0.3, 5.0, 1.5), seed=4850 + i)
        C2, R2 = F.simulate("q_persev", (0.3, 5.0, 1.5), seed=6850 + i)
        bics = []
        for j, m in enumerate(models):
            f = F.fit(m, C1, R1)
            held[j] += F.loglik(m, f["params"], C2, R2) / len(C2)
            bics.append(f["bic"])
        bic_pick[int(np.argmin(bics))] += 1
    return {"models": models, "held_out": held / n, "bic_share": bic_pick / n}


def compute_flex() -> dict:
    """What each model can produce: stay-after-win against stay-after-loss for 60 random parameter settings each."""
    rng = np.random.default_rng(4860)
    out = {}
    gens = {"wsls": lambda: (rng.uniform(0.0, 0.6),), "q": lambda: (rng.uniform(0.05, 1.0), rng.uniform(0.5, 15)),
            "q_persev": lambda: (rng.uniform(0.05, 1.0), rng.uniform(0.5, 15), rng.uniform(-3, 3))}
    for m, g in gens.items():
        pts = [list(F.stay_after(*F.simulate(m, g(), seed=int(rng.integers(1 << 30)))).values()) for _ in range(60)]
        out[m] = np.array(pts)
    return {"wsls": out["wsls"], "q": out["q"], "q_persev": out["q_persev"]}


def compute_shrinktrials() -> dict:
    """Errors in each person's learning rate (logit scale), alone and shrunk, by trials per person."""
    ts = np.array([30, 60, 120, 240])
    ml, eb = [], []
    for t in ts:
        gs = [F.group_fit(n_people=40, trials=int(t), seed=4870 + int(t) + 1000 * k) for k in range(4)]
        ml.append(np.mean([g["rmse_ml"] for g in gs])); eb.append(np.mean([g["rmse_eb"] for g in gs]))
    return {"trials": ts, "ml": np.array(ml), "eb": np.array(eb)}


def compute_samples() -> dict:
    """Resource-rational sampling: choose between two options by drawing k noisy samples of their difference
    (signal 0.3 SD per sample); accuracy is Phi(0.3 sqrt k); with a cost c per sample, the best k."""
    from scipy import stats
    ks = np.arange(1, 41)
    acc = stats.norm.cdf(0.3 * np.sqrt(ks))
    costs = np.array([0.002, 0.005, 0.01, 0.02])
    best = np.array([int(ks[np.argmax(acc - c * ks)]) for c in costs])
    return {"k": ks, "acc": acc, "costs": costs, "best_k": best}



def compute_powerk() -> dict:
    """How many exponential learners must be averaged before a power law fits the average better?"""
    ks = np.array([1, 2, 5, 10, 30])
    share = []
    for k in ks:
        wins = []
        for r in range(60):
            pc = F.practice_curves(n=int(k), seed=4800 + 31 * r + int(k))
            wins.append(pc["avg_rss_pow"] < pc["avg_rss_exp"])
        share.append(float(np.mean(wins)))
    return {"k": ks, "power_wins": np.array(share)}

ITEMS = {"powerk": compute_powerk, "jump": compute_jump, "practice": compute_practice, "example": compute_example,
         "recovery": compute_recovery, "surface": compute_surface, "confusion": compute_confusion,
         "group": compute_group, "ppc": compute_ppc,
         "signatures": compute_signatures, "starts": compute_starts, "trials": compute_trials,
         "tradeoff": compute_tradeoff, "crossval": compute_crossval, "flex": compute_flex,
         "shrinktrials": compute_shrinktrials, "samples": compute_samples}

if __name__ == "__main__":
    CACHE.main(ITEMS)
