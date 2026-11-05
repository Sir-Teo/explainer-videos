"""Precompute everything in Part 2 of *Philosophy, Built* ("The Laws of Thought": propositional logic and SAT).

    python -m videos.philosophy.philosophy2.compute            # everything missing (a few minutes on one core)
    python -m videos.philosophy.philosophy2.compute --force solvers

Results are cached in ``.cache/philosophy2/<name>.json``; scenes call ``load(name)``. Every table, proof, search and
count here is computed by the Reasoner (``explainer.philosophy.reasoner.prop``) on this machine, exactly; the
solvers are checked against brute force where brute force is possible.

Items:
    jevons      Jevons's logical abacus (1869) on "iron is a metal, every metal is an element": the eight
                combinations, the ones each premise strikes out, and what survives
    connectives the sixteen binary truth functions, with names, and which of them is complete on its own
    post        Post's five classes for each connective, and the functional completeness of sets of connectives
    tables      truth tables: Peirce's law; modus ponens, modus tollens, affirming the consequent and denying the
                antecedent with their countermodels; how many rows a table needs for n atoms, and how long
    blowup      CNF by distribution against Tseitin's encoding, for (x1 & y1) | ... | (xn & yn)
    knights     Smullyan's knights and knaves: the brute-force table, the unique solution, and a resolution proof
    proofs      Fitch proofs, each checked: modus tollens, contraposition, excluded middle, Peirce's law
    soundness   each inference rule's soundness condition, checked as a tautology
    lindenbaum  Lindenbaum's construction run on a consistent set: formulas in order, each added or its negation
    dpll        a recorded DPLL search tree on a small formula
    cdcl        a recorded CDCL run: decisions, propagations, a conflict, the clause learned, the backjump
    solvers     the pigeonhole formulas PHP(n+1, n): resolution saturation, DPLL and CDCL work against n; random
                3-SAT at 4.26 clauses per variable for DPLL and CDCL
    pythag      the numbers 1 ... 400 split into two colours with no one-coloured Pythagorean triple, by our solver
    knights2    the problem-set puzzle: A says "B is a knave", B says "A and C are of the same kind"
    tonk        Prior's tonk (1960): no truth function satisfies both its rules
    transition  random 3-SAT: the chance of satisfiability and DPLL's work against clauses per atom, n = 20, 30, 40
    elenchus    Republic I (Cephalus and Polemarchus): the claims, their minimal inconsistent sets, the minimal
                correction sets, and the hitting-set duality
    evil        the logical problem of evil (Mackie 1955): the six claims and the positions that escape them
"""

from __future__ import annotations

import itertools
import random
import statistics
import time

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner.prop import And, Iff, Imp, Not, Or, Var, parse, show

CACHE = Cache("philosophy2")
load = CACHE.load


def _v(v: dict) -> dict:
    return {k: bool(x) for k, x in v.items()}


# ---------------------------------------------------------------------------
def compute_jevons() -> dict:
    """Jevons's 'method of indirect inference' (Principles of Science, 1874; the logic piano, 1869): write out every
    combination of the terms, strike out each that contradicts a premise, read the conclusion off what is left."""
    names = ["I", "M", "E"]  # iron, metal, element
    premises = [("iron is a metal", parse("I -> M")), ("every metal is an element", parse("M -> E"))]
    rows = []
    for v in prop.valuations(names):
        struck = [k for k, (_, f) in enumerate(premises) if not prop.evaluate(f, v)]
        rows.append({"v": _v(v), "struck_by": struck})
    survivors = [r["v"] for r in rows if not r["struck_by"]]
    concl = parse("I -> E")
    assert all(prop.evaluate(concl, v) for v in survivors)
    assert prop.entails([f for _, f in premises], concl)[0]
    return {"names": names, "premises": [t for t, _ in premises], "rows": rows,
            "survivors": survivors, "conclusion": "I -> E",
            "iron_rows": [r for r in survivors if r["I"]]}


