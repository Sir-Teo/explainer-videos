"""Psyche's reasoning: Part 24 of *Psychology, Built* (reasoning and problem solving).

Syllogisms: every syllogism's valid conclusions by brute force over set models, and four accounts of what people
answer instead (logic, atmosphere, matching, and the probability heuristics' min-rule), scored against people.
The selection task: Oaksford and Chater's optimal data selection, the expected information gain of each card.
Search: the Tower of Hanoi's state space, the optimal path, and a goal-stack production system whose pauses come
where it sets subgoals.  Insight: the nine-dot puzzle solved by brute force, with and without leaving the box.
Analogy: a structure-mapping matcher.  Imagery: rotation at a constant speed, fitted per person.  Causes: delta P
and causal power.  Everyday prediction: the Bayesian predictor under power-law, Erlang and Gaussian priors.

numpy and scipy only.  Every function is deterministic given its arguments (and a ``rng`` where it samples)."""

from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np

# ------------------------------------------------------------------------------------------------ syllogisms
# A syllogism: two premises over terms A, B, C (B the middle term).  Moods: A all, I some, E no, O some ... not.
# Figure 1: A-B, B-C; 2: B-A, C-B; 3: A-B, C-B; 4: B-A, B-C (the order used by Khemlani and Johnson-Laird, 2012).
QUANT = {"All": "A", "Some": "I", "No": "E", "Some not": "O"}
WORD = {v: k for k, v in QUANT.items()}
RESPONSES = [q + d for q in "AIEO" for d in ("ac", "ca")] + ["NVC"]


def _regions():
    """The eight kinds of individual: membership in (A, B, C)."""
    return list(itertools.product((0, 1), repeat=3))


REG = _regions()


def _holds(mood: str, x: int, y: int, model) -> bool:
    """Is 'mood x y' true in a model (the set of nonempty regions)?  x, y index the terms 0, 1, 2."""
    xs = [r for r in model if r[x]]
    if mood == "A":
        return all(r[y] for r in xs)
    if mood == "I":
        return any(r[y] for r in xs)
    if mood == "E":
        return not any(r[y] for r in xs)
    if mood == "O":
        return any(not r[y] for r in xs)
    raise ValueError(mood)


@lru_cache(maxsize=None)
def _models():
    """Every model in which A, B and C are all nonempty (existential presupposition): subsets of the regions."""
    out = []
    for bits in range(1, 256):
        m = [REG[k] for k in range(8) if bits >> k & 1]
        if all(any(r[t] for r in m) for t in range(3)):
            out.append(tuple(m))
    return out


def premises(task: str):
    """'A1' style code to the two premises as (mood, x, y) with terms 0=A, 1=B, 2=C.  Task codes are mood pairs and
    a figure, e.g. 'AI1' is All A are B, Some B are C."""
    m1, m2, fig = task[0], task[1], int(task[2])
    first = {1: (0, 1), 2: (1, 0), 3: (0, 1), 4: (1, 0)}[fig]
    second = {1: (1, 2), 2: (2, 1), 3: (2, 1), 4: (1, 2)}[fig]
    return (m1, *first), (m2, *second)


def valid_conclusions(task: str) -> list:
    """The responses (from RESPONSES) true in every model of the premises; ['NVC'] if none is."""
    p1, p2 = premises(task)
    ms = [m for m in _models() if _holds(*p1, m) and _holds(*p2, m)]
    out = []
    for r in RESPONSES[:-1]:
        x, y = (0, 2) if r[1:] == "ac" else (2, 0)
        if all(_holds(r[0], x, y, m) for m in ms):
            out.append(r)
    return out or ["NVC"]


TASKS = [a + b + str(f) for a in "AIEO" for b in "AIEO" for f in (1, 2, 3, 4)]


def figural_direction(task: str) -> list:
    """The figural effect: A-B, B-C favours an a-c conclusion; B-A, C-B favours c-a; the others either."""
    f = int(task[2])
    return {1: ["ac"], 2: ["ca"], 3: ["ac", "ca"], 4: ["ac", "ca"]}[f]


