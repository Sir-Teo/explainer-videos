"""Games (Agora, Part 11): what happens when my best choice depends on yours.

**Strategic form.**  :func:`pure_nash` (every cell where both play a best response), :func:`iterated_elimination`
(strictly dominated strategies removed round by round, the order recorded), :func:`support_enumeration` (every Nash
equilibrium of a nondegenerate bimatrix game, by solving the indifference conditions on each pair of supports),
:func:`mixed_2x2` (the mixed equilibrium of a two-by-two game by indifference), :func:`best_response_curves` (the
two players' best-response correspondences for drawing).

**The guessing game.**  :func:`guessing_winner` (the number closest to p times the mean), :func:`level_k` (Nagel's
iteration steps from a reference point), :func:`cognitive_hierarchy` (Camerer, Ho and Chong: level 0 uniform,
Poisson(tau) levels, each level best-responding to the normalized mix below it) and :func:`fit_tau` (the tau that
matches an observed mean).

**Extensive form.**  :class:`Node` trees, :func:`backward_induction` (subgame-perfect play and payoffs, ties broken
toward the first action), :func:`centipede` (Rosenthal's game with a growing pot), :func:`entry_game` (the chain
store's threat, credible or not).

**Repetition.**  :func:`grim_threshold` (the discount factor above which grim trigger sustains cooperation),
:func:`folk_region` (feasible payoffs, the minmax point, and the individually rational part), a strategy library
(ALLC, ALLD, TFT, GRIM, TF2T, WSLS, GTFT, RANDOM, JOSS) with :func:`play_match` and :func:`tournament` (a round
robin, optionally with noise) and :func:`ecology` (Axelrod's ecological tournament, the replicator on match
scores).

**Coordination, evolution and learning.**  :func:`correlated_equilibrium` (the best correlated equilibrium by
linear programming), :func:`replicator` (the replicator dynamic for a symmetric game), :func:`is_ess` (Maynard Smith's
conditions), :func:`fictitious_play` (Brown and Robinson's learning rule), :func:`regret_matching` (Hart and
Mas-Colell: average play converges to the set of coarse correlated equilibria, and to Nash in zero-sum games).

**Incomplete information.**  :func:`bayes_nash_2x2` (pure Bayesian Nash equilibria of a game in which one player has
two types, by checking every type-contingent plan).

**Bargaining.**  :func:`rubinstein` (the alternating-offers split, 1 / (1 + delta) for equal patience).

Plain numpy and scipy.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq, linprog


# ---------------------------------------------------------------------------------------------------------------
# strategic form


def _as(A):
    return np.asarray(A, float)


def pure_nash(A, B) -> list[tuple[int, int]]:
    """Cells (i, j) where row's payoff A[i, j] is a best response to column j and column's B[i, j] to row i."""
    A, B = _as(A), _as(B)
    out = []
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i, j] >= A[:, j].max() - 1e-12 and B[i, j] >= B[i, :].max() - 1e-12:
                out.append((i, j))
    return out


def iterated_elimination(A, B) -> dict:
    """Remove strictly dominated pure strategies (dominated by another pure strategy) for either player, round by
    round, until none is left.  Returns the surviving rows and columns and the order of removal."""
    A, B = _as(A), _as(B)
    rows, cols = list(range(A.shape[0])), list(range(A.shape[1]))
    order = []
    changed = True
    while changed:
        changed = False
        for r in list(rows):
            if any(all(A[s, c] > A[r, c] for c in cols) for s in rows if s != r):
                rows.remove(r)
                order.append(("row", r))
                changed = True
        for c in list(cols):
            if any(all(B[r, d] > B[r, c] for r in rows) for d in cols if d != c):
                cols.remove(c)
                order.append(("col", c))
                changed = True
    return {"rows": rows, "cols": cols, "order": order}


def support_enumeration(A, B, tol: float = 1e-9) -> list[dict]:
    """Every Nash equilibrium of a nondegenerate bimatrix game (row payoffs A, column payoffs B), by support
    enumeration: for each pair of equal-size supports, solve for the mixtures that make the other player indifferent
    over the support, and keep those that are probabilities and best responses."""
    A, B = _as(A), _as(B)
    m, n = A.shape
    found = []
    for k in range(1, min(m, n) + 1):
        for I in itertools.combinations(range(m), k):
            for J in itertools.combinations(range(n), k):
                # column mixture q on J makes row indifferent across I:  A[I, J] q = v 1,  sum q = 1
                M = np.zeros((k + 1, k + 1))
                M[:k, :k] = A[np.ix_(I, J)]
                M[:k, k] = -1
                M[k, :k] = 1
                rhs = np.zeros(k + 1)
                rhs[k] = 1
                N = np.zeros((k + 1, k + 1))
                N[:k, :k] = B[np.ix_(I, J)].T
                N[:k, k] = -1
                N[k, :k] = 1
                try:
                    sq = np.linalg.solve(M, rhs)
                    sp = np.linalg.solve(N, rhs)
                except np.linalg.LinAlgError:
                    continue
                q_s, v = sq[:k], sq[k]
                p_s, w = sp[:k], sp[k]
                if (q_s < -tol).any() or (p_s < -tol).any():
                    continue
                p = np.zeros(m)
                q = np.zeros(n)
                p[list(I)] = p_s
                q[list(J)] = q_s
                if (A @ q > v + tol).any() or (p @ B > w + tol).any():
                    continue
                if not any(np.allclose(p, e["p"], atol=1e-7) and np.allclose(q, e["q"], atol=1e-7) for e in found):
                    found.append({"p": p, "q": q, "row_payoff": float(p @ A @ q), "col_payoff": float(p @ B @ q)})
    return found


def mixed_2x2(A, B) -> dict:
    """The fully mixed equilibrium of a 2x2 game: p = Pr(row plays its first strategy) makes column indifferent, and
    q = Pr(column plays its first) makes row indifferent."""
    A, B = _as(A), _as(B)
    q = (A[1, 1] - A[0, 1]) / (A[0, 0] - A[0, 1] - A[1, 0] + A[1, 1])
    p = (B[1, 1] - B[1, 0]) / (B[0, 0] - B[1, 0] - B[0, 1] + B[1, 1])
    P, Q = np.array([p, 1 - p]), np.array([q, 1 - q])
    return {"p": float(p), "q": float(q), "row_payoff": float(P @ A @ Q), "col_payoff": float(P @ B @ Q)}


def best_response_curves(A, B, n: int = 201) -> dict:
    """For 2x2 games: row's best p (Pr first row) against each q, and column's best q against each p, as step curves
    (a vertical segment at the indifference point)."""
    A, B = _as(A), _as(B)
    grid = np.linspace(0, 1, n)
    row_gain = [(A[0, 0] - A[1, 0]) * q + (A[0, 1] - A[1, 1]) * (1 - q) for q in grid]   # first minus second row
    col_gain = [(B[0, 0] - B[0, 1]) * p + (B[1, 0] - B[1, 1]) * (1 - p) for p in grid]   # first minus second col
    return {"grid": grid, "row_best": np.where(np.array(row_gain) > 0, 1.0, 0.0),
            "col_best": np.where(np.array(col_gain) > 0, 1.0, 0.0)}


# ---------------------------------------------------------------------------------------------------------------
# the guessing game


def guessing_winner(choices, p: float = 2 / 3) -> dict:
    """The target p times the mean, and the choice (or choices) closest to it."""
    x = np.asarray(choices, float)
    target = p * x.mean()
    d = np.abs(x - target)
    win = x[d <= d.min() + 1e-12]
    return {"mean": float(x.mean()), "median": float(np.median(x)), "target": float(target),
            "winner": float(win[0]), "n_winners": int(len(win))}


def level_k(p: float = 2 / 3, steps: int = 6, reference: float = 50.0) -> np.ndarray:
    """Nagel's iteration steps: a level-k player chooses reference times p^k."""
    return reference * p ** np.arange(steps + 1)


