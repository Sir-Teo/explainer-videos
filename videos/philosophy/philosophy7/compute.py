"""Precompute everything in Part 7 of *Philosophy, Built* ("The Limits of Proof": Gödel, Turing, Tarski, Löb).

    python -m videos.philosophy.philosophy7.compute            # everything missing (about ten seconds)

Items:
    miu         Hofstadter's MIU system: theorems by number of steps, and the invariant that keeps MU out
    q           Robinson's Q computing 2 + 2 and 2 × 2, axiom by axiom
    recursion   primitive recursive functions built from five combinators; Ackermann's function outgrowing them
    beta        the Chinese remainder theorem (Sunzi's problem) and Gödel's β-function coding a sequence
    numbering   Gödel numbers of formulas, decoded again; the size of the Gödel number of a two-line proof
    quine       a Python quine run and checked; Quine's sentence and a Gödel-style diagonal sentence, checked
    tm          Turing machines: space–time diagrams of the 2- and 4-state champions; every 2-state machine run
    beavers     the busy beaver champions for 2–5 states, simulated (BB(5) = 47,176,870 steps)
    ramsey      R(3,3) = 6: the 12 good colourings of K5, and none of K6, by brute force
    berry       shortest names of numbers in a toy language; the least number not nameable in k symbols
    gl          provability logic: Gödel's and Henkin's fixed points, Löb, and the second theorem, checked on every
                finite GL frame up to four worlds
    minds       the Lucas–Penrose argument as a Price List
    delta0      a truth predicate for bounded sentences: four sentences decided by finite search
"""

from __future__ import annotations

import math

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import arith as A
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy7")
load = CACHE.load


def compute_miu() -> dict:
    levels = A.miu_theorems(5)
    allt = sorted({t for lv in A.miu_theorems(7) for t in lv}, key=lambda x: (len(x), x))
    return {"levels": levels[:5], "count7": len(allt), "mu": "MU" in allt,
            "invariant": all(t.count("I") % 3 for t in allt),
            "examples": [[s, [[t, r] for t, r in A.miu_successors(s)]] for s in ("MI", "MIIII", "MUUI")]}


def compute_q() -> dict:
    out = {}
    for name, t in (("add", ("+", A.numeral(2), A.numeral(2))), ("mul", ("*", A.numeral(2), A.numeral(2)))):
        out[name] = [[A.term_str(s, tex=True), ax] for s, ax in A.q_steps(t)]
    return out


def compute_recursion() -> dict:
    lib = {k: f.size() for k, f in A.PR_LIBRARY.items()}
    vals = {"add": A.PR_ADD(3, 4), "mul": A.PR_MUL(3, 4), "exp": A.PR_EXP(2, 5), "pred": A.PR_PRED(7),
            "fact": A.PR_FACT(5)}
    ack = [[A.ackermann_small(m, n) for n in range(5)] for m in range(4)]
    assert ack == [[A.ackermann(m, n) for n in range(5)] for m in range(4)]
    return {"sizes": lib, "values": vals, "ack": ack, "a40": A.ackermann(4, 0), "a41": A.ackermann(4, 1),
            "a42_digits": A.digits_of_2_pow(65536)}


def compute_beta() -> dict:
    x, M = A.crt(A.SUNZI)
    seq = [2, 3, 5]
    c, d = A.beta_code(seq)
    mods = [1 + (i + 1) * d for i in range(len(seq))]
    return {"sunzi": {"pairs": A.SUNZI, "x": x, "M": M}, "seq": seq, "c": c, "d": d, "mods": mods,
            "check": [A.beta(c, d, i) for i in range(len(seq))]}


