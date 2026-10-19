"""The small worlds of Part 26: a gridworld with slippery moves, the cliff walk, the random walk, and the cart-pole.

All are exact and tiny, so values can be computed to the last digit (the gridworld's transition matrix is written
out in full) or learned in seconds (the cart-pole's physics is Barto, Sutton & Anderson 1983, with Gym's constants).
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# The gridworld: 6 x 9, walls, a goal (+1) and a pit (-1); a move goes where intended 80% of the time and slips to
# either side 10% each (Russell & Norvig's rule).  Rows count from the top.
# ---------------------------------------------------------------------------
GRID = [
    ".........",
    "..#####..",
    "......#.G",
    ".##...#.P",
    "......#..",
    "S........",
]
ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
ACTION_NAMES = ["up", "right", "down", "left"]


class GridWorld:
    def __init__(self, layout=GRID, slip=0.1, step_reward=0.0, gamma=0.95):
        self.layout = layout
        self.rows, self.cols = len(layout), len(layout[0])
        self.slip, self.step_reward, self.gamma = slip, step_reward, gamma
        self.cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if layout[r][c] != "#"]
        self.index = {rc: i for i, rc in enumerate(self.cells)}
        self.n = len(self.cells)
        self.terminal = np.array([layout[r][c] in "GP" for r, c in self.cells])
        self.exit_reward = np.array([1.0 if layout[r][c] == "G" else -1.0 if layout[r][c] == "P" else 0.0
                                     for r, c in self.cells])
        self.start = self.index[next((r, c) for r, c in self.cells if layout[r][c] == "S")]
        # P[a, s, s'] and the expected reward R[a, s]
        self.P = np.zeros((4, self.n, self.n))
        self.R = np.zeros((4, self.n))
        for s, (r, c) in enumerate(self.cells):
            for a in range(4):
                if self.terminal[s]:  # a terminal cell pays its reward once and ends
                    self.R[a, s] = self.exit_reward[s]
                    continue
                self.R[a, s] = step_reward
                for b, p in ((a, 1 - 2 * slip), ((a + 1) % 4, slip), ((a + 3) % 4, slip)):
                    dr, dc = ACTIONS[b]
                    rr, cc = r + dr, c + dc
                    ok = 0 <= rr < self.rows and 0 <= cc < self.cols and layout[rr][cc] != "#"
                    self.P[a, s, self.index[(rr, cc)] if ok else s] += p

    def bellman(self, V):
        """(T V)(s) = max_a R(s, a) + gamma sum_s' P(s' | s, a) V(s'), and the maximizing action."""
        Q = self.R + self.gamma * self.P @ V
        return Q.max(0), Q.argmax(0), Q

    def value_iteration(self, V0, tol=1e-10, max_iter=2000):
        Vs, pis = [V0.copy()], []
        V = V0.copy()
        for _ in range(max_iter):
            V2, pi, _ = self.bellman(V)
            Vs.append(V2)
            pis.append(pi)
            if np.abs(V2 - V).max() < tol:
                break
            V = V2
        return np.array(Vs), np.array(pis)

    def evaluate(self, pi):
        """V^pi exactly: solve (I - gamma P_pi) V = R_pi.  ``pi`` is an action per state, or an (n, 4) table."""
        pi = np.asarray(pi)
        if pi.ndim == 1:
            pi = np.eye(4)[pi]
        Ppi = np.einsum("sa,ast->st", pi, self.P)
        Rpi = np.einsum("sa,as->s", pi, self.R)
        return np.linalg.solve(np.eye(self.n) - self.gamma * Ppi, Rpi)

    def policy_iteration(self, pi0):
        pis, Vs = [np.asarray(pi0)], []
        pi = np.asarray(pi0)
        while True:
            V = self.evaluate(pi)
            Vs.append(V)
            _, new, Q = self.bellman(V)
            # keep the old action on ties, so the loop ends
            keep = Q[pi, np.arange(self.n)] >= Q.max(0) - 1e-12
            new = np.where(keep, pi, new)
            if np.array_equal(new, pi):
                return pis, Vs
            pi = new
            pis.append(pi)

    def grid_of(self, v, fill=np.nan):
        g = np.full((self.rows, self.cols), fill, float)
        for s, (r, c) in enumerate(self.cells):
            g[r, c] = v[s]
        return g


# ---------------------------------------------------------------------------
# The cliff walk (Sutton & Barto, Example 6.6): 4 x 12, start bottom-left, goal bottom-right, the cells between are
# a cliff (-100 and back to the start); every step costs 1.
# ---------------------------------------------------------------------------
CLIFF_ROWS, CLIFF_COLS = 4, 12


def cliff_step(r, c, a):
    dr, dc = ACTIONS[a]
    r, c = min(max(r + dr, 0), CLIFF_ROWS - 1), min(max(c + dc, 0), CLIFF_COLS - 1)
    if r == CLIFF_ROWS - 1 and 0 < c < CLIFF_COLS - 1:
        return CLIFF_ROWS - 1, 0, -100.0, False
    return r, c, -1.0, (r == CLIFF_ROWS - 1 and c == CLIFF_COLS - 1)


# ---------------------------------------------------------------------------
# The random walk (Sutton & Barto, Example 6.2): states 1..n in a row, start in the middle, step left or right with
# equal chance; falling off the right end pays 1, the left end 0.  True values: k / (n + 1).
# ---------------------------------------------------------------------------
def walk_episode(n, rng):
    s = (n + 1) // 2
    states, rewards = [s], []
    while True:
        s += 1 if rng.random() < 0.5 else -1
        if s == 0:
            rewards.append(0.0)
            return states, rewards
        if s == n + 1:
            rewards.append(1.0)
            return states, rewards
        rewards.append(0.0)
        states.append(s)


# ---------------------------------------------------------------------------
# The cart-pole (Barto, Sutton & Anderson 1983; Gym's CartPole-v1 constants): push the cart left or right to keep
# the pole up; +1 for every step, the episode ends when the pole passes 12 degrees, the cart leaves the track, or
# after 500 steps.
# ---------------------------------------------------------------------------
class CartPole:
    g, mc, mp, l, F, dt = 9.8, 1.0, 0.1, 0.5, 10.0, 0.02
    theta_max, x_max, horizon = 12 * 2 * np.pi / 360, 2.4, 500

    def __init__(self, rng):
        self.rng = rng

    def reset(self):
        self.s = self.rng.uniform(-0.05, 0.05, 4)
        self.t = 0
        return self.s.copy()

    def step(self, a):
        x, xd, th, thd = self.s
        f = self.F if a == 1 else -self.F
        ct, st = np.cos(th), np.sin(th)
        m = self.mc + self.mp
        temp = (f + self.mp * self.l * thd ** 2 * st) / m
        tha = (self.g * st - ct * temp) / (self.l * (4 / 3 - self.mp * ct ** 2 / m))
        xa = temp - self.mp * self.l * tha * ct / m
        x, xd = x + self.dt * xd, xd + self.dt * xa
        th, thd = th + self.dt * thd, thd + self.dt * tha
        self.s = np.array([x, xd, th, thd])
        self.t += 1
        fell = abs(x) > self.x_max or abs(th) > self.theta_max
        return self.s.copy(), 1.0, fell, self.t >= self.horizon
