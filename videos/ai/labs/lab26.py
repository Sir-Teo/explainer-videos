"""Lab 26: run value iteration from two starts on the film's gridworld and watch the contraction; then learn Q from samples."""

import numpy as np

from videos.coursekit import labs

TITLE = "Bellman's contraction, sweep by sweep"
GOAL = ("On the 44-state slippery gridworld of chapters 3 and 4, run value iteration from zeros and from random values, "
        "check that every sweep shrinks their distance by at least gamma, solve the greedy policy's linear system, and "
        "let Q-learning find nearly the same values from sampled moves alone.")
TASKS = [
    "Set gamma = 0.99. How many sweeps does value iteration now need, and how does that compare with log(tol)/log(gamma)?",
    "Give every step a cost (step_reward = -0.04) and print the greedy path from S. Where does the policy change?",
    "Replace Q-learning's max over next actions by the action actually taken (Sarsa) and compare the two learned paths.",
]

GRID = [".........",
        "..#####..",
        "......#.G",
        ".##...#.P",
        "......#..",
        "S........"]  # the film's layout: a goal (+1), a pit (-1), walls
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


def gridworld(slip=0.1, step_reward=0.0):
    """P[a, s, s'] and R[a, s]: a move goes where intended with probability 1 - 2 slip and to either side with slip."""
    cells = [(r, c) for r in range(6) for c in range(9) if GRID[r][c] != "#"]
    index = {rc: i for i, rc in enumerate(cells)}
    n = len(cells)
    P, R = np.zeros((4, n, n)), np.zeros((4, n))
    terminal = np.array([GRID[r][c] in "GP" for r, c in cells])
    for s, (r, c) in enumerate(cells):
        for a in range(4):
            if terminal[s]:  # a terminal cell pays its reward once and ends
                R[a, s] = 1.0 if GRID[r][c] == "G" else -1.0
                continue
            R[a, s] = step_reward
            for b, p in ((a, 1 - 2 * slip), ((a + 1) % 4, slip), ((a + 3) % 4, slip)):
                rr, cc = r + MOVES[b][0], c + MOVES[b][1]
                ok = 0 <= rr < 6 and 0 <= cc < 9 and GRID[rr][cc] != "#"
                P[a, s, index[(rr, cc)] if ok else s] += p
    return cells, index, P, R, terminal


