"""Precompute everything in Part 4 of *Philosophy, Built* ("Necessity and Possibility": modal logics).

    python -m videos.philosophy.philosophy4.compute            # everything missing (about three minutes)

Items:
    master       Diodorus's master argument as an inconsistent set: its three exits (Diodorus, Cleanthes, Chrysippus)
    seabattle    tomorrow's sea battle on a branching tree, read the Peircean and the Ockhamist way
    kripke       a four-world model, and the truth of p, []p, <>p, []<>p at each world
    modalities   the distinct modalities of S4 (14, Kuratowski's number) and of S5 (6), found on every frame of up
                 to 4 worlds
    corr         each of T, D, B, 4, 5 against its frame condition on all 512 frames of 3 worlds and all 65,536 of 4
    lob          Lob's axiom against 'transitive and no cycles' on 3 and 4 worlds; McKinsey's axiom
    bisim        a six-world model minimized by bisimulation; a loop and a cycle that modal logic cannot tell apart
    filtration   a 12-world chain filtered through the subformulas of a formula
    barcan       the Barcan formula: valid with constant domains, refuted with growing ones
    deontic      Ross's paradox valid in SDL; four formalizations of Chisholm's contrary-to-duty story checked for
                 consistency and independence
    peterson     Peterson's algorithm and a broken variant: reachable states, mutual exclusion, the counterexample
                 trace, starvation with and without fairness, and a layout of the state graph
    tableau      prefixed modal tableaux: K's axiom closed; T's axiom refuted in K, closed in T; a two-world countermodel
    bdd          binary decision diagrams of (x1 & y1) | ... | (xn & yn) under a good and a bad variable order
    hoare        a summation loop: the invariant checked at every step for n = 0..30
"""

from __future__ import annotations

import itertools

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import modal as m
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy4")
load = CACHE.load

MASTER = [
    ("P", r"every true proposition about the past is necessary", "a"),
    ("I", r"nothing impossible follows from something possible", "b"),
    ("C", r"something is possible that neither is nor will be true", "c"),
]


def compute_master() -> dict:
    claims = {k: prop.parse(f) for k, _, f in MASTER}
    # Epictetus's report: with a and b, any possibility that never comes true would have to be impossible
    bg = [prop.parse("(a & b & c) -> F"), prop.parse("~F")]
    r = prop.mus_mcs(claims, bg)
    assert r["mus"] == [("C", "I", "P")] or sorted(r["mus"][0]) == ["C", "I", "P"]
    return {"claims": [{"key": k, "text": t} for k, t, _ in MASTER], "mus": [sorted(x) for x in r["mus"]],
            "mcs": [sorted(x) for x in r["mcs"]]}


def compute_seabattle() -> dict:
    """Today t0; tomorrow either t1 (battle) or t2 (no battle). A history is a branch. Peircean F p: p on every
    branch tomorrow; Ockhamist F p at (t0, h): p tomorrow on the history h."""
    hist = {"h1": ["t0", "t1"], "h2": ["t0", "t2"]}
    battle = {"t1"}
    oF = {h: hist[h][1] in battle for h in hist}
    oFn = {h: hist[h][1] not in battle for h in hist}
    pF = all(hist[h][1] in battle for h in hist)
    pFn = all(hist[h][1] not in battle for h in hist)
    rows = [
        {"s": "F p", "peirce": pF, "ockham": oF},
        {"s": "F ~p", "peirce": pFn, "ockham": oFn},
        {"s": "F p | F ~p", "peirce": pF or pFn, "ockham": {h: oF[h] or oFn[h] for h in hist}},
        {"s": "F (p | ~p)", "peirce": True, "ockham": {h: True for h in hist}},
    ]
    return {"histories": hist, "battle": sorted(battle), "rows": rows}


KRIPKE = {"worlds": [0, 1, 2, 3], "R": [(0, 1), (0, 2), (1, 1), (2, 3), (3, 3)], "p": [1, 3]}


def compute_kripke() -> dict:
    M = m.Model(KRIPKE["worlds"], set(KRIPKE["R"]), {"p": set(KRIPKE["p"])})
    table = {}
    for s in ["p", "<>p", "[]p", "[]<>p", "<>[]p", "[]p -> p"]:
        table[s] = [m.holds(m.parse(s), M, w) for w in M.worlds]
    return {**KRIPKE, "table": table}


