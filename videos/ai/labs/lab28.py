"""Lab 28: train a tiny policy from a checker with GRPO, and measure what it sharpens: accuracy, entropy, pass@k."""

from math import comb

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, log_softmax

TITLE = "Learning from a checker: GRPO in miniature"
GOAL = ("Give a softmax policy 40 questions with 12 possible answers each and a checker that says only right or wrong; "
        "train it with GRPO's group advantages through the series' autodiff, and check the group baseline, the k1 and k3 "
        "KL estimators and the unbiased pass@k estimator against exact values.")
TASKS = [
    "Drop the division by the group's spread (Dr. GRPO's change). Which questions now learn more slowly, and why?",
    "Shrink the group from 8 answers to 2. What share of groups carries no signal at the start, and what happens to the curve?",
    "Train for 2,000 steps instead of 100 and plot pass@256 on the hardest five questions. Does it rise or fall?",
]


def pass_at_k(p, k):
    """Exact pass@k: the chance that at least one of k independent tries is right."""
    return 1 - (1 - p) ** k


def unbiased(c, n, k):
    """Chen et al.'s estimator from c right answers among n samples: 1 - C(n - c, k) / C(n, k)."""
    return 1 - comb(n - c, k) / comb(n, k)


def run(seed=0):
    rng = np.random.default_rng(seed)
    Q, m, G, steps, lr = 40, 12, 8, 100, 0.3
    right = rng.integers(m, size=Q)
    theta0 = 1.2 * rng.standard_normal((Q, m))
    theta = Tensor(theta0.copy(), requires_grad=True)
    rows = np.arange(Q)

    def probs(t):
        e = np.exp(t - t.max(1, keepdims=True))
        return e / e.sum(1, keepdims=True)

    def entropy(p):
        return float(-(p * np.log(p)).sum(1).mean() / np.log(2))

    p0 = probs(theta0)
    acc, ent, silent = [], [], []
    loo_gap = 0.0
    for _ in range(steps):
        p = probs(theta.data)
        acc.append(p[rows, right].mean())
        ent.append(entropy(p))
        y = (rng.random((Q, G, 1)) > p.cumsum(1)[:, None, :]).sum(-1).clip(max=m - 1)  # G sampled answers a question
        r = (y == right[:, None]).astype(float)
        mean, std = r.mean(1, keepdims=True), r.std(1, keepdims=True)
        silent.append(float((std == 0).mean()))
        loo = (r.sum(1, keepdims=True) - r) / (G - 1)  # the leave-one-out baseline of problem 1
        loo_gap = max(loo_gap, np.abs((r - mean) - (G - 1) / G * (r - loo)).max())
        adv = (r - mean) / (std + 1e-6)
        theta.grad = np.zeros_like(theta.data)
        logp = log_softmax(theta)[np.repeat(rows, G), y.ravel()]
        loss = -(logp * adv.ravel()).sum() * (1.0 / G)  # the policy-gradient surrogate, one group a question
        loss.backward()
        theta.data -= lr * theta.grad
    p1 = probs(theta.data)
    acc.append(p1[rows, right].mean())
    ent.append(entropy(p1))

    # the KL from the trained policy back to the starting one, and its estimators, by exact enumeration
    ratio = p0 / p1  # r = pi_ref / pi_theta
    k1, k3 = -np.log(ratio), ratio - 1 - np.log(ratio)
    kl = float((p1 * np.log(p1 / p0)).sum(1).mean())
    e_k1, e_k3 = float((p1 * k1).sum(1).mean()), float((p1 * k3).sum(1).mean())
    k1_negative = float((p1 * (k1 < 0)).sum(1).mean())

    # pass@k from n = 16 samples: the expectation of each estimator over c ~ Binomial(n, p), exactly
    n, k = 16, 8
    pr = p0[rows, right]
    c = np.arange(n + 1)
    pmf = stats.binom.pmf(c[None, :], n, pr[:, None])
    est_unbiased = float((pmf * np.array([unbiased(ci, n, k) for ci in c])).sum(1).mean())
    est_plugin = float((pmf * (1 - (1 - c / n) ** k)).sum(1).mean())
    exact = float(pass_at_k(pr, k).mean())

    ks = 2 ** np.arange(11)
    before = np.array([pass_at_k(p0[rows, right], kk).mean() for kk in ks])
    after = np.array([pass_at_k(p1[rows, right], kk).mean() for kk in ks])
    drained = int((p1[rows, right] < 1e-3).sum())

    lab = labs.Lab()
    lab.row("right on one try", f"{acc[0]:.1%} before, {acc[-1]:.1%} after {steps} GRPO steps")
    lab.row("entropy of the answer", f"{ent[0]:.2f} bits before, {ent[-1]:.2f} after")
    lab.row("groups with no signal", f"{silent[0]:.0%} at the start, {np.mean(silent[-10:]):.0%} at the end")
    lab.row("KL(trained || start), exact", f"{kl:.4f} nats   E[k1] = {e_k1:.4f}   E[k3] = {e_k3:.4f}   (k1 < 0 on {k1_negative:.0%} of samples)")
    lab.row(f"pass@{k} from {n} samples, start", f"exact {exact:.4f}   unbiased estimator {est_unbiased:.4f}   plug-in {est_plugin:.4f}")
    lab.row("pass@1024", f"{before[-1]:.4f} before, {after[-1]:.4f} after   ({drained} of {Q} right answers drained below 1 in 1,000)")
    lab.note = ("A checker's right-or-wrong signal is enough to move probability onto the right answers, and the policy "
                "pays for it in entropy: one try gets much better, while a thousand tries, which nearly always held a right "
                "answer already, gain almost nothing.")

    assert loo_gap < 1e-12, "the group-mean baseline is the leave-one-out baseline times (G - 1)/G"
    assert acc[-1] > acc[0] + 0.3, "GRPO learns from the checker"
    assert ent[-1] < 0.6 * ent[0], "and spends entropy to do it"
    assert abs(e_k1 - kl) < 1e-12 and abs(e_k3 - kl) < 1e-12 and k3.min() >= 0 and k1.min() < 0, "k1 and k3 are unbiased; only k3 is never negative"
    assert abs(est_unbiased - exact) < 1e-12, "the pass@k estimator is unbiased"
    assert est_plugin < exact - 0.005, "the plug-in estimate falls short"
    assert after[0] - before[0] > 5 * (after[-1] - before[-1]), "RL sharpens one try far more than it widens many"

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(steps + 1)
    ax[0].plot(t, acc, color=labs.GREEN, label="right on one try")
    ax[0].set(title="GRPO from a right-or-wrong checker", xlabel="training step", ylabel="share right", ylim=(0, 1.02))
    twin = ax[0].twinx()
    twin.plot(t, ent, color=labs.PURPLE, label="entropy (bits, right axis)")
    twin.set_ylim(0, ent[0] * 1.1)
    twin.grid(False)
    twin.spines["right"].set_visible(True)
    lines = ax[0].get_lines() + twin.get_lines()
    ax[0].legend(lines, [ln.get_label() for ln in lines], loc="center right")
    ax[1].semilogx(ks, before, "o-", color=labs.MUTED, label="before training", base=2)
    ax[1].semilogx(ks, after, "o-", color=labs.GOLD, label="after GRPO", base=2)
    ax[1].set(title="Sharper, or wider? Exact pass@k", xlabel="tries k", ylabel="share of questions passed", ylim=(0, 1.02))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
