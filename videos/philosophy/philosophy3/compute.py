"""Precompute everything in Part 3 of *Philosophy, Built* ("All and Some": first-order logic).

    python -m videos.philosophy.philosophy3.compute            # everything missing (about a minute)

Items:
    love        a four-person structure and Tarski's evaluation of 'everyone loves someone' and 'someone is loved by
                everyone', quantifier by quantifier; and every relation on 3 people (2^9 = 512) counted: how many
                make each sentence true, and the implication between them checked on all of them
    capture     substitution with and without variable capture
    counting    'at least two', 'exactly one', 'exactly two' checked on every structure of sizes 1-4
    russell     'the present king of France is bald': Russell's analysis, both scopes, in structures with no
                king, one king, two kings
    moods       the 256 syllogistic moods in first-order logic: Boolean-valid (15) and with existential import (24),
                agreeing with Part 1; minimal countermodel sizes
    tableaux    the drinker paradox, De Morgan's horse heads, Barbara and 'everybody loves a lover' closed by the
                tableau, step by step; an invalid argument whose open branch is the countermodel;
                the quantifier swap: the tree runs forever, and the model finder refutes it with two people
    monadic     the finite model property for monadic logic: random satisfiable sentences in k = 2 predicates, and
                the size of their smallest models (never more than 2^k)
    skolem      Skolem's paradox as an inconsistent set: its exits
    infinity    a sentence with only infinite models: no model of sizes 1-4 (all 2^16 relations at size 4)
    atp         unification, the occurs check, and a three-step resolution proof of 'everybody loves a lover'
    compact     'there are at least n things' for n = 1..5 on every size 1..6: the ladder behind compactness
    ef          Ehrenfeucht-Fraisse games on linear orders of lengths 1-9: who wins in 2 and 3 rounds
    beard       Plato's beard as an inconsistent set: its four exits
    henkin      Henkin's completeness construction in miniature: witnesses, a maximal consistent set, the term model
"""

from __future__ import annotations

import itertools
import random

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import fol, prop, syllogism as sy

CACHE = Cache("philosophy3")
load = CACHE.load

AE = "forall x exists y L(x, y)"
EA = "exists y forall x L(x, y)"


def compute_love() -> dict:
    people = ["Ann", "Bo", "Cy", "Di"]
    L = {(0, 1), (1, 2), (2, 0), (3, 2)}
    M = fol.Structure(range(4), {"L": L})
    ae, ea = fol.parse(AE), fol.parse(EA)
    # the evaluation, quantifier by quantifier: for each x, the first y that x loves
    witness = {}
    for x in range(4):
        ys = [y for y in range(4) if (x, y) in L]
        witness[x] = ys[0] if ys else None
    loved_by_all = [y for y in range(4) if all((x, y) in L for x in range(4))]
    assert fol.holds(ae, M) and not fol.holds(ea, M)
    # every relation on three people
    n = 3
    pairs = list(itertools.product(range(n), repeat=2))
    c_ae = c_ea = c_both = 0
    for bits in itertools.product((False, True), repeat=len(pairs)):
        R = {p for p, b in zip(pairs, bits) if b}
        S = fol.Structure(range(n), {"L": R})
        a, e = fol.holds(ae, S), fol.holds(ea, S)
        c_ae += a
        c_ea += e
        c_both += a and e
        assert not e or a                 # 'someone is loved by everyone' implies 'everyone loves someone'
    return {"people": people, "loves": sorted(map(list, L)), "witness": witness, "loved_by_all": loved_by_all,
            "relations": 2 ** len(pairs), "count_ae": c_ae, "count_ea": c_ea, "count_both": c_both, "n": n}