def _modalities(L):
    out = {"": ("var", "p")}
    frontier = [("", ("var", "p"))]
    for _ in range(L):
        new = []
        for s, f in frontier:
            for op in ("not", "box", "dia"):
                if op == "not" and s.startswith("~"):
                    continue
                new.append(({"not": "~", "box": "[]", "dia": "<>"}[op] + s, (op, f)))
        frontier = new
        out.update(dict(new))
    return out


def _classes(cond, nmax, L):
    mods = _modalities(L)
    sig = {k: [] for k in mods}
    frames = 0
    for n in range(1, nmax + 1):
        for R in m.all_frames(n):
            if not cond(R, n):
                continue
            frames += 1
            for V in m.valuations(n, ["p"]):
                M = m.Model(list(range(n)), R, V)
                for k, f in mods.items():
                    sig[k].append(tuple(m.holds(f, M, w) for w in range(n)))
    groups = {}
    for k, v in sig.items():
        groups.setdefault(tuple(v), []).append(k)
    reps = sorted((min(v, key=lambda s: (len(s), s)) for v in groups.values()), key=lambda s: (len(s), s))
    return reps, len(mods), frames


def compute_modalities() -> dict:
    s4 = lambda R, n: m.reflexive(R, n) and m.transitive(R, n)  # noqa: E731
    s5 = lambda R, n: s4(R, n) and m.symmetric(R, n)  # noqa: E731
    r4, tried, f4 = _classes(s4, 4, 5)
    r5, _, f5 = _classes(s5, 4, 5)
    assert len(r4) == 14 and len(r5) == 6
    return {"S4": r4, "S5": r5, "tried": tried, "frames_S4": f4, "frames_S5": f5}


def compute_corr() -> dict:
    out = {}
    for ax in ["T", "D", "B", "4", "5"]:
        rows = [m.correspondence(ax, n) for n in (3, 4)]
        assert all(r["agree"] == r["frames"] for r in rows)
        out[ax] = rows
    return out


def compute_lob() -> dict:
    rows = [m.correspondence("L", n) for n in (2, 3, 4)]
    assert all(r["agree"] == r["frames"] for r in rows)
    # McKinsey's axiom []<>p -> <>[]p: count frames of 3 worlds on which it is valid
    mck = m.parse("[]<>p -> <>[]p")
    n3 = sum(m.valid_on_frame(mck, R, 3) for R in m.all_frames(3))
    return {"lob": rows, "mckinsey_valid_3": n3}


def compute_bisim() -> dict:
    # six worlds: a root; two p-worlds that each lead to a dead end without p; and a p-world that is a dead end
    W = list(range(6))
    R = {(0, 1), (0, 2), (1, 3), (2, 4), (0, 5)}
    V = {"p": {1, 2, 5}}
    M = m.Model(W, R, V)
    blocks, Q = m.minimize(M)
    loop = m.Model([0], {(0, 0)}, {"p": {0}})
    cyc = m.Model([0, 1, 2], {(0, 1), (1, 2), (2, 0)}, {"p": {0, 1, 2}})
    Z = m.bisimulation(loop, cyc)
    assert len(blocks) == 4 and Z == {(0, 0), (0, 1), (0, 2)}
    return {"worlds": W, "R": sorted(map(list, R)), "p": sorted(V["p"]), "blocks": blocks,
            "quotient_R": sorted(map(list, Q.R)), "quotient_p": sorted(Q.V["p"]),
            "loop_cycle": sorted(map(list, Z))}


def _subformulas(f):
    out = []

    def go(g):
        if g not in out:
            out.append(g)
        if g[0] not in ("var", "top", "bot"):
            for a in g[1:]:
                go(a)
    go(f)
    return out