def compute_numbering() -> dict:
    table = [[s, A.CODE[s]] for s, _ in A.SYMBOLS] + [[v, A.CODE[v]] for v in A.VARS[:3]]
    f1 = "0=0"
    f2 = "∀x(x+0=x)"
    g1, g2 = A.godel_number(f1), A.godel_number(f2)
    proof = ["0=0", "S0=S0"]
    return {"table": table, "f1": f1, "g1": str(g1), "f1_codes": [A.CODE[t] for t in A.tokens(f1)],
            "f2": f2, "g2_digits": len(str(g2)), "f2_codes": [A.CODE[t] for t in A.tokens(f2)],
            "decoded": A.godel_decode(g2), "proof": proof, "proof_digits": str(A.sequence_digits(proof)),
            "proof_digits_log10": round(math.log10(A.sequence_digits(proof)), 1)}


def compute_quine() -> dict:
    s = A.quine_sentence()
    g = A.diag(A.GODEL_TEMPLATE)
    return {"src": A.QUINE, "out": A.run_python(A.QUINE), "ok": A.quine_check(), "sentence": s,
            "subject_ok": A.quine_subject(s) == s, "template": A.GODEL_TEMPLATE, "godel": g,
            "godel_ok": A.diag_subject(g) == g}


def compute_tm() -> dict:
    st2 = A.space_time(A.CHAMPIONS[2], 6, pad=1)
    st4 = A.space_time(A.CHAMPIONS[4], 107, pad=1)
    search = A.busy_beaver_search(2, 50)
    tm2 = A.parse_tm(A.CHAMPIONS[2])
    rules = [[st, sym, *tm2[(st, sym)]] for st in "AB" for sym in (0, 1)]
    return {"st2": [[r, h, s] for r, h, s in st2], "st4": [[r, h, s] for r, h, s in st4], "search": search,
            "rules2": rules}


def compute_beavers() -> dict:
    out = []
    for n, code in A.CHAMPIONS.items():
        r = A.run_tm_fast(code, 10 ** 8)
        out.append({"n": n, "code": code, "steps": r["steps"], "ones": r["ones"], "halted": r["halted"]})
    return {"champions": out}


def compute_ramsey() -> dict:
    good = A.mono_triangle_free(5)
    none = A.mono_triangle_free(6)
    # the pentagon (red) and pentagram (blue) colouring of K5
    red = [[i, (i + 1) % 5] for i in range(5)]
    blue = [[i, (i + 2) % 5] for i in range(5)]
    return {"k5": good, "k6": none, "red": red, "blue": blue, "k6_colourings": 2 ** 15, "k5_colourings": 2 ** 10}


def compute_berry() -> dict:
    best = A.rpn_values(7)
    grid = [[n, best[n][0] if n in best else 9] for n in range(1, 301)]
    names = {}
    for n in (10, 100, 1000, 92, 239, 729, 4096):
        if n in best:
            names[str(n)] = [best[n][0], A.infix(best[n][1])]
    return {"grid": grid, "berry": {"3": A.berry(3), "5": A.berry(5), "7": A.berry(7)}, "names": names}


def compute_gl() -> dict:
    out = {}
    for k, f in A.GL_FACTS.items():
        ok, n = A.gl_valid(f, 4)
        out[k] = {"formula": f, "valid": ok, "frames": n}
    return out


MINDS = [("M", r"mechanism: \ our mathematical knowledge is what some formal system $F$ proves", "m"),
         ("K", r"we can know that $F$ is consistent", "k"),
         ("C", r"$F$ is in fact consistent", "c")]


def compute_minds() -> dict:
    claims = {k: prop.parse(f) for k, _, f in MINDS}
    # background, a theorem: Gödel II, a consistent F does not prove Con(F); with M and K, F proves Con(F)
    bg = [prop.parse("(m & k & c) -> F"), prop.parse("~F")]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in MINDS], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_delta0() -> dict:
    return {"examples": [{"s": s, "gloss": g, "value": A.delta0_eval(s)} for s, g in A.DELTA0_EXAMPLES]}


ITEMS = {"miu": compute_miu, "q": compute_q, "recursion": compute_recursion, "beta": compute_beta,
         "numbering": compute_numbering, "quine": compute_quine, "tm": compute_tm, "beavers": compute_beavers,
         "ramsey": compute_ramsey, "berry": compute_berry, "gl": compute_gl, "minds": compute_minds,
         "delta0": compute_delta0}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
