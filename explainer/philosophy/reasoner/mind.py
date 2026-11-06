"""Mind and machine, built (Part 30).

* Functionalism: one machine table for a 'pain role', realized in two substrates (a threshold network and a hydraulic
  tank), running in lockstep: behaviour identical by construction, physical states different.
* The Chinese room: a rulebook that answers questions about a restaurant story by matching symbols, perfect on a narrow
  test and helpless outside it.
* Blockhead (Block 1981): the size of a lookup table that could hold up its end of a conversation.
* Supervenience, weak, strong and global, checked on small sets of worlds.
* The exclusion argument as a Price List (in compute), and Conway's Life: a glider gun firing, and a glider's speed
  found only by running it (Bedau's weak emergence).
* Dretske: the information a gauge carries about a tank, and why misrepresentation is hard for it.
* Systematicity: a compositional interpreter against a lookup table on held-out commands.
* Decodable is not used: a linear probe reads a variable the network ignores.
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np

# ---------------------------------------------------------------------------
# Functionalism: one role, two realizers
# ---------------------------------------------------------------------------
STATES = ["calm", "hurt", "soothed"]
INPUTS = ["bump", "nothing", "aspirin"]
# machine table: (state, input) -> list of (probability, next state, output)
TABLE = {
    ("calm", "bump"): [(0.9, "hurt", "say ouch"), (0.1, "calm", "carry on")],
    ("calm", "nothing"): [(1.0, "calm", "carry on")],
    ("calm", "aspirin"): [(1.0, "calm", "carry on")],
    ("hurt", "bump"): [(1.0, "hurt", "say ouch")],
    ("hurt", "nothing"): [(0.7, "hurt", "wince"), (0.3, "calm", "carry on")],
    ("hurt", "aspirin"): [(0.8, "soothed", "sigh"), (0.2, "hurt", "wince")],
    ("soothed", "bump"): [(0.5, "hurt", "say ouch"), (0.5, "soothed", "carry on")],
    ("soothed", "nothing"): [(0.6, "calm", "carry on"), (0.4, "soothed", "carry on")],
    ("soothed", "aspirin"): [(1.0, "soothed", "carry on")],
}


def _choose(options, u):
    acc = 0.0
    for p, nxt, out in options:
        acc += p
        if u < acc:
            return nxt, out
    return options[-1][1], options[-1][2]


class NeuralRealizer:
    """The role in a 'neural' substrate: the state is a one-hot vector over three units, the input another, and a
    layer of threshold units (one per table entry and outcome) fires for exactly the matching entry."""

    def __init__(self):
        self.v = np.array([1, 0, 0])           # calm
        rows = []
        for (s, i), opts in TABLE.items():
            lo = 0.0
            for p, nxt, out in opts:
                rows.append((STATES.index(s), INPUTS.index(i), lo, lo + p, STATES.index(nxt), out))
                lo += p
        self.units = rows

    def step(self, inp, u):
        x = np.zeros(3)
        x[INPUTS.index(inp)] = 1
        for si, ii, lo, hi, nxt, out in self.units:
            drive = self.v[si] + x[ii] + (1 if lo <= u < hi else 0)
            if drive >= 3:                      # a threshold unit: all three conditions
                self.v = np.eye(3, dtype=int)[nxt]
                return out
        raise RuntimeError("no unit fired")

    def physical(self):
        return "units " + "".join(str(int(b)) for b in self.v)


class HydraulicRealizer:
    """The same role in water: the state is the level of a tank (0, 2 or 1 litres for calm, hurt, soothed), and the
    table is a set of valves keyed to levels and to the input pipe."""
    LEVEL = {"calm": 0.0, "hurt": 2.0, "soothed": 1.0}

    def __init__(self):
        self.level = 0.0

    def step(self, inp, u):
        state = {v: k for k, v in self.LEVEL.items()}[self.level]
        nxt, out = _choose(TABLE[(state, inp)], u)
        self.level = self.LEVEL[nxt]
        return out

    def physical(self):
        return f"{self.level:.0f} litres"


def realizers(steps: int = 1000, seed: int = 1967) -> dict:
    """Putnam (1967): pain is a functional state, multiply realizable. Feed both realizers the same 1000 inputs and the
    same random draws: their outputs agree at every step, though their physical states never look alike."""
    rng = random.Random(seed)
    n, h = NeuralRealizer(), HydraulicRealizer()
    agree, trace = 0, []
    counts = {}
    for t in range(steps):
        inp = rng.choices(INPUTS, weights=[0.3, 0.5, 0.2])[0]
        u = rng.random()
        a, b = n.step(inp, u), h.step(inp, u)
        agree += a == b
        counts[a] = counts.get(a, 0) + 1
        if t < 40:
            trace.append({"t": t, "input": inp, "neural": n.physical(), "hydraulic": h.physical(), "output": a})
    return {"steps": steps, "agree": agree, "trace": trace, "outputs": counts, "table": len(TABLE),
            "entries": sum(len(v) for v in TABLE.values())}


# ---------------------------------------------------------------------------
# The Chinese room: a rulebook
# ---------------------------------------------------------------------------
STORY = "一个男人走进餐馆，点了一个汉堡。汉堡端上来时烤焦了。他很生气，没付钱就走了。"
RULES = [  # (pattern of symbols, answer of symbols)
    ("吃", "没有。"),                   # did he eat ...?
    ("付钱", "没有。"),                 # did he pay?
    ("点了什么", "一个汉堡。"),          # what did he order?
    ("点", "汉堡。"),
    ("烤焦", "是的。"),                 # was it burnt?
    ("生气", "是的，他很生气。"),        # was he angry?
    ("去哪", "餐馆。"),                 # where did he go?
    ("谁", "一个男人。"),                # who?
]
NARROW = [
    ("他吃了汉堡吗？", "没有。"), ("他付钱了吗？", "没有。"), ("他点了什么？", "一个汉堡。"),
    ("汉堡烤焦了吗？", "是的。"), ("他生气了吗？", "是的，他很生气。"), ("他去哪了？", "餐馆。"),
    ("谁走进了餐馆？", "一个男人。"), ("他点了汉堡吗？", "汉堡。"),
]
WIDE = [("你喜欢汉堡吗？", None), ("今天天气怎么样？", None), ("他为什么不吃？", None), ("你是谁？", None)]


def rulebook() -> dict:
    """Searle (1980): a man who knows no Chinese follows a rulebook that matches the shapes of incoming symbols and
    copies out others. On a narrow test about one story it is perfect; asked anything else, its first matching rule
    gives a confident wrong answer, or no rule matches at all."""
    def answer(q):
        for pat, ans in RULES:
            if pat in q:
                return ans, pat
        return None, None

    narrow = []
    for q, want in NARROW:
        a, pat = answer(q)
        narrow.append({"q": q, "answer": a, "rule": pat, "right": a == want})
    wide = []
    for q, _ in WIDE:
        a, pat = answer(q)
        wide.append({"q": q, "answer": a, "rule": pat})
    return {"story": STORY, "rules": len(RULES), "narrow": narrow, "narrow_right": sum(r["right"] for r in narrow),
            "wide": wide, "wide_unmatched": sum(r["answer"] is None for r in wide)}


# ---------------------------------------------------------------------------
# Blockhead
# ---------------------------------------------------------------------------
def blockhead(minutes=(1, 10, 60), chars_per_minute: int = 300, alphabet: int = 27) -> dict:
    """Block (1981): a machine that stores, for every possible conversation so far, a sensible next reply would pass any
    test of that length. Its table needs an entry for every string the judge could type: alphabet^length. Compare
    with roughly 10^80 atoms in the observable universe."""
    rows = []
    for m in minutes:
        n = m * chars_per_minute
        rows.append({"minutes": m, "chars": n, "log10_entries": round(n * math.log10(alphabet), 1)})
    return {"rows": rows, "alphabet": alphabet, "chars_per_minute": chars_per_minute, "log10_atoms": 80}


# ---------------------------------------------------------------------------
# Supervenience
# ---------------------------------------------------------------------------
def _weak(worlds):
    for w in worlds:
        for (a, (pa, ma)), (b, (pb, mb)) in itertools.combinations(w.items(), 2):
            if pa == pb and ma != mb:
                return False
    return True


def _strong(worlds):
    seen = {}
    for w in worlds:
        for _, (p, m) in w.items():
            if p in seen and seen[p] != m:
                return False
            seen[p] = m
    return True


def _global(worlds):
    seen = {}
    for w in worlds:
        phys = tuple(sorted((k, p) for k, (p, m) in w.items()))
        ment = tuple(sorted((k, m) for k, (p, m) in w.items()))
        if phys in seen and seen[phys] != ment:
            return False
        seen[phys] = ment
    return True


WORLD_SETS = {
    "A": [{"a": ("P1", "M1"), "b": ("P1", "M1")}, {"a": ("P1", "M2"), "b": ("P1", "M2")}],
    "B": [{"a": ("P1", "M1"), "b": ("P1", "M2")}, {"a": ("P2", "M1"), "b": ("P2", "M1")}],
    "C": [{"a": ("P1", "M1"), "b": ("P2", "M2")}, {"a": ("P2", "M2"), "b": ("P2", "M2")}],
}


def supervenience(sets=None) -> dict:
    """Kim's three supervenience relations of the mental (M) on the physical (P), checked on small sets of worlds.
    Weak: within any world, physical twins are mental twins. Strong: across all worlds. Global: worlds alike in
    their whole physical distribution are alike mentally. Set A: weak but not strong or global; B: global but not
    weak; C: all three."""
    sets = WORLD_SETS if sets is None else sets
    out = {}
    for k, ws in sets.items():
        out[k] = {"weak": _weak(ws), "strong": _strong(ws), "global": _global(ws), "worlds": ws}
    return out


# ---------------------------------------------------------------------------
# Conway's Life
# ---------------------------------------------------------------------------
GOSPER = ["........................O...........", "......................O.O...........",
          "............OO......OO............OO", "...........O...O....OO............OO",
          "OO........O.....O...OO..............", "OO........O...O.OO....O.O...........",
          "..........O.....O.......O...........", "...........O...O....................",
          "............OO......................"]
GLIDER = [".O.", "..O", "OOO"]


def _life_step(live, w, h):
    from collections import Counter
    c = Counter((x + dx, y + dy) for x, y in live for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    return {p for p, n in c.items() if (n == 3 or (n == 2 and p in live)) and 0 <= p[0] < w and 0 <= p[1] < h}


def _pattern(rows, ox=0, oy=0):
    return {(ox + x, oy + y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == "O"}


def life(gens: int = 150, w: int = 64, h: int = 46, frames_every: int = 3) -> dict:
    """Conway's Game of Life (1970): a cell is born with exactly three live neighbours and survives with two or three.
    Gosper's glider gun (1970) fires a glider every 30 generations. A lone glider moves one cell diagonally every 4
    generations: a fact about the rule that, in general, only running it reveals (Bedau 1997). Cells leaving the
    board are dropped."""
    live = _pattern(GOSPER, 1, 1)
    frames, pops = [], []
    for g in range(gens + 1):
        if g % frames_every == 0:
            frames.append(sorted(live))
        pops.append(len(live))
        live = _life_step(live, w, h)
    # count gliders: cells outside the gun's bounding box, divided by 5
    gun_box = (0, 0, 38, 12)
    outside = [p for p in frames[-1] if not (gun_box[0] <= p[0] <= gun_box[2] and gun_box[1] <= p[1] <= gun_box[3])]
    # a lone glider's speed
    g0 = _pattern(GLIDER, 5, 5)
    cur = set(g0)
    for _ in range(4):
        cur = _life_step(cur, 100, 100)
    shift = {(x - 1, y - 1) for x, y in cur} == g0
    return {"gens": gens, "w": w, "h": h, "frames_every": frames_every, "frames": frames, "pop": pops,
            "gliders_out": len(outside) // 5, "glider_c4": shift}


# ---------------------------------------------------------------------------
# Dretske: information and misrepresentation
# ---------------------------------------------------------------------------
def gauge(levels=4, noises=(0.0, 0.1, 0.3, 0.6)) -> dict:
    """Dretske (1981): a signal carries the information that s is F if P(s is F | signal) = 1. A fuel gauge with four
    marks: with no noise the reading carries log2 4 = 2 bits about the tank; with noise it carries less, and no single
    reading carries the information that the tank is at any level, so information alone cannot say what the gauge
    represents when it is wrong."""
    rows = []
    for e in noises:
        # with prob 1-e the needle shows the true level; otherwise a neighbouring mark
        M = np.zeros((levels, levels))
        for s in range(levels):
            nb = [t for t in (s - 1, s + 1) if 0 <= t < levels]
            M[s, s] += 1 - e
            for t in nb:
                M[s, t] += e / len(nb)
        joint = M / levels
        pr = joint.sum(0)
        with np.errstate(divide="ignore", invalid="ignore"):
            mi = np.nansum(np.where(joint > 0, joint * np.log2(joint / ((1 / levels) * pr[None, :])), 0))
        post = joint / pr[None, :]
        certain = int((post.max(0) >= 1 - 1e-12).sum())
        rows.append({"noise": e, "bits": round(float(mi), 4), "readings_certain": certain})
    return {"levels": levels, "max_bits": math.log2(levels), "rows": rows}


# ---------------------------------------------------------------------------
# Systematicity
# ---------------------------------------------------------------------------
PRIMS = {"walk": "WALK", "run": "RUN", "look": "LOOK", "jump": "JUMP"}
MODS = {"": 1, " twice": 2, " thrice": 3}


def _interpret(cmd):
    if " and " in cmd:
        a, b = cmd.split(" and ")
        return _interpret(a) + _interpret(b)
    for m, k in sorted(MODS.items(), key=lambda kv: -len(kv[0])):
        if m and cmd.endswith(m):
            return _interpret(cmd[: -len(m)]) * k
    return [PRIMS[cmd]]


def systematicity() -> dict:
    """Fodor and Pylyshyn (1988): whoever can think 'John loves Mary' can think 'Mary loves John'. A SCAN-like command
    language (Lake and Baroni 2018): 'jump' is seen only alone in training. A compositional interpreter, given the
    meaning of 'jump', handles every held-out command with it; a lookup table of the training pairs handles none."""
    cmds = []
    for p in PRIMS:
        for m in MODS:
            cmds.append(p + m)
    cmds += [a + " and " + b for a in list(cmds) for b in list(cmds)]
    train = [c for c in cmds if "jump" not in c] + ["jump"]
    test = [c for c in cmds if "jump" in c and c != "jump"]
    table = {c: _interpret(c) for c in train}
    table_right = sum(table.get(c) == _interpret(c) for c in test)
    comp_right = sum(_interpret(c) == _interpret(c) for c in test)
    return {"train": len(train), "test": len(test), "table_right": table_right, "comp_right": comp_right,
            "example": {"cmd": "jump twice and look thrice", "out": _interpret("jump twice and look thrice")}}


# ---------------------------------------------------------------------------
# Decodable is not used
# ---------------------------------------------------------------------------
def probe_vs_use(n: int = 4000, hidden: int = 32, seed: int = 2021) -> dict:
    """A network's hidden layer h = relu(W [x, y] + b) mixes two binary inputs; its readout uses only y. A linear probe
    reads x off h perfectly. Remove the probe's direction from h (amnesic probing, Elazar et al. 2021; iterative
    nullspace projection, Ravfogel et al. 2020) until a freshly trained probe is at chance: the readout of y, which
    never used x, is still perfect. Decodable is not the same as used."""
    rng = np.random.default_rng(seed)
    X = rng.integers(0, 2, size=(n, 2)).astype(float)
    W = rng.normal(size=(2, hidden))
    b = rng.normal(scale=0.3, size=hidden)
    H = np.maximum(0, (2 * X - 1) @ W + b)
    tr, te = slice(0, n // 2), slice(n // 2, n)
    Hc = H - H[tr].mean(0)
    one = np.ones((n, 1))
    wy, *_ = np.linalg.lstsq(np.c_[Hc[tr], one[tr]], 2 * X[tr, 1] - 1, rcond=None)

    def task(Hm):
        return float(((np.c_[Hm, one] @ wy)[te] > 0).astype(float).__eq__(X[te, 1]).mean())

    def probe(Hm):
        w, *_ = np.linalg.lstsq(np.c_[Hm[tr], one[tr]], 2 * X[tr, 0] - 1, rcond=None)
        return float((((np.c_[Hm, one] @ w)[te] > 0) == (X[te, 0] > 0.5)).mean()), w[:-1]

    rows, P = [], np.eye(hidden)
    for r in range(hidden):
        acc, w = probe(Hc @ P)
        rows.append({"removed": r, "probe_x": round(acc, 4), "task_y": round(task(Hc @ P), 4)})
        if acc < 0.55:
            break
        d = P @ w
        d /= np.linalg.norm(d)
        P = P @ (np.eye(hidden) - np.outer(d, d))
    return {"hidden": hidden, "n_test": n - n // 2, "rows": rows}


# ---------------------------------------------------------------------------
# Ramsey-Lewis: counting the occupants of a role
# ---------------------------------------------------------------------------
def _support(table, inputs):
    """The folk theory as platitudes: for each mental state and input, the set of possible (next state, output)."""
    return {(s, i): frozenset((n, o) for p, n, o in opts if p > 0) for (s, i), opts in table.items() if i in inputs}


def _brain():
    """A 'brain' of seven microstates: calm is realized by c1 or c2, hurt by h1, h2 or h3, soothed by s1 or s2; each
    microstate's transitions go to particular microstates of the right kind (which ones varies)."""
    blocks = {"calm": ["c1", "c2"], "hurt": ["h1", "h2", "h3"], "soothed": ["s1", "s2"]}
    trans = {}
    for s, micros in blocks.items():
        for k, m in enumerate(micros):
            for i in INPUTS:
                trans[(m, i)] = frozenset((blocks[n][(k + j) % len(blocks[n])], o)
                                          for j, (p, n, o) in enumerate(TABLE[(s, i)]) if p > 0)
    return sorted(m for v in blocks.values() for m in v), trans