def run(seed=0):
    rng = np.random.default_rng(seed)
    gamma = 0.95
    cells, index, P, R, terminal = gridworld()
    n = len(cells)
    T = lambda V: (R + gamma * P @ V).max(0)  # the Bellman optimality operator

    # value iteration from two starts
    V, U = np.zeros(n), rng.uniform(-1, 1, n)
    gap, err_trace = [np.abs(V - U).max()], []
    for _ in range(400):
        V, U = T(V), T(U)
        gap.append(np.abs(V - U).max())
    v_star = V
    gap = np.array(gap)
    ratios = gap[1:40] / gap[:39]
    W = np.zeros(n)
    for _ in range(120):
        err_trace.append(np.abs(W - v_star).max())
        W = T(W)
    sweeps = int(np.argmax(np.array(err_trace) < 1e-6))

    # the greedy policy, evaluated exactly: V = (I - gamma P_pi)^-1 r_pi
    Q_star = R + gamma * P @ v_star
    pi = Q_star.argmax(0)
    P_pi, r_pi = P[pi, np.arange(n)], R[pi, np.arange(n)]
    v_pi = np.linalg.solve(np.eye(n) - gamma * P_pi, r_pi)

    # Q-learning: no model in the update, only one sampled next state per (state, action) in every round
    Q, rounds = np.zeros((n, 4)), 4000
    cum = P.cumsum(-1).transpose(1, 0, 2)  # [s, a, s']
    q_err = []
    for k in range(1, rounds + 1):
        q_err.append(np.abs(Q.max(1) - v_star).max())
        s2 = np.minimum((rng.random((n, 4, 1)) > cum).sum(-1), n - 1)
        target = R.T + gamma * Q.max(1)[s2] * ~terminal[:, None]
        Q += (target - Q) / k ** 0.6
    q_err.append(np.abs(Q.max(1) - v_star).max())
    live = ~terminal
    # how much value the learned greedy policy gives up, measured exactly
    pi_q = Q.argmax(1)
    v_q = np.linalg.solve(np.eye(n) - gamma * P[pi_q, np.arange(n)], R[pi_q, np.arange(n)])
    loss, loss_start = (v_star - v_q)[live].max(), (v_star - v_q)[index[(5, 0)]]

    lab = labs.Lab()
    lab.row("states, discount", f"{n}, gamma = {gamma}")
    lab.row("largest ratio of successive gaps (two starts)", f"{ratios.max():.4f}   (theorem: at most {gamma})")
    lab.row("sweeps until within 1e-6 of V*", f"{sweeps}   (bound from gamma^k: {int(np.ceil(np.log(1e-6) / np.log(gamma)))})")
    lab.row("V* at the start cell", f"{v_star[index[(5, 0)]]:.4f}   linear solve for the greedy policy: {v_pi[index[(5, 0)]]:.4f}")
    lab.row("Q-learning: largest error in max_a Q", f"{q_err[-1]:.3f} after {rounds} rounds   ({q_err[20]:.3f} after 20)")
    lab.row("value its greedy policy gives up", f"{abs(loss_start):.4f} at the start cell, at most {abs(loss):.4f} in any state")
    lab.note = ("Each sweep shrinks the distance between any two value tables by at least gamma, so value iteration "
                "converges from anywhere; Q-learning reaches nearly the same values from samples, without the model.")

    assert n == 44, "the film's gridworld"
    assert np.all(gap[1:] <= gamma * gap[:-1] + 1e-12), "the Bellman operator is a gamma-contraction in the max norm"
    assert np.all(gap[1:60] <= gamma ** np.arange(1, 60) * gap[0] + 1e-12), "under the dashed line gamma^k"
    assert np.abs(v_pi - v_star).max() < 1e-8, "V* is the value of its own greedy policy"
    assert np.abs(T(v_star) - v_star).max() < 1e-9, "V* is the fixed point"
    assert q_err[-1] < 0.06 and q_err[-1] < 0.2 * q_err[20], "Q-learning approaches V* from samples"
    assert loss_start < 0.03 and loss <= 2 * q_err[-1] / (1 - gamma), "and its greedy policy is nearly optimal"

    fig, ax = labs.figure(2, size=(11, 4.2))
    k = np.arange(len(gap))
    ax[0].semilogy(k[:100], np.maximum(gap[:100], 1e-16), color=labs.BLUE, label="distance between the two runs")
    ax[0].semilogy(k[:100], gamma ** k[:100] * gap[0], color=labs.GOLD, ls="--", label=r"bound $\gamma^k\,\|V_0-U_0\|_\infty$")
    ax[0].set(title="Value iteration from two starts", xlabel="sweep k", ylabel="largest difference (log scale)")
    ax[0].legend()
    g = np.full((6, 9), np.nan)
    for i, (r, c) in enumerate(cells):
        g[r, c] = v_star[i]
    im = ax[1].imshow(g, cmap="RdYlGn", vmin=-1, vmax=1)
    arrows = "↑→↓←"
    for i, (r, c) in enumerate(cells):
        mark = "G" if GRID[r][c] == "G" else "P" if GRID[r][c] == "P" else arrows[pi_q[i]]
        ax[1].text(c, r, mark, ha="center", va="center", color="black", fontsize=11,
                   fontweight="bold" if mark in "GP" else "normal")
    ax[1].set(title="V* (colour) and Q-learning's greedy moves (arrows)", xticks=[], yticks=[])
    ax[1].grid(False)
    fig.colorbar(im, ax=ax[1], shrink=0.8)
    lab.fig = fig
    return lab
