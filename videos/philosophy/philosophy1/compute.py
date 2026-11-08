"""Precompute everything in Part 1 of *Philosophy, Built* ("Calculemus": arguments, the Greeks, syllogistic,
Llull and Leibniz).

    python -m videos.philosophy.philosophy1.compute            # everything missing (a few seconds)

Results are cached in ``.cache/philosophy1/<name>.json``; scenes call ``load(name)``.

Items:
    zeno        Achilles and the tortoise in exact fractions: each stage of the chase, the partial sums, the meeting
                time 100/9 s; the dichotomy's 1 - 2^-n; Thomson's lamp's states
    meno        the slave boy's squares: the guesses (side 4, side 3) and the diagonal (area 8)
    line        Plato's divided line cut twice in one ratio: the two middle segments always come out equal
    euthyphro   the Euthyphro dilemma as an inconsistent set: its minimal inconsistent set and the five exits
    moods       all 256 moods: valid with empty terms allowed (15), with existential import (24), their names,
                countermodels for the famous fallacies
    leibniz     Leibniz's characteristic numbers (1679): an illustrative assignment, and every mood checked
                against every assignment built from the primes 2, 3, 5 (the 24 traditional moods survive, exactly)
    llull       Llull's Ars brevis: nine principles, 36 pairs, 84 triples, 729 settings of three wheels
    hexagrams   the 64 hexagrams in Shao Yong's order, read as binary 0 ... 63 (Leibniz 1703)
    forms       arguments checked by form: valid and invalid, with countermodels
    unicorn     the unicorn argument (Darapti) as an inconsistent set: its four exits
    thirdman    the Third Man (Parmenides 132a, after Vlastos 1954) as an inconsistent set
    conversion  immediate inferences checked over all Venn models: which sentences convert, with and without import
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import comb

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop, syllogism as sy

CACHE = Cache("philosophy1")
load = CACHE.load


def fr(x: Fraction) -> list:
    return [x.numerator, x.denominator]


def compute_zeno() -> dict:
    va, vt, head = Fraction(10), Fraction(1), Fraction(100)  # metres per second, metres
    stages = []
    a, t_pos, t = Fraction(0), head, Fraction(0)
    for k in range(12):
        dt = (t_pos - a) / va             # Achilles runs to where the tortoise was
        t += dt
        a = t_pos
        t_pos = t_pos + vt * dt
        stages.append({"k": k + 1, "dt": fr(dt), "t": fr(t), "achilles": fr(a), "gap": fr(t_pos - a)})
    meet = head / (va - vt)
    assert meet == Fraction(100, 9)
    assert abs(float(meet) - float(t)) < 1e-9 * 10
    dich = [fr(1 - Fraction(1, 2 ** n)) for n in range(1, 16)]
    lamp = [{"t": fr(1 - Fraction(1, 2 ** n)), "on": n % 2 == 0} for n in range(0, 10)]
    return {"speeds": [10, 1], "head": 100, "stages": stages, "meet": fr(meet), "meet_float": float(meet),
            "dichotomy": dich, "lamp": lamp}


def compute_meno() -> dict:
    side = 2
    tries = [{"side": 4, "area": 16, "who": "boy"}, {"side": 3, "area": 9, "who": "boy"},
             {"side": "diagonal", "area": 8, "who": "Socrates"}]
    # the diagonal square is made of four half-squares of the original: 4 * (area / 2) = 2 * area
    assert 4 * (side * side) // 2 == 8
    return {"side": side, "area": side * side, "target": 2 * side * side, "tries": tries,
            "diagonal": 2 ** 0.5 * side}


def compute_line() -> dict:
    out = []
    for k in (Fraction(3, 2), Fraction(2), Fraction(3), Fraction(5, 2)):
        x = k / (1 + k)                    # the first cut: ratio k : 1
        a, b = x * k / (1 + k), x / (1 + k)
        c, d = (1 - x) * k / (1 + k), (1 - x) / (1 + k)
        assert b == c                      # the two middle segments are equal, whatever k
        out.append({"k": fr(k), "segments": [fr(a), fr(b), fr(c), fr(d)]})
    return {"cuts": out}


EUTHYPHRO = [
    ("D", r"The pious is the god-loved: one thing, two names", "d"),
    ("E1", r"The gods love the pious because it is pious", "e1"),
    ("E2", r"The god-loved is god-loved because the gods love it", "e2"),
    ("Sub", r"If they are one thing, either name may stand in a `because'", "(d & e1) -> x"),
    ("Asym", r"Nothing is so because of something that is so because of it", "x -> ~e2"),
]


def compute_euthyphro() -> dict:
    claims = {k: prop.parse(f) for k, _, f in EUTHYPHRO}
    r = prop.mus_mcs(claims)
    assert r["mus"] == [tuple(k for k, _, _ in EUTHYPHRO)]
    assert r["mcs"] == [(k,) for k, _, _ in EUTHYPHRO]
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in EUTHYPHRO], **r,
            "note": "x: the gods love it because it is god-loved (Sub swaps 'pious' for 'god-loved' in E1)"}


def _model_rows(m):
    return sorted([list(r) for r in m])


def compute_moods() -> dict:
    moods = sy.all_moods()
    rows = []
    for m in moods:
        b, t = sy.valid(m), sy.valid(m, existential=True)
        rows.append({"figure": m[0], "mood": m[1], "boolean": b, "traditional": t, "name": sy.NAMES.get(m)})
    boolean = [r for r in rows if r["boolean"]]
    trad = [r for r in rows if r["traditional"]]
    assert len(boolean) == 15 and len(trad) == 24
    by_fig = {f: {"boolean": sum(r["boolean"] for r in rows if r["figure"] == f),
                  "traditional": sum(r["traditional"] for r in rows if r["figure"] == f)} for f in (1, 2, 3, 4)}
    # undistributed middle: figure 2 AAA (all P are M, all S are M, so all S are P) -- a countermodel
    cm = sy.countermodel((2, "AAA"))
    darapti = sy.countermodel((3, "AAI"))         # valid only if the middle term is inhabited
    return {"rows": rows, "boolean": [[r["figure"], r["mood"], r["name"]] for r in boolean],
            "traditional": [[r["figure"], r["mood"], r["name"]] for r in trad], "by_figure": by_fig,
            "undistributed": _model_rows(cm), "darapti_empty": _model_rows(darapti),
            "models": 256}


def compute_leibniz() -> dict:
    # an illustrative assignment in Leibniz's scheme (not his own numbers): each term a pair (+, -) of coprime numbers
    terms = {"animal": (2, 5), "rational": (3, 7), "man": (6, 35), "stone": (11, 2)}
    checks = [("A", "man", "animal"), ("A", "man", "rational"), ("I", "animal", "rational"), ("E", "man", "stone"),
              ("A", "animal", "man")]
    shown = [{"kind": k, "x": x, "y": y, "holds": sy.leibniz_holds(k, terms[x], terms[y])} for k, x, y in checks]
    assert [s["holds"] for s in shown] == [True, True, True, True, False]
    pairs = sy.leibniz_pairs((2, 3, 5))
    surv = [m for m in sy.all_moods() if sy.leibniz_countermodel(m) is None]
    assert set(surv) == set(sy.NAMES)
    # a counterexample in numbers for the undistributed middle
    ce = sy.leibniz_countermodel((2, "AAA"))
    return {"terms": {k: list(v) for k, v in terms.items()}, "shown": shown, "pairs": len(pairs),
            "assignments": len(pairs) ** 3, "survivors": [[f, m, sy.NAMES[(f, m)]] for f, m in surv],
            "undistributed_ce": {k: list(v) for k, v in ce.items()}}


def compute_llull() -> dict:
    principles = [("B", "Bonitas", "goodness"), ("C", "Magnitudo", "greatness"), ("D", "Eternitas", "eternity"),
                  ("E", "Potestas", "power"), ("F", "Sapientia", "wisdom"), ("G", "Voluntas", "will"),
                  ("H", "Virtus", "virtue"), ("I", "Veritas", "truth"), ("K", "Gloria", "glory")]
    letters = [p[0] for p in principles]
    pairs = ["".join(c) for c in itertools.combinations(letters, 2)]
    triples = ["".join(c) for c in itertools.combinations(letters, 3)]
    assert len(pairs) == comb(9, 2) == 36 and len(triples) == comb(9, 3) == 84
    return {"principles": principles, "pairs": pairs, "triples": triples, "wheels": 9 ** 3}


def compute_hexagrams() -> dict:
    """Shao Yong's 'Former Heaven' sequence, as Leibniz read it in 1703: yin (broken) = 0, yang (solid) = 1,
    the six lines read as a binary numeral; the sequence runs from all-yin (0) to all-yang (63)."""
    hexes = []
    for n in range(64):
        bits = [(n >> (5 - i)) & 1 for i in range(6)]   # most significant line first
        hexes.append({"n": n, "bits": bits})
    assert hexes[0]["bits"] == [0] * 6 and hexes[63]["bits"] == [1] * 6
    return {"hexagrams": hexes}


def compute_forms() -> dict:
    out = []
    for label, mood, names in [
        ("valid", (1, "AAA"), {"S": "Greeks", "M": "humans", "P": "mortals"}),
        ("same form, other words", (1, "AAA"), {"S": "whales", "M": "fish", "P": "things with gills"}),
        ("invalid", (2, "AAA"), {"S": "dogs", "M": "mortals", "P": "cats"}),
    ]:
        prem, concl = sy.premises(mood)
        cm = sy.countermodel(mood)
        out.append({"label": label, "mood": list(mood), "premises": [sy.describe(k, x, y, names) for k, x, y in prem],
                    "conclusion": sy.describe(*concl, names), "valid": cm is None})
    assert [o["valid"] for o in out] == [True, True, False]
    return {"forms": out}


UNICORN = [
    ("u1", r"`All unicorns are one-horned' is true", "u1"),
    ("u2", r"`All unicorns are horses' is true", "u2"),
    ("V", r"Darapti is valid", "(u1 & u2) -> s"),
    ("ns", r"`Some horses are one-horned' is not true", "~s"),
]


def compute_unicorn() -> dict:
    claims = {k: prop.parse(f) for k, _, f in UNICORN}
    r = prop.mus_mcs(claims)
    assert r["mus"] == [("u1", "u2", "V", "ns")] and len(r["mcs"]) == 4
    darapti = (3, "AAI")
    cm = sy.countermodel(darapti)
    assert cm is not None and sy.valid(darapti, existential=True)
    m_inhabited = any(reg[1] for reg in cm)
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in UNICORN], **r,
            "countermodel": _model_rows(cm), "middle_inhabited": m_inhabited}


THIRDMAN = [
    ("OM", r"One over many: any group of large things has a Form of Largeness over it", "om"),
    ("SP", r"Self-predication: the Form of Largeness is itself large", "sp"),
    ("NI", r"Non-identity: a Form is not one of the things it is over", "ni"),
    ("U", r"Uniqueness: there is exactly one Form of Largeness", "u"),
    ("R", r"OM, SP and NI give a second, third, ... Form (Vlastos 1954)", "(om & sp & ni) -> two"),
    ("Q", r"Uniqueness rules out a second Form", "u -> ~two"),
]


def compute_thirdman() -> dict:
    claims = {k: prop.parse(f) for k, _, f in THIRDMAN}
    bg = [claims.pop("R"), claims.pop("Q")]
    r = prop.mus_mcs(claims, bg)
    assert r["mus"] == [("OM", "SP", "NI", "U")]
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in THIRDMAN if k not in ("R", "Q")],
            "bridges": [t for k, t, _ in THIRDMAN if k in ("R", "Q")], **r}


def compute_conversion() -> dict:
    out = []
    for kind in "AEIO":
        for imp in (False, True):
            ok = all(sy.holds(kind, "P", "S", m) for m in sy.models(imp) if sy.holds(kind, "S", "P", m))
            out.append({"kind": kind, "import": imp, "converts": ok})
    # conversion by limitation: all S are P, so some P are S
    lim = {imp: all(sy.holds("I", "P", "S", m) for m in sy.models(imp) if sy.holds("A", "S", "P", m))
           for imp in (False, True)}
    conv = {(o["kind"], o["import"]): o["converts"] for o in out}
    assert conv[("E", False)] and conv[("I", False)] and not conv[("A", True)] and not conv[("O", True)]
    assert not lim[False] and lim[True]
    return {"simple": out, "limitation": {str(k): v for k, v in lim.items()}}


ITEMS = {"thirdman": compute_thirdman, "conversion": compute_conversion, "unicorn": compute_unicorn, "zeno": compute_zeno, "meno": compute_meno, "line": compute_line, "euthyphro": compute_euthyphro,
         "moods": compute_moods, "leibniz": compute_leibniz, "llull": compute_llull, "hexagrams": compute_hexagrams,
         "forms": compute_forms}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