NAMES16 = {
    (False, False, False, False): ("⊥", "contradiction"), (False, False, False, True): ("↓", "nor"),
    (False, False, True, False): ("↚", "converse non-implication"), (False, False, True, True): ("¬p", "not p"),
    (False, True, False, False): ("↛", "non-implication"), (False, True, False, True): ("¬q", "not q"),
    (False, True, True, False): ("⊕", "exclusive or"), (False, True, True, True): ("↑", "nand"),
    (True, False, False, False): ("∧", "and"), (True, False, False, True): ("↔", "if and only if"),
    (True, False, True, False): ("q", "q"), (True, False, True, True): ("→", "if ... then"),
    (True, True, False, False): ("p", "p"), (True, True, False, True): ("←", "converse implication"),
    (True, True, True, False): ("∨", "or"), (True, True, True, True): ("⊤", "tautology"),
}


def compute_connectives() -> dict:
    """The 16 truth functions of two arguments, in the order (p, q) = TT, TF, FT, FF; which are complete alone."""
    out = []
    for bits in itertools.product((True, False), repeat=4):
        sym, name = NAMES16[bits]
        tbl = dict(zip(itertools.product((True, False), repeat=2), bits))
        cls = prop._post_classes(bits, 2)
        out.append({"bits": list(bits), "sym": sym, "name": name, "classes": cls,
                    "sheffer": not any(cls.values())})
        assert tbl[(True, True)] == bits[0]
    sheffer = [c["sym"] for c in out if c["sheffer"]]
    assert sheffer == ["↑", "↓"]
    # which truth function could 'if p then q' be? Three demands, each a filter on the 16:
    #   modus ponens is valid:            f(T, F) = F  (and f(T, T) = T, or 'p, if p then q' would refute itself)
    #   'if p then p' is always true:     f(T, T) = T and f(F, F) = T
    #   'if p then q' is not symmetric:   f(F, T) != f(T, F)  (else 'if p then q' says the same as 'if q then p')
    demands = [("modus ponens", lambda b: b[1] is False and b[0] is True),
               ("if p then p", lambda b: b[0] is True and b[3] is True),
               ("not symmetric", lambda b: b[2] != b[1])]
    alive = [c["sym"] for c in out]
    filt = []
    for name, ok in demands:
        alive = [c["sym"] for c in out if c["sym"] in alive and ok(tuple(c["bits"]))]
        filt.append({"demand": name, "survivors": list(alive)})
    assert alive == ["→"]
    return {"functions": out, "sheffer": sheffer, "count_n": {n: 2 ** (2 ** n) for n in range(1, 6)},
            "conditional": filt}


def compute_post() -> dict:
    classes = ["T0", "T1", "self-dual", "monotone", "affine"]
    conns = ["¬", "∧", "∨", "→", "↔", "⊕", "↑", "↓", "⊤", "⊥"]
    member = {}
    for c in conns:
        n, fn = prop.CONNECTIVES[c]
        table = tuple(fn(*r) for r in itertools.product((True, False), repeat=n))
        member[c] = prop._post_classes(table, n)
    sets = [["¬", "∧"], ["¬", "∨"], ["¬", "→"], ["→", "⊥"], ["↑"], ["↓"], ["∧", "∨"], ["∧", "∨", "⊤", "⊥"],
            ["¬", "↔"], ["⊕", "∧", "⊤"], ["→"], ["∧", "∨", "→", "↔"]]
    res = []
    for S in sets:
        ok, esc = prop.post_complete(S)
        res.append({"set": S, "complete": ok, "escapes": esc, "stuck_in": [k for k, v in esc.items() if not v]})
    # brute-force cross-check of completeness for every set: generate all 2-ary functions by composition
    for r in res:
        r["generated"] = len(_closure(r["set"]))
        assert (r["generated"] == 16) == r["complete"], r
    return {"classes": classes, "member": member, "sets": res}


def _closure(conns) -> set:
    """The binary truth functions (as 4-tuples over TT, TF, FT, FF) built from p, q and the connectives."""
    rows = list(itertools.product((True, False), repeat=2))
    have = {tuple(r[0] for r in rows), tuple(r[1] for r in rows)}
    for c in conns:
        n, fn = prop.CONNECTIVES[c]
        if n == 0:
            have.add(tuple(fn() for _ in rows))
    while True:
        new = set(have)
        for c in conns:
            n, fn = prop.CONNECTIVES[c]
            if n == 1:
                for a in have:
                    new.add(tuple(fn(x) for x in a))
            elif n == 2:
                for a in have:
                    for b in have:
                        new.add(tuple(fn(x, y) for x, y in zip(a, b)))
        if new == have:
            return have
        have = new


