"""The small worlds of Part 29, all exact and cheap enough to run on a laptop's CPU.

* :class:`Track`, a loop of road in a field of grass (a grid): the expert drives round it; imitation learners learn
  from it (behaviour cloning and DAgger, chapters 9 and 10).  Every policy here is a table from cell to action, so its
  expected cost over T steps is computed exactly, by pushing the distribution over cells through the Markov chain.
* :class:`Catch`, a ball falling in a 12 x 12 picture and a paddle that must catch it (the Dreamer-lite, chapter 12).
* :func:`cartpole_step`, the cart-pole of Part 26 (Barto, Sutton & Anderson 1983, with Gym's constants), vectorized
  over many copies whose physics differ (domain randomization, chapter 16).
* :func:`arm_chunks`, smooth seven-joint trajectories at 50 Hz (minimum-jerk moves between random poses): the
  actions FAST compresses (chapter 15).
* :func:`detour_demo`, two-dimensional demonstrations that pass an obstacle on the left or on the right, half each:
  why a robot policy should be a generative model (chapter 14).
"""

from __future__ import annotations

import numpy as np

from videos.ai.ai26.envs import CartPole

MOVES = np.array([(-1, 0), (0, 1), (1, 0), (0, -1)])  # up, right, down, left (rows count from the top)


# ---------------------------------------------------------------------------
# The track: a loop of road in a field
# ---------------------------------------------------------------------------
class Track:
    """A grid ``rows`` x ``cols``; the road is a closed loop of cells, driven anticlockwise; everything else is grass.

    Each step the driver picks one of four moves; with probability ``slip`` the car goes in a random direction instead
    (the same for every driver).  The cost is 1 for every step that ends on the grass.  The expert follows the road,
    and from the grass heads back to the nearest road cell."""

    def __init__(self, rows=15, cols=23, slip=0.2):
        self.rows, self.cols, self.slip = rows, cols, slip
        self.n = rows * cols
        loop = self._loop()
        self.loop = loop
        self.on = np.zeros(self.n, bool)
        self.on[[self.idx(r, c) for r, c in loop]] = True
        # the expert: along the loop on the road; on the grass, down the distance to the road
        dist = self._dist_to_road()
        self.dist = dist
        self.expert = np.zeros(self.n, int)
        for i, (r, c) in enumerate(loop):
            nr, nc = loop[(i + 1) % len(loop)]
            self.expert[self.idx(r, c)] = int(np.flatnonzero((MOVES == (nr - r, nc - c)).all(1))[0])
        for s in range(self.n):
            if self.on[s]:
                continue
            r, c = divmod(s, cols)
            best = min(range(4), key=lambda a: (dist[self.idx(*self._go(r, c, a))], a))
            self.expert[s] = best
        # T[a] : the cell after intending move a from each cell (n,) ; P[a] the slip-mixed transition matrix
        self.next = np.array([[self.idx(*self._go(*divmod(s, cols), a)) for s in range(self.n)] for a in range(4)])

    def idx(self, r, c):
        return r * self.cols + c

    def _go(self, r, c, a):
        dr, dc = MOVES[a]
        rr, cc = r + dr, c + dc
        if 0 <= rr < self.rows and 0 <= cc < self.cols:
            return rr, cc
        return r, c

    def _loop(self):
        """A rounded loop with a bend in it: a rectangle's outline, with a notch pushed in from the top."""
        r0, r1, c0, c1 = 3, self.rows - 4, 3, self.cols - 4
        path = [(r0, c) for c in range(c0, c1 + 1)]
        path += [(r, c1) for r in range(r0 + 1, r1 + 1)]
        path += [(r1, c) for c in range(c1 - 1, c0 - 1, -1)]
        path += [(r, c0) for r in range(r1 - 1, r0, -1)]
        # the notch: along the top edge between two columns, the road dips down three rows
        a, b, depth = c0 + 5, c0 + 10, 3
        top = [(r0, c) for c in range(c0, a)]
        top += [(r, a) for r in range(r0, r0 + depth + 1)]
        top += [(r0 + depth, c) for c in range(a + 1, b)]
        top += [(r, b) for r in range(r0 + depth, r0, -1)]
        top += [(r0, c) for c in range(b, c1 + 1)]
        path = top + path[c1 - c0 + 1:]
        path = path[::-1]  # anticlockwise on screen
        assert len(set(path)) == len(path)
        for (r, c), (rr, cc) in zip(path, path[1:] + path[:1]):
            assert abs(r - rr) + abs(c - cc) == 1
        return path

    def _dist_to_road(self):
        from collections import deque

        d = np.full(self.n, 10 ** 6)
        q = deque()
        for r, c in self.loop:
            d[self.idx(r, c)] = 0
            q.append((r, c))
        while q:
            r, c = q.popleft()
            for a in range(4):
                rr, cc = self._go(r, c, a)
                if d[self.idx(rr, cc)] > d[self.idx(r, c)] + 1:
                    d[self.idx(rr, cc)] = d[self.idx(r, c)] + 1
                    q.append((rr, cc))
        return d

    # --- one policy (a table, intended moves) as a Markov chain over cells -----------------------------------
    def chain(self, table):
        """The transition matrix P[s, s'] when the intended move in cell s is ``table[s]``."""
        P = np.zeros((self.n, self.n))
        ar = np.arange(self.n)
        np.add.at(P, (ar, self.next[table, ar]), 1 - self.slip)
        for a in range(4):
            np.add.at(P, (ar, self.next[a, ar]), self.slip / 4)
        return P

    def start(self):
        """Each episode starts on a road cell, chosen uniformly."""
        p = self.on.astype(float)
        return p / p.sum()

    def cost_curve(self, table, T):
        """E[cost of steps 1..t] for t = 1..T, exactly; and the distribution over cells at each step (T+1, n)."""
        P = self.chain(table)
        p = self.start()
        ps = [p]
        for _ in range(T):
            p = p @ P
            ps.append(p)
        ps = np.array(ps)
        per = ps[1:] @ (~self.on).astype(float)
        return np.cumsum(per), ps

    def rollout(self, table, steps, g, s0=None):
        """A sampled run: (cells visited, intended moves), starting on a random road cell."""
        on_cells = np.flatnonzero(self.on)
        s = int(g.choice(on_cells)) if s0 is None else int(s0)
        cells = [s]
        for _ in range(steps):
            a = int(table[s])
            if g.random() < self.slip:
                a = int(g.integers(4))
            s = int(self.next[a, s])
            cells.append(s)
        return np.array(cells)


