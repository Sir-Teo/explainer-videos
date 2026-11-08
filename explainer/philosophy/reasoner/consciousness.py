"""Consciousness, built (Part 31).

* A toy global workspace (Baars; Dehaene): a recurrent unit that either decays or 'ignites' into a self-sustaining
  broadcast, and the masking curve it produces: report is all-or-none and jumps at a critical stimulus-mask delay.
* A simplified integrated information (labelled as such): effective information across the minimum-information
  bipartition, in the style of IIT 2.0 (Balduzzi and Tononi 2008), computed exhaustively for small logic-gate
  networks; not IIT 4.0's Phi.
* Aaronson's objection (2014): regular grids of XOR gates score ever higher on such measures, with no plausible
  experience.
* Active inference (Friston): a T-maze agent that minimizes expected free energy, looking at a cue before it moves.
"""

from __future__ import annotations

import itertools
import math
import random

import numpy as np

# ---------------------------------------------------------------------------
# A global workspace: ignition and masking
# ---------------------------------------------------------------------------
def _run_workspace(strength, soa, dt=1.0, T=600, gain=0.08, thresh=55.0, recur=1.6, tau=50.0, noise=0.0,
                   rng=None):
    """One trial: a stimulus of given strength drives the workspace unit from t = 0 until the mask arrives at `soa`
    ms (the mask cuts the input). Activity w obeys tau dw/dt = -w + 100 sigmoid(gain (input + recur w - thresh)),
    a bistable loop: below threshold it relaxes; above it, recurrent excitation sustains a high, broadcast state."""
    w = 0.0
    trace = []
    for k in range(int(T / dt)):
        t = k * dt
        inp = strength if t < soa else 0.0
        drive = gain * (inp + recur * w - thresh)
        target = 100.0 / (1.0 + math.exp(-drive))
        w += dt / tau * (target - w)
        if noise and rng is not None:
            w += noise * rng.normal() * math.sqrt(dt)
            w = max(w, 0.0)
        trace.append(w)
    return trace


def workspace(soas=tuple(range(10, 121, 10)), trials: int = 200, strength: float = 30.0, noise: float = 0.6,
              seed: int = 2001, probe_soa: int = 50) -> dict:
    """Seen or not seen, as a function of the delay between a stimulus and the mask that follows it. Each trial adds
    noise; a trial counts as 'seen' if the workspace is in its high state 400 ms after stimulus onset. The curve is
    sigmoidal and steep: conscious access as ignition (Dehaene, Sergent and Changeux 2003; Del Cul et al. 2007)."""
    rng = np.random.default_rng(seed)
    rows = []
    for soa in soas:
        seen = 0
        for _ in range(trials):
            tr = _run_workspace(strength, soa, noise=noise, rng=rng)
            seen += int(tr[400] > 50)
        rows.append({"soa": soa, "seen": seen, "trials": trials})
    # at the threshold delay, late activity is bimodal: ignition is all or none
    late = [_run_workspace(strength, probe_soa, noise=noise, rng=rng)[400] for _ in range(trials)]
    hist = np.histogram(np.clip(late, 0, 109.9), bins=11, range=(0, 110))[0].tolist()
    sub = _run_workspace(strength, 30)
    sup = _run_workspace(strength, 80)
    return {"rows": rows, "trace_sub": [round(x, 2) for x in sub[::5]], "trace_sup": [round(x, 2) for x in sup[::5]],
            "dt_trace": 5, "strength": strength, "probe_soa": probe_soa, "late_hist": hist,
            "late_low": int(sum(x < 20 for x in late)), "late_high": int(sum(x > 80 for x in late)), "trials": trials}


# ---------------------------------------------------------------------------
# A simplified integrated information
# ---------------------------------------------------------------------------
GATES = {
    "OR": lambda ins: int(any(ins)), "AND": lambda ins: int(all(ins)), "XOR": lambda ins: int(sum(ins) % 2),
    "COPY": lambda ins: int(ins[0]), "NOT": lambda ins: int(not ins[0]), "MAJ": lambda ins: int(sum(ins) * 2 > len(ins)),
}