def compute_capture() -> dict:
    f = fol.parse("exists y L(x, y)")         # x loves somebody
    good = fol.subst(f, "x", "a")             # a loves somebody
    bad = ("ex", "y", fol.subst(f[2], "x", "y"))   # naive: y loves somebody -> 'somebody loves themselves'
    renamed = ("ex", "z", fol.subst(fol.subst(f[2], "y", "z"), "x", "y"))
    return {"f": fol.show(f), "good": fol.show(good), "captured": fol.show(bad), "renamed": fol.show(renamed)}


def compute_counting() -> dict:
    sents = {
        "at least two": "exists x exists y (P(x) & P(y) & ~x = y)",
        "exactly one": "exists x (P(x) & forall y (P(y) -> y = x))",
        "exactly two": "exists x exists y (P(x) & P(y) & ~x = y & forall z (P(z) -> z = x | z = y))",
    }
    out = {}
    for name, s in sents.items():
        f = fol.parse(s)
        ok = True
        for n in range(1, 5):
            for k in range(0, n + 1):
                M = fol.Structure(range(n), {"P": {(i,) for i in range(k)}})
                want = {"at least two": k >= 2, "exactly one": k == 1, "exactly two": k == 2}[name]
                ok &= fol.holds(f, M) == want
        assert ok
        out[name] = {"formula": s, "tex": fol.show(f, tex=True), "checked_sizes": [1, 2, 3, 4]}
    return out


def compute_russell() -> dict:
    wide = fol.parse("exists x (K(x) & forall y (K(y) -> y = x) & B(x))")            # the king is bald
    neg_wide = fol.parse("exists x (K(x) & forall y (K(y) -> y = x) & ~B(x))")        # the king is not bald
    neg_narrow = ("not", wide)                                                       # it is not the case that ...
    rows = []
    for name, K, B in [("no king", set(), set()), ("one bald king", {(0,)}, {(0,)}),
                       ("one hairy king", {(0,)}, set()), ("two kings", {(0,), (1,)}, {(0,), (1,)})]:
        M = fol.Structure(range(3), {"K": K, "B": B})
        rows.append({"world": name, "bald": fol.holds(wide, M), "not_bald_wide": fol.holds(neg_wide, M),
                     "not_bald_narrow": fol.holds(neg_narrow, M)})
    assert rows[0] == {"world": "no king", "bald": False, "not_bald_wide": False, "not_bald_narrow": True}
    return {"wide": fol.show(wide, tex=True), "neg_wide": fol.show(neg_wide, tex=True),
            "neg_narrow": fol.show(neg_narrow, tex=True), "rows": rows}


def _mood_fol(mood):
    prem, concl = sy.premises(mood)
    tr = {"A": "forall x ({x}(x) -> {y}(x))", "E": "forall x ({x}(x) -> ~{y}(x))", "I": "exists x ({x}(x) & {y}(x))",
          "O": "exists x ({x}(x) & ~{y}(x))"}
    ps = [fol.parse(tr[k].format(x=a, y=b)) for k, a, b in prem]
    c = fol.parse(tr[concl[0]].format(x=concl[1], y=concl[2]))
    return ps, c


def compute_moods() -> dict:
    imp = [fol.parse(f"exists x {t}(x)") for t in "SMP"]
    boolean, trad, sizes = [], [], []
    for mood in sy.all_moods():
        ps, c = _mood_fol(mood)
        cm = fol.countermodel(ps, c, max_size=4)
        if cm is None:
            boolean.append(mood)
        else:
            sizes.append(len(cm.domain))
            if len(cm.domain) == 3:
                needs3 = {"mood": [mood[0], mood[1]], "premises": [list(p) for p in sy.premises(mood)[0]],
                          "conclusion": list(sy.premises(mood)[1])}
        if fol.countermodel(ps + imp, c, max_size=4) is None:
            trad.append(mood)
    assert len(boolean) == 15 and len(trad) == 24
    assert set(boolean) == {m for m in sy.all_moods() if sy.valid(m)}
    assert set(trad) == set(sy.NAMES)
    return {"boolean": len(boolean), "traditional": len(trad), "needs3": needs3,
            "max_countermodel": max(sizes), "countermodel_sizes": {str(k): sizes.count(k) for k in sorted(set(sizes))}}


