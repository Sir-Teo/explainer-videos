"""Phenomenology and its heirs, built (Part 29).

* Husserl's adumbrations: a cube seen from 4000 viewpoints never shows more than three faces at once, yet every face
  is seen from some viewpoint; and eidetic variation as free variation of a triangle (an analogy).
* Husserl's time-consciousness: a 'knife-edge' present against a retentional present, on every ordering of five
  notes; and the coordinates of his diagram of sinking retentions.
* The frame problem (McCarthy and Hayes 1969; Dennett 1984): frame axioms against successor-state axioms (Reiter
  1991), Dennett's robots R1, R1D1 and R2D1 in a planner, and the cost of considering what is irrelevant.
* Braitenberg's vehicles (1984): behaviour from the coupling of body, sensors and world.
* Eternal recurrence: a reversible cellular automaton must return to its start; Simmel's wheels need not.
* The hermeneutic circle as an iteration between parts and whole (an analogy).
* Saussure in geometry: word vectors under rotation, and orthogonal Procrustes.
* Strategic gaming of a threshold (Goodhart; normalization).
* Definitions that only lead to other words: the minimum set that must be grounded.
"""

from __future__ import annotations

import itertools
import math
import random
from collections import deque

import numpy as np

# ---------------------------------------------------------------------------
# Husserl: adumbrations of a cube
# ---------------------------------------------------------------------------
FACES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}


def visible_faces(eye) -> list:
    """Faces of the cube [-1/2, 1/2]^3 seen from a point outside it: a face is visible iff the eye lies beyond the
    plane of that face."""
    e = np.asarray(eye, float)
    return [f for f, (ax, sg) in FACES.items() if sg * e[ax] > 0.5]


def adumbrations(n: int = 4000, dist: float = 1.3, seed: int = 1907) -> dict:
    """Husserl: a physical thing is given only in profiles (Abschattungen). From n random viewpoints at distance
    `dist` from the centre, count the faces seen at once; and the union of what is seen from all of them."""
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(n, 3))
    v = dist * v / np.linalg.norm(v, axis=1, keepdims=True)
    counts = {1: 0, 2: 0, 3: 0}
    seen = set()
    for e in v:
        fs = visible_faces(e)
        counts[len(fs)] = counts.get(len(fs), 0) + 1
        seen |= set(fs)
    return {"n": n, "dist": dist, "counts": counts, "max_at_once": max(k for k, c in counts.items() if c),
            "union": sorted(seen), "all_six": len(seen) == 6}