# ---------------------------------------------------------------------------
# Catch: a ball falls; a paddle at the bottom must be under it
# ---------------------------------------------------------------------------
class Catch:
    """12 x 12 pixels.  The ball starts in the top row at a random column, falls one row a step and drifts one column
    left or right (or not at all), bouncing off the walls.  The paddle, 3 pixels wide on the bottom row, moves left,
    stays, or moves right.  When the ball reaches the bottom row the reward is +1 if the paddle is under it and -1 if
    not, and a new ball appears.  An episode is ``drops`` balls."""

    S = 12

    def __init__(self, g, drops=6):
        self.g, self.drops = g, drops

    def _new_ball(self):
        self.bx, self.by = int(self.g.integers(self.S)), 0
        self.vx = int(self.g.integers(-1, 2))

    def reset(self):
        self.px = int(self.g.integers(1, self.S - 1))
        self._new_ball()
        self.done_drops = 0
        return self.obs()

    def obs(self):
        o = np.zeros((self.S, self.S), np.float32)
        o[self.by, self.bx] = 1.0
        o[self.S - 1, max(self.px - 1, 0):self.px + 2] = 1.0
        return o

    def step(self, a):
        self.px = int(np.clip(self.px + (a - 1), 1, self.S - 2))
        self.by += 1
        nx = self.bx + self.vx
        if nx < 0 or nx >= self.S:
            self.vx = -self.vx
            nx = self.bx + self.vx
        self.bx = nx
        r = 0.0
        if self.by == self.S - 1:
            r = 1.0 if abs(self.bx - self.px) <= 1 else -1.0
            self.done_drops += 1
            o = self.obs()  # the ball shown on the bottom row, then a new one
            self._new_ball()
            return o, r, self.done_drops >= self.drops
        return self.obs(), r, False

    def state(self):
        return (self.bx, self.by, self.px)


# ---------------------------------------------------------------------------
# The cart-pole, many at once, each with its own physics
# ---------------------------------------------------------------------------
NOMINAL = dict(l=CartPole.l, mp=CartPole.mp, mc=CartPole.mc, F=CartPole.F, delay=0, noise=0.0)