def compute_tables() -> dict:
    peirce = parse("((p -> q) -> p) -> p")
    rows, cols = prop.truth_table(peirce)
    forms = {
        "modus ponens": (["p -> q", "p"], "q"),
        "modus tollens": (["p -> q", "~q"], "~p"),
        "affirming the consequent": (["p -> q", "q"], "p"),
        "denying the antecedent": (["p -> q", "~p"], "~q"),
        "disjunctive syllogism": (["p | q", "~p"], "q"),
        "hypothetical syllogism": (["p -> q", "q -> r"], "p -> r"),
    }
    verdicts = {}
    for k, (ps, c) in forms.items():
        ok, cm = prop.entails([parse(x) for x in ps], parse(c))
        verdicts[k] = {"premises": ps, "conclusion": c, "valid": ok, "countermodel": _v(cm) if cm else None}
    assert verdicts["modus ponens"]["valid"] and not verdicts["affirming the consequent"]["valid"]
    # the cost of tables: rows for n atoms at a billion rows a second
    cost = []
    for n in (10, 20, 30, 40, 60, 80, 100, 300):
        secs = 2 ** n / 1e9
        cost.append({"n": n, "rows": 2 ** n, "seconds": secs, "years": secs / 3.15576e7})
    # measured: how fast this machine fills rows of a 20-atom table (pure Python)
    f = And(*[Imp(Var(f"x{i}"), Var(f"x{i + 1}")) for i in range(19)])
    names = [f"x{i}" for i in range(20)]
    t = time.perf_counter()
    k = 0
    for v in prop.valuations(names):
        prop.evaluate(f, v)
        k += 1
        if k >= 200000:
            break
    rate = k / (time.perf_counter() - t)
    return {"peirce": {"cols": [show(c) for c in cols], "rows": [[_v(v), vals] for v, vals in rows],
                       "tautology": prop.tautology(peirce)},
            "forms": verdicts, "cost": cost, "python_rows_per_second": rate}


def compute_blowup() -> dict:
    out = []
    for n in range(1, 13):
        f = Or(*[And(Var(f"x{i}"), Var(f"y{i}")) for i in range(1, n + 1)])
        names = prop.atoms(f)
        if n <= 11:
            cl = prop.cnf_clauses(f, names)
            nd, lits = len(cl), sum(len(c) for c in cl)
        else:
            nd, lits = 2 ** n, n * 2 ** n
        tc, tn = prop.tseitin(f, names)
        out.append({"n": n, "dist_clauses": nd, "dist_literals": lits, "tseitin_clauses": len(tc),
                    "tseitin_vars": len(tn), "tseitin_literals": sum(len(c) for c in tc)})
        assert n > 11 or nd == 2 ** n
    return {"rows": out}


def compute_knights() -> dict:
    """Smullyan (What Is the Name of This Book?, 1978): A says 'all of us are knaves'; B says 'exactly one of us is a
    knight'. Knights tell only truths, knaves only lies: a speaker's claim is true iff the speaker is a knight."""
    a, b, c = Var("a"), Var("b"), Var("c")
    exactly_one = Or(And(a, Not(b), Not(c)), And(Not(a), b, Not(c)), And(Not(a), Not(b), c))
    s1 = Iff(a, And(Not(a), Not(b), Not(c)))
    s2 = Iff(b, exactly_one)
    rows = []
    for v in prop.valuations(["a", "b", "c"]):
        rows.append({"v": _v(v), "s1": prop.evaluate(s1, v), "s2": prop.evaluate(s2, v)})
    sols = [r["v"] for r in rows if r["s1"] and r["s2"]]
    assert sols == [{"a": False, "b": True, "c": False}]
    # resolution: from the puzzle's clauses, refute "A is a knight"
    names = ["a", "b", "c"]
    cl = prop.cnf_clauses(And(s1, s2), names)
    ref = prop.resolution_refute(cl + [frozenset([1])])
    assert ref["refuted"]
    proof = [{"clause": sorted(c), "from": [sorted(x), sorted(y)]} for c, x, y in ref["proof"]]
    # SAT: one call
    model = prop.solve([s1, s2])
    return {"statements": [show(s1), show(s2)], "rows": rows, "solution": sols[0], "clauses": [sorted(c) for c in cl],
            "refute_a": proof, "derived": ref["derived"], "solver": _v(model)}


