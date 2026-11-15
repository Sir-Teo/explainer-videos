"""Monochord's orchestra (Part 41): measured spectra, additive notes, sections, blend, spacing and the matching solver.

    python -m pytest -q tests/music/test_orchestra.py
"""

import numpy as np
import pytest

from explainer.music.monochord import SR
from explainer.music.monochord import orchestra as O


def test_profiles_keep_the_measured_shapes():
    cl = O.PROFILES["clarinet"]
    assert all(cl[k] > cl[k + 1] + 10 for k in (2, 4))                 # odd harmonics strong, even weak (closed cylinder)
    assert O.PROFILES["trumpet f"][3] > O.PROFILES["trumpet p"][3] + 30  # harder blowing: tens of dB more upper harmonics
    assert O.centroid(O.levels("trumpet f"), 233.0) > 1.6 * O.centroid(O.levels("trumpet p"), 233.0)
    assert all(len(v) == O.H for v in O.PROFILES.values())


def test_note_is_harmonic_and_section_adds_power():
    y = O.note("clarinet", 57, 1.0)
    S = np.abs(np.fft.rfft(y[int(0.2 * SR):]))
    f = np.fft.rfftfreq(len(y) - int(0.2 * SR), 1 / SR)
    f0 = f[np.argmax(S)]
    assert abs(f0 - O.hz(57)) < 3.0
    one = O.rms_db(O.section("violin", 67, 1.5, players=1, seed=2))
    eight = O.rms_db(O.section("violin", 67, 1.5, players=8, seed=2))
    assert 6.0 < eight - one < 15.0                                    # between incoherent (9 dB) give or take, and coherent (18 dB)


def test_fusion_of_ravels_combination():
    f0 = O.hz(60)
    ravel = [("horn", 60, 1.0), ("piccolo", 79, 0.3), ("piccolo", 88, 0.2)]
    assert O.fusion(ravel, f0, cents=20) > 0.99                         # every partial within 20 cents of one series
    off = [("horn", 60, 1.0), ("piccolo", 78, 0.3)]                     # a semitone low: off the series
    assert O.fusion(off, f0, cents=20) < 0.95


def test_spacing_roughness():
    low = O.voicing_roughness([36, 40, 43])
    open_ = O.voicing_roughness([36, 43, 52])
    high = O.voicing_roughness([72, 76, 79])
    assert low > open_ > high


def test_solver_spells_a_vowel():
    f0 = 130.81
    tgt = O.vowel_target(f0=f0)
    r = O.match(tgt, f0, budget=4)
    e = r["error_by_size"]
    assert e[1] > e[2] > e[4] and r["error_db"] == pytest.approx(e[4])
    assert len(r["chosen"]) <= 4 and all(c["gain"] >= 0 for c in r["chosen"])
    for c in r["chosen"]:
        lo, hi, _ = O.RANGES["trumpet" if c["instrument"].startswith("trumpet") else c["instrument"]]
        assert lo <= c["key"] <= hi
