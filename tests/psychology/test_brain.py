"""Psyche's brain: architectures that can be lesioned, the logic of dissociation, maps, and lesion mapping."""

import math

import numpy as np
import pytest

from explainer.psychology.psyche import brain as B


def test_lichtheim_predicts_three_syndromes():
    table = B.LICHTHEIM.table(B.APHASIAS)
    broca, wernicke, conduction = (table[k] for k in B.APHASIAS)
    assert broca["understand speech"] == 1 and broca["speak"] == 0 and broca["repeat"] == 0
    assert wernicke["understand speech"] == 0 and wernicke["speak"] == 1 and wernicke["repeat"] == 0
    # the syndrome the diagram predicted before it had been described: repetition lost, the rest spared
    assert conduction == {"understand speech": 1.0, "speak": 1.0, "repeat": 0.0}
    assert B.LICHTHEIM.dissociates("speak", "understand speech")["double"]


def test_partial_lesions_multiply_along_a_route():
    p = B.LICHTHEIM.performance({"hearing": 0.5, "word sounds": 0.5})
    assert p["understand speech"] == pytest.approx(0.25) and p["speak"] == 1.0
    with pytest.raises(KeyError):
        B.LICHTHEIM.performance({"no such part": 1.0})


def test_memory_architecture_after_the_operation():
    p = B.MEMORY.performance({"hippocampal system": 1.0})
    assert p["recall today tomorrow"] == 0
    assert p["recall childhood"] == p["repeat seven digits"] == p["learn mirror tracing"] == 1


def test_one_resource_gives_one_direction_only_without_noise():
    d = B.dissociations("one", noise=0.0, rng=np.random.default_rng(1))
    assert d["a_only"] > 0.1 and d["b_only"] == 0
    assert B.chance_of_double(d["a_only"], d["b_only"], 500) == pytest.approx(0.0, abs=1e-12)


def test_noisy_tests_fake_a_double_dissociation():
    quiet = B.dissociations("one", noise=0.0, rng=np.random.default_rng(1))
    noisy = B.dissociations("one", noise=0.10, rng=np.random.default_rng(1))
    assert noisy["b_only"] > quiet["b_only"] and noisy["b_only"] > 0.01
    assert B.chance_of_double(noisy["a_only"], noisy["b_only"], 100) > 0.9
    two = B.dissociations("two", noise=0.0, rng=np.random.default_rng(1))
    assert two["a_only"] > 0.1 and two["b_only"] > 0.1
    for d in (quiet, noisy, two):
        assert d["a_only"] + d["b_only"] + d["both"] + d["neither"] == pytest.approx(1.0)


def test_chance_of_double_limits():
    assert B.chance_of_double(0.2, 0.0, 50) == pytest.approx(0.0, abs=1e-12)
    assert B.chance_of_double(0.5, 0.5, 1) == pytest.approx(0.0)
    assert B.chance_of_double(0.5, 0.5, 2) == pytest.approx(0.5)


def test_crawford_howell_is_more_cautious_than_z():
    from scipy import stats

    controls = [34, 31, 38, 29, 35, 33, 36, 30]
    r = B.crawford_howell(20, controls)
    assert r["df"] == 7 and r["t"] == pytest.approx(r["z"] / math.sqrt(9 / 8))
    assert r["p"] > stats.norm.cdf(r["z"])  # a small norm sample cannot support a one-in-a-million claim
    assert B.crawford_howell(np.mean(controls), controls)["p"] == pytest.approx(0.5)
    with pytest.raises(ValueError):
        B.crawford_howell(1.0, [2.0])


def test_magnification_and_its_integrals():
    assert B.magnification(0.0) == pytest.approx(17.3 / 0.75)
    e = np.linspace(0, 30, 30001)
    assert B.cortical_distance(30.0) == pytest.approx(np.trapezoid(B.magnification(e), e), rel=1e-4)
    # the area is the integral of M^2 over the half disc
    area = np.trapezoid(B.magnification(e) ** 2 * math.pi * e, e)
    assert B.cortical_area(30.0) == pytest.approx(area, rel=1e-3)
    assert 0.4 < B.area_share(10.0) < 0.5 and B.area_share(90.0) == pytest.approx(1.0)


def test_blind_spot_geometry():
    d = B.blind_spot(57.0)
    assert d["near"] < d["centre"] < d["far"]
    assert d["centre"] == pytest.approx(57 * math.tan(math.radians(15)))
    assert 5 < d["width"] < 7  # at 57 cm a degree is about a centimetre


def test_lesion_map_is_displaced_toward_the_trunk():
    shifts = np.array([B.lesion_study(rng=np.random.default_rng(s))["shift"] for s in range(6)])
    # the critical region lies above the trunk (row 20), at row 26: the map's centre is pulled back toward it
    assert shifts[:, 1].mean() < -1.0
    free = np.array([B.lesion_study(rng=np.random.default_rng(s), vascular=False)["shift"] for s in range(6)])
    assert abs(free[:, 1].mean()) < abs(shifts[:, 1].mean())
