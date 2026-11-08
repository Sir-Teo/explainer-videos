"""Tests for the Reasoner's space and time (Part 25)."""

import math

from explainer.philosophy.reasoner import spacetime as S


def test_bucket_and_shifts():
    b = S.bucket()
    rises = [r["rise_mm"] for r in b["rows"]]
    assert rises[0] == 0 and rises == sorted(rises)
    # z = w^2 r^2 / 2g at the rim
    assert math.isclose(rises[-1], 1000 * 36 * 0.15 ** 2 / (2 * 9.81), rel_tol=1e-3)
    rows = S.shifts()["rows"]
    assert all(r["relationally_same"] for r in rows)
    assert [r["world"] for r in rows if r["inertial_effects"]] == ["rotating"]


def test_incongruent_counterparts():
    i = S.incongruent()
    assert i["left_area"] == -i["right_area"] != 0
    assert i["rigid_sign_changes"] == 0
    assert i["mobius_orientation_flips"] and i["mobius_width_end"] == [-1.0, 0.0, 0.0]


def test_poincare_disk():
    rows = S.disk_triangles()["rows"]
    sums = [r["sum_deg"] for r in rows]
    assert sums == sorted(sums, reverse=True) and sums[0] < 180 and sums[-1] > 0
    for r in rows:
        assert math.isclose(r["area"], math.pi - math.radians(r["sum_deg"]), abs_tol=1e-3)
    # a geodesic through the centre is a diameter; others stay inside the disk
    t = S.hyp_triangle((0.0, 0.5), (0.4, -0.3), (-0.4, -0.3))
    for side in t["sides"].values():
        assert all(x * x + y * y < 1 for x, y in side)
    assert 14 < S.gauss_triangle()["excess_arcsec"] < 16
    w = S.disk_world()["rows"]
    assert all(r["ratio_over_pi"] > 1 for r in w)


def test_relativity():
    rows = {r["v"]: r for r in S.simultaneity()["rows"]}
    assert rows[0.0]["first"] == "together" and rows[0.6]["first"] == "B" and rows[-0.6]["first"] == "A"
    assert all(r["timelike_order_kept"] for r in rows.values())
    rp = S.rietdijk_putnam((0.6, 1.0))
    assert rp["spacelike"] and abs(rp["t_prime"]) < 1e-9


def test_hole_and_ctcs():
    assert S.hole()["outside_fixed"]
    c = S.ctc()
    assert c["grandfather"]["classical_consistent"] == []
    assert c["grandfather"]["deutsch"] == [[0.5, 0.0], [0.0, 0.5]]
    assert c["knowledge"]["classical_consistent"] == [0, 1]


def test_best_matching_removes_the_arbitrary_motion():
    m = S.best_matching()
    assert m["intrinsic_distance"] < 0.2 * m["raw_distance"]
    assert m["intrinsic_distance"] <= m["true_change"] + 1e-9
    assert abs(m["angle_found"] - m["angle_put_in"]) < 0.2


def test_boost_and_clock_transport():
    g = S.galilean_boost(0.6)
    assert abs(g["velocity_shift"] + 0.6) < 1e-6 and g["max_acceleration_change"] < 1e-8
    rows = S.clock_transport()["rows"]
    eps = [r["eps"] for r in rows]
    assert eps == sorted(eps) and abs(eps[-1] - 0.5) < 1e-3
    for r in rows:
        assert abs(r["lag"] - r["approx"]) / r["approx"] < 0.1


def test_causal_set_recovers_dimension():
    assert abs(S.ordering_fraction(2) - 0.5) < 1e-12 and abs(S.ordering_fraction(4) - 0.1) < 1e-12
    d = S.causal_set(n=300)
    for r in d["rows"]:
        assert round(r["estimate"]) == r["d"]
    assert 0 < d["n_links"] < d["n_relations"]


def test_twins_straight_is_longest():
    d = S.twins(n_wiggly=100)
    assert all(abs(r["tau"] - r["formula"]) < 1e-9 for r in d["rows"])
    assert d["n_wiggly"] == 100 and d["max_wiggly"] < d["T"]
