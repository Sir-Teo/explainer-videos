"""Monochord's form tools (Part 21) against hand-built cases.

    python -m pytest -q tests/music/test_form.py
"""

import numpy as np
import pytest

from explainer.music.monochord import form as FM


def blocks(plan, length=8):
    """Notes for a plan of sections: each letter its own chord, held a beat at a time."""
    chords = {"A": (60, 64, 67), "B": (62, 66, 69), "C": (65, 69, 72)}
    ev, t = [], 0.0
    for x in plan:
        for k in range(length):
            for p in chords[x]:
                ev.append((p, t, 1.0))
            t += 1.0
    return ev


def test_ssm_shape_and_stripes():
    C = FM.chroma_notes(blocks("ABA"), step=1.0)
    S = FM.ssm(C)
    assert S.shape == (24, 24) and np.allclose(S, S.T) and np.allclose(np.diag(S), 1.0)
    assert np.allclose([S[k, 16 + k] for k in range(8)], 1.0)                   # A returns after 16 beats
    assert S[0, 8] < 0.5


def test_novelty_finds_the_seams():
    S = FM.ssm(FM.chroma_notes(blocks("ABCA"), step=1.0))
    nov = FM.novelty(S, L=4)
    found = FM.peaks(nov, min_gap=4, threshold=0.3)
    assert FM.boundary_score(found, [8, 16, 24], tol=1)["f"] == 1.0
    S2 = FM.ssm(FM.chroma_notes(blocks("AA"), step=1.0))                       # a seam between a passage and its repeat
    assert FM.novelty(S2, L=4)[8] == pytest.approx(0.0, abs=1e-9) or max(FM.novelty(S2, L=4)[5:12]) < 0.5


def test_boundary_score():
    sc = FM.boundary_score([8, 17, 30], [8, 16, 24], tol=2)
    assert sc["hits"] == 2 and sc["precision"] == pytest.approx(2 / 3) and sc["recall"] == pytest.approx(2 / 3)
    assert FM.boundary_score([16, 16], [16], tol=1)["hits"] == 1                # each truth matched once


def test_labels_and_repetition():
    S = FM.ssm(FM.chroma_notes(blocks("ABAC"), step=1.0))
    assert FM.label_sections(S, [8, 16, 24]) == ["A", "B", "A", "C"]
    assert FM.repeated_share([0, 2, 4, 5, 0, 2, 4, 5], [1] * 8, n=4) == 0.5          # the repeat, not the first statement
    assert FM.repeated_share([0, 2, 4, 5, 7, 9, 11, 12], [1] * 8, n=4) == 0.5          # 7 9 11 12 is 0 2 4 5, transposed
    assert FM.repeated_share([0, 2, 4, 5, 7, 9, 11, 12], [1] * 8, n=4, transposed=False) == 0.0
    assert FM.repeated_share([0, 3, 7, 8, 1, 10, 4, 11], [1] * 8, n=4) == 0.0


def test_golden_base_rate():
    assert FM.golden_base_rate(0.5, 0.75, 0.02) == pytest.approx(0.16)
    assert FM.PHI == pytest.approx(0.6180339887)
    assert FM.golden_hits([0.6, 0.62, 0.7], tol=0.02) == 2