def cognitive_hierarchy(tau: float, p: float = 2 / 3, kmax: int = 30, level0: float = 50.0) -> dict:
    """Camerer, Ho and Chong's model of the p-beauty contest: levels are Poisson(tau); level 0 chooses at random
    (mean ``level0``); level k believes the others are drawn from levels 0..k-1 in their Poisson proportions, and
    chooses p times that mixture's mean (a large-population best response).  Returns each level's choice and share,
    and the population's mean."""
    from scipy.stats import poisson  # noqa: PLC0415

    f = poisson.pmf(np.arange(kmax + 1), tau)
    f = f / f.sum()
    x = np.zeros(kmax + 1)
    x[0] = level0
    for k in range(1, kmax + 1):
        w = f[:k] / f[:k].sum()
        x[k] = p * float(w @ x[:k])
    return {"choices": x, "shares": f, "mean": float(f @ x)}


def fit_tau(observed_mean: float, p: float = 2 / 3, level0: float = 50.0) -> float:
    """The tau whose cognitive-hierarchy mean equals ``observed_mean`` (the mean falls as tau rises)."""
    return float(brentq(lambda t: cognitive_hierarchy(t, p, level0=level0)["mean"] - observed_mean, 1e-6, 30.0,
                        xtol=1e-10))


# ---------------------------------------------------------------------------------------------------------------
# extensive form