PROOFS = {
    "modus_tollens": (["p -> q", "~q"], "~p", [
        (0, "p -> q", "premise", []), (0, "~q", "premise", []), (1, "p", "assume", []),
        (1, "q", "impE", [1, 3]), (1, "⊥", "notE", [4, 2]), (0, "~p", "notI", [(3, 5)])]),
    "contraposition": (["p -> q"], "~q -> ~p", [
        (0, "p -> q", "premise", []), (1, "~q", "assume", []), (2, "p", "assume", []),
        (2, "q", "impE", [1, 3]), (2, "⊥", "notE", [4, 2]), (1, "~p", "notI", [(3, 5)]),
        (0, "~q -> ~p", "impI", [(2, 6)])]),
    "excluded_middle": ([], "p | ~p", [
        (1, "~(p | ~p)", "assume", []), (2, "p", "assume", []), (2, "p | ~p", "orI", [2]),
        (2, "⊥", "notE", [3, 1]), (1, "~p", "notI", [(2, 4)]), (1, "p | ~p", "orI", [5]),
        (1, "⊥", "notE", [6, 1]), (0, "~~(p | ~p)", "notI", [(1, 7)]), (0, "p | ~p", "dne", [8])]),
    "peirce": ([], "((p -> q) -> p) -> p", [
        (1, "(p -> q) -> p", "assume", []), (2, "~p", "assume", []), (3, "p", "assume", []),
        (3, "⊥", "notE", [3, 2]), (3, "q", "botE", [4]), (2, "p -> q", "impI", [(3, 5)]),
        (2, "p", "impE", [1, 6]), (2, "⊥", "notE", [7, 2]), (1, "~~p", "notI", [(2, 8)]),
        (1, "p", "dne", [9]), (0, "((p -> q) -> p) -> p", "impI", [(1, 10)])]),
}


def compute_proofs() -> dict:
    out = {}
    for k, (prem, goal, lines) in PROOFS.items():
        ok, msg = prop.check_fitch(lines, prem, goal)
        assert ok, (k, msg)
        assert prop.entails([parse(p) for p in prem], parse(goal))[0]
        uses_dne = any(r == "dne" for _, _, r, _ in lines)
        out[k] = {"premises": prem, "goal": goal, "lines": [[d, f, r, [list(x) if isinstance(x, tuple) else x
                                                                       for x in refs]] for d, f, r, refs in lines],
                  "ok": ok, "classical": uses_dne}
    # a broken proof the checker rejects: using a line from inside a closed subproof
    bad = PROOFS["modus_tollens"][2][:-1] + [(0, "q", "reit", [4])]
    ok, msg = prop.check_fitch(bad)
    assert not ok
    out["broken"] = {"lines": [[d, f, r, refs] for d, f, r, refs in bad], "ok": ok, "message": msg}
    return out


SOUNDNESS = [
    ("andI", "A ∧ B from A and B", "A & B", ["A", "B"]),
    ("andE", "A from A ∧ B", "A", ["A & B"]),
    ("orI", "A ∨ B from A", "A | B", ["A"]),
    ("impE", "B from A → B and A", "B", ["A -> B", "A"]),
    ("notE", "⊥ from A and ¬A", "⊥", ["A", "~A"]),
    ("botE", "anything from ⊥", "B", ["⊥"]),
    ("dne", "A from ¬¬A", "A", ["~~A"]),
    # discharging rules: if Γ, A ⊨ B then Γ ⊨ A → B, i.e. ((G & A) -> B) -> (G -> (A -> B)) is a tautology
    ("impI", "A → B from a subproof A ... B", "((G & A) -> B) -> (G -> (A -> B))", []),
    ("notI", "¬A from a subproof A ... ⊥", "((G & A) -> ⊥) -> (G -> ~A)", []),
    ("orE", "C from A ∨ B, A ... C, B ... C", "((G & A) -> C) & ((G & B) -> C) -> (G & (A | B) -> C)", []),
]