def predict(task: str, account: str) -> list:
    """The responses an account predicts for a syllogism.

    ``logic``: the valid conclusions.  ``atmosphere`` (Woodworth and Sells 1935): negative if either premise is,
    particular if either premise is.  ``matching`` (Wetherick and Gilhooly 1995): the mood of the more conservative
    premise (No over Some and Some not, over All).  ``phm`` (Chater and Oaksford 1999): the mood of the less
    informative premise, All > Some > No > Some not.  Directions follow the figure."""
    m1, m2 = task[0], task[1]
    dirs = figural_direction(task)
    if account == "logic":
        return valid_conclusions(task)
    if account == "atmosphere":
        neg = m1 in "EO" or m2 in "EO"
        part = m1 in "IO" or m2 in "IO"
        q = {(False, False): "A", (False, True): "I", (True, False): "E", (True, True): "O"}[(neg, part)]
    elif account == "matching":
        rank = {"E": 3, "O": 2, "I": 2, "A": 1}
        cands = [m for m in (m1, m2) if rank[m] == max(rank[m1], rank[m2])]
        return [c + d for c in dict.fromkeys(cands) for d in dirs]
    elif account == "phm":
        info = {"A": 4, "I": 3, "E": 2, "O": 1}
        q = m1 if info[m1] <= info[m2] else m2
    else:
        raise ValueError(account)
    return [q + d for d in dirs]


def parse_ccobra(task: str, response: str):
    """A CCOBRA row ('Some;models;managers/All;models;clerks', 'Some;managers;clerks') to ('IA4', 'Iac')."""
    (q1, x1, y1), (q2, x2, y2) = [p.split(";") for p in task.split("/")]
    mid = ({x1, y1} & {x2, y2}).pop()
    a = x1 if x1 != mid else y1
    c = x2 if x2 != mid else y2
    if (x1, y1) == (a, mid) and (x2, y2) == (mid, c):
        fig = 1
    elif (x1, y1) == (mid, a) and (x2, y2) == (c, mid):
        fig = 2
    elif (x1, y1) == (a, mid) and (x2, y2) == (c, mid):
        fig = 3
    else:
        fig = 4
    code = QUANT[q1] + QUANT[q2] + str(fig)
    if response.strip() == "NVC":
        return code, "NVC"
    q, s, p = response.split(";")
    return code, QUANT[q] + ("ac" if (s, p) == (a, c) else "ca")


def response_table(tasks, responses) -> np.ndarray:
    """A 64 x 9 table of response proportions, rows in TASKS order, columns in RESPONSES order."""
    T = np.zeros((len(TASKS), len(RESPONSES)))
    ti = {t: k for k, t in enumerate(TASKS)}
    ri = {r: k for k, r in enumerate(RESPONSES)}
    for t, r in zip(tasks, responses):
        T[ti[t], ri[r]] += 1
    n = T.sum(axis=1, keepdims=True)
    return np.divide(T, n, out=np.zeros_like(T), where=n > 0)  # a syllogism nobody answered stays all zero


def score(table: np.ndarray, account: str) -> dict:
    """How an account fares: the share of all responses it predicts ('coverage'), the share of syllogisms whose
    commonest response it predicts ('hits'), and how many responses it predicts per syllogism on average."""
    ri = {r: k for k, r in enumerate(RESPONSES)}
    cov, hits, n = [], [], []
    for k, t in enumerate(TASKS):
        pr = predict(t, account)
        idx = [ri[r] for r in pr]
        cov.append(table[k, idx].sum())
        hits.append(int(np.argmax(table[k])) in idx)
        n.append(len(idx))
    return {"coverage": float(np.mean(cov)), "hits": float(np.mean(hits)), "n_predicted": float(np.mean(n))}


# ------------------------------------------------------------------------------------- the selection task
def _h(p) -> float:
    p = np.asarray(p, float)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def selection_information(a: float = 0.1, b: float = 0.2, prior_md: float = 0.5) -> dict:
    """Oaksford and Chater (1994): expected information gain, in bits, of turning each card of 'if p then q'.

    Two hypotheses: dependence (MD, every p is a q) and independence (MI).  P(p) = a and P(q) = b are the same
    under both (rarity: both small).  For a card showing one side, the gain is the prior entropy over MD/MI less
    the expected posterior entropy after seeing the other side."""
    if not 0 < a <= b < 1:
        raise ValueError("needs 0 < a <= b < 1")
    joint = {  # P(p-side, q-side) under each hypothesis
        "MD": {(1, 1): a, (1, 0): 0.0, (0, 1): b - a, (0, 0): 1 - b},
        "MI": {(1, 1): a * b, (1, 0): a * (1 - b), (0, 1): (1 - a) * b, (0, 0): (1 - a) * (1 - b)},
    }
    prior = {"MD": prior_md, "MI": 1 - prior_md}
    h0 = _h(list(prior.values()))
    out = {}
    for card, (side, val) in {"p": (0, 1), "not-p": (0, 0), "q": (1, 1), "not-q": (1, 0)}.items():
        eh = 0.0
        for hidden in (0, 1):
            key = (val, hidden) if side == 0 else (hidden, val)
            like = {h: joint[h][key] / sum(v for k, v in joint[h].items() if k[side] == val) for h in prior}
            p_y = sum(prior[h] * like[h] for h in prior)
            if p_y == 0:
                continue
            post = [prior[h] * like[h] / p_y for h in prior]
            eh += p_y * _h(post)
        out[card] = h0 - eh
    return out


