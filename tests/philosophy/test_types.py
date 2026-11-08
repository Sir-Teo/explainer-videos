"""Part 9's Reasoner: propositions as types, and the small objects of the philosophy of mathematics."""

from explainer.philosophy.reasoner import mathphil as M
from explainer.philosophy.reasoner import types as T


def test_proofs_are_programs():
    for s, name in T.EXAMPLES:
        t = T.parse_type(s)
        pr = T.prove(t)
        if name in ("excluded middle", "Peirce's law", "double negation out"):
            assert pr is None
            cm = T.countermodel(t)
            assert cm is not None and cm["worlds"] == 2
        else:
            assert pr is not None, name
            assert T.type_of(pr) == t, name
    k = T.prove(T.parse_type("A -> B -> A"))
    assert T.show_term(T.rename(k)) == "λx. λy. x"


def test_normalization_and_transport():
    t = ("app", ("lam", "p", T.parse_type("A & B"), ("pair", ("snd", ("v", "p")), ("fst", ("v", "p")))),
         ("pair", ("v", "a"), ("v", "b")))
    seq = T.normalize(t)
    assert T.show_term(seq[-1]) == "⟨b, a⟩"
    ctx = {"a": T.parse_type("A"), "b": T.parse_type("B")}
    assert all(T.type_of(x, ctx) == T.parse_type("B & A") for x in seq)  # reduction preserves the type
    assert all(T.transport_check().values())
    assert [T.winding_number(T.loop_path(n, 0.8)) for n in (-2, 0, 1, 3)] == [-2, 0, 1, 3]


def test_frege_and_abstraction():
    d = M.frege_numbers(4)
    assert d["class_sizes"] == [1, 4, 6, 4, 1] and d["successor"] == [(0, 1), (1, 2), (2, 3), (3, 4)]
    for row in M.abstraction_demands(5):
        assert row["HP"] == row["n"] + 1 > row["n"] and row["BLV"] == 2 ** row["n"] and row["NP"] == 1
    assert M.hp_model_on_naturals()["ok"]


def test_structures():
    r = M.roots_of_unity()
    assert r["autos"] == [(0, 1, 2, 3), (0, 3, 2, 1)] and r["fixed"] == [0, 2]
    g = M.graph_symmetries()
    assert g["an asymmetric graph"]["autos"] == 1 and g["two points"]["fixed"] == []
    reps = M.representations(M.nominal_facts())
    base = M.LINE_POINTS
    assert len(reps) == 4 and all(len({p[k] / base[k] for k in base if base[k]}) == 1 for p in reps)


def test_examples():
    b = M.bombelli()
    assert b["cube"] == (2, 11) and b["check"] and b["disc"] == "-121"
    digits = M.pi_digits(800)
    assert digits.startswith("3141592653") and M.first_run(digits, "999999") == 762
    t = M.typical()
    assert t[0]["typical"] == ["Edith"] and t[1]["typical"] == [] and t[-1]["typical"] == []
    cyc = {c["cycle"]: c["overlap"] for c in M.cicadas(12, 18)}
    assert sorted(cyc, key=cyc.get)[:2] == [17, 13]
    chis = {k: M.euler(v)["chi"] for k, v in M.POLYHEDRA.items()}
    assert chis == {"tetrahedron": 2, "cube": 2, "octahedron": 2, "twin tetrahedra": 3, "picture frame": 0}
    ms = M.missing_square()
    assert not ms["equal"] and ms["figure2"] == "33"
    assert M.goldbach_checked(20000)["counterexample"] is None