def _step_table(gates, inputs):
    """All 2^n states -> next states, as bit arrays (row k is state k in binary, node 0 the highest bit)."""
    n = len(gates)
    states = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    nxt = np.zeros_like(states)
    for i, g in enumerate(gates):
        ins = states[:, inputs[i]]
        if g == "XOR":
            nxt[:, i] = ins.sum(axis=1) % 2
        elif g == "OR":
            nxt[:, i] = ins.max(axis=1)
        elif g == "AND":
            nxt[:, i] = ins.min(axis=1)
        elif g == "COPY":
            nxt[:, i] = ins[:, 0]
        elif g == "NOT":
            nxt[:, i] = 1 - ins[:, 0]
        elif g == "MAJ":
            nxt[:, i] = (2 * ins.sum(axis=1) > ins.shape[1]).astype(np.int8)
        else:
            raise ValueError(g)
    return states, nxt


def _codes(bits, cols):
    if not len(cols):
        return np.zeros(len(bits), dtype=np.int64)
    w = 1 << np.arange(len(cols) - 1, -1, -1)
    return (bits[:, cols].astype(np.int64) * w).sum(axis=1)


def _ei(states, nxt, x1, parts):
    """Effective information of the whole system's state x1 across a partition (Balduzzi and Tononi 2008): the KL
    divergence, in bits, between the whole's cause repertoire (a uniform prior over past states, conditioned on
    producing x1) and the product of each part's own cause repertoire (each part conditioned on its own current
    state, with inputs from outside it treated as noise)."""
    x1 = np.asarray(x1)
    whole = np.all(nxt == x1, axis=1)
    pw = whole / whole.sum()
    q = np.ones(len(states))
    for part in parts:
        part = list(part)
        m = np.all(nxt[:, part] == x1[part], axis=1)
        codes = _codes(states, part)
        rep = np.bincount(codes[m], minlength=1 << len(part)) / m.sum()
        q = q * rep[codes]
    sel = pw > 0
    if np.any(q[sel] <= 0):
        return math.inf
    return float(np.sum(pw[sel] * np.log2(pw[sel] / q[sel])))


def phi_simple(gates, inputs, x1) -> dict:
    """A simplified integrated information for a small deterministic network in state x1 (in the style of IIT 2.0,
    Balduzzi and Tononi 2008, over bipartitions only; not the measure of IIT 4.0): the effective information across
    every bipartition, normalized by the smaller part's size; Phi is the effective information across the
    bipartition where the normalized value is smallest, the minimum-information bipartition."""
    n = len(gates)
    states, nxt = _step_table(gates, inputs)
    x1 = np.asarray(x1, dtype=np.int8)
    if not np.any(np.all(nxt == x1, axis=1)):
        raise ValueError("state has no past: not reachable")
    best = None
    for r in range(1, n // 2 + 1):
        for A in itertools.combinations(range(n), r):
            B = tuple(i for i in range(n) if i not in A)
            if r == n - r and A > B:
                continue
            ei = _ei(states, nxt, x1, (A, B))
            norm = ei / min(len(A), len(B))
            if best is None or norm < best[0] - 1e-12:
                best = (norm, ei, A, B)
    return {"phi": round(best[1], 4), "mib": [list(best[2]), list(best[3])], "n": n}


def _reachable_state(gates, inputs):
    states, nxt = _step_table(gates, inputs)
    return tuple(int(v) for v in max(map(tuple, nxt.tolist())))


NETWORKS = {
    "two separate pairs": (["COPY", "COPY", "COPY", "COPY"], [[1], [0], [3], [2]]),
    "a feedforward chain": (["COPY", "COPY", "COPY", "COPY"], [[0], [0], [1], [2]]),
    "OR, AND, XOR loop": (["OR", "AND", "XOR"], [[1, 2], [0, 2], [0, 1]]),
    "a ring of four XORs": (["XOR"] * 4, [[3, 1], [0, 2], [1, 3], [2, 0]]),
}


def phi_examples() -> dict:
    """The simplified measure on four small networks, each in a reachable state: two separate pairs and a
    feedforward chain score zero; loops score above zero."""
    out = {}
    for name, (g, ins) in NETWORKS.items():
        x1 = _reachable_state(g, ins)
        r = phi_simple(g, ins, x1)
        out[name] = {"gates": g, "inputs": ins, "state": list(x1), **r}
    return out


def _torus(rows, cols):
    n = rows * cols
    ins = []
    for r in range(rows):
        for c in range(cols):
            nb = {((r + dr) % rows) * cols + (c + dc) % cols for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))}
            nb.discard(r * cols + c)
            ins.append(sorted(nb))
    return ["XOR"] * n, ins