# --------------------------------------------------------------------------------------- the Tower of Hanoi
def hanoi_states(n: int) -> list:
    """Every state of n discs on three pegs: a tuple giving each disc's peg, smallest disc first."""
    return list(itertools.product(range(3), repeat=n))


def hanoi_moves(state) -> list:
    """The legal moves from a state, as (disc, from, to): a disc may move if no smaller disc is on its peg, onto a
    peg with no smaller disc."""
    out = []
    for d, peg in enumerate(state):
        if any(state[s] == peg for s in range(d)):
            continue
        for to in range(3):
            if to != peg and not any(state[s] == to for s in range(d)):
                out.append((d, peg, to))
    return out


def hanoi_graph(n: int):
    """States and edges of the state space (3**n states; the Sierpinski graph)."""
    S = hanoi_states(n)
    idx = {s: k for k, s in enumerate(S)}
    edges = set()
    for s in S:
        for d, _, to in hanoi_moves(s):
            t = list(s)
            t[d] = to
            edges.add(tuple(sorted((idx[s], idx[tuple(t)]))))
    return S, sorted(edges)


def hanoi_layout(n: int) -> dict:
    """2-D positions for the states: the Sierpinski triangle.  The largest disc picks one of three corners; inside
    that corner's sub-triangle the two other pegs swap places, so that every move of the largest disc joins the two
    nearest corners of neighbouring sub-triangles, and so on down to the smallest disc."""
    corners = np.array([[0.0, 1.0], [-0.866, -0.5], [0.866, -0.5]])
    pos = {}
    for s in hanoi_states(n):
        p = np.zeros(2)
        scale = 1.0
        perm = [0, 1, 2]  # peg -> corner, at the current level
        for d in reversed(range(n)):  # largest disc first
            c = perm[s[d]]
            p = p + scale * corners[c]
            a_, b_ = [k for k in range(3) if k != c]
            perm = [b_ if q == a_ else a_ if q == b_ else q for q in perm]
            scale /= 2
        pos[s] = p
    return pos


def hanoi_shortest(start, goal) -> list:
    """The shortest path between two states, by breadth-first search."""
    from collections import deque

    prev = {tuple(start): None}
    q = deque([tuple(start)])
    while q:
        s = q.popleft()
        if s == tuple(goal):
            break
        for d, _, to in hanoi_moves(s):
            t = list(s)
            t[d] = to
            t = tuple(t)
            if t not in prev:
                prev[t] = s
                q.append(t)
    path = [tuple(goal)]
    while prev[path[-1]] is not None:
        path.append(prev[path[-1]])
    return path[::-1]


def goal_stack_solver(n: int, start: int = 0, goal: int = 2, t_move: float = 1.0, t_goal: float = 1.5) -> dict:
    """A goal-recursion production system (after Simon 1975 and Anderson's ACT-R models of the tower).

    To get disc d to peg g: if a smaller disc is in the way, push a subgoal to move the discs above it to the other
    peg; when clear, move d.  Each move costs ``t_move`` seconds and each subgoal pushed before it ``t_goal``: the
    latency of a move is long where a new tower of subgoals has to be built.  Returns the moves, their latencies and
    the states visited (it is optimal: 2**n - 1 moves)."""
    state = [start] * n
    moves, lat, states = [], [], [tuple(state)]
    pending = [0]

    def solve(d, g):
        if d < 0:
            return
        if state[d] == g:
            solve(d - 1, g)
            return
        other = 3 - state[d] - g
        if any(state[s] != other for s in range(d)):
            pending[0] += 1  # a subgoal: get the smaller discs out of the way
            solve(d - 1, other)
        lat.append(t_move + t_goal * pending[0])
        pending[0] = 0
        moves.append((d, state[d], g))
        state[d] = g
        states.append(tuple(state))
        solve(d - 1, g)

    solve(n - 1, goal)
    return {"moves": moves, "latency": np.array(lat), "states": states}