def compute_soundness() -> dict:
    out = []
    for rule, words, concl, prem in SOUNDNESS:
        if prem:
            ok = prop.entails([parse(p) for p in prem], parse(concl))[0]
        else:
            ok = prop.tautology(parse(concl))
        out.append({"rule": rule, "words": words, "check": concl, "premises": prem, "sound": ok})
        assert ok, rule
    # and one unsound rule, for contrast: from A → B and B, infer A
    bad, cm = prop.entails([parse("A -> B"), parse("B")], parse("A"))
    return {"rules": out, "unsound": {"rule": "B, A → B ⊢ A", "sound": bad, "countermodel": _v(cm)}}


def _formulas_by_size(names, max_size):
    """All formulas over ``names`` with ¬ and → (Post's own basis for this demo), by size, deduplicated."""
    by = {1: [Var(n) for n in names]}
    for s in range(2, max_size + 1):
        out = [Not(f) for f in by[s - 1]]
        for i in range(1, s - 1):
            for a in by[i]:
                for b in by[s - 1 - i]:
                    out.append(Imp(a, b))
        by[s] = out
    seq = []
    for s in range(1, max_size + 1):
        seq.extend(by[s])
    return seq


def compute_lindenbaum() -> dict:
    """Lindenbaum's lemma, run: list the formulas φ1, φ2, ...; from Γ0 add φn if that stays consistent, else ¬φn.
    The limit is maximal consistent, and it is a valuation's set of truths."""
    start = [parse("p | q"), parse("~p")]
    seq = _formulas_by_size(["p", "q", "r"], 4)[:24]
    gamma = list(start)
    steps = []
    for f in seq:
        if prop.satisfiable_bf(gamma + [f]) is not None:
            gamma.append(f)
            steps.append({"f": show(f), "added": show(f), "chose": "it"})
        else:
            gamma.append(Not(f))
            steps.append({"f": show(f), "added": show(Not(f)), "chose": "negation"})
    v = prop.satisfiable_bf(gamma)
    assert v is not None
    # every formula in the list is decided the way the valuation says
    for st, f in zip(steps, seq):
        assert (st["chose"] == "it") == prop.evaluate(f, v)
    return {"start": [show(f) for f in start], "steps": steps, "valuation": _v(v)}


DPLL_FORMULA = ["a | b", "~a | c", "~a | ~c | d", "~d | e", "~d | ~e", "b | ~c", "~b | c | e"]


def compute_dpll() -> dict:
    names = ["a", "b", "c", "d", "e"]
    fs = [parse(s) for s in DPLL_FORMULA]
    cl = [prop.cnf_clauses(f, names)[0] for f in fs]
    model, st = prop.dpll(cl, 5, record=True)
    nodes = [{"decision": n.decision, "forced": n.forced, "end": n.end, "children": n.children, "parent": n.parent}
             for n in st["nodes"]]
    bf = prop.satisfiable_bf(fs)
    assert (model is None) == (bf is None)
    return {"names": names, "clauses": [sorted(c) for c in cl], "nodes": nodes,
            "model": {names[k - 1]: v for k, v in model.items()} if model else None,
            "stats": {k: st[k] for k in ("decisions", "propagations", "conflicts")}}


CDCL_FORMULA = ["~a | b", "~a | c", "~b | ~c | d", "~d | e", "~d | ~e | f", "~f | ~a", "a | g", "~g | h", "~h | b"]


def compute_cdcl() -> dict:
    names = ["a", "b", "c", "d", "e", "f", "g", "h"]
    cl = [prop.cnf_clauses(parse(s), names)[0] for s in CDCL_FORMULA]
    model, st = prop.cdcl(cl, len(names), record=True)
    bf = prop.satisfiable_bf([parse(s) for s in CDCL_FORMULA])
    assert (model is None) == (bf is None)
    ev = [{"kind": k, "lit": (list(x) if isinstance(x, tuple) else x), "clause": c, "level": lv}
          for k, x, c, lv in st["events"]]
    return {"names": names, "clauses": [sorted(c) for c in cl], "events": ev,
            "learned": [list(c) for c in st["learned"]],
            "model": {names[k - 1]: v for k, v in model.items()} if model else None,
            "stats": {k: st[k] for k in ("decisions", "propagations", "conflicts")}}