@dataclass
class Node:
    """A game tree: a decision node has a ``player`` (0 or 1) and named ``moves`` to children; a leaf has
    ``payoff``."""
    player: int | None = None
    moves: dict = field(default_factory=dict)
    payoff: tuple | None = None
    name: str = ""


def backward_induction(node: Node) -> dict:
    """Subgame-perfect play: at each decision node the mover takes the move whose subgame value is best for her
    (ties to the first move listed).  Returns the value, the path of moves from the root, and the plan at every node
    (keyed by node name)."""
    plan = {}

    def solve(nd):
        if nd.payoff is not None:
            return tuple(nd.payoff), []
        best, best_path, best_move = None, None, None
        for mv, child in nd.moves.items():
            val, path = solve(child)
            if best is None or val[nd.player] > best[nd.player] + 1e-12:
                best, best_path, best_move = val, path, mv
        plan[nd.name] = best_move
        return best, [best_move] + best_path

    value, path = solve(node)
    return {"value": value, "path": path, "plan": plan}


def centipede(n: int = 4, start: tuple = (0.4, 0.1), grow: float = 2.0) -> Node:
    """Rosenthal's centipede with McKelvey and Palfrey's payoffs: at node k (k = 0..n-1) the mover, player k mod 2,
    may take the larger share, start[0] grow^k, leaving the other start[1] grow^k; passing grows the pot.  If every
    node passes, the player who would move next takes start[0] grow^n."""

    def leaf(k, name):
        big, small = start[0] * grow ** k, start[1] * grow ** k
        return Node(payoff=(big, small) if k % 2 == 0 else (small, big), name=name)

    node = leaf(n, "end")
    for k in reversed(range(n)):
        node = Node(player=k % 2, moves={"take": leaf(k, f"take{k}"), "pass": node}, name=f"node{k}")
    return node


def entry_game(fight: tuple = (-1, -1), accommodate: tuple = (1, 1), stay_out: tuple = (0, 4)) -> Node:
    """An entrant decides whether to enter; if it does, the incumbent fights or accommodates.  Payoffs are
    (entrant, incumbent)."""
    inc = Node(player=1, moves={"accommodate": Node(payoff=accommodate, name="acc"),
                                "fight": Node(payoff=fight, name="fight")}, name="incumbent")
    return Node(player=0, moves={"enter": inc, "stay out": Node(payoff=stay_out, name="out")}, name="entrant")


def rubinstein(delta1: float, delta2: float | None = None) -> dict:
    """Rubinstein's alternating-offers bargaining over a pie of 1: the proposer's subgame-perfect share is
    (1 - delta2) / (1 - delta1 delta2), agreed at once."""
    d2 = delta1 if delta2 is None else delta2
    share = (1 - d2) / (1 - delta1 * d2)
    return {"proposer": share, "responder": 1 - share}


