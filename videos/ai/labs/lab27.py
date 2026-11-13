"""Lab 27: climb the KL-regularized objective by gradient ascent, land on its closed form, and measure best-of-n's price."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, log_softmax

TITLE = "Reinforcement learning on a leash, and Goodhart's law"
GOAL = ("For eight candidate answers with a reference policy and a reward, maximize E[r] - beta KL(pi || pi_ref) by "
        "gradient ascent with the series' autodiff and compare with pi* = pi_ref e^(r/beta) / Z; then pick the best of n "
        "answers by a noisy proxy reward and measure the KL paid and the gold reward actually gained.")
TASKS = [
    "Lower beta from 1 to 0.1 and to 0.01. What share of pi* sits on the best answer, and what is KL(pi* || pi_ref)?",
    "Make the proxy's noise as large as gold's spread (noise = 1). What fraction of the proxy's gain is real now?",
    "Give the proxy a heavy-tailed error (rng.standard_t(2)) and plot gold against n. Does gold still rise with n?",
]


def objective(theta, r, log_ref, beta):
    """J(pi) = E_pi[r] - beta KL(pi || pi_ref) for pi = softmax(theta), as a Tensor."""
    lp = log_softmax(theta)
    return (lp.exp() * (Tensor(r) - (lp - Tensor(log_ref)) * beta)).sum()


def best_of_n_discrete(ref, order, n):
    """The law of the best of n draws from ``ref`` when answers are ranked by ``order`` (no ties)."""
    F = np.cumsum(ref[order])
    p = np.empty_like(ref)
    p[order] = F ** n - np.r_[0.0, F[:-1]] ** n
    return p


def run(seed=0):
    rng = np.random.default_rng(seed)
    m, beta = 8, 0.5
    ref = rng.dirichlet(4 * np.ones(m))
    r = rng.standard_normal(m)

    # 1. gradient ascent on J against the closed form
    theta = Tensor(np.zeros(m), requires_grad=True)
    trace = []
    for _ in range(3000):
        theta.grad = np.zeros(m)
        J = objective(theta, r, np.log(ref), beta)
        J.backward()
        trace.append(float(J.data))
        theta.data += 2.0 * theta.grad
    pi = np.exp(theta.data - theta.data.max())
    pi /= pi.sum()
    Z = (ref * np.exp(r / beta)).sum()
    star = ref * np.exp(r / beta) / Z
    J_star = beta * np.log(Z)
    gap = np.abs(pi - star).max()

    # 2. best-of-n: the KL paid, for continuous rewards and for these eight answers
    ns = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])
    kl_formula = np.log(ns) - (ns - 1) / ns
    u = rng.random((40_000, 16)).max(1)  # the reward quantile of the best of 16
    kl_mc = np.mean(np.log(16) + 15 * np.log(u))
    order = np.argsort(r)
    kl_disc = []
    for n in ns:
        p = best_of_n_discrete(ref, order, n)
        kl_disc.append(float((p[p > 0] * np.log(p[p > 0] / ref[p > 0])).sum()))
    kl_disc = np.array(kl_disc)

    # 3. regressional Goodhart: choose by a proxy = gold + noise, and see what gold says
    noise, trials = 0.7, 4000
    shrink = 1 / (1 + noise ** 2)  # sigma_G^2 / (sigma_G^2 + sigma_E^2) with sigma_G = 1
    proxy_gain, gold_gain = [], []
    for n in ns:
        gold = rng.standard_normal((trials, n))
        proxy = gold + noise * rng.standard_normal((trials, n))
        pick = proxy.argmax(1)
        proxy_gain.append(proxy[np.arange(trials), pick].mean())
        gold_gain.append(gold[np.arange(trials), pick].mean())
    proxy_gain, gold_gain = np.array(proxy_gain), np.array(gold_gain)

    lab = labs.Lab()
    lab.row("gradient ascent against pi_ref e^(r/beta)/Z", f"largest difference {gap:.1e}")
    lab.row("J at the end of the climb", f"{trace[-1]:.6f}   (beta log Z = {J_star:.6f})")
    lab.row("best of 16, continuous reward: KL", f"{kl_mc:.3f} nats   (log n - (n-1)/n = {kl_formula[4]:.3f})")
    lab.row("best of 16 among these eight answers: KL", f"{kl_disc[4]:.3f} nats   (below the bound)")
    lab.row("best of 256 by the proxy", f"proxy says +{proxy_gain[-1]:.2f}, gold says +{gold_gain[-1]:.2f}")
    lab.row("gold gained per unit of proxy", f"{gold_gain[-1] / proxy_gain[-1]:.3f}   (theory {shrink:.3f})")
    lab.note = ("The leash has an exact optimum, the reference reweighted by e^(r/beta); selecting harder on a noisy reward "
                "buys proxy score at a known KL price, and only a fixed fraction of that score is real.")

    assert gap < 1e-3 and -1e-4 < trace[-1] - J_star < 1e-12, "gradient ascent climbs to the closed-form optimum"
    assert np.all(np.diff(trace) > -1e-12), "J never falls on the way"
    for _ in range(20):  # no other policy does better (Gibbs' inequality)
        q = rng.dirichlet(np.ones(m))
        assert float(objective(Tensor(np.log(q)), r, np.log(ref), beta).data) <= J_star + 1e-12
    assert abs(kl_mc - kl_formula[4]) < 0.02, "best-of-n's KL for an atomless reward"
    assert np.all(kl_disc <= kl_formula + 1e-12), "for discrete answers the formula is an upper bound"
    assert np.all(np.abs(gold_gain[1:] / proxy_gain[1:] - shrink) < 0.05), "regressional Goodhart: E[G | R] = shrink R"

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(m)
    srt = np.argsort(-r)
    ax[0].bar(x - 0.27, ref[srt], 0.27, color=labs.MUTED, label="reference $\\pi_{ref}$")
    for k, (b, color) in enumerate(((2.0, labs.BLUE), (0.5, labs.GOLD))):
        w = ref * np.exp(r / b)
        ax[0].bar(x + 0.27 * k, (w / w.sum())[srt], 0.27, color=color, label=f"optimum, beta = {b:g}")
    ax[0].plot(x + 0.27, pi[srt], "o", color=labs.RED, ms=4, label="gradient ascent, beta = 0.5")
    ax[0].set(title="The leash: the reference reweighted by $e^{r/\\beta}$", xlabel="answers, best reward first",
              ylabel="probability", xticks=x, xticklabels=[f"{v:+.1f}" for v in r[srt]])
    ax[0].legend()
    ax[1].plot(kl_formula, proxy_gain, "o-", color=labs.ORANGE, label="what the proxy believes")
    ax[1].plot(kl_formula, gold_gain, "o-", color=labs.GREEN, label="what gold says")
    ax[1].plot(kl_formula, shrink * proxy_gain, "--", color=labs.MUTED, label=f"{shrink:.2f} x the proxy (theory)")
    for n, kx, gy in zip(ns[1::2], kl_formula[1::2], proxy_gain[1::2]):
        ax[1].annotate(f"n={n}", (kx, gy), textcoords="offset points", xytext=(-4, 7), fontsize=8, color=labs.MUTED, ha="right")
    ax[1].set(title="Best of n by a noisy proxy", xlabel="KL paid, log n - (n-1)/n (nats)", ylabel="mean score of the pick")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