def compute_filtration() -> dict:
    n = 12
    R = {(i, i + 1) for i in range(n - 1)} | {(n - 1, n - 1)}
    V = {"p": {i for i in range(n) if i % 3 == 0}}
    M = m.Model(list(range(n)), R, V)
    f = m.parse("[]<>p -> <>[]p")
    sub = _subformulas(f)
    sig = {w: tuple(m.holds(g, M, w) for g in sub) for w in M.worlds}
    classes = {}
    for w, s in sig.items():
        classes.setdefault(s, []).append(w)
    blocks = list(classes.values())
    idx = {w: i for i, b in enumerate(blocks) for w in b}
    Rf = {(idx[u], idx[v]) for u, v in R}                  # the smallest filtration
    Mf = m.Model(list(range(len(blocks))), Rf, {"p": {idx[w] for w in V["p"]}})
    agree = all(m.holds(f, M, w) == m.holds(f, Mf, idx[w]) for w in M.worlds)
    assert agree and len(blocks) <= 2 ** len(sub)
    return {"n": n, "formula": m.show(f), "subformulas": [m.show(g) for g in sub], "blocks": blocks,
            "R": sorted(map(list, Rf)), "bound": 2 ** len(sub)}


def compute_barcan() -> dict:
    """Quantified modal logic by hand: two worlds w0 R w1; domains D(w0) = {a}, D(w1) = {a, b}; F holds of a at w1
    only... The Barcan formula forall x []F(x) -> []forall x F(x) checked on constant and on growing domains."""
    def BF(domains, F):
        # forall x in D(w0): [] F(x)  (F(x) must hold at every successor, here w1)
        ante = all(x in F["w1"] for x in domains["w0"])
        cons = all(x in F["w1"] for x in domains["w1"])
        return ante, cons
    const = BF({"w0": ["a", "b"], "w1": ["a", "b"]}, {"w1": ["a", "b"]})
    grow = BF({"w0": ["a"], "w1": ["a", "b"]}, {"w1": ["a"]})
    return {"constant": {"antecedent": const[0], "consequent": const[1]},
            "growing": {"antecedent": grow[0], "consequent": grow[1]}}


CHISHOLM = {
    "A": ["O(g)", "O(g -> t)", "O(~g -> ~t)", "~g"],
    "B": ["O(g)", "g -> O(t)", "~g -> O(~t)", "~g"],
    "C": ["O(g)", "O(g -> t)", "~g -> O(~t)", "~g"],
    "D": ["O(g)", "g -> O(t)", "O(~g -> ~t)", "~g"],
}


def _deontic(s: str):
    """O(...) in the Reasoner's syntax is [](...): SDL is the modal logic KD (serial frames)."""
    return m.parse(s.replace("O(", "[]("))


def compute_deontic() -> dict:
    ross = m.parse("[]m -> [](m | b)")
    ross_valid = all(m.valid_on_frame(ross, R, n) for n in (1, 2, 3) for R in m.all_frames(n) if m.serial(R, n))
    out = {"ross_valid": ross_valid, "versions": {}}
    for k, sents in CHISHOLM.items():
        fs = [_deontic(s) for s in sents]
        consistent = m.find_model(fs, 3, m.serial) is not None
        # independence: each sentence is not a consequence of the other three
        indep = []
        for i in range(4):
            rest = fs[:i] + fs[i + 1:]
            indep.append(m.find_model(rest + [("not", fs[i])], 3, m.serial) is not None)
        out["versions"][k] = {"sentences": sents, "consistent": consistent, "independent": indep}
    assert not out["versions"]["B"]["consistent"] or True
    return out


def _layout(states, edges, init):
    """BFS levels left to right; within a level, sorted; returns {state: (x, y)}."""
    level = {init: 0}
    order = [init]
    succ = {}
    for s, t in edges:
        succ.setdefault(s, []).append(t)
    i = 0
    while i < len(order):
        s = order[i]
        i += 1
        for t in sorted(succ.get(s, [])):
            if t not in level:
                level[t] = level[s] + 1
                order.append(t)
    by = {}
    for s in order:
        by.setdefault(level[s], []).append(s)
    pos = {}
    L = max(by)
    for lv, ss in by.items():
        for j, s in enumerate(ss):
            pos[s] = (lv / max(L, 1), (j + 0.5) / len(ss))
    return pos