# ---------------------------------------------------------------------------------------------------------------
# repetition


def grim_threshold(T: float, R: float, P: float, S: float) -> float:
    """A prisoner's dilemma with temptation T > reward R > punishment P > sucker S: grim trigger sustains cooperation
    when delta >= (T - R) / (T - P)."""
    return (T - R) / (T - P)


def folk_region(A, B) -> dict:
    """The feasible payoffs (the convex hull of the pure outcomes), each player's pure-strategy minmax, and the
    feasible, individually rational payoffs (sampled as a polygon by clipping the hull)."""
    from scipy.spatial import ConvexHull  # noqa: PLC0415

    A, B = _as(A), _as(B)
    pts = np.column_stack([A.ravel(), B.ravel()])
    hull = ConvexHull(pts)
    poly = pts[hull.vertices]
    minmax = (float(A.max(axis=0).min()), float(B.max(axis=1).min()))

    def clip(poly, axis, lo):
        out = []
        for a, b in zip(poly, np.roll(poly, -1, axis=0)):
            ina, inb = a[axis] >= lo, b[axis] >= lo
            if ina:
                out.append(a)
            if ina != inb:
                t = (lo - a[axis]) / (b[axis] - a[axis])
                out.append(a + t * (b - a))
        return np.array(out)

    ir = clip(clip(poly, 0, minmax[0]), 1, minmax[1])
    return {"feasible": poly, "minmax": minmax, "rational": ir}


# strategies: each is f(my_history, their_history, rng) -> 1 for cooperate, 0 for defect


def _allc(m, t, rng):
    return 1


def _alld(m, t, rng):
    return 0


def _tft(m, t, rng):
    return 1 if not t else t[-1]


def _grim(m, t, rng):
    return 0 if 0 in t else 1


def _tf2t(m, t, rng):
    return 0 if len(t) >= 2 and t[-1] == 0 and t[-2] == 0 else 1


def _wsls(m, t, rng):
    # win-stay, lose-shift (Pavlov): cooperate if both did the same last round
    return 1 if not m else int(m[-1] == t[-1])


def _gtft(m, t, rng):
    # generous tit for tat: forgive a defection a third of the time
    return 1 if not t or t[-1] == 1 or rng.random() < 1 / 3 else 0


def _random(m, t, rng):
    return int(rng.random() < 0.5)


def _joss(m, t, rng):
    # tit for tat that sneaks in a defection a tenth of the time
    return 0 if (not t or t[-1] == 1) and rng.random() < 0.1 else _tft(m, t, rng)


STRATEGIES = {"ALLC": _allc, "ALLD": _alld, "TFT": _tft, "GRIM": _grim, "TF2T": _tf2t, "WSLS": _wsls,
              "GTFT": _gtft, "RANDOM": _random, "JOSS": _joss}

PD = {"R": 3.0, "T": 5.0, "S": 0.0, "P": 1.0}   # Axelrod's payoffs


def play_match(a: str, b: str, rounds: int = 200, noise: float = 0.0, seed: int = 0, payoff=PD) -> dict:
    """One match of the repeated prisoner's dilemma; with ``noise`` each intended move is flipped with that
    probability.  Returns each side's total and its moves."""
    rng = np.random.default_rng(seed)
    fa, fb = STRATEGIES[a], STRATEGIES[b]
    ha, hb = [], []
    sa = sb = 0.0
    table = {(1, 1): (payoff["R"], payoff["R"]), (1, 0): (payoff["S"], payoff["T"]),
             (0, 1): (payoff["T"], payoff["S"]), (0, 0): (payoff["P"], payoff["P"])}
    for _ in range(rounds):
        x, y = fa(ha, hb, rng), fb(hb, ha, rng)
        if noise and rng.random() < noise:
            x = 1 - x
        if noise and rng.random() < noise:
            y = 1 - y
        pa, pb = table[(x, y)]
        sa += pa
        sb += pb
        ha.append(x)
        hb.append(y)
    return {"a": sa, "b": sb, "moves_a": ha, "moves_b": hb}