def _thermostat():
    """A three-state thermostat (off, warming, on), fed the same inputs and giving outputs from the same repertoire,
    whose dynamics do not fit the role under any assignment."""
    T = {("off", "bump"): {("warming", "carry on")}, ("warming", "bump"): {("on", "say ouch")},
         ("on", "bump"): {("on", "say ouch")}, ("off", "nothing"): {("off", "carry on")},
         ("warming", "nothing"): {("off", "carry on")}, ("on", "nothing"): {("warming", "wince")},
         ("off", "aspirin"): {("off", "carry on")}, ("warming", "aspirin"): {("off", "sigh")},
         ("on", "aspirin"): {("warming", "sigh")}}
    return ["off", "warming", "on"], {k: frozenset(v) for k, v in T.items()}


def _partitions(items, k):
    if k == 0:
        if not items:
            yield []
        return
    if len(items) < k:
        return
    first, rest = items[0], items[1:]
    for p in _partitions(rest, k - 1):
        yield [[first]] + p
    for p in _partitions(rest, k):
        for j in range(len(p)):
            yield p[:j] + [[first] + p[j]] + p[j + 1:]


def _realizations(micros, trans, theory, inputs):
    """Every way of assigning the mental terms to the blocks of a partition of the microstates (each term to one
    block, the blocks covering every state) that makes the Ramsey sentence of the theory true: from every microstate
    in a term's block, on each input, the possible (block of next state, output) pairs are exactly the theory's."""
    terms = STATES
    found, candidates = [], 0
    for part in _partitions(list(micros), len(terms)):
        for perm in itertools.permutations(terms):
            candidates += 1
            of = {m: perm[b] for b, block in enumerate(part) for m in block}
            ok = all(frozenset((of[n], o) for n, o in trans[(m, i)]) == theory[(of[m], i)]
                     for m in micros for i in inputs)
            if ok:
                found.append({t: sorted(part[perm.index(t)]) for t in terms})
    return candidates, found