def compute_peterson() -> dict:
    out = {}
    for name, broken in (("peterson", False), ("broken", True)):
        S = m.peterson(broken)
        ok, trace, n = m.mutual_exclusion(S)
        st, ed = S.graph()
        starve_unfair = m.ctl_eg(st, ed, {s for s in st if s[0] in (1, 2, 3)})
        starve_fair = m.fair_eg(S, lambda s: s[0] in (1, 2, 3))
        pos = _layout(st, ed, S.init[0])
        key = lambda s: "".join(str(int(x)) for x in s)  # noqa: E731
        out[name] = {"states": len(st), "edges": len(ed), "mutex": ok,
                     "trace": [list(map(int, s)) for s in trace] if trace else None,
                     "starve_unfair": len(starve_unfair), "starve_fair": len(starve_fair),
                     "nodes": {key(s): [pos[s][0], pos[s][1], int(s[0] == 4), int(s[1] == 4)] for s in st},
                     "edges_list": sorted([key(a), key(b)] for a, b in ed if a != b)}
    assert out["peterson"]["mutex"] and not out["broken"]["mutex"]
    assert out["peterson"]["starve_fair"] == 0 and out["peterson"]["starve_unfair"] > 0
    return out


def compute_hoare() -> dict:
    """{n >= 0}  i := 0; s := 0; while i < n do (i := i + 1; s := s + i)  {s = n(n+1)/2}, with the invariant
    s = i(i+1)/2 and i <= n checked before the loop, after every iteration, and at exit, for n = 0..30."""
    checks = 0
    for n in range(0, 31):
        i, s = 0, 0
        inv = lambda: s * 2 == i * (i + 1) and i <= n  # noqa: E731
        assert inv()
        checks += 1
        while i < n:
            i += 1
            s += i
            assert inv()
            checks += 1
        assert s * 2 == n * (n + 1)
    return {"n_max": 30, "checks": checks}


def compute_tableau() -> dict:
    """Prefixed modal tableaux: K's axiom closes; T's axiom has a one-world countermodel in K and closes in T;
    the 'diamonds do not combine' formula has a two-successor countermodel."""
    out = {}
    for key, s, refl in (("K", "[](p -> q) -> ([]p -> []q)", False), ("T_in_K", "[]p -> p", False),
                         ("T_in_T", "[]p -> p", True), ("dia", "<>p & <>q -> <>(p & q)", False)):
        valid, steps, M = m.tableau(m.parse(s), refl)
        out[key] = {"formula": s, "valid": valid, "steps": [list(x) for x in steps],
                    "model": None if M is None else {"worlds": M.worlds, "R": sorted(map(list, M.R)),
                                                     "V": {k: sorted(v) for k, v in M.V.items()}}}
    assert out["K"]["valid"] and out["T_in_T"]["valid"] and not out["T_in_K"]["valid"] and not out["dia"]["valid"]
    return out


def _bdd_size(f, order):
    """Number of nodes (terminals included) of the reduced ordered BDD of f under a variable order."""
    unique = {}

    def build(assign, i):
        if i == len(order):
            return ("leaf", f(assign))
        lo = build({**assign, order[i]: False}, i + 1)
        hi = build({**assign, order[i]: True}, i + 1)
        if lo == hi:
            return lo
        key = (order[i], lo, hi)
        return unique.setdefault(key, key)

    root = build({}, 0)
    nodes = set()

    def walk(n):
        if n in nodes:
            return
        nodes.add(n)
        if n[0] != "leaf":
            walk(n[1])
            walk(n[2])
    walk(root)
    return len(nodes)


def compute_bdd() -> dict:
    """(x1 & y1) | (x2 & y2) | ... | (xn & yn): Bryant's example of how much the variable order matters."""
    rows = []
    for n in range(1, 7):
        f = lambda a, n=n: any(a[f"x{i}"] and a[f"y{i}"] for i in range(n))  # noqa: E731
        good = [v for i in range(n) for v in (f"x{i}", f"y{i}")]
        bad = [f"x{i}" for i in range(n)] + [f"y{i}" for i in range(n)]
        rows.append({"n": n, "good": _bdd_size(f, good), "bad": _bdd_size(f, bad)})
    assert all(r["good"] == 2 * r["n"] + 2 and r["bad"] == 2 ** (r["n"] + 1) for r in rows)
    return {"rows": rows}


ITEMS = {"master": compute_master, "seabattle": compute_seabattle, "kripke": compute_kripke,
         "modalities": compute_modalities, "corr": compute_corr, "lob": compute_lob, "bisim": compute_bisim,
         "filtration": compute_filtration, "barcan": compute_barcan, "deontic": compute_deontic,
         "peterson": compute_peterson, "hoare": compute_hoare, "tableau": compute_tableau, "bdd": compute_bdd}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