def compute_tableaux() -> dict:
    out = {}
    cases = {
        "drinker": ([], "exists x (D(x) -> forall y D(y))"),
        "horses": (["forall x (H(x) -> A(x))"], "forall x ((exists y (Hd(x, y) & H(y))) -> exists y (Hd(x, y) & A(y)))"),
        "barbara": (["forall x (M(x) -> P(x))", "forall x (S(x) -> M(x))"], "forall x (S(x) -> P(x))"),
        "romeo": (["forall x forall y (L(x, y) -> forall z L(z, x))", "L(romeo, juliet)"], "L(me, you)"),
    }
    for k, (ps, c) in cases.items():
        r = fol.prove([fol.parse(p) for p in ps], fol.parse(c))
        assert r.closed, k
        out[k] = {"premises": ps, "conclusion": c, "closed": r.closed, "branches": r.branches,
                  "steps": [[rule, fol.show(f), d] for rule, f, d in r.steps] if len(r.steps) < 100 else [],
                  "n_steps": len(r.steps)}
    ps, c = ["exists x (S(x) & P(x))", "exists x (P(x) & M(x))"], "exists x (S(x) & M(x))"
    r = fol.prove([fol.parse(p) for p in ps], fol.parse(c))
    assert not r.closed and not r.gave_up and r.countermodel is not None
    out["open"] = {"premises": ps, "conclusion": c, "closed": False, "branches": r.branches,
                   "steps": [[rule, fol.show(f), d] for rule, f, d in r.steps],
                   "countermodel": {"domain": list(r.countermodel.domain),
                                    "preds": {k: sorted(v) for k, v in r.countermodel.preds.items()}}}
    cm = fol.countermodel([fol.parse(AE)], fol.parse(EA))
    r = fol.prove([fol.parse(AE)], fol.parse(EA))
    assert not r.closed and r.gave_up         # the tree never closes: each person needs a new one to love
    out["swap"] = {"premise": AE, "conclusion": EA, "countermodel": sorted(map(list, cm.preds["L"])),
                   "size": len(cm.domain), "tableau_gave_up": r.gave_up,
                   "tableau_steps": [[rule, fol.show(f), d] for rule, f, d in r.steps]}
    return out


def _random_monadic(rng):
    """A conjunction of 1-5 existential demands (some x with this mix of P, Q and their negations) and, sometimes,
    a universal constraint: sentences whose smallest models range from 1 to 4 elements."""
    lit = lambda name, pos, v: ("P", name, (v,)) if pos else ("not", ("P", name, (v,)))  # noqa: E731
    parts = []
    for _ in range(rng.randint(1, 5)):
        parts.append(("ex", "x", ("and", lit("P", rng.random() < 0.5, "x"), lit("Q", rng.random() < 0.5, "x"))))
    if rng.random() < 0.4:
        parts.append(("all", "x", ("or", lit("P", rng.random() < 0.5, "x"), lit("Q", rng.random() < 0.5, "x"))))
    f = parts[0]
    for q in parts[1:]:
        f = ("and", f, q)
    return f


def compute_monadic() -> dict:
    rng = random.Random(3)
    sizes = []
    unsat = 0
    tried = 0
    while len(sizes) < 300 and tried < 2000:
        tried += 1
        f = _random_monadic(rng)
        M = fol.find_model([f], max_size=5)
        if M is None:
            unsat += 1
            continue
        sizes.append(len(M.domain))
    assert max(sizes) <= 4                     # 2^k with k = 2 predicates
    return {"k": 2, "bound": 4, "satisfiable": len(sizes), "unsatisfiable_up_to_5": unsat,
            "smallest_model_sizes": {str(s): sizes.count(s) for s in sorted(set(sizes))}}