def tournament(names, rounds: int = 200, noise: float = 0.0, repeats: int = 5, seed: int = 1980,
               self_play: bool = True) -> dict:
    """Axelrod's round robin: every strategy meets every other (and, as in his tournaments, a copy of itself),
    ``repeats`` times; scores are average points per round.  Returns the score matrix (row's average against
    column) and the ranking."""
    names = list(names)
    k = len(names)
    M = np.zeros((k, k))
    rng = np.random.default_rng(seed)
    for i in range(k):
        for j in range(i, k):
            if i == j and not self_play:
                continue
            tot_i = tot_j = 0.0
            for _ in range(repeats):
                r = play_match(names[i], names[j], rounds, noise, int(rng.integers(1 << 31)))
                tot_i += r["a"]
                tot_j += r["b"]
            M[i, j] = tot_i / (repeats * rounds)
            M[j, i] = tot_j / (repeats * rounds) if i != j else M[i, j]
    mask = np.ones((k, k), bool) if self_play else ~np.eye(k, dtype=bool)
    score = np.array([M[i][mask[i]].mean() for i in range(k)])
    order = list(np.argsort(-score))
    return {"names": names, "matrix": M, "score": score, "ranking": [names[i] for i in order]}


def ecology(M, generations: int = 200, x0=None) -> np.ndarray:
    """Axelrod's ecological tournament: the population shares follow the discrete replicator x_i' = x_i (M x)_i /
    (x' M x) on the match-score matrix M.  Returns the shares by generation."""
    M = _as(M)
    k = M.shape[0]
    x = np.full(k, 1 / k) if x0 is None else _as(x0)
    out = [x.copy()]
    for _ in range(generations):
        f = M @ x
        x = x * f / (x @ f)
        out.append(x.copy())
    return np.array(out)


# ---------------------------------------------------------------------------------------------------------------
# coordination, evolution and learning


def correlated_equilibrium(A, B, objective=None) -> dict:
    """The correlated equilibrium maximizing ``objective`` (default: the sum of payoffs), by linear programming over
    distributions on outcomes subject to each player's obedience constraints."""
    A, B = _as(A), _as(B)
    m, n = A.shape
    c = -(A + B).ravel() if objective is None else -np.asarray(objective, float).ravel()
    rows = []
    for i in range(m):
        for i2 in range(m):
            if i2 != i:
                r = np.zeros((m, n))
                r[i, :] = A[i2, :] - A[i, :]      # deviating from i to i2 must not pay
                rows.append(r.ravel())
    for j in range(n):
        for j2 in range(n):
            if j2 != j:
                r = np.zeros((m, n))
                r[:, j] = B[:, j2] - B[:, j]
                rows.append(r.ravel())
    res = linprog(c, A_ub=np.array(rows), b_ub=np.zeros(len(rows)), A_eq=np.ones((1, m * n)), b_eq=[1.0],
                  bounds=[(0, 1)] * (m * n), method="highs")
    P = res.x.reshape(m, n)
    return {"P": P, "row_payoff": float((P * A).sum()), "col_payoff": float((P * B).sum())}


def replicator(A, x0, T: float = 30.0, steps: int = 3000) -> np.ndarray:
    """The replicator dynamic dx_i/dt = x_i ((A x)_i - x' A x) for a symmetric game with payoff matrix A, by RK4."""
    A = _as(A)
    x = _as(x0).copy()
    h = T / steps

    def f(x):
        g = A @ x
        return x * (g - x @ g)

    out = [x.copy()]
    for _ in range(steps):
        k1 = f(x)
        k2 = f(x + h / 2 * k1)
        k3 = f(x + h / 2 * k2)
        k4 = f(x + h * k3)
        x = x + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x = np.clip(x, 0, None)
        x = x / x.sum()
        out.append(x.copy())
    return np.array(out)


