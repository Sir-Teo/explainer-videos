"""Precompute everything in Part 9 of *Philosophy, Built* ("What Is Mathematics About?").

    python -m videos.philosophy.philosophy9.compute            # everything missing (about half a minute)

Items:
    meno        Socrates and the boy: the guesses for doubling a square, and the square on the diagonal
    frege       Frege's numbers on a domain of four: 16 concepts, 5 numbers (1-4-6-4-1), successor 0 -> ... -> 4
    demands     abstraction principles counted on small domains: Hume's principle, Basic Law V, nuisance
    hpmodel     a model of Hume's principle on the natural numbers: #F = 0 if F is infinite, else |F| + 1
    bombelli    x^3 = 15x + 4 through the square root of -121: (2 + i)^3 = 2 + 11i, and x = 4
    pi          3,000 digits of pi; where six 9s first appear; Brouwer's pattern not yet; Goldbach checked
    brouwer     Brouwer's real number r, to n places, for the six-9s pattern
    curry       the propositional proof search: proofs as lambda terms, type-checked; or a two-world countermodel
    normal      a proof with a detour, normalized step by step; every step keeps its type
    typical     Russell's typical Englishman, level by level, and with every property whatever
    roots       the symmetries of {1, i, -1, -i}: swapping i and -i preserves everything
    graphs      the symmetries of five small graphs; which points the structure alone can pick out
    cicadas     how often an emergence meets a predator's peak, for periods 10 to 20 years
    represent   five points known only by betweenness and congruence; every coordinate system for them
    transport   unary and binary numerals: an equivalence, and a property carried across it
    winding     loops on a circle and their winding numbers
    euler       V - E + F for five polyhedra, and Kepler's urchin
    missing     Curry's missing-square puzzle: slopes and areas
    euclid      'infinitely many primes', misstated and stated: what a checker certifies
    kernel      the size of the Reasoner's proof checker
    bfprice     the Benacerraf-Field puzzle as a Price List
"""

from __future__ import annotations

import inspect

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import mathphil as M
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import types as T

CACHE = Cache("philosophy9")
load = CACHE.load

BF = [("O", r"`7 is prime' is about an object: \ the number 7", "o"),
      ("A", r"that object is abstract: \ outside space and time, \ with no causes", "a"),
      ("K", r"we know that 7 is prime", "k"),
      ("C", r"to know about objects, \ we need a connection to them \ that could explain our reliability", "c")]


def compute_meno() -> dict:
    return {"guesses": M.meno()}


def compute_frege() -> dict:
    return M.frege_numbers(4)


def compute_demands() -> dict:
    return {"rows": M.abstraction_demands(5)}


def compute_hpmodel() -> dict:
    return M.hp_model_on_naturals(7)


def compute_bombelli() -> dict:
    return M.bombelli()


def compute_pi() -> dict:
    d = M.pi_digits(3000)
    return {"digits": d, "six9": M.first_run(d, "999999"), "brouwer": M.first_run(d, "0123456789"),
            "goldbach": M.goldbach_checked(100_000)}


def compute_brouwer() -> dict:
    d = M.pi_digits(800)
    return {"approx": [[n, str(M.brouwer_real(d, "999999", n))] for n in (1, 2, 3, 4, 5, 6, 10, 20)],
            "place": M.first_run(d, "999999")}


def compute_curry() -> dict:
    out = []
    for s, name in T.EXAMPLES:
        t = T.parse_type(s)
        pr = T.prove(t)
        row = {"name": name, "type": T.show_type(t), "tex": T.show_type(t, tex=True)}
        if pr is not None:
            assert T.type_of(pr) == t
            row["term"] = T.show_term(T.rename(pr))
        else:
            row["countermodel"] = T.countermodel(t)
        out.append(row)
    return {"rows": out}


def compute_normal() -> dict:
    t = ("app", ("lam", "p", T.parse_type("A & B"), ("pair", ("snd", ("v", "p")), ("fst", ("v", "p")))),
         ("pair", ("v", "a"), ("v", "b")))
    ctx = {"a": T.parse_type("A"), "b": T.parse_type("B")}
    seq = T.normalize(t)
    return {"steps": [T.show_term(x) for x in seq], "types": [T.show_type(T.type_of(x, ctx)) for x in seq]}


def compute_typical() -> dict:
    return {"levels": M.typical(), "people": M.ENGLISHMEN}


def compute_roots() -> dict:
    return M.roots_of_unity()


def compute_graphs() -> dict:
    return M.graph_symmetries()


def compute_cicadas() -> dict:
    return {"rows": M.cicadas(10, 20)}


def compute_represent() -> dict:
    f = M.nominal_facts()
    reps = M.representations(f)
    return {"hidden": M.LINE_POINTS, "bet": len(f["bet"]), "cong": sorted(f["cong"]), "reps": reps}


def compute_transport() -> dict:
    rows = [[k, T.unary(k), T.binary(k), T.even_unary(T.unary(k))] for k in range(7)]
    return {"rows": rows, **T.transport_check(64)}


def compute_winding() -> dict:
    return {"loops": [[n, T.winding_number(T.loop_path(n, w))] for n, w in ((0, 1.2), (1, 0.5), (2, 0.4), (-1, 0.6))]}


def compute_euler() -> dict:
    return {"rows": {k: M.euler(v) for k, v in M.POLYHEDRA.items()}, "urchin": M.URCHIN}


def compute_missing() -> dict:
    return M.missing_square()


def compute_euclid() -> dict:
    return M.euclid_statements(12)


def compute_kernel() -> dict:
    src = inspect.getsource(T.type_of)
    return {"lines": len([ln for ln in src.splitlines() if ln.strip() and not ln.strip().startswith(('"', '#'))])}


def compute_bfprice() -> dict:
    claims = {k: prop.parse(f) for k, _, f in BF}
    bg = [prop.parse("(o & a & k & c) -> F"), prop.parse("~F")]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in BF], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"meno": compute_meno, "frege": compute_frege, "demands": compute_demands, "hpmodel": compute_hpmodel,
         "bombelli": compute_bombelli, "pi": compute_pi, "brouwer": compute_brouwer, "curry": compute_curry,
         "normal": compute_normal, "typical": compute_typical, "roots": compute_roots, "graphs": compute_graphs,
         "cicadas": compute_cicadas, "represent": compute_represent, "transport": compute_transport,
         "winding": compute_winding, "euler": compute_euler, "missing": compute_missing, "euclid": compute_euclid,
         "kernel": compute_kernel, "bfprice": compute_bfprice}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
