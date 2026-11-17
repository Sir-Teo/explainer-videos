"""Lab 17: temporal-difference learning on Pavlov's task and the migration of the error to the cue; second-order
conditioning; a reversal bandit fitted by maximum likelihood, with parameter recovery; the regret of five exploration
policies; the two-step task's stay probabilities; the successor representation and the two revaluations;
distributional TD; and Redish's drug that cannot be predicted away."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import rl

TITLE = "Reward and prediction: TD learning, bandits, maps and the successor representation"
GOAL = ("Run TD(0) with a delay line and watch the error move from the juice to the cue and dip at an omission; "
        "teach a second cue through the first; fit a Q-learner's learning rate and inverse temperature from its "
        "choices, and check whether a fit can be trusted; compare how five policies explore; tell model-free from "
        "model-based agents in the two-step task; compute a successor matrix and predict which revaluations it "
        "passes; recover a reward distribution from optimistic and pessimistic learners; and see why a drug's "
        "surge never stops teaching.")
TASKS = [
    "Raise the discount gamma from 0.98 to 0.999 and lower it to 0.8. How does the size of the error at the cue, "
    "after training, depend on gamma and on the delay between cue and juice? Derive the answer from the Bellman "
    "equation.",
    "Fit the bandit with 50, 100 and 400 trials per player. At what length does the correlation between true and "
    "fitted learning rates pass 0.9? What does that say about studies that fit 80 trials?",
    "Give the successor learner a learning rate for M and let it relearn M from experience after a transition "
    "change. How many passes through the new path does it need to pass the transition revaluation?",
]

CUE, REW = 5, 20


def run(seed=0):
    out = labs.Lab()

    # 1. the error moves to the cue
    D, V = rl.td_conditioning(trials=150, cue=CUE, reward=REW, omit=(149,))
    out.row("trial 1: the error at the juice, and at the cue", f"{D[0, REW]:.2f}, {D[0, CUE - 1]:.2f}")
    out.row("trial 140: the error at the juice, and at the cue", f"{D[140, REW]:.3f}, {D[140, CUE - 1]:.2f}")
    out.row("trial 150, juice omitted: the error when it was due", f"{D[149, REW]:.2f}")
    expect = 0.98 ** (REW - CUE + 1)
    assert abs(D[140, CUE - 1] - expect) < 0.02, "after training the cue's error is the discounted reward"
    out.row("the cue's error after training, and gamma^(steps to the juice)", f"{D[140, CUE - 1]:.3f}, {expect:.3f}")
    first_peak = [int(np.argmax(D[k, CUE:REW + 1])) + CUE for k in range(0, 60, 10)]
    out.row("where the error peaks within the trial, trials 1, 11, ..., 51 (step)", ", ".join(map(str, first_peak)))
    so = rl.second_order()
    out.row("second-order conditioning: A's value after 1, 20 and 60 trials with B and no reward",
            f"{so[0]:.2f}, {so[19]:.2f}, {so[-1]:.2f}")

    # 2. a bandit, fitted
    P = np.r_[np.tile([0.8, 0.2], (100, 1)), np.tile([0.2, 0.8], (100, 1))]
    C, R, _ = rl.q_learning_bandit(P, trials=200, alpha=0.3, beta=5.0, rng=np.random.default_rng(seed + 5))
    a, b, _ = rl.fit_bandit(C, R)
    ws, ls = rl.win_stay_lose_shift(C, R)
    out.row("one player (alpha 0.3, beta 5): fitted alpha, beta; win-stay, lose-shift",
            f"{a:.2f}, {b:.1f}; {ws:.0%}, {ls:.0%}")
    rng = np.random.default_rng(seed + 23)
    ta, fa = [], []
    for k in range(16):
        t_a, t_b = rng.uniform(0.1, 0.8), rng.uniform(2.0, 10.0)
        c, r, _ = rl.q_learning_bandit(P, trials=200, alpha=t_a, beta=t_b, rng=np.random.default_rng(seed + 1000 + k))
        ta.append(t_a)
        fa.append(rl.fit_bandit(c, r)[0])
    rec = float(np.corrcoef(ta, fa)[0, 1])
    out.row("parameter recovery over 16 players: correlation of true and fitted alpha", f"{rec:.2f}")

    # 3. exploring
    reg = {p: np.mean([rl.explore_regret(p, trials=2000, rng=np.random.default_rng(seed + s))[-1] for s in range(20)])
           for p in ("greedy", "epsilon", "softmax", "ucb", "thompson")}
    out.row("regret after 2,000 plays: greedy, epsilon, softmax, UCB1, Thompson",
            ", ".join(f"{v:.0f}" for v in reg.values()))

    # 4. habits and plans
    sp = {}
    for name, w in (("model-free", 0.0), ("model-based", 1.0)):
        sp[name] = np.mean([list(rl.stay_probabilities(rl.two_step(w, rng=np.random.default_rng(seed + s))).values())
                            for s in range(12)], axis=0)
        out.row(f"two-step, {name}: P(stay) after rewarded-common, rewarded-rare, unrewarded-common, unrewarded-rare",
                ", ".join(f"{v:.2f}" for v in sp[name]))
    T = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 1.0]])
    M = rl.successor_matrix(T, gamma=0.9)
    assert np.allclose(M, np.eye(3) + 0.9 * T @ M), "M satisfies its own Bellman equation, M = I + gamma T M"
    out.row("a three-state chain: M from the start state", ", ".join(f"{v:.2f}" for v in M[0]))
    for kind in ("reward", "transition"):
        res = rl.revaluation(kind)
        out.row(f"{kind} revaluation: does V(2) now beat V(1)? model-free, successor, model-based",
                ", ".join("yes" if v2 > v1 else "no" for v1, v2 in res.values()))

    # 5. beyond the mean
    r = np.r_[np.full(300, 0.1), np.full(200, 0.3), np.full(150, 1.2), np.full(150, 2.5), np.full(100, 5.0),
              np.full(100, 10.0)]
    taus = np.linspace(0.05, 0.95, 7)
    v = rl.distributional_td(r, taus, lr=0.02, epochs=40, rng=np.random.default_rng(seed + 3))
    ex = np.array([rl.expectile(r, t) for t in taus])
    out.row("distributional TD against the exact expectiles (tau 0.05 ... 0.95), largest gap",
            f"{np.abs(v - ex).max():.2f} (values {v[0]:.2f} ... {v[-1]:.2f}; mean {r.mean():.2f})")
    nat, drug = rl.redish(trials=200), rl.redish(trials=200, drug=0.5)
    out.row("Redish: the cue's value after 50 and 200 uses, food; drug", f"{nat[49]:.2f}, {nat[-1]:.2f}; "
            f"{drug[49]:.2f}, {drug[-1]:.2f}")
    out.note = ("The error starts at the juice and moves back to the cue, where it settles at the discounted reward; "
                "an omission dips exactly when the juice was due. The bandit's learning rate is fitted, but one "
                "player pins it loosely: recovery across players says how far to trust it. Thompson sampling "
                "explores best here. Model-free and model-based agents differ only after rare transitions; the "
                "successor learner passes reward revaluation and fails transition revaluation. Optimists and "
                "pessimists together carry the whole distribution, and a drug's surge never stops teaching.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].imshow(D[:120:2], aspect="auto", cmap="Greens", vmin=0, vmax=1)
    ax[0].set(title="The TD error, trial by trial", xlabel="time step (cue at 5, juice at 20)", ylabel="trial / 2")
    for (name, col) in (("model-free", labs.BLUE), ("model-based", labs.PINK)):
        ax[1].plot(range(4), sp[name], marker="o", color=col, lw=1.6, label=name)
    ax[1].set_xticks(range(4), ["rew, common", "rew, rare", "unrew, common", "unrew, rare"], fontsize=8)
    ax[1].set(title="The two-step task", ylabel="P(stay)")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
