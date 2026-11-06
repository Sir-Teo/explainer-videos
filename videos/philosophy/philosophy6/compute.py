"""Precompute everything in Part 6 of *Philosophy, Built* ("Paradise and Paradox": sets and the infinite).

    python -m videos.philosophy.philosophy6.compute            # everything missing (a few seconds)

Items:
    hotel       Galileo's squares and Hilbert's hotel: the first pairings of each bijection
    pairing     Cantor's pairing of ℕ × ℕ on a 6 × 6 grid; the Calkin–Wilf tree and its enumeration of the rationals
    diagonal    eight listed binary 'reals' and the diagonal that escapes them all
    cantor      every function from an n-element set to its power set misses the diagonal set, n = 1..4
    russell     Russell's set as a propositional atom: r ↔ ¬r is unsatisfiable; Curry's c ↔ (c → q) entails any q
    hf          the first sixteen hereditarily finite sets under Ackermann's coding; von Neumann's and Zermelo's
                numerals; the sizes of V_0 .. V_5; Kuratowski's pairs checked
    ordinals    ordinal arithmetic in Cantor normal form: non-commutativity, and a ladder of ordinals up to ω^ω^ω
    goodstein   Goodstein's sequences from 3 and 4, in hereditary base, with their strictly falling ordinals
    hydra       Hercules and the hydra: a small battle drawn blow by blow; the number of blows for a neck of k heads
    freegroup   the free group on a, b: reduced words to length 3 for the Cayley graph; the paradoxical split
    forcing     a generic path that meets a dense set for each of six ground reals, and so differs from all of them
    hilbert     Hilbert's space-filling curve, orders 1 to 5; Cantor's digit interleaving of the square onto the line
    chprice     the continuum as a Price List: realism, provability from justified axioms, and no new axioms
    game        Zermelo (1913): noughts and crosses solved by backward induction
"""

from __future__ import annotations

import random

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import sets as S

CACHE = Cache("philosophy6")
load = CACHE.load


def compute_hotel() -> dict:
    return {"squares": [[n, n * n] for n in range(1, 11)], "plus_one": [[n, n + 1] for n in range(1, 9)],
            "double": [[n, 2 * n] for n in range(1, 9)]}


def compute_pairing() -> dict:
    grid = [[S.cantor_pair(x, y) for x in range(6)] for y in range(6)]
    assert sorted(v for row in grid for v in row)[:21] == list(range(21))
    levels = [[(1, 1)]]
    for _ in range(3):
        nxt = []
        for a, b in levels[-1]:
            nxt += [(a, a + b), (a + b, b)]
        levels.append(nxt)
    cw = S.calkin_wilf(15)
    assert cw == [q for lv in levels for q in lv]
    return {"grid": grid, "tree": levels, "sequence": cw}


def compute_diagonal() -> dict:
    rng = random.Random(1874)
    rows = [[rng.randint(0, 1) for _ in range(8)] for _ in range(8)]
    d = S.diagonal(rows)
    assert all(d != r for r in rows)
    return {"rows": rows, "diagonal": d}


def compute_cantor() -> dict:
    return {"checks": [S.cantor_check(n) for n in (1, 2, 3, 4)]}


def compute_russell() -> dict:
    r = prop.parse("r <-> ~r")
    curry = prop.entails([prop.parse("c <-> (c -> q)")], prop.parse("q"))[0]
    return {"russell_satisfiable": prop.satisfiable([r]), "curry_entails_q": curry}


def compute_hf() -> dict:
    sets = [{"code": i, "tex": S.show_set(S.ackermann_decode(i), tex=True), "rank": S.rank(S.ackermann_decode(i)),
             "bits": format(i, "b")} for i in range(16)]
    vn = [{"n": n, "code": S.ackermann_code(S.von_neumann(n)), "tex": S.show_set(S.von_neumann(n), tex=True)}
          for n in range(5)]
    ze = [{"n": n, "code": S.ackermann_code(S.zermelo_numeral(n)), "tex": S.show_set(S.zermelo_numeral(n), tex=True)}
          for n in range(5)]
    sizes = [S.V_size(k) for k in range(6)]
    assert [len(S.V(k)) for k in range(5)] == sizes[:5]
    return {"sets": sets, "von_neumann": vn, "zermelo": ze, "V_sizes": sizes, "kuratowski": S.kuratowski_check(16),
            "V3": [S.show_set(x, tex=True) for x in sorted(S.V(3), key=S.ackermann_code)]}