def _expander(n, seed):
    """A random 3-regular graph (a configuration-model draw, redrawn until simple), each node an XOR of its three
    neighbours."""
    rng = random.Random(seed)
    while True:
        stubs = [v for v in range(n) for _ in range(3)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for a, b in zip(stubs[::2], stubs[1::2]):
            if a == b or (min(a, b), max(a, b)) in edges:
                ok = False
                break
            edges.add((min(a, b), max(a, b)))
        if ok:
            break
    ins = [sorted({b for a, b in edges if a == v} | {a for a, b in edges if b == v}) for v in range(n)]
    return ["XOR"] * n, ins


def _adder():
    """A 2-bit adder as a closed network: four input nodes that hold their bits (each copies itself), and four
    feedforward gates computing the sum bits and carries."""
    gates = ["COPY", "COPY", "COPY", "COPY", "XOR", "AND", "XOR", "MAJ"]
    #        a0      a1      b0      b1      s0      c0     s1     c1
    inputs = [[0], [1], [2], [3], [0, 2], [0, 2], [1, 3, 5], [1, 3, 5]]
    return gates, inputs


def aaronson(seed: int = 2014, seeds: int = 6) -> dict:
    """Aaronson (2014): Phi rewards structure that is hard to cut, whatever it computes. Under the simplified
    measure, at eight to ten nodes: a 2-bit adder, which does something useful, is feedforward and scores 0; a ring
    of XOR gates, a 2-by-5 torus of them and random 3-regular XOR expanders, which do nothing in particular, score
    more. (Aaronson proved that suitable XOR expanders have Phi growing without bound; at these sizes the
    simplified measure only shows the ordering.)"""
    rows = []
    g, ins = _adder()
    rows.append({"name": "a 2-bit adder", "n": 8, "phi": phi_simple(g, ins, _reachable_state(g, ins))["phi"]})
    g, ins = ["XOR"] * 10, [[(i - 1) % 10, (i + 1) % 10] for i in range(10)]
    rows.append({"name": "a ring of ten XORs", "n": 10, "phi": phi_simple(g, ins, _reachable_state(g, ins))["phi"]})
    g, ins = _torus(2, 5)
    rows.append({"name": "a 2-by-5 torus of XORs", "n": 10,
                 "phi": phi_simple(g, ins, _reachable_state(g, ins))["phi"]})
    vals = []
    for k in range(seeds):
        g, ins = _expander(10, seed + 1000 * k)
        vals.append(phi_simple(g, ins, _reachable_state(g, ins))["phi"])
    rows.append({"name": "random XOR expanders", "n": 10, "phi": round(float(np.mean(vals)), 3), "phis": vals})
    # the adder does add: two ticks after any state, with the inputs held, the outputs are the sum
    g, ins = _adder()
    states, nxt = _step_table(g, ins)
    w = 1 << np.arange(len(g) - 1, -1, -1)
    two = nxt[(nxt.astype(np.int64) * w).sum(axis=1)]
    ok = all(int(t[4]) + 2 * int(t[6]) + 4 * int(t[7]) == int(s0[0]) + 2 * int(s0[1]) + int(s0[2]) + 2 * int(s0[3])
             for s0, t in zip(states, two))
    return {"rows": rows, "adder_adds": bool(ok)}


def unfolding(steps: int = 3) -> dict:
    """Doerig, Schurger, Hess and Herzog (2019), the unfolding argument: any recurrent network can be unrolled into a
    feedforward one with the same input-output behaviour, and IIT gives every feedforward network Phi = 0. The OR,
    AND, XOR loop has Phi = 1 under the simplified measure; unrolled for three steps (a layer holding the start,
    then one layer per step), its last layer matches the loop's state after three steps from every one of the eight
    starts, and its Phi is 0."""
    lg, lin = NETWORKS["OR, AND, XOR loop"]
    loop_phi = phi_simple(lg, lin, _reachable_state(lg, lin))["phi"]
    gates, inputs = ["COPY"] * 3, [[0], [1], [2]]
    for t in range(steps):
        base = 3 * t
        gates += lg
        inputs += [[base + j for j in ins] for ins in lin]
    n = len(gates)
    states, nxt = _step_table(gates, inputs)
    # run the unrolled net for `steps` ticks from each start (layer 0 = start, others arbitrary 0)
    match = 0
    for start in itertools.product((0, 1), repeat=3):
        x = np.array(list(start) + [0] * (n - 3), dtype=np.int8)
        for _ in range(steps):
            x = nxt[int("".join(map(str, x.tolist())), 2)]
        loop = np.array(start, dtype=np.int8)
        ls, lnxt = _step_table(lg, lin)
        for _ in range(steps):
            loop = lnxt[int("".join(map(str, loop.tolist())), 2)]
        match += bool(np.array_equal(x[-3:], loop))
    un_phi = phi_simple(gates, inputs, _reachable_state(gates, inputs))["phi"]
    return {"loop_phi": loop_phi, "unrolled_phi": un_phi, "nodes": n, "steps": steps, "match": match}


# ---------------------------------------------------------------------------
# Active inference: a T-maze
# ---------------------------------------------------------------------------
def tmaze(cue_validity: float = 0.98, reward_pref: float = 3.0, hit: float = 0.98) -> dict:
    """Friston et al. (2015), simplified. The reward is in the left or the right arm, with even odds. From the
    centre the agent can go straight to an arm (arms are absorbing: it stays there), or first visit a cue whose
    signal points to the reward's side with the given validity. Each two-step policy is scored by its expected free
    energy, G = risk - epistemic value, summed over the steps: risk is minus the expected log preference for the
    outcomes (reward +3, no reward -3, in nats), and epistemic value is the expected information gain about where
    the reward is. Policies are chosen with probability proportional to exp(-G)."""
    prior = np.array([0.5, 0.5])

    def outcomes(loc, s):
        if loc == "centre":
            return {"nothing": 1.0}
        if loc == "cue":
            good, bad = ("cue says left", "cue says right") if s == 0 else ("cue says right", "cue says left")
            return {good: cue_validity, bad: 1 - cue_validity}
        there = (loc == "left" and s == 0) or (loc == "right" and s == 1)
        return {"reward": hit, "no reward": 1 - hit} if there else {"reward": 1 - hit, "no reward": hit}

    pref = {"reward": reward_pref, "no reward": -reward_pref}

    def step(loc, belief):
        po = {}
        for s_ in (0, 1):
            for o, p in outcomes(loc, s_).items():
                po[o] = po.get(o, 0.0) + belief[s_] * p
        risk = -sum(p * pref.get(o, 0.0) for o, p in po.items())
        ig, posts = 0.0, {}
        for o, p in po.items():
            post = np.array([belief[s_] * outcomes(loc, s_).get(o, 0.0) for s_ in (0, 1)])
            post = post / post.sum()
            posts[o] = (p, post)
            ig += p * sum(post[s_] * math.log(post[s_] / belief[s_]) for s_ in (0, 1) if post[s_] > 0)
        return risk, ig, posts

    def second(first, rule, belief_after):
        if first in ("left", "right"):
            return first
        if first == "centre":
            return "centre"
        cued = "left" if belief_after[0] >= belief_after[1] else "right"
        return cued if rule == "cued" else ("right" if cued == "left" else "left")

    plans = [("go left at once", "left", None), ("go right at once", "right", None),
             ("look at the cue, then the cued arm", "cue", "cued"),
             ("look at the cue, then the other arm", "cue", "other"), ("stay at the centre", "centre", None)]
    rows = []
    for name, first, rule in plans:
        r1, i1, posts = step(first, prior)
        r2 = i2 = 0.0
        for o, (p, post) in posts.items():
            rr, ii, _ = step(second(first, rule, post), post)
            r2 += p * rr
            i2 += p * ii
        rows.append({"policy": name, "risk": round(float(r1 + r2), 4), "epistemic": round(float(i1 + i2), 4),
                     "G": round(float(r1 + r2 - i1 - i2), 4)})
    z = sum(math.exp(-r["G"]) for r in rows)
    for r in rows:
        r["p"] = round(math.exp(-r["G"]) / z, 4)
    rows.sort(key=lambda r: r["G"])
    lik = np.array([cue_validity, 1 - cue_validity])        # seeing 'cue says left'

    def F(q):
        q = np.asarray(q, float)
        return float(sum(q[k] * (math.log(q[k]) - math.log(prior[k] * lik[k])) for k in (0, 1) if q[k] > 0))
    exact = prior * lik / (prior * lik).sum()
    return {"policies": rows, "best": rows[0]["policy"], "F_exact": round(F(exact), 4),
            "F_prior": round(F(prior), 4), "F_wrong": round(F([0.1, 0.9]), 4),
            "surprise": round(-math.log((prior * lik).sum()), 4), "posterior": [round(float(x), 4) for x in exact]}


# ---------------------------------------------------------------------------
# Higher-order theories: metacognition in signal detection
# ---------------------------------------------------------------------------
def metacognition(d: float = 1.5, trials: int = 20000, seed: int = 1997) -> dict:
    """A first-order signal-detection observer (d' = 1.5) says 'present' when its internal signal exceeds zero; a
    second-order monitor reads the same signal with its own noise and turns it into confidence. With a good monitor,
    confidence tracks being right (type-2 area under the ROC well above a half); in a 'blindsight' observer the
    monitor's noise swamps it: the same first-order accuracy, confidence at chance (Weiskrantz 1986; Lau and
    Rosenthal 2011; Lau 2022's perceptual reality monitoring, in miniature)."""
    rng = np.random.default_rng(seed)
    stim = rng.integers(0, 2, trials)
    x = rng.normal(0, 1, trials) + np.where(stim == 1, d / 2, -d / 2)
    say = (x > 0).astype(int)
    correct = say == stim

    def auroc2(conf):
        c, w = conf[correct], conf[~correct]
        order = np.argsort(np.concatenate([c, w]))
        ranks = np.empty(len(order))
        ranks[order] = np.arange(1, len(order) + 1)
        rc = ranks[:len(c)].sum()
        return float((rc - len(c) * (len(c) + 1) / 2) / (len(c) * len(w)))

    rows = []
    for name, sm in (("a normal observer", 0.3), ("a weaker monitor", 1.0), ("blindsight", 20.0)):
        conf = np.abs(x + rng.normal(0, sm, trials))
        qs = np.quantile(conf, np.linspace(0, 1, 21))
        roc = [[round(float((conf[~correct] >= q).mean()), 4), round(float((conf[correct] >= q).mean()), 4)]
               for q in qs[::-1]]
        rows.append({"observer": name, "meta_noise": sm, "correct": round(float(correct.mean()), 4),
                     "auroc2": round(auroc2(conf), 4), "roc": roc})
    return {"d": d, "trials": trials, "rows": rows}


# ---------------------------------------------------------------------------
# The meta-problem: a self-model that cannot say what it can tell apart (an analogy)
# ---------------------------------------------------------------------------
FOCAL = {  # rough sRGB prototypes of Berlin and Kay's eleven basic colour terms
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (200, 30, 30), "green": (40, 160, 60),
    "yellow": (240, 220, 40), "blue": (40, 70, 200), "brown": (130, 80, 30), "purple": (130, 50, 160),
    "pink": (240, 150, 180), "orange": (240, 140, 20), "grey": (128, 128, 128),
}


def introspection(levels: int = 16) -> dict:
    """A perceiver that tells apart every one of 16^3 = 4096 shades, whose model of its own states keeps only which of
    eleven basic colour words a state falls under. Asked whether two shades under one word differ, it can tell that
    they do; asked how, its self-model has nothing to say: 12 bits discriminated, at most log2 11 = 3.46 reported.
    The share of discriminable pairs it can only call 'different, but both just like this' is computed. On
    illusionist views (Frankish, Dennett; Chalmers's meta-problem, 2018), reports that experiences are simple,
    intrinsic and ineffable are what such a self-model would produce. An analogy only."""
    vals = np.linspace(0, 255, levels)
    pts = np.array(list(itertools.product(vals, vals, vals)))
    names = list(FOCAL)
    protos = np.array([FOCAL[k] for k in names], float)
    lab = np.argmin(((pts[:, None, :] - protos[None]) ** 2).sum(axis=2), axis=1)
    counts = np.bincount(lab, minlength=len(names))
    n = len(pts)
    same = int((counts * (counts - 1)).sum() // 2)
    total = n * (n - 1) // 2
    return {"shades": n, "words": len(names), "bits_seen": round(math.log2(n), 2),
            "bits_said": round(math.log2(len(names)), 2), "same_word_pairs": same, "pairs": total,
            "share_unsayable": round(same / total, 4),
            "per_word": {names[k]: int(counts[k]) for k in range(len(names))}}


# ---------------------------------------------------------------------------
# Two-dimensional semantics: water, pain, and the zombie scenario
# ---------------------------------------------------------------------------
SCENARIOS = {  # what each scenario contains
    "Earth": {"watery": "H2O", "feeling": True, "C-fibres": True},
    "Twin Earth": {"watery": "XYZ", "feeling": True, "C-fibres": True},
    "zombie world": {"watery": "H2O", "feeling": False, "C-fibres": True},
}


def two_d() -> dict:
    """Chalmers's two-dimensional semantics (Part 22), on three scenarios. Rows: a scenario considered as actual;
    columns: a world considered as counterfactual. 'Water' picks out, in the row's scenario, whatever is watery
    there, and then rigidly that stuff in every column; 'pain' picks out the feeling itself, in every row and
    column; 'C-fibre firing' picks out C-fibre firing. 'Water is H2O' is true on every column of the Earth row
    (necessary) but false in the Twin Earth row (not a priori): its primary and secondary intensions differ. For
    'pain is C-fibre firing' the two coincide, so the zombie row's falsity carries over to a column: if the zombie
    scenario is coherent, the identity is not necessary."""
    names = list(SCENARIOS)

    def water(row, col):
        stuff = SCENARIOS[row]["watery"]          # fixed by the row, then held rigid
        return stuff == "H2O"

    def pain(row, col):
        # 'pain' picks out the feeling under either intension, so the row makes no difference: the identity holds
        # at a world iff the feeling and C-fibre firing go together there
        w = SCENARIOS[col]
        return w["feeling"] == w["C-fibres"]

    mats = {}
    for name, fn in (("water is H2O", water), ("pain is C-fibre firing", pain)):
        m = [[fn(r, c) for c in names] for r in names]
        primary = [m[k][k] for k in range(len(names))]
        secondary = m[0]
        mats[name] = {"matrix": m, "primary": primary, "secondary": secondary,
                      "a_priori": all(primary), "necessary": all(secondary)}
    return {"scenarios": names, "sentences": mats}


# ---------------------------------------------------------------------------
# Mary's room: what she can rule out
# ---------------------------------------------------------------------------
def mary() -> dict:
    """Jackson (1982), as an epistemic model. Mary knows every physical truth about colour vision, so every
    possibility she leaves open agrees on all of them; what differs is what seeing red is like. Before her release
    three possibilities remain (red looks like this; red looks the way green looks to us; there is nothing it is
    like); seeing a tomato leaves one. On the dualist reading she has ruled out real possibilities, so she has
    learnt a fact the physical truths did not fix. On the ability hypothesis (Lewis 1988, Nemirow 1990) nothing is
    ruled out: she gains three abilities. On the phenomenal-concept reading (Loar 1990) the three were never three
    worlds, only three ways one fact could be presented."""
    worlds = [
        {"name": "red looks like this", "physical": "all as in the textbooks", "phenomenal": "this"},
        {"name": "red looks as green looks to us", "physical": "all as in the textbooks", "phenomenal": "inverted"},
        {"name": "nothing it is like", "physical": "all as in the textbooks", "phenomenal": "none"},
    ]
    before = [w["name"] for w in worlds]
    after = [w["name"] for w in worlds if w["phenomenal"] == "this"]
    return {"worlds": worlds, "before": before, "after": after, "physical_agree": len({w["physical"] for w in worlds}),
            "abilities": ["to imagine red", "to recognize red when she sees it", "to remember seeing red"]}


# ---------------------------------------------------------------------------
# Indicator properties (Butlin, Long et al. 2023), on the Reasoner's toys
# ---------------------------------------------------------------------------
INDICATORS = [
    ("RPT-1", "recurrent processing", "input modules using algorithmic recurrence"),
    ("RPT-2", "recurrent processing", "organised, integrated perceptual representations"),
    ("GWT-1", "global workspace", "multiple specialised systems working in parallel"),
    ("GWT-2", "global workspace", "a limited-capacity workspace: a bottleneck, with selective attention"),
    ("GWT-3", "global workspace", "global broadcast of the workspace's contents to all modules"),
    ("GWT-4", "global workspace", "state-dependent attention, querying modules in succession"),
    ("HOT-1", "higher-order", "generative, top-down or noisy perception modules"),
    ("HOT-2", "higher-order", "metacognitive monitoring that tells reliable perception from noise"),
    ("HOT-3", "higher-order", "agency guided by belief formation that heeds the monitoring"),
    ("HOT-4", "higher-order", "sparse and smooth coding: a quality space"),
    ("AST-1", "attention schema", "a predictive model of the system's own attention"),
    ("PP-1", "predictive processing", "input modules using predictive coding"),
    ("AE-1", "agency and embodiment", "learning from feedback and selecting outputs to pursue goals"),
    ("AE-2", "agency and embodiment", "modelling how outputs change inputs, and using the model"),
]

TOYS = {  # by inspection of the code in this module; each reason is what the code does
    "the workspace (chapter 8)": {"RPT-1": "the unit's activity feeds back on itself",
                                  "GWT-2": "a single unit through which a stimulus must pass"},
    "the metacognitive observer (chapter 9)": {"HOT-1": "its perceptual signal is noisy",
                                               "HOT-2": "a monitor rates how reliable each percept is"},
    "the T-maze agent (chapter 12)": {"PP-1": "it predicts its observations from a generative model",
                                      "AE-2": "it models how going to the cue changes what it will observe"},
}


def indicators() -> dict:
    """Butlin, Long and colleagues (2023) derived fourteen indicator properties from scientific theories of
    consciousness, assuming computational functionalism, and concluded that no current AI system is a strong
    candidate while no obvious technical barrier stands in the way. Applied, by inspection, to three toys built in
    this part: each meets two indicators, six between them, in a few dozen lines of code each. More indicators are
    meant to raise credence; meeting some is cheap."""
    rows = []
    for code, theory, text in INDICATORS:
        rows.append({"code": code, "theory": theory, "text": text,
                     "toys": {t: (code in m) for t, m in TOYS.items()}})
    met = {t: sorted(m) for t, m in TOYS.items()}
    return {"indicators": rows, "met": met, "reasons": TOYS, "total": len(INDICATORS),
            "distinct": len({c for m in TOYS.values() for c in m})}