def compute_henkin() -> dict:
    """Henkin's construction in miniature: a consistent set, a witness for its existential, then every atomic
    sentence over the names decided in turn (kept if still satisfiable, denied if not), and the term model read off."""
    gamma = ["exists x L(a, x)", "forall x ~L(x, x)"]
    witness = "L(a, c)"                                   # the Henkin witness c for 'exists x L(a, x)'
    star = [fol.parse(g) for g in gamma] + [fol.parse(witness)]
    decided = []
    for at in ["L(a, a)", "L(a, c)", "L(c, a)", "L(c, c)"]:
        f = fol.parse(at)
        keep = fol.find_model(star + [f], max_size=3) is not None
        star.append(f if keep else ("not", f))
        decided.append([at, keep])
    names = ["a", "c"]
    L = {tuple(fol.parse(at)[2]) for at, keep in decided if keep}
    M = fol.Structure(names, {"L": L}, {}, {n: n for n in names})
    assert all(fol.holds(fol.parse(g), M) for g in gamma)
    return {"gamma": gamma, "witness": witness, "decided": decided, "domain": names, "L": sorted(map(list, L))}


def at_least(n: int) -> str:
    """'There are at least n things': n variables, pairwise different."""
    xs = [f"x{i}" for i in range(1, n + 1)]
    diff = " & ".join(f"~{a} = {b}" for a, b in itertools.combinations(xs, 2)) or "x1 = x1"
    return "".join(f"exists {x} " for x in xs) + f"({diff})"


def compute_compact() -> dict:
    """The sentences 'at least n things', checked on structures of sizes 1-6: each finite set of them has a finite
    model, while together they have only infinite models."""
    grid = []
    for n in range(1, 6):
        f = fol.parse(at_least(n))
        grid.append([fol.holds(f, fol.Structure(range(k), {})) for k in range(1, 7)])
    assert all(grid[n - 1][k - 1] == (k >= n) for n in range(1, 6) for k in range(1, 7))
    return {"sizes": list(range(1, 7)), "grid": grid, "tex": {n: fol.show(fol.parse(at_least(n)), tex=True)
                                                            for n in (2, 3)}}


INFINITY = ("forall x exists y R(x, y) & forall x ~R(x, x) & "
            "forall x forall y forall z (R(x, y) & R(y, z) -> R(x, z))")


def compute_infinity() -> dict:
    """An axiom of infinity in pure logic: every element has a successor, R is irreflexive and transitive. True in
    (N, <); no finite model, so its negation is invalid yet has no finite countermodel."""
    f = fol.parse(INFINITY)
    checked = []
    for n in range(1, 5):
        checked.append([n, 2 ** (n * n), fol.find_model([f], max_size=n, min_size=n) is None])
    assert all(none for _, _, none in checked)
    # (N, <) restricted: in every finite initial segment the last element has no successor
    return {"formula": INFINITY, "tex": fol.show(f, tex=True), "checked": checked}


def compute_atp() -> dict:
    """Unification (with the occurs check failing) and a first-order resolution refutation of 'everybody loves a
    lover; Romeo loves Juliet; so I love you', against the tableau's blind search."""
    def tr(a, b):
        t = []
        s = fol.unify(fol.parse(a), fol.parse(b), trace=t)
        out = []
        for step in t:
            if step[0] == "occurs":
                out.append(["occurs", step[1], fol.show(("P", "_", (step[2],)))[2:-1]])
            else:
                out.append([step[0], fol.show(("P", "_", (fol.resolve_term(step[1], s or {}),)))[2:-1]])
        return {"a": a, "b": b, "ok": s is not None, "steps": out}

    cl_src = ["~L(x, y) | L(z, x)", "L(romeo, juliet)", "~L(me, you)"]
    cl = [fol.parse_clause(c) for c in cl_src]
    ok, der = fol.resolution(cl)
    assert ok
    proof = fol.resolution_proof(cl, der)
    assert [p[1] for p in proof[3:]] == ["L(x, romeo)", "¬L(you, x)", "□"]
    return {"unify": tr("Knows(john, x)", "Knows(y, mother(y))"), "occurs": tr("Knows(x, x)", "Knows(y, mother(y))"),
            "clauses": cl_src, "derived": len(der),
            "proof": [[n, c, list(ps), u] for n, c, ps, u in proof]}


