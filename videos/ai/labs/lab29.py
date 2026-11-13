"""Lab 29: clone an expert on the film's windy lane, check the T^2 eps bound, and repair the clone with DAgger."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, cross_entropy

TITLE = "Behaviour cloning against DAgger on a windy lane"
GOAL = ("An expert keeps a car in a lane against a side wind; a learner sees the offset through a noisy camera and "
        "copies the expert's steering from 400 labels, either all from the expert's drives (behaviour cloning) or mostly "
        "from its own (DAgger). Compute each learner's expected steps off the lane exactly, for 24 learners of each kind.")
TASKS = [
    "Give both methods 1,600 labels instead of 400. Which one improves, and which is limited by readings it never sees?",
    "Set the camera noise to 0. What is eps on the expert's drives now, and can behaviour cloning still leave the lane?",
    "Run DAgger with 2 rounds of 200 labels instead of 8 rounds of 50, and compare the cost at T = 400.",
]

D, WIND, NOISE = 10, 0.3, 0.2  # the film's lane: offsets -10 .. 10, a push to the right 30% of the time
OFFS = np.arange(-D, D + 1)
S = len(OFFS)
EXPERT = np.where(OFFS >= 0, -1, 1)  # steer back towards the centre; it never leaves |d| <= 1
COST = (np.abs(OFFS) >= 2).astype(float)  # a step off the lane costs 1
POBS = np.zeros((S, S))  # P(camera reading | offset): one cell off either way with probability NOISE
for _i in range(S):
    for _nz, _p in ((-1, NOISE / 2), (0, 1 - NOISE), (1, NOISE / 2)):
        POBS[_i, min(max(_i + _nz, 0), S - 1)] += _p


def chain(table=None):
    """P[d, d'] when the learner steers by ``table[reading]`` (None: the expert, who knows d)."""
    P = np.zeros((S, S))
    for i in range(S):
        acts = [(1.0, EXPERT[i])] if table is None else [(POBS[i, j], table[j]) for j in range(S) if POBS[i, j] > 0]
        for po, a in acts:
            for w, pw in ((1, WIND), (0, 1 - WIND)):
                P[i, min(max(i + a + w, 0), S - 1)] += po * pw
    return P


def run_exact(table, T):
    """The expected cumulative cost J(1..T) from the centre, and the offset's distribution before each step."""
    P, p, ps, per = chain(table), np.eye(S)[D], [], []
    for _ in range(T):
        ps.append(p)
        p = p @ P
        per.append(p @ COST)
    return np.cumsum(per), np.array(ps)


def rollout(table, T, rng):
    """A sampled drive: the camera's readings and the expert's label at each step."""
    i, obs, labels = D, [], []
    slips, gusts = rng.choice([-1, 0, 1], size=T, p=[NOISE / 2, 1 - NOISE, NOISE / 2]), rng.random(T) < WIND
    for k in range(T):
        o = min(max(i + slips[k], 0), S - 1)
        obs.append(o)
        labels.append((EXPERT[i] + 1) // 2)  # class 0: steer left, class 1: steer right
        a = EXPERT[i] if table is None else table[o]
        i = min(max(i + a + gusts[k], 0), S - 1)
    return obs, labels


def fit(obs, labels, init, steps=25):
    """One row of logits per camera reading, fitted by cross-entropy with the series' autodiff; the learner steers by
    the larger logit.  Readings it was never shown keep their initial logits: an arbitrary but fixed action."""
    theta = Tensor(init.copy(), requires_grad=True)
    obs, labels = np.array(obs), np.array(labels)
    for _ in range(steps):
        theta.grad = np.zeros_like(theta.data)
        cross_entropy(theta[obs], labels).backward()
        theta.data -= 20.0 * theta.grad
    return np.where(theta.data[:, 1] > theta.data[:, 0], 1, -1)


def run(seed=0):
    rng = np.random.default_rng(seed)
    T, N, rounds, learners = 400, 400, 8, 24
    J_exp, ps_exp = run_exact(None, T)

    def eps(table, horizon):  # the learner's error rate on the expert's own first `horizon` steps
        wrong = (table[None, :] != EXPERT[:, None]).astype(float)
        return float((ps_exp[:horizon] @ (POBS * wrong).sum(1)).mean())

    bc, dagger, J_bc, J_da, unseen = [], [], [], [], []
    for _ in range(learners):
        init = 0.01 * rng.standard_normal((S, 2))
        obs, labels = [], []
        for _ in range(rounds):  # behaviour cloning: eight drives by the expert
            o, l = rollout(None, N // rounds, rng)
            obs, labels = obs + o, labels + l
        bc.append(fit(obs, labels, init))
        unseen.append(S - len(set(obs)))
        obs, labels = rollout(None, N // rounds, rng)  # DAgger: one drive by the expert, then the learner drives
        table = fit(obs, labels, init)
        for _ in range(rounds - 1):
            o, l = rollout(table, N // rounds, rng)
            obs, labels = obs + o, labels + l
            table = fit(obs, labels, init)
        dagger.append(table)
        J_bc.append(run_exact(bc[-1], T)[0])
        J_da.append(run_exact(table, T)[0])
    J_bc, J_da = np.array(J_bc), np.array(J_da)
    e_bc = np.mean([eps(t, T) for t in bc])
    e_da = np.mean([eps(t, T) for t in dagger])
    m_bc, m_da = J_bc.mean(0), J_da.mean(0)
    slope = lambda J: np.log(J[399] / J[199]) / np.log(2)

    lab = labs.Lab()
    lab.row("expert", f"{J_exp[-1]:.1f} expected steps off the lane in {T}")
    lab.row("error on the expert's drives, eps", f"behaviour cloning {e_bc:.3f}   DAgger {e_da:.3f}")
    lab.row(f"expected steps off the lane in {T}", f"behaviour cloning {m_bc[-1]:.0f} ({J_bc[:, -1].min():.0f} to {J_bc[:, -1].max():.0f})"
                                                  f"   DAgger {m_da[-1]:.0f} ({J_da[:, -1].min():.0f} to {J_da[:, -1].max():.0f})")
    lab.row("behaviour cloning against its bounds at T = 400", f"T eps = {T * e_bc:.0f}   cost {m_bc[-1]:.0f}   T^2 eps = {T * T * e_bc:.0f}")
    lab.row("growth from T = 200 to 400 (log-log slope)", f"behaviour cloning {slope(m_bc):.2f}   DAgger {slope(m_da):.2f}")
    lab.row("camera readings behaviour cloning never saw", f"{np.mean(unseen):.1f} of {S} on average")
    lab.note = ("Both learners are about equally accurate where the expert drives, but the clone's rare errors carry it to "
                "readings it has no labels for, and there the cost compounds; DAgger asks the expert about exactly those.")

    assert J_exp[-1] == 0, "the expert never leaves the lane"
    for table, J in zip(bc + dagger, list(J_bc) + list(J_da)):
        for t in (10, 50, 200, 400):
            assert J[t - 1] <= t * t * eps(table, t) + 1e-9, "Ross and Bagnell's bound J <= J* + T^2 eps"
    assert m_bc[-1] > 1.5 * T * e_bc, "the clone's cost is well above T eps: errors compound"
    assert m_da[-1] < 0.9 * m_bc[-1], "DAgger leaves the lane less with the same number of labels"

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(1, T + 1)
    for J in J_bc:
        ax[0].loglog(t, np.maximum(J, 1e-3), color=labs.RED, alpha=0.25, lw=1)
    for J in J_da:
        ax[0].loglog(t, np.maximum(J, 1e-3), color=labs.GREEN, alpha=0.25, lw=1)
    ax[0].loglog(t, m_bc, color=labs.RED, lw=2.4, label="behaviour cloning (mean of 24)")
    ax[0].loglog(t, m_da, color=labs.GREEN, lw=2.4, label="DAgger (mean of 24)")
    ax[0].loglog(t, t ** 2 * e_bc, color=labs.MUTED, ls="--", label=r"$T^2\varepsilon$")
    ax[0].loglog(t, t * e_bc, color=labs.MUTED, ls=":", label=r"$T\varepsilon$")
    ax[0].set(title="Expected steps off the lane by time T", xlabel="horizon T", ylabel="steps off the lane",
              ylim=(1e-2, 3 * T), xlim=(1, T))
    ax[0].legend(loc="upper left")
    occ = lambda tables: np.mean([run_exact(tb, T)[1].mean(0) for tb in tables], 0)
    w = 0.3
    ax[1].bar(OFFS - w, ps_exp.mean(0), w, color=labs.MUTED, label="expert")
    ax[1].bar(OFFS, occ(bc), w, color=labs.RED, label="behaviour cloning")
    ax[1].bar(OFFS + w, occ(dagger), w, color=labs.GREEN, label="DAgger")
    ax[1].axvspan(-1.5, 1.5, color=labs.BLUE, alpha=0.1)
    ax[1].set(title=f"Where the car spends its {T} steps (lane shaded)", xlabel="offset from the centre",
              ylabel="share of time", xticks=OFFS[::2])
    ax[1].legend()
    lab.fig = fig
    return lab