def ramsey() -> dict:
    """Lewis (1972): pain is the occupant of the pain role in the Ramsey sentence of folk psychology,
    there exist x, y, z such that T(x, y, z). On three systems: the 'brain' has exactly one realization of the full
    theory among 1806 candidates, with pain a disjunction of three microstates; the tank has one among 6; a
    three-state thermostat none among 6. A weaker theory, with the aspirin platitudes left out, still has a unique occupant in the
    brain; with only the bump platitudes it no longer does."""
    out = {}
    full = list(INPUTS)
    systems = {"brain": _brain(), "tank": (["0 L", "1 L", "2 L"], None), "thermostat": _thermostat()}
    lv = {"0 L": "calm", "2 L": "hurt", "1 L": "soothed"}
    tank_trans = {}
    for m, s in lv.items():
        for i in INPUTS:
            tank_trans[(m, i)] = frozenset(({v: k for k, v in lv.items()}[n], o) for p, n, o in TABLE[(s, i)] if p > 0)
    systems["tank"] = (["0 L", "1 L", "2 L"], tank_trans)
    for name, (micros, trans) in systems.items():
        cand, found = _realizations(micros, trans, _support(TABLE, full), full)
        out[name] = {"states": len(micros), "candidates": cand, "realizations": len(found), "found": found}
    weak = {}
    for label_, inputs in (("without aspirin", ["bump", "nothing"]), ("bumps only", ["bump"])):
        micros, trans = systems["brain"]
        cand, found = _realizations(micros, trans, _support(TABLE, inputs), inputs)
        weak[label_] = {"candidates": cand, "realizations": len(found), "found": found[:4]}
    out["weak"] = weak
    return out