def cartpole_returns(W, phys, episodes, g, horizon=500):
    """Run linear policies ``push right iff w . s + b > 0`` (W: (P, 5)) on ``episodes`` copies each, every copy with
    its own physics drawn by ``phys(n, g)`` (a dict of arrays of length P * episodes).  Returns the mean steps balanced
    per policy (P,).  Part 26's equations (Gym's constants), vectorized; an optional one-step action delay and sensor
    noise, the usual gaps between a simulator and a robot."""
    P = W.shape[0]
    n = P * episodes
    pr = phys(n, g)
    l, mp, mc, F = (np.asarray(pr[k], float) for k in ("l", "mp", "mc", "F"))
    delay = np.asarray(pr["delay"], int)
    noise = np.asarray(pr["noise"], float)
    w = np.repeat(W, episodes, axis=0)
    s = g.uniform(-0.05, 0.05, (n, 4))
    alive = np.ones(n, bool)
    steps = np.zeros(n)
    prev = np.ones(n)  # the action decided last step (applied now when delayed)
    gr, dt = CartPole.g, CartPole.dt
    for _ in range(horizon):
        obs = s + noise[:, None] * g.standard_normal((n, 4)) * np.array([0.1, 0.3, 0.02, 0.3])
        act = (np.einsum("ij,ij->i", obs, w[:, :4]) + w[:, 4] > 0).astype(float)
        a = np.where(delay > 0, prev, act)
        prev = act
        f = np.where(a > 0, F, -F)
        x, xd, th, thd = s.T
        ct, st = np.cos(th), np.sin(th)
        m = mc + mp
        temp = (f + mp * l * thd ** 2 * st) / m
        tha = (gr * st - ct * temp) / (l * (4 / 3 - mp * ct ** 2 / m))
        xa = temp - mp * l * tha * ct / m
        s = np.stack([x + dt * xd, xd + dt * xa, th + dt * thd, thd + dt * tha], 1)
        steps += alive
        fell = (np.abs(s[:, 0]) > CartPole.x_max) | (np.abs(s[:, 2]) > CartPole.theta_max)
        alive &= ~fell
        if not alive.any():
            break
    return steps.reshape(P, episodes).mean(1)


# ---------------------------------------------------------------------------
# Robot-arm motion: what FAST compresses
# ---------------------------------------------------------------------------
def min_jerk(t):
    return 10 * t ** 3 - 15 * t ** 4 + 6 * t ** 5


def arm_chunks(n, g, joints=7, hz=50, seconds=1.0):
    """``n`` one-second chunks of a seven-joint arm (radians), each a piece of a long smooth motion: minimum-jerk
    moves between random poses, each move 0.4-1.6 s long, plus a little tremor.  (n, H, joints)."""
    H = int(hz * seconds)
    total = n * H + 200
    out = np.zeros((total, joints))
    t, pose = 0, g.uniform(-1, 1, joints)
    while t < total:
        dur = int(g.uniform(0.4, 1.6) * hz)
        new = np.clip(pose + g.normal(0, 0.6, joints), -2.5, 2.5)
        s = min_jerk(np.linspace(0, 1, dur + 1)[1:])[:, None]
        seg = pose + s * (new - pose)
        k = min(dur, total - t)
        out[t:t + k] = seg[:k]
        t += k
        pose = new
    out += 0.002 * g.standard_normal(out.shape)
    start = int(g.integers(0, 200))
    return out[start:start + n * H].reshape(n, H, joints)


# ---------------------------------------------------------------------------
# Two ways round an obstacle
# ---------------------------------------------------------------------------
OBST = (0.0, 0.0, 0.32)  # centre x, y and radius
GOAL = (1.0, 0.0)


def detour_demo(g, steps=40):
    """One demonstration: from the left edge to the goal on the right, passing the obstacle above or below (a coin
    flip), as a smooth curve through a waypoint over or under it.  Returns (steps + 1, 2) positions."""
    y0 = g.uniform(-0.25, 0.25)
    side = 1.0 if g.random() < 0.5 else -1.0
    t = np.linspace(0, 1, steps + 1)
    x = -1.0 + 2.0 * t
    bump = side * (OBST[2] + 0.22 + 0.04 * g.standard_normal()) * np.exp(-((x - OBST[0]) / 0.42) ** 2)
    y = y0 * (1 - min_jerk(t)) + bump
    return np.stack([x, y], 1)