def compute_solvers() -> dict:
    php = []
    for n in range(1, 8):
        cl, nv = prop.pigeonhole(n)
        row = {"n": n, "vars": nv, "clauses": len(cl), "table_rows": 2 ** nv}
        if n <= 4:
            t = time.perf_counter()
            r = prop.resolution_refute(cl, limit=2_000_000)
            row["resolution_derived"] = r["derived"]
            row["resolution_refuted"] = r["refuted"]
            row["resolution_seconds"] = time.perf_counter() - t
        t = time.perf_counter()
        m, st = prop.dpll(cl, nv)
        assert m is None
        row["dpll_decisions"] = st["decisions"]
        row["dpll_seconds"] = time.perf_counter() - t
        t = time.perf_counter()
        m, st = prop.cdcl(cl, nv)
        assert m is None
        row["cdcl_conflicts"] = st["conflicts"]
        row["cdcl_decisions"] = st["decisions"]
        row["cdcl_seconds"] = time.perf_counter() - t
        php.append(row)
        print(f"    PHP({n + 1},{n}): {row}", flush=True)
    rnd = []
    for n in (20, 30, 40, 50, 60):
        dd, cc, sat = [], [], 0
        for seed in range(7):
            rng = random.Random(1000 * n + seed)
            cl = prop.random_ksat(n, round(4.26 * n), 3, rng)
            m1, s1 = prop.dpll(cl, n)
            m2, s2 = prop.cdcl(cl, n)
            assert (m1 is None) == (m2 is None)
            sat += m1 is not None
            dd.append(s1["decisions"])
            cc.append(s2["decisions"])
        rnd.append({"n": n, "dpll_decisions_median": statistics.median(dd), "cdcl_decisions_median": statistics.median(cc),
                    "dpll": dd, "cdcl": cc, "satisfiable": sat, "seeds": 7})
        print(f"    random 3-SAT n={n}: {rnd[-1]['dpll_decisions_median']} vs {rnd[-1]['cdcl_decisions_median']}",
              flush=True)
    return {"php": php, "random": rnd}


def compute_pythag(n: int = 400) -> dict:
    """Heule, Kullmann and Marek (2016) showed {1, ..., 7824} can be 2-coloured with no monochromatic a^2 + b^2 = c^2
    and {1, ..., 7825} cannot. The small case, here: colour 1 ... n with our CDCL solver, and check it."""
    triples = [(a, b, c) for c in range(1, n + 1) for a in range(1, c) for b in range(a, c) if a * a + b * b == c * c]
    used = sorted({x for t in triples for x in t})
    cl = []
    for a, b, c in triples:
        cl.append(frozenset([a, b, c]))
        cl.append(frozenset([-a, -b, -c]))
    t = time.perf_counter()
    model, st = prop.cdcl(cl, n)
    secs = time.perf_counter() - t
    assert model is not None
    colour = [bool(model[i]) for i in range(1, n + 1)]
    for a, b, c in triples:
        assert not (colour[a - 1] == colour[b - 1] == colour[c - 1])
    return {"n": n, "triples": triples, "in_triples": len(used), "colour": colour, "seconds": secs,
            "conflicts": st["conflicts"], "decisions": st["decisions"], "published": {"max_n": 7824,
                                                                                    "proof_tb": 200}}


def compute_knights2() -> dict:
    a, b, c = Var("a"), Var("b"), Var("c")
    s1 = Iff(a, Not(b))
    s2 = Iff(b, Iff(a, c))
    sols = [_v(v) for v in prop.valuations(["a", "b", "c"]) if prop.evaluate(s1, v) and prop.evaluate(s2, v)]
    return {"statements": [show(s1), show(s2)], "solutions": sols}