def is_ess(A, x, tol: float = 1e-9) -> bool:
    """Maynard Smith's test for a symmetric game, against every pure mutant: x is an ESS if u(x, x) > u(y, x), or
    u(x, x) = u(y, x) and u(x, y) > u(y, y), for each pure y different from x."""
    A = _as(A)
    x = _as(x)
    for i in range(A.shape[0]):
        y = np.zeros(A.shape[0])
        y[i] = 1
        if np.allclose(y, x):
            continue
        uxx, uyx, uxy, uyy = x @ A @ x, y @ A @ x, x @ A @ y, y @ A @ y
        if uyx > uxx + tol:
            return False
        if abs(uyx - uxx) <= tol and not uxy > uyy + tol:
            return False
    return True


def fictitious_play(A, B, rounds: int = 2000, start=(0, 0)) -> dict:
    """Brown's fictitious play: each round each player best-responds to the other's empirical frequencies so far
    (ties to the lowest index).  Returns the running frequencies of each player's actions."""
    A, B = _as(A), _as(B)
    m, n = A.shape
    cr, cc = np.zeros(m), np.zeros(n)
    cr[start[0]] += 1
    cc[start[1]] += 1
    fr, fc = [cr / cr.sum()], [cc / cc.sum()]
    for _ in range(rounds - 1):
        i = int(np.argmax(A @ (cc / cc.sum())))
        j = int(np.argmax((cr / cr.sum()) @ B))
        cr[i] += 1
        cc[j] += 1
        fr.append(cr / cr.sum())
        fc.append(cc / cc.sum())
    return {"row": np.array(fr), "col": np.array(fc)}


def regret_matching(A, B, rounds: int = 20000, seed: int = 2000) -> dict:
    """Hart and Mas-Colell's regret matching: each player plays each action with probability proportional to its
    positive cumulative regret (uniformly when none is positive).  Returns the average strategies over time and the
    final average regrets."""
    A, B = _as(A), _as(B)
    m, n = A.shape
    rng = np.random.default_rng(seed)
    Rr, Rc = np.zeros(m), np.zeros(n)
    sr, sc = np.zeros(m), np.zeros(n)
    avg_r, avg_c = [], []
    for t in range(1, rounds + 1):
        pr_ = np.maximum(Rr, 0)
        pr_ = pr_ / pr_.sum() if pr_.sum() > 0 else np.full(m, 1 / m)
        pc_ = np.maximum(Rc, 0)
        pc_ = pc_ / pc_.sum() if pc_.sum() > 0 else np.full(n, 1 / n)
        i = rng.choice(m, p=pr_)
        j = rng.choice(n, p=pc_)
        Rr += A[:, j] - A[i, j]
        Rc += B[i, :] - B[i, j]
        sr += pr_
        sc += pc_
        if t % max(rounds // 400, 1) == 0:
            avg_r.append(sr / t)
            avg_c.append(sc / t)
    return {"row": np.array(avg_r), "col": np.array(avg_c), "regret_row": float(np.maximum(Rr, 0).max() / rounds),
            "regret_col": float(np.maximum(Rc, 0).max() / rounds)}


# ---------------------------------------------------------------------------------------------------------------
# incomplete information


def bayes_nash_2x2(A_types, B, prior) -> list[dict]:
    """Pure Bayesian Nash equilibria when the row player has types (with row payoff matrices ``A_types`` and prior
    ``prior``) and the column player, who does not know the type, has payoffs ``B_types[t]`` (one matrix per type).
    Checks every plan (an action for each row type) against every column action."""
    A_types = [_as(a) for a in A_types]
    B = [_as(b) for b in B]
    prior = np.asarray(prior, float)
    m, n = A_types[0].shape
    out = []
    for plan in itertools.product(range(m), repeat=len(A_types)):
        for j in range(n):
            ok_row = all(A_types[t][plan[t], j] >= A_types[t][:, j].max() - 1e-12 for t in range(len(A_types)))
            col_val = [sum(prior[t] * B[t][plan[t], jj] for t in range(len(A_types))) for jj in range(n)]
            if ok_row and col_val[j] >= max(col_val) - 1e-12:
                out.append({"plan": plan, "col": j, "col_payoff": float(col_val[j])})
    return out