SKOLEM = [
    ("C", r"ZFC has a countable model (Löwenheim--Skolem, if ZFC is consistent)", "c"),
    ("U", r"ZFC proves: there are uncountably many real numbers", "u"),
    ("T", r"what ZFC proves is true in every model of ZFC", "t"),
    ("A", r"`uncountable' means the same inside a model as outside it", "a"),
]


def compute_skolem() -> dict:
    claims = {k: prop.parse(f) for k, _, f in SKOLEM}
    bg = [prop.parse("(c & u & t & a) -> F"), prop.parse("~F")]
    r = prop.mus_mcs(claims, bg)
    assert r["mus"] == [("C", "U", "T", "A")]
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in SKOLEM], **r}


def ef_duplicator_wins(m: int, n: int, k: int) -> bool:
    """The k-round Ehrenfeucht-Fraisse game on the linear orders 0 < 1 < ... < m-1 and 0 < ... < n-1: does the
    duplicator have a winning strategy (so no sentence of quantifier depth k tells the two orders apart)?"""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def win(pairs, k):
        if k == 0:
            return True
        for side in (0, 1):
            for e in range(m if side == 0 else n):
                ok = False
                for f in range(n if side == 0 else m):
                    a, b = (e, f) if side == 0 else (f, e)
                    if all((a < x) == (b < y) and (a == x) == (b == y) for x, y in pairs):
                        if win(tuple(sorted(set(pairs + ((a, b),)))), k - 1):
                            ok = True
                            break
                if not ok:
                    return False
        return True
    return win((), k)


def compute_ef() -> dict:
    """Ehrenfeucht-Fraisse games on finite linear orders of lengths 1-9, for 2 and 3 rounds: the duplicator wins
    exactly when the lengths are equal or both at least 2^k - 1, so 'even length' is not first-order."""
    grids = {}
    for k in (2, 3):
        g = [[ef_duplicator_wins(m, n, k) for n in range(1, 10)] for m in range(1, 10)]
        assert all(g[m - 1][n - 1] == (m == n or min(m, n) >= 2 ** k - 1) for m in range(1, 10) for n in range(1, 10))
        grids[k] = g
    return {"sizes": list(range(1, 10)), "grids": grids}


BEARD = [
    ("N", r"`Pegasus does not exist' is true", "n"),
    ("A", r"that sentence is about Pegasus", "a"),
    ("B", r"a true sentence about something needs that thing to have being, in some sense", "b"),
    ("E", r"whatever has being exists", "e"),
]


def compute_beard() -> dict:
    """Plato's beard (Quine 1948) as an inconsistent set: the four exits are four schools."""
    claims = {k: prop.parse(f) for k, _, f in BEARD}
    bg = [prop.parse("(n & a & b) -> h"), prop.parse("(h & e) -> x"), prop.parse("n -> ~x")]
    r = prop.mus_mcs(claims, bg)
    assert r["mus"] == [("N", "A", "B", "E")] and len(r["mcs"]) == 4
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in BEARD], **r}


ITEMS = {"love": compute_love, "capture": compute_capture, "counting": compute_counting, "russell": compute_russell,
         "moods": compute_moods, "tableaux": compute_tableaux, "monadic": compute_monadic, "skolem": compute_skolem, "henkin": compute_henkin,
         "compact": compute_compact, "infinity": compute_infinity,
         "atp": compute_atp, "beard": compute_beard,
         "ef": compute_ef}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