def compute_tonk() -> dict:
    """tonk-I: from A infer A tonk B; tonk-E: from A tonk B infer B. For tonk to be a sound truth function f we need
    A ⊨ f(A, B) (so f(T, x) = T) and f(A, B) ⊨ B (so f(x, F) = F): the row (T, F) cannot be both."""
    rows = list(itertools.product((True, False), repeat=2))
    fits = []
    for bits in itertools.product((True, False), repeat=4):
        f = dict(zip(rows, bits))
        intro = all(f[(a, b)] for a, b in rows if a)
        elim = all(b for a, b in rows if f[(a, b)])
        if intro and elim:
            fits.append(bits)
    assert fits == []
    intro_ok = [NAMES16[b][0] for b in itertools.product((True, False), repeat=4)
                if all(dict(zip(rows, b))[(a, c)] for a, c in rows if a)]
    elim_ok = [NAMES16[b][0] for b in itertools.product((True, False), repeat=4)
               if all(c for (a, c), v in zip(rows, b) if v)]
    return {"both": fits, "intro_only": intro_ok, "elim_only": elim_ok}


def compute_transition() -> dict:
    ratios = [round(2.0 + 0.25 * k, 2) for k in range(21)]
    out = {}
    for n in (20, 30, 40):
        part = CACHE.partial(f"transition_{n}", {"ratios": ratios, "seeds": 30})
        for r in ratios:
            key = f"{r:.2f}"
            if key in part:
                continue
            sat, work = 0, []
            for seed in range(30):
                rng = random.Random(100000 * n + int(100 * r) * 100 + seed)
                cl = prop.random_ksat(n, round(r * n), 3, rng)
                m, st = prop.dpll(cl, n)
                sat += m is not None
                work.append(st["decisions"])
            part[key] = {"p_sat": sat / 30, "median_decisions": statistics.median(work)}
        out[str(n)] = [{"ratio": r, **part[f"{r:.2f}"]} for r in ratios]
        part.finish()
        print(f"    n={n}: peak work at ratio {max(out[str(n)], key=lambda x: x['median_decisions'])['ratio']}", flush=True)
    return {"ratios": ratios, "by_n": out, "seeds": 30}


# ---------------------------------------------------------------------------
# The elenchus and the first Price List
# ---------------------------------------------------------------------------
REPUBLIC = [
    ("D1", r"Justice is giving back what is owed", "o -> j"),
    ("o", r"Returning a mad friend's weapon is giving back what is owed", "o"),
    ("nj", r"Returning it is not just", "~j"),
    ("D2", r"Justice is helping friends and harming enemies", "h -> j2"),
    ("h", r"The just will sometimes harm an enemy", "h"),
    ("H", r"Harming a person makes them worse, that is, less just", "h -> w"),
    ("N", r"It is not the work of justice to make anyone less just", "j2 -> ~w"),
]


def compute_elenchus() -> dict:
    claims = {k: parse(f) for k, _, f in REPUBLIC}
    r = prop.mus_mcs(claims)
    hs = prop.hitting_sets(r["mus"])
    assert {tuple(sorted(h)) for h in hs} == {tuple(sorted(m)) for m in r["mcs"]}
    assert len(r["mus"]) == 2 and len(r["mcs"]) == 3 * 4
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in REPUBLIC], **r,
            "hitting_sets": [list(h) for h in hs], "subsets_checked": 2 ** len(REPUBLIC)}


EVIL = [
    ("G", r"God exists", "G"),
    ("omnipotent", r"God is omnipotent", "G -> o"),
    ("omniscient", r"God is omniscient", "G -> k"),
    ("good", r"God is wholly good", "G -> g"),
    ("bridge", r"A good, all-knowing, all-powerful being would prevent all evil", "(o & k & g) -> ~e"),
    ("evil", r"There is evil", "e"),
]


def compute_evil() -> dict:
    claims = {k: parse(f) for k, _, f in EVIL}
    r = prop.mus_mcs(claims)
    assert r["mus"] == [tuple(k for k, _, _ in EVIL)]
    assert r["mcs"] == [(k,) for k, _, _ in EVIL]
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in EVIL], **r}


ITEMS = {
    "jevons": compute_jevons, "connectives": compute_connectives, "post": compute_post, "tables": compute_tables,
    "blowup": compute_blowup, "knights": compute_knights, "proofs": compute_proofs, "soundness": compute_soundness,
    "lindenbaum": compute_lindenbaum, "dpll": compute_dpll, "cdcl": compute_cdcl, "solvers": compute_solvers,
    "tonk": compute_tonk, "transition": compute_transition, "pythag": compute_pythag, "knights2": compute_knights2, "elenchus": compute_elenchus, "evil": compute_evil,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