def hill_climb(n: int, start: int = 0, goal: int = 2, max_moves: int = 200, rng=None) -> list:
    """A greedy solver that prefers moves putting more discs on the goal peg (ties at random, no immediate undo):
    it reaches the goal, but rarely by the shortest path."""
    rng = np.random.default_rng(rng)
    s = tuple([start] * n)
    path = [s]
    last = None
    for _ in range(max_moves):
        if all(p == goal for p in s):
            break
        opts = []
        for d, fr, to in hanoi_moves(s):
            if last is not None and (d, to, fr) == last:
                continue
            t = list(s)
            t[d] = to
            score = sum((d_ + 1) for d_ in range(n) if t[d_] == goal and all(t[e] == goal for e in range(d_, n)))
            opts.append((score, rng.random(), (d, fr, to), tuple(t)))
        opts.sort(reverse=True)
        _, _, last, s = opts[0]
        path.append(s)
    return path


# ------------------------------------------------------------------------------------------ the nine dots
def nine_dots(lo: int = 0, hi: int = 2, segments: int = 4) -> list:
    """Every way to draw ``segments`` connected straight lines, turning only at lattice points in [lo, hi]^2, that
    pass through all nine dots of the 3 x 3 grid [0, 2]^2.  Returns the distinct drawings (as point lists): a path
    and its reverse are one drawing, and so are two that differ only in how far an end line runs past its last
    dot."""
    dots = [(x, y) for x in range(3) for y in range(3)]
    pts = [(x, y) for x in range(lo, hi + 1) for y in range(lo, hi + 1)]

    def covered(p, q):
        out = set()
        (x0, y0), (x1, y1) = p, q
        for d in dots:
            cross = (x1 - x0) * (d[1] - y0) - (y1 - y0) * (d[0] - x0)
            if cross == 0 and min(x0, x1) <= d[0] <= max(x0, x1) and min(y0, y1) <= d[1] <= max(y0, y1):
                out.add(d)
        return out

    seg_cache = {}
    sols = set()

    def dfs(path, cov, left):
        if len(cov) == 9:
            sols.add(min(tuple(path), tuple(reversed(path))))
            return
        if left == 0 or 9 - len(cov) > 3 * left:
            return
        for q in pts:
            if q == path[-1]:
                continue
            key = (path[-1], q)
            if key not in seg_cache:
                seg_cache[key] = covered(*key)
            new = seg_cache[key] - cov
            if not new:
                continue
            dfs(path + [q], cov | seg_cache[key], left - 1)

    for p in pts:
        dfs([p], set(), segments)

    def trim(path):  # an end segment drawn past its last dot is the same drawing as one stopped at that dot
        path = list(path)
        for end, nxt in ((0, 1), (len(path) - 1, len(path) - 2)):
            on = sorted(seg_cache.get((path[nxt], path[end])) or seg_cache.get((path[end], path[nxt])),
                        key=lambda d: -abs(d[0] - path[nxt][0]) - abs(d[1] - path[nxt][1]))
            path[end] = on[0]
        return min(tuple(path), tuple(reversed(path)))

    return [list(s) for s in sorted({trim(s) for s in sols})]