def compute_ordinals() -> dict:
    w, one, two = S.OMEGA, S.ONE, S.Ord.nat(2)
    facts = {"1+w = w": one + w == w, "w+1 > w": w < w + one, "2w = w": two * w == w, "w2 = w+w": w * two == w + w,
             "w*w = w^2": w * w == S.Ord.omega_power(two)}
    assert all(facts.values())
    ladder = [S.Ord.nat(0), S.Ord.nat(1), S.Ord.nat(2), w, w + one, w + two, w * two, w * two + one, w * S.Ord.nat(3),
              S.Ord.omega_power(two), S.Ord.omega_power(two) + w, S.Ord.omega_power(S.Ord.nat(3)),
              S.Ord.omega_power(w), S.Ord.omega_power(w) + one, S.Ord.omega_power(w + one),
              S.Ord.omega_power(S.Ord.omega_power(two)), S.Ord.omega_tower(3)]
    assert all(a < b for a, b in zip(ladder, ladder[1:]))
    return {"facts": facts, "ladder": [o.tex() for o in ladder]}


def _g(n, steps):
    out = []
    for t in S.goodstein(n, steps):
        out.append({"base": t["base"], "value": t["value"], "tex": t["tex"], "ordinal": t["ordinal"].tex()})
    return out


def compute_goodstein() -> dict:
    g3 = S.goodstein(3, 10)
    g4 = S.goodstein(4, 14)
    for g in (g3, g4):
        ords = [t["ordinal"] for t in g]
        assert all(b < a for a, b in zip(ords, ords[1:]))
    return {"g3": _g(3, 10), "g4": _g(4, 14), "g19": _g(19, 4)}


def compute_hydra() -> dict:
    h = (((), ()),)
    r = S.hydra_battle(h, record=14)
    hist = [{"step": x["step"], "size": x["size"], "ordinal": x["ordinal"].tex(), "tree": x["tree"]} for x in r["history"]]
    counts = []
    for k in (1, 2, 3, 4):
        n = S.hydra2_steps(k, cap=10 ** 3000)
        counts.append({"k": k, "steps": None if n is None else str(n), "ordinal": S.Ord.omega_power(S.Ord.nat(k)).tex()})
    assert r["steps"] == 13 and counts[2]["steps"] == "22539988369405" and counts[3]["steps"] is None
    return {"battle": hist, "steps": r["steps"], "counts": counts}


def compute_freegroup() -> dict:
    ws = S.words(3)
    return {"words": ws, "check": S.paradoxical_check(6)}


def compute_forcing() -> dict:
    rng = random.Random(1963)
    ground = [[rng.randint(0, 1) for _ in range(8)] for _ in range(6)]
    r = S.generic_real(ground, 8)
    assert r["differs"]
    return {"ground": ground, **r}


def _hilbert(order: int) -> list:
    """The points of Hilbert's curve of the given order in the unit square (the classic d2xy recursion)."""
    n = 2 ** order
    pts = []
    for d in range(n * n):
        x = y = 0
        t = d
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x, y = s - 1 - x, s - 1 - y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        pts.append([(x + 0.5) / n, (y + 0.5) / n])
    return pts


def compute_hilbert() -> dict:
    curves = {str(k): _hilbert(k) for k in range(1, 6)}
    for k, c in curves.items():
        assert len(c) == 4 ** int(k)
        assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1.0001 / 2 ** int(k) for a, b in zip(c, c[1:]))
    x, y = "0.1415926", "0.7182818"
    z = "0." + "".join(a + b for a, b in zip(x[2:], y[2:]))
    return {"curves": curves, "x": x, "y": y, "z": z}


CHPRICE = [("R", r"realism: \ CH has a determinate truth value", "r"),
           ("K", r"every mathematical truth follows from justified axioms", "k"),
           ("N", r"no new justified axiom will settle CH", "n")]


def compute_chprice() -> dict:
    claims = {k: prop.parse(f) for k, _, f in CHPRICE}
    # the background is a theorem: CH is independent of ZFC and of the known large cardinals (Gödel, Cohen,
    # Lévy–Solovay); so with K and N, neither CH nor its negation is a truth, contradicting R
    bg = [prop.parse("(r & k & n) -> F"), prop.parse("~F")]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in CHPRICE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_game() -> dict:
    return S.tictactoe()


ITEMS = {"hotel": compute_hotel, "pairing": compute_pairing, "diagonal": compute_diagonal, "cantor": compute_cantor,
         "russell": compute_russell, "hf": compute_hf, "ordinals": compute_ordinals, "goodstein": compute_goodstein, "hydra": compute_hydra,
         "freegroup": compute_freegroup, "forcing": compute_forcing, "hilbert": compute_hilbert, "chprice": compute_chprice, "game": compute_game}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
