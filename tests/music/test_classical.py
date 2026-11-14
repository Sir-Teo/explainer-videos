"""Monochord's Classical toolkit (Part 26)."""

from explainer.music.monochord import classical as CL


def _movement(voices, time=(4, 4)):
    return CL.Movement({"composer": "test", "name": "test/movement1", "time": list(time), "voices": voices})


def test_cadence_and_gaps():
    q = 24                                  # ticks to a quarter; a 4/4 bar is 96
    top = [(76, 0, 4 * q), (74, 4 * q, 3 * q), (72, 7 * q, q), (72, 8 * q, 4 * q), (71, 12 * q, 4 * q), (72, 16 * q, 4 * q)]
    bass = [(48, 0, 4 * q), (43, 4 * q, 4 * q), (48, 8 * q, 4 * q), (43, 12 * q, 4 * q), (36, 16 * q, 4 * q)]
    m = _movement([top, bass])
    assert m.bars == 5 and m.beat == q
    assert CL.cadences(m) == [2, 4]          # G down to C onto bars 2 and 4, the top voice on C
    assert CL.phrase_gaps(m) == [2]


def test_harmonic_rhythm_and_leads():
    q = 24
    held = [(60, 0, 8 * q)]
    moving = [(64 + (k % 2) * 3, k * q, q) for k in range(8)]
    m = _movement([moving, held])
    assert abs(CL.harmonic_rhythm(m) - 1.0) < 1e-9       # the top changes every beat
    assert CL.lead_voices(m) == [0, 0]
    still = _movement([[(64, 0, 8 * q)], held])
    assert CL.harmonic_rhythm(still) == 0.0


def test_accompaniment_figures():
    q = 24
    alberti = [(p, k * q // 2, q // 2) for k, p in enumerate([48, 55, 52, 55] * 4)]     # C G E G: a broken triad
    scale = [(p, k * q // 2, q // 2) for k, p in enumerate([48, 50, 52, 53, 55, 57, 59, 60] * 2)]
    tune = [(72, 0, 8 * q)]
    assert CL.accompaniment_bars(_movement([tune, alberti])) == 1.0
    assert CL.accompaniment_bars(_movement([tune, scale])) == 0.0


def test_second_key():
    plan = [{"bar": 0.0, "key": (0, "major")}, {"bar": 2.0, "key": (7, "major")}, {"bar": 4.0, "key": (2, "minor")},
            {"bar": 6.0, "key": (7, "major")}, {"bar": 8.0, "key": (7, "major")}, {"bar": 10.0, "key": (0, "major")}]
    assert CL.second_key(plan) == (7, "major", 6.0)      # a key that holds two windows, not a passing one
    assert CL.second_key(plan[:1] + plan[-1:]) is None