# ---------------------------------------------------------------------------
# Dennett's real patterns
# ---------------------------------------------------------------------------
def _h2(p):
    return 0.0 if p <= 0 or p >= 1 else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def real_patterns(noises=(0.0, 0.01, 0.05, 0.1, 0.25, 0.5), rows: int = 10, cols: int = 90, seed: int = 1991) -> dict:
    """Dennett (1991), 'Real Patterns': frames of a bar code (ten black dots, ten white, repeated) with each dot
    flipped with some probability. A pattern is real if describing the frame by the pattern plus its exceptions is
    shorter than the bit map. Two-part code: the pattern (fixed, a few bits) plus the exceptions (log2 C(n, k) bits for
    k flips among n dots); and a check with an off-the-shelf compressor (lzma) over a long run of frames. At 50% noise
    the pattern saves nothing: there is no pattern."""
    import lzma
    rng = np.random.default_rng(seed)
    n = rows * cols
    base = np.array([[1 if (c // 10) % 2 == 0 else 0 for c in range(cols)] for _ in range(rows)])
    out = []
    for p in noises:
        flips = rng.random((rows, cols)) < p
        frame = (base ^ flips).astype(int)
        k = int(flips.sum())
        exc = math.lgamma(n + 1) / math.log(2) - (math.lgamma(k + 1) + math.lgamma(n - k + 1)) / math.log(2)
        two_part = exc + math.log2(n + 1) + 20       # k itself, and the pattern (period and phase)
        # empirical: 200 frames, one byte per dot packed as bits
        long = (np.tile(base, (200, 1)) ^ (rng.random((200 * rows, cols)) < p)).astype(np.uint8)
        packed = np.packbits(long.ravel()).tobytes()
        ratio = len(lzma.compress(packed, preset=9)) * 8 / long.size
        out.append({"noise": p, "frame": frame.tolist(), "flips": k, "two_part_bits": round(two_part, 1),
                    "bitmap_bits": n, "ratio_two_part": round(two_part / n, 3), "entropy": round(_h2(p), 3),
                    "ratio_lzma": round(ratio, 3), "predict": round(1 - p, 3)})
    return {"rows": rows, "cols": cols, "frames": out}


# ---------------------------------------------------------------------------
# Proportional causes: Yablo's pigeon
# ---------------------------------------------------------------------------
SHADES = [("scarlet", True), ("crimson", True), ("maroon", True), ("teal", False), ("navy", False), ("olive", False)]


def proportional(hit: float = 0.95, false_alarm: float = 0.05) -> dict:
    """Yablo (1992); Woodward (2003); List and Menzies (2009). Sophie, a pigeon, is trained to peck at red. The
    physical variable is the exact shade; 'red' supervenes on it. Under interventions (each value set with equal
    probability), compare candidate causes of pecking: how much the cause's two settings differ in their effect, the
    information it carries about pecking, and how many bits of the cause it takes. 'Red' makes the whole difference
    with one bit; 'scarlet' makes less of a difference; the exact shade makes the same difference as red with more
    bits than it needs. Realization-insensitivity: had the red been a different red, Sophie would still have pecked."""
    peck = {s: (hit if r else false_alarm) for s, r in SHADES}

    def info(groups):
        # mutual information between a cause variable (a partition of the shades, values chosen uniformly) and pecking
        py = sum(peck[s] for s, _ in SHADES) / len(SHADES)
        I, Hc = 0.0, 0.0
        for g in groups:
            q = 1 / len(groups)
            pg = sum(peck[s] for s in g) / len(g)
            Hc -= q * math.log2(q)
            for y, pyv in ((1, pg), (0, 1 - pg)):
                marg = py if y else 1 - py
                if pyv > 0:
                    I += q * pyv * math.log2(pyv / marg)
        return I, Hc

    reds = [s for s, r in SHADES if r]
    others = [s for s, r in SHADES if not r]
    cands = {
        "red": [reds, others],
        "scarlet": [["scarlet"], [s for s, _ in SHADES if s != "scarlet"]],
        "the exact shade": [[s] for s, _ in SHADES],
        "coloured": [[s for s, _ in SHADES]],
    }
    rows = []
    for name, groups in cands.items():
        I, Hc = info(groups)
        if len(groups) == 2:
            a = sum(peck[s] for s in groups[0]) / len(groups[0])
            b = sum(peck[s] for s in groups[1]) / len(groups[1])
            diff = round(a - b, 3)
        else:
            diff = None
        rows.append({"cause": name, "values": len(groups), "difference": diff, "info": round(I, 4),
                     "cause_bits": round(Hc, 4)})
    insens = {s: peck[s] for s in reds}
    return {"peck": peck, "rows": rows, "insensitive": insens, "hit": hit, "false_alarm": false_alarm}


def glider_law(gens: int = 600, size: int = 400) -> dict:
    """A law at the level of gliders, found by running the rules: on a board large enough for every glider to fly
    free, Gosper's gun has exactly 36 + 5k live cells at generation 30k (k = 0 ... 20), and k - 1 gliders clear of
    the gun; between those generations the count wobbles."""
    live = _pattern(GOSPER, 1, 1)
    pops, rows = [], []
    for g in range(gens + 1):
        pops.append(len(live))
        if g % 30 == 0:
            out = sum(1 for p in live if not (0 <= p[0] <= 38 and 0 <= p[1] <= 12))
            rows.append({"gen": g, "pop": len(live), "outside": out})
        live = _life_step(live, size, size)
    holds = sum(r["pop"] == 36 + 5 * (r["gen"] // 30) for r in rows)
    return {"gens": gens, "pop": pops, "rows": rows, "holds": holds, "points": len(rows),
            "min_pop": min(pops), "max_pop": max(pops)}