# ------------------------------------------------------------------------------------------------ analogy
def structure_map(base: list, target: list) -> dict:
    """Structure mapping (Gentner 1983), by brute force over one-to-one object correspondences.

    ``base`` and ``target`` are lists of relations (name, arg1, arg2, ...), where an argument may itself be a
    relation (a tuple), as in ('cause', ('divide', 'army'), ('capture', 'army', 'fortress')).  A mapping scores one
    point for each base relation whose image under the mapping is in the target, and a point more for each
    higher-order relation matched with all its arguments (systematicity).  Returns the best mapping and its score,
    and the matched relations."""
    def objects(rels):
        out = []
        for r in rels:
            for a in r[1:]:
                for o in (objects([a]) if isinstance(a, tuple) else [a]):
                    if o not in out:
                        out.append(o)
        return out

    bo, to = objects(base), objects(target)
    tset = set(target)

    def image(r, m):
        return (r[0],) + tuple(image(a, m) if isinstance(a, tuple) else m.get(a, "?") for a in r[1:])

    def all_rels(rels):
        out = []
        for r in rels:
            out.append(r)
            out += all_rels([a for a in r[1:] if isinstance(a, tuple)])
        return out

    tall = set(all_rels(target)) | tset
    best = (-1, None, [])
    k = min(len(bo), len(to))
    for perm in itertools.permutations(to, k):
        for chosen in itertools.combinations(bo, k) if len(bo) > k else [tuple(bo)]:
            m = dict(zip(chosen, perm))
            matched = [r for r in all_rels(base) if image(r, m) in tall]
            s = len(matched) + sum(1 for r in matched if any(isinstance(a, tuple) for a in r[1:]))
            if s > best[0]:
                best = (s, m, matched)
    return {"score": best[0], "mapping": best[1], "matched": best[2]}


# ------------------------------------------------------------------------------------------------ imagery
def rotation_fit(angle, rt) -> dict:
    """Least-squares line of response time on angular disparity: intercept (ms), slope (ms per degree) and the
    implied rotation rate (degrees per second)."""
    angle, rt = np.asarray(angle, float), np.asarray(rt, float)
    ok = np.isfinite(angle) & np.isfinite(rt)
    b, a = np.polyfit(angle[ok], rt[ok], 1)
    return {"intercept": float(a), "slope": float(b), "rate": float(1000.0 / b) if b > 0 else float("inf")}


def rotation_model(angles, rate: float = 90.0, t0: float = 1500.0, step: float = 10.0, sd_step: float = 0.3,
                   n: int = 200, rng=None) -> np.ndarray:
    """Psyche rotates the image in small steps of ``step`` degrees until it matches, each step taking a gamma-
    distributed time with mean step/rate seconds (cv ``sd_step``), plus ``t0`` ms to encode and respond.  Returns
    an (n, len(angles)) array of simulated times (ms)."""
    rng = np.random.default_rng(rng)
    angles = np.asarray(angles, float)
    k = 1.0 / sd_step ** 2
    mean = 1000.0 * step / rate
    out = np.empty((n, len(angles)))
    for j, a in enumerate(angles):
        steps = int(np.ceil(a / step))
        out[:, j] = t0 + (rng.gamma(k * steps, mean / k, n) if steps else 0.0)
    return out


# ------------------------------------------------------------------------------------------------- causes
def delta_p(table) -> float:
    """P(e | c) - P(e | not c) from a 2 x 2 table [[e&c, not-e&c], [e&not-c, not-e&not-c]]."""
    t = np.asarray(table, float)
    return float(t[0, 0] / t[0].sum() - t[1, 0] / t[1].sum())


def causal_power(table) -> float:
    """Cheng's (1997) generative causal power: delta P / (1 - P(e | not c))."""
    t = np.asarray(table, float)
    pe_nc = t[1, 0] / t[1].sum()
    return float("nan") if pe_nc >= 1 else delta_p(t) / (1 - pe_nc)


# --------------------------------------------------------------------------------------- everyday prediction
def predict_total(t, prior: str, **kw) -> float:
    """The posterior median of a total duration t_total, having seen it reach t (sampled uniformly within it), under
    a prior: 'power' (p ∝ t_total^-gamma, ``gamma``), 'erlang' (shape 2, ``scale``) or 'gauss' (``mu``, ``sigma``).
    The likelihood of t given t_total is 1/t_total for t_total >= t (Griffiths and Tenenbaum 2006)."""
    if prior == "power":
        return float(t * 2 ** (1.0 / kw.get("gamma", 1.0)))
    grid = np.linspace(t, t + 20 * kw.get("scale", kw.get("sigma", 1.0)) + 5 * kw.get("mu", 0.0), 20001)[1:]
    if prior == "erlang":
        s = kw["scale"]
        pri = grid / s ** 2 * np.exp(-grid / s)
    elif prior == "gauss":
        pri = np.exp(-0.5 * ((grid - kw["mu"]) / kw["sigma"]) ** 2)
    else:
        raise ValueError(prior)
    post = pri / grid
    c = np.cumsum(post)
    return float(grid[np.searchsorted(c, c[-1] / 2)])