def cube_profile(azimuth: float, elevation: float, dist: float = 3.2, scale: float = 1.0) -> list:
    """A perspective drawing of the cube from a viewpoint at the given azimuth and elevation (degrees): a list of
    (face, 2-d polygon, shade) for the visible faces, back to front."""
    az, el = math.radians(azimuth), math.radians(elevation)
    eye = dist * np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
    fwd = -eye / np.linalg.norm(eye)
    right = np.cross(fwd, [0, 0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    light = np.array([0.4, -0.3, 0.85])
    light /= np.linalg.norm(light)
    out = []
    for f in visible_faces(eye):
        ax, sg = FACES[f]
        others = [i for i in range(3) if i != ax]
        corners = []
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            p = np.zeros(3)
            p[ax] = sg * 0.5
            p[others[0]] = a * 0.5
            p[others[1]] = b * 0.5
            d = p - eye
            z = d @ fwd
            corners.append([round(float(scale * (d @ right) / z * 2.2), 4), round(float(scale * (d @ up) / z * 2.2), 4)])
        normal = np.zeros(3)
        normal[ax] = sg
        depth = float(np.linalg.norm(normal * 0.5 - eye))
        out.append((f, corners, round(0.35 + 0.65 * max(0.0, float(normal @ light)), 3), depth))
    out.sort(key=lambda t: -t[3])
    return [(f, c, sh) for f, c, sh, _ in out]


# ---------------------------------------------------------------------------
# Eidetic variation (an analogy)
# ---------------------------------------------------------------------------
def _angles(P):
    a, b, c = (np.linalg.norm(P[1] - P[2]), np.linalg.norm(P[0] - P[2]), np.linalg.norm(P[0] - P[1]))
    A = math.acos(max(-1, min(1, (b * b + c * c - a * a) / (2 * b * c))))
    B = math.acos(max(-1, min(1, (a * a + c * c - b * b) / (2 * a * c))))
    return (a, b, c), (A, B, math.pi - A - B)


def eidetic(n: int = 5000, seed: int = 1913, tol: float = 1e-9) -> dict:
    """Husserl's eidetic variation, imitated by sampling (his variation is in imagination, and is meant to reach
    every case): vary a triangle freely, and sort its properties into those that survive every variation
    (candidates for the essence) and those that do not (accidents)."""
    rng = np.random.default_rng(seed)
    props = {"three sides": 0, "angles sum to 180": 0, "longest side faces the largest angle": 0,
             "at least two acute angles": 0, "each side shorter than the other two together": 0,
             "obtuse": 0, "acute": 0, "right-angled": 0, "isosceles": 0, "a side longer than 1": 0}
    used = 0
    while used < n:
        P = rng.random((3, 2))
        sides, ang = _angles(P)
        if min(sides) < 1e-6:
            continue
        used += 1
        A = np.array(ang)
        S = np.array(sides)
        props["three sides"] += 1
        props["angles sum to 180"] += abs(sum(ang) - math.pi) < 1e-9
        props["longest side faces the largest angle"] += int(np.argmax(S)) == int(np.argmax(A))
        props["at least two acute angles"] += int((A < math.pi / 2).sum()) >= 2
        props["each side shorter than the other two together"] += all(
            S[i] < S.sum() - S[i] for i in range(3))
        props["obtuse"] += bool((A > math.pi / 2 + tol).any())
        props["acute"] += bool((A < math.pi / 2 - tol).all())
        props["right-angled"] += bool((abs(A - math.pi / 2) < 1e-3).any())
        props["isosceles"] += bool(min(abs(S[0] - S[1]), abs(S[1] - S[2]), abs(S[0] - S[2])) < 1e-3)
        props["a side longer than 1"] += bool(S.max() > 1)
    rows = [{"property": k, "count": int(v), "share": round(v / n, 4), "invariant": v == n} for k, v in props.items()]
    return {"n": n, "rows": rows}


# ---------------------------------------------------------------------------
# Time-consciousness: retention
# ---------------------------------------------------------------------------
def retention(n_notes: int = 5, decay: float = 0.5) -> dict:
    """Every ordering of n distinct notes (120 melodies for n = 5). A 'knife-edge' present holds only the current
    note; a short window holds the last two; a retentional present holds every past note, fainter the further it
    has sunk (weight decay^age). Count the melodies each can tell apart at the final moment, and whether the order can
    be read back from the retentional present."""
    melodies = list(itertools.permutations(range(n_notes)))

    def state(m, kind):
        if kind == "knife":
            return (m[-1],)
        if kind == "window":
            return tuple(m[-2:])
        w = np.zeros(n_notes)
        for age, note in enumerate(reversed(m)):
            w[note] += decay ** age
        return tuple(np.round(w, 9))

    out = {}
    for kind in ("knife", "window", "retention"):
        out[kind] = len({state(m, kind) for m in melodies})
    decoded = 0
    for m in melodies:
        w = np.array(state(m, "retention"))
        order = tuple(int(i) for i in np.argsort(w))          # faintest first = earliest
        decoded += order == m
    return {"n_notes": n_notes, "melodies": len(melodies), "distinct": out, "decoded": decoded, "decay": decay}


def husserl_diagram(n: int = 5, slope: float = 0.55) -> dict:
    """Husserl's 1905 diagram: the horizontal line of now-points 0..n-1; from each now-point a diagonal sinking into
    retention; the vertical at the current now is the cross-section of the living present."""
    nows = [[float(t), 0.0] for t in range(n)]
    diag = {k: [[float(t), -slope * (t - k)] for t in range(k, n)] for k in range(n)}
    section = [[float(n - 1), -slope * (n - 1 - k)] for k in range(n)]
    return {"nows": nows, "diagonals": diag, "section": section, "slope": slope}


# ---------------------------------------------------------------------------
# The frame problem
# ---------------------------------------------------------------------------
def axiom_counts(sizes=((3, 5), (10, 50), (100, 1000))) -> dict:
    """McCarthy and Hayes (1969): in the situation calculus, for every action and every fluent it does not affect, an
    explicit frame axiom ('painting does not move the wagon'): about 2 A F of them. Reiter (1991): one successor-state
    axiom per fluent, F in all, each saying exactly when the fluent is true after an action."""
    return {"rows": [{"actions": a, "fluents": f, "frame_axioms": 2 * a * f, "ssa": f} for a, f in sizes]}


BASE_FLUENTS = ("robot_out", "wagon_out", "battery_out", "bomb_out", "battery_on", "bomb_on", "door_open")
START = {"robot_out": False, "wagon_out": False, "battery_out": False, "bomb_out": False, "battery_on": True,
         "bomb_on": True, "door_open": False}


def _actions(n_irrelevant: int):
    acts = ["open_door", "pull_wagon_out", "remove_bomb", "remove_battery"]
    acts += [f"toggle_{i}" for i in range(n_irrelevant)]
    return acts


def _applicable(state, a) -> bool:
    if a == "open_door":
        return not state["door_open"]
    if a == "pull_wagon_out":
        return state["door_open"] and not state["wagon_out"] and not state["robot_out"]
    if a in ("remove_bomb", "remove_battery"):
        x = a.split("_")[1]
        return state[f"{x}_on"] and not state["wagon_out"]
    return True


def _successor(state, a, ramification: bool = True) -> dict:
    """Successor-state axioms: a fluent is true after a iff a made it true, or it was true and a did not make it
    false. `ramification=False` gives R1's incomplete model: pulling the wagon moves the wagon, the robot and the
    battery it wants, and nothing else."""
    s = dict(state)
    if a == "open_door":
        s["door_open"] = True
    elif a == "pull_wagon_out":
        s["robot_out"] = s["wagon_out"] = True
        for x in ("battery", "bomb"):
            if state[f"{x}_on"] and (ramification or x == "battery"):
                s[f"{x}_out"] = True
    elif a in ("remove_bomb", "remove_battery"):
        s[f"{a.split('_')[1]}_on"] = False
    elif a.startswith("toggle_"):
        k = "irr_" + a.split("_")[1]
        s[k] = not s.get(k, False)
    return s


def _goal(s) -> bool:
    return s["battery_out"] and s["robot_out"] and not s["bomb_out"]


def _plan(n_irrelevant: int, ramification: bool = True, relevant_only: bool = False):
    acts = _actions(n_irrelevant)
    if relevant_only:
        acts = [a for a in acts if not a.startswith("toggle_")]
    start = dict(START)
    for i in range(n_irrelevant):
        start[f"irr_{i}"] = False
    key = lambda s: tuple(sorted(s.items()))
    frontier = deque([(start, [])])
    seen = {key(start)}
    expanded = derived = 0
    while frontier:
        s, path = frontier.popleft()
        if _goal(s):
            return path, expanded, derived
        expanded += 1
        for a in acts:
            if not _applicable(s, a):
                continue
            t = _successor(s, a, ramification)
            derived += len(t)                        # every fluent's value after a, deduced
            k = key(t)
            if k not in seen:
                seen.add(k)
                frontier.append((t, path + [a]))
    return None, expanded, derived


def robots(irrelevant=(0, 2, 4, 6, 8)) -> dict:
    """Dennett (1984), 'Cognitive Wheels'. R1's battery is on a wagon in a room, with a bomb on the same wagon. R1
    plans with an incomplete model of pulling, and carries the bomb out with the battery. R1D1 deduces every
    consequence of every action it considers; R2D1 also deduces, for each, that it is irrelevant. With successor-state
    axioms the planner finds the right plan, but breadth-first search still considers every irrelevant action, and the
    work grows with the number of irrelevant fluents; told in advance which actions are relevant, it does not."""
    r1_plan, _, _ = _plan(0, ramification=False)
    s = dict(START)
    for a in r1_plan:
        s = _successor(s, a, ramification=True)
    r1_outcome = {"bomb_out": s["bomb_out"], "battery_out": s["battery_out"]}
    good, _, _ = _plan(0)
    rows = []
    for k in irrelevant:
        p, e, d = _plan(k)
        p2, e2, d2 = _plan(k, relevant_only=True)
        rows.append({"irrelevant": k, "fluents": len(BASE_FLUENTS) + k, "expanded": e, "derived": d,
                     "expanded_relevant": e2, "derived_relevant": d2, "plan_len": len(p)})
    return {"r1_plan": r1_plan, "r1_outcome": r1_outcome, "plan": good, "rows": rows}


# ---------------------------------------------------------------------------
# Braitenberg's vehicles
# ---------------------------------------------------------------------------
VEHICLES = {"2a": ("uncrossed", "excite"), "2b": ("crossed", "excite"), "3a": ("uncrossed", "inhibit"),
            "3b": ("crossed", "inhibit")}


def braitenberg(steps: int = 900, dt: float = 0.02, start=(-3.0, -1.2, 0.0), light=(0.0, 0.0)) -> dict:
    """Braitenberg (1984): two light sensors at the front, two wheels. Wire each sensor to the wheel on its own side
    (uncrossed) or the other (crossed); let more light drive the wheel faster (excite) or slower (inhibit). 2a turns
    away ('fear'), 2b turns toward and speeds into the light ('aggression'), 3a approaches and slows, facing it
    ('love'), 3b approaches and slows but turns away ('exploration'). The paths are computed by integrating the
    kinematics; nothing in the vehicles represents the light."""
    L = np.array(light, float)
    out = {}
    for name, (wiring, sign) in VEHICLES.items():
        x, y, th = start
        path = [[x, y]]
        mind = 1e9
        for _ in range(steps):
            sens = []
            for side in (+1, -1):                      # +1 = left sensor
                ang = th + side * 0.5
                sp = np.array([x + 0.25 * math.cos(ang), y + 0.25 * math.sin(ang)])
                d2 = float(((sp - L) ** 2).sum())
                sens.append(4.0 / (1.0 + d2))
            sl, sr = sens
            if wiring == "crossed":
                wl, wr = sr, sl
            else:
                wl, wr = sl, sr
            if sign == "inhibit":
                wl, wr = 2.2 - 1.2 * wl, 2.2 - 1.2 * wr
                wl, wr = max(0.0, wl), max(0.0, wr)
            else:
                wl, wr = 0.4 + wl, 0.4 + wr
            v = (wl + wr) / 2
            om = (wr - wl) / 0.5
            th += om * dt
            x += v * math.cos(th) * dt
            y += v * math.sin(th) * dt
            mind = min(mind, math.hypot(x - L[0], y - L[1]))
            path.append([round(x, 4), round(y, 4)])
        out[name] = {"path": path[::6], "min_dist": round(mind, 3), "final": [round(x, 3), round(y, 3)],
                     "final_dist": round(math.hypot(x - L[0], y - L[1]), 3)}
    return {"vehicles": out, "light": list(light), "start": list(start)}


# ---------------------------------------------------------------------------
# Eternal recurrence
# ---------------------------------------------------------------------------
def _eca(rule: int, x: np.ndarray) -> np.ndarray:
    l, r = np.roll(x, 1), np.roll(x, -1)
    idx = (l << 2) | (x << 1) | r
    table = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return table[idx]


def reversible_ca(n: int, rule: int = 90, max_steps: int = 1_000_000):
    """Fredkin's second-order trick: x(t+1) = f(x(t)) XOR x(t-1) is invertible for any rule f, so on a finite ring
    every state returns. Start from one live cell; return the recurrence time and the first rows."""
    prev = np.zeros(n, dtype=np.uint8)
    cur = np.zeros(n, dtype=np.uint8)
    cur[n // 2] = 1
    p0, c0 = prev.copy(), cur.copy()
    rows = [cur.copy()]
    for t in range(1, max_steps + 1):
        prev, cur = cur, _eca(rule, cur) ^ prev
        if t < 400:
            rows.append(cur.copy())
        if np.array_equal(prev, p0) and np.array_equal(cur, c0):
            return t, rows
    return None, rows


def recurrence(sizes=range(5, 21), rule: int = 150, show_n: int = 11) -> dict:
    """A finite deterministic world whose law can be run backwards must repeat itself (Poincare 1890, in the discrete
    case trivially): recurrence times of a reversible cellular automaton on rings of n cells. Simmel's objection
    (1907): three wheels turning at rates 1, 2 and 1/pi are never all back at the start together; the third's
    closest approach at the times the first two coincide shrinks, but never reaches zero."""
    periods = {}
    for n in sizes:
        t, _ = reversible_ca(n, rule)
        periods[n] = t
    t_show, rows = reversible_ca(show_n, rule)
    simmel = []
    best, best_k = 1.0, None
    marks = {10, 100, 1000, 10_000, 100_000}
    for k in range(1, 100_001):
        f = (k / math.pi) % 1.0
        d = min(f, 1 - f)
        if d < best:
            best, best_k = d, k
        if k in marks:
            simmel.append({"T": k, "closest": round(best, 7), "at": best_k})
    return {"rule": rule, "periods": periods, "show_n": show_n, "show_period": t_show,
            "rows": [r.tolist() for r in rows[: min(len(rows), t_show + 3 if t_show else 40)]], "simmel": simmel}


# ---------------------------------------------------------------------------
# The hermeneutic circle (an analogy)
# ---------------------------------------------------------------------------
SENSES = {"bank": ("river", "money"), "current": ("river", "money"), "deposit": ("river", "money"),
          "branch": ("river", "money"), "fish": ("river",), "boat": ("river",), "reeds": ("river",),
          "loan": ("money",), "cash": ("money",), "interest": ("money",)}
TEXTS = {"the boatman's text": ["bank", "current", "fish", "deposit", "boat", "branch", "reeds"],
         "a text that cannot answer back": ["bank", "current", "deposit", "branch"],
         "a mixed text": ["bank", "fish", "current", "loan", "deposit"]}


def hermeneutic(prejudices=(0.1, 0.9), iters: int = 12) -> dict:
    """Part and whole: the reading of each ambiguous word depends on what the whole text is about, and what the text
    is about is estimated from the readings of its words. Start from a prejudice (the probability that the text is
    about the river), read the parts in its light, re-estimate the whole, and repeat. A text with enough unambiguous
    words corrects any prejudice; a wholly ambiguous one cannot answer back, and leaves the prejudice as it was."""
    out = {}
    for name, words in TEXTS.items():
        runs = []
        for p in prejudices:
            th = p
            traj = [round(th, 4)]
            for _ in range(iters):
                post = []
                for w in words:
                    s = SENSES[w]
                    lr = (th if "river" in s else 0.0) / len(s) if len(s) else 0
                    lm = ((1 - th) if "money" in s else 0.0) / len(s)
                    post.append(lr / (lr + lm) if lr + lm > 0 else 0.5)
                th = float(np.mean(post))
                traj.append(round(th, 4))
            runs.append({"prejudice": p, "trajectory": traj, "final": traj[-1]})
        out[name] = {"words": words, "runs": runs}
    return {"texts": out, "iters": iters}


# ---------------------------------------------------------------------------
# Saussure in geometry: rotation and Procrustes
# ---------------------------------------------------------------------------
def procrustes(k: int = 6, anchors: int = 8, seed: int = 1916) -> dict:
    """The structuralist claim, in a vector space: a word's position means nothing by itself, only its relations to
    the others. Rotate Part 28's word vectors by a random orthogonal matrix: every coordinate changes, every cosine
    and every nearest neighbour stays. Orthogonal Procrustes (W = U V^T from the SVD of X^T Y) recovers the rotation
    from a few anchor words, and then carries every word to its image. Words that keep exactly the same company sit at
    the same point, and no structure can tell them apart."""
    from . import pragmatics as G
    words, idx, ppmi = G._cooc()
    U, s, _ = np.linalg.svd(ppmi)
    E = U[:, :k] * s[:k]
    E = E / np.linalg.norm(E, axis=1, keepdims=True).clip(1e-12)
    rng = np.random.default_rng(seed)
    Q, R = np.linalg.qr(rng.normal(size=(k, k)))
    Q = Q * np.sign(np.diag(R))
    F = E @ Q
    coord_corr = float(np.corrcoef(E.ravel(), F.ravel())[0, 1])
    cos_change = float(np.abs(E @ E.T - F @ F.T).max())

    def nn(M, w):
        i = idx[w]
        sims = np.round(M @ M[i], 9)
        order = np.lexsort((np.arange(len(words)), -sims))
        return [words[j] for j in order if j != i][:3]

    same_nn = all(nn(E, w) == nn(F, w) for w in words)
    pick = random.Random(seed).sample(words, anchors)
    X = np.array([E[idx[w]] for w in pick])
    Y = np.array([F[idx[w]] for w in pick])
    u, _, vt = np.linalg.svd(X.T @ Y)
    W = u @ vt
    resid = float(np.abs(W - Q).max())
    map_error = float(np.abs(E @ W - F).max())
    pos = {}
    for w in words:
        pos.setdefault(tuple(np.round(E[idx[w]], 6)), []).append(w)
    shared = sorted([g for g in pos.values() if len(g) > 1], key=len, reverse=True)
    sample = {w: {"before": [round(float(x), 3) for x in E[idx[w]][:3]],
                  "after": [round(float(x), 3) for x in F[idx[w]][:3]]} for w in ("king", "queen")}
    return {"k": k, "words": len(words), "coord_corr": round(coord_corr, 3), "cos_change": cos_change,
            "same_nn": same_nn, "anchors": pick, "resid": resid, "map_error": map_error, "shared": shared, "sample": sample,
            "cos_king_queen": round(float(E[idx["king"]] @ E[idx["queen"]]), 4)}


# ---------------------------------------------------------------------------
# Foucault and Goodhart: a threshold that people optimize against
# ---------------------------------------------------------------------------
def gaming(n: int = 20000, tau: float = 0.5, budget: float = 0.4, seed: int = 1975) -> dict:
    """A score x is used to sort people: those with x >= tau are accepted. Honestly, x equals a person's underlying
    quality q. Once the threshold is known, everyone within `budget` below it moves to exactly tau. The population
    piles up at the norm, and the score stops tracking quality: the share of the accepted who truly have q >= tau
    falls."""
    rng = np.random.default_rng(seed)
    q = rng.normal(size=n)
    x = q.copy()
    movers = (q < tau) & (q >= tau - budget)
    x[movers] = tau
    acc0 = q >= tau
    acc1 = x >= tau
    bins = np.linspace(-3, 3, 31)
    h0, _ = np.histogram(q, bins=bins)
    h1, _ = np.histogram(x, bins=bins)
    return {"n": n, "tau": tau, "budget": budget, "movers": int(movers.sum()),
            "accepted_before": int(acc0.sum()), "accepted_after": int(acc1.sum()),
            "precision_after": round(float((q[acc1] >= tau).mean()), 4),
            "bins": bins.round(3).tolist(), "hist_before": h0.tolist(), "hist_after": h1.tolist()}


# ---------------------------------------------------------------------------
# A closed dictionary: every definition leads to other words
# ---------------------------------------------------------------------------
DICTIONARY = {
    "thing": ["being"], "being": ["existing"], "existing": ["thing"],
    "good": ["valuable"], "valuable": ["worthy"], "worthy": ["good"],
    "sign": ["meaning"], "meaning": ["word"], "word": ["sign", "thing"],
    "object": ["thing", "seen"], "seen": ["eye", "thing"], "eye": ["body", "thing"], "body": ["thing", "living"],
    "living": ["being", "thing"], "right": ["good", "true"], "true": ["real", "thing"], "real": ["existing", "thing"],
    "fact": ["true", "thing"],
}


def _acyclic(nodes, edges) -> bool:
    indeg = {v: 0 for v in nodes}
    for a in nodes:
        for b in edges.get(a, []):
            if b in indeg:
                indeg[b] += 1
    todo = [v for v in nodes if indeg[v] == 0]
    seen = 0
    while todo:
        v = todo.pop()
        seen += 1
        for b in edges.get(v, []):
            if b in indeg:
                indeg[b] -= 1
                if indeg[b] == 0:
                    todo.append(b)
    return seen == len(nodes)


def dictionary(d=None) -> dict:
    """Follow the definitions of a small closed dictionary: every chain stays inside it and returns to a word already
    met. To break every circle, some words must get their meaning from outside the dictionary (Harnad 1990): the
    smallest such set is a minimum feedback vertex set of the definition graph, found here by exhaustive search."""
    d = DICTIONARY if d is None else d
    words = sorted(d)
    chains = {}
    for w in words:
        path, cur = [w], w
        while True:
            cur = d[cur][0]
            if cur in path:
                path.append(cur)
                break
            path.append(cur)
        chains[w] = path
    best = None
    for r in range(1, len(words) + 1):
        for S in itertools.combinations(words, r):
            rest = [w for w in words if w not in S]
            if _acyclic(rest, d):
                best = list(S)
                break
        if best:
            break
    n_min = len(best)
    count = sum(1 for S in itertools.combinations(words, n_min) if _acyclic([w for w in words if w not in S], d))
    return {"words": len(words), "edges": sum(len(v) for v in d.values()), "chains": chains, "grounding": best,
            "grounding_size": n_min, "n_minimum_sets": count, "dictionary": d}
