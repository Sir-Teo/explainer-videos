"""Monochord's neo-Riemannian toolkit (Part 31)."""

from explainer.music.monochord import neoriemann as N

C = (0, "M")


def test_moves_are_involutions_and_parsimonious():
    for t in N.TRIADS:
        for k in "PLR":
            u = N.OPS[k](t)
            assert N.OPS[k](u) == t and u[1] != t[1]
            assert N.common_tones(t, u) == 2 and N.voice_leading(t, u) == (2 if k == "R" else 1)
    assert N.name(N.P(C)) == "Cm" and N.name(N.L(C)) == "Em" and N.name(N.R(C)) == "Am"


def test_groups_dual_and_dihedral():
    G, H = N.plr_group(), N.ti_group()
    assert len(G) == len(H) == 24 and N.commute(G, H)
    assert N.is_simply_transitive(G) and N.is_simply_transitive(H)
    assert {w: N.order(w) for w in ("P", "PL", "PR", "LR")} == {"P": 2, "PL": 3, "PR": 4, "LR": 12}
    assert all(N.apply("R" + "LR" * 3, t) == N.P(t) for t in N.TRIADS)


def test_tonnetz_distances_and_systems():
    assert N.distance_histogram(C) == {0: 1, 1: 3, 2: 6, 3: 8, 4: 5, 5: 1}
    far = [t for t, w in N.shortest_paths(C).items() if len(w) == 5]
    assert [N.name(t) for t in far] == ["Bbm"]
    hexa, octa = N.systems("PL"), N.systems("PR")
    assert [len(s) for s in hexa] == [6] * 4 and [len(s) for s in octa] == [8] * 3
    assert len(N.cycle("RL")) == 24
    assert sorted(N.name(t) for t in N.weitzmann(0)) == sorted(["C", "E", "Ab", "C#m", "Fm", "Am"])


def test_hamiltonian_cycles_by_two_counts():
    assert N.hamiltonian_cycles(("L", "R")) == 1
    assert N.hamiltonian_cycles() == 62


def test_sevenths_and_harmonizer():
    nb = N.seventh_neighbours(("7", 0))
    assert len(nb) == 10 and sum(1 for _, _, c in nb if c == 3) == 1
    assert (("7", 6), 2, 2) in nb                                                         # the tritone substitution
    walk = N.harmonize([0, 7, 9, 7, 5, 4, 2, 0], start=C, end=C)
    assert walk[0] == walk[-1] == C and all(m in N.pcs(t) for m, t in zip([0, 7, 9, 7, 5, 4, 2, 0], walk))
