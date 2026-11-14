"""Monochord's sound-mass toolkit (Part 30)."""

import numpy as np

from explainer.music.monochord import soundmass as S


def test_tape():
    y = np.sin(2 * np.pi * 220 * np.arange(4800) / 48000)
    assert len(S.speed(y, 2.0)) == 2400 and len(S.speed(y, 0.5)) == 9600
    assert np.allclose(S.reverse(S.reverse(y)), y)
    assert len(S.loop(y[:480], 5)) == 2400
    burst = np.concatenate([np.ones(100), np.zeros(1000)])
    assert S.attack_time(burst) < 0.003


def test_phasing_and_sieves():
    pats = S.phase_patterns([0, 2, 4, 0, 2, 4, 7, 4, 2, 0, 2, 4])
    assert pats[0]["unisons"] == 12 and [p["unisons"] for p in pats] == [p["unisons"] for p in [pats[0]] + pats[1:][::-1]]
    assert S.sieve(S.DIATONIC_SIEVE) == [0, 2, 4, 5, 7, 9, 11]
    assert S.sieve(S.OCTATONIC_SIEVE) == [0, 1, 3, 4, 6, 7, 9, 10] and S.sieve(S.WHOLE_TONE_SIEVE) == [0, 2, 4, 6, 8, 10]
    s = S.sieve([[(5, 0)], [(7, 2)]], 70)
    assert [x for x in s if x < 35] == [x - 35 for x in s if 35 <= x < 70]               # period 35


def test_poisson_and_masses():
    rng = np.random.default_rng(0)
    on = S.poisson_onsets(5.0, 2000.0, rng)
    gaps = np.diff(on)
    assert abs(np.mean(gaps) - 0.2) < 0.01 and abs(np.std(gaps) - 0.2) < 0.01
    assert abs(sum(S.poisson_pmf(k, 5.0) for k in range(40)) - 1) < 1e-9
    b = S.beat_rates(S.cluster(69.0, 1.0, 3))
    assert all(12 < x < 14 for x in b)                                                    # a quarter tone at A4: ~13 Hz


def test_spectra():
    sr = 48000
    t = np.arange(sr) / sr
    y = np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 300 * t)
    lv = S.harmonic_levels(y, 100.0, 4, sr)
    assert lv[0] == 0.0 and abs(lv[2] + 6.02) < 0.3 and lv[1] < -40
    notes = S.orchestrate(100.0, lv, floor_db=-30)
    assert [n["harmonic"] for n in notes] == [1, 3]
    assert abs(S.harmonic_key(3, 440.0 / 3) - 69.0) < 1e-9
