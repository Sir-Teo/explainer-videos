"""Precompute everything in Part 8 of *Philosophy, Built* ("The Liar": truth and paradox).

    python -m videos.philosophy.philosophy8.compute            # everything missing (a few seconds)

Items:
    tschema     the liar derived from the T-schema, as propositional logic: unsatisfiable (Part 2's SAT solver)
    grelling    autological and heterological adjectives, computed; 'heterological' has no consistent value
    kripke      the toy world, its references, and Kripke's jump stage by stage to the least fixed point
    fixed       every fixed point of the jump; grounded, ungrounded and paradoxical sentences; the intrinsic point
    revenge     the exclusion liar: the jump never settles, and no fixed point exists
    revision    revision sequences from three starting hypotheses; the verdicts over all 8,192 starts
    yablo       Yablo's sequence truncated to n sentences: exactly one consistent assignment, the last one true
    lp          the same jump read with gluts: the liar both true and false (Priest)
    curry       Curry's sentence: classically it proves anything; in the fixed point it is neither
    liarprice   the liar as a Price List: classical logic, the T-schema, self-reference, no true contradictions
    exam        the surprise exam: the students' backward elimination
    moore       Moore's paradox in belief logic: saying it is consistent, believing it is not (KD4)
    tarskidef   Tarski's satisfaction clauses on a three-object model; truth for every sentence up to depth 2
    st          strict-tolerant consequence: the liar's two halves are valid, their composition is not
    schema      the T-biconditionals in the least fixed point: undesignated in K3, designated in LP
    announce    the surprise exam as repeated public announcement (Gerbrandy)
    programs    the toy world as recursive programs: the ungrounded sentences never return
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import truth as Tr

CACHE = Cache("philosophy8")
load = CACHE.load


def compute_tschema() -> dict:
    # l: 'the liar is true'. The liar says ~T(L); the T-schema then gives T(L) <-> ~T(L).
    return {"formula": "l <-> ~l", "sat": prop.satisfiable([prop.parse("l <-> ~l")])}


def compute_grelling() -> dict:
    return Tr.grelling()


def compute_kripke() -> dict:
    stages = Tr.kripke_stages(Tr.WORLD)
    return {"names": list(Tr.WORLD), "gloss": Tr.GLOSS, "refs": Tr.refs(Tr.WORLD), "stages": stages}


def compute_fixed() -> dict:
    fps = Tr.fixed_points(Tr.WORLD)
    return {"fixed": fps, "classes": Tr.classify(Tr.WORLD), "intrinsic": Tr.intrinsic(Tr.WORLD),
            "lfp": Tr.least_fixed_point(Tr.WORLD)}


def compute_revenge() -> dict:
    return {"iterates": Tr.iterate(Tr.REVENGE, 6), "fixed": Tr.all_fixed_points(Tr.REVENGE)}


def compute_revision() -> dict:
    names = list(Tr.WORLD)
    starts = {"all false": {n: False for n in names}, "all true": {n: True for n in names},
              "mixed": {n: (i % 2 == 0) for i, n in enumerate(names)}}
    seqs = {k: Tr.revision(Tr.WORLD, h, 6) for k, h in starts.items()}
    return {"names": names, "seqs": seqs, "verdicts": Tr.revision_verdicts(Tr.WORLD), "starts": 2 ** len(names)}


def compute_yablo() -> dict:
    out = {}
    for n in range(1, 9):
        sols = Tr.yablo_solutions(n)
        out[str(n)] = [[k for k, v in s.items() if v] for s in sols]
    return {"solutions": out}


def compute_lp() -> dict:
    lfp = Tr.least_fixed_point(Tr.WORLD)
    return {"glut": {n: ("b" if v == "n" else v) for n, v in lfp.items()}}


def compute_curry() -> dict:
    world = {"C": ("imp", ("T", "C"), ("fact", False))}
    # classically: C <-> (C -> q) entails q
    ent = prop.entails([prop.parse("c <-> (c -> q)")], prop.parse("q"))[0]
    return {"kleene": Tr.least_fixed_point(world)["C"], "classical_entails_q": bool(ent),
            "fixed": Tr.all_fixed_points(world)}


LIAR = [("C", r"classical logic: \ excluded middle and the usual rules", "c"),
        ("T", r"the T-schema: \ `$A$' is true iff $A$, \ for every sentence", "t"),
        ("S", r"self-reference: \ the language can say `this sentence is not true'", "s"),
        ("N", r"no contradiction is true", "n")]


def compute_liarprice() -> dict:
    claims = {k: prop.parse(f) for k, _, f in LIAR}
    bg = [prop.parse("(c & t & s & n) -> F"), prop.parse("~F")]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in LIAR], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_exam() -> dict:
    return {"struck": Tr.surprise_exam(5), "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]}


def compute_moore() -> dict:
    return Tr.moore()


def compute_tarskidef() -> dict:
    ss = Tr.tarski_sentences(2)
    pick = [("some", "x", ("White", "x")), ("all", "x", ("White", "x")), ("not", ("some", "x", ("Green", "x"))),
            ("all", "x", ("not", ("Green", "x"))), ("some", "x", ("not", ("Black", "x")))]
    return {"count": len(ss), "true": sum(Tr.tarski_true(f) for f in ss),
            "examples": [[Tr.tarski_show(f), Tr.tarski_true(f)] for f in pick],
            "domain": Tr.TARSKI_DOMAIN, "predicates": {k: sorted(v) for k, v in Tr.TARSKI_PREDICATES.items()}}


def compute_st() -> dict:
    return Tr.st_demo()


def compute_schema() -> dict:
    return {"values": Tr.t_schema_values(Tr.WORLD)}


def compute_announce() -> dict:
    return {"steps": Tr.exam_announcements(5), "wednesday_after_one": Tr.surprise_holds(3, {1, 2, 3, 4})}


def compute_programs() -> dict:
    return {"runs": Tr.run_definitions(), "lfp": Tr.least_fixed_point(Tr.WORLD)}


ITEMS = {"tschema": compute_tschema, "grelling": compute_grelling, "kripke": compute_kripke, "fixed": compute_fixed,
         "revenge": compute_revenge, "revision": compute_revision, "yablo": compute_yablo, "lp": compute_lp,
         "curry": compute_curry, "liarprice": compute_liarprice, "exam": compute_exam, "moore": compute_moore,
         "tarskidef": compute_tarskidef, "st": compute_st, "schema": compute_schema, "announce": compute_announce,
         "programs": compute_programs}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
