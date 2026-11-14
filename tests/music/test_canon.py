"""Monochord's canon tools (Part 20) against brute force and hand-checked theory.

    python -m pytest -q tests/music/test_canon.py
"""

from itertools import product

from explainer.music.monochord import canon as K


def brute_canons(n, delay, steps, notes):
    follow = {p: K.diatonic(p, steps) for p in notes}
    tot = 0
    for mel in product(notes, repeat=n):
        if mel[0] % 12 or mel[-1] % 12 or not all(K._ok_move(a, b) for a, b in zip(mel, mel[1:])):
            continue
        ok = True
        for k in range(delay, n):
            x, y = mel[k], follow[mel[k - delay]]
            if not K._vert_ok(x, y) or (k > delay and K._parallel(mel[k - 1], follow[mel[k - 1 - delay]], x, y)):
                ok = False
                break
        tot += ok
    return tot


def brute_crabs(n, notes):
    triad = {0, 4, 7}
    tot = 0
    for mel in product(notes, repeat=n):
        if mel[0] % 12 not in triad or mel[-1] % 12 not in triad or not all(K._ok_move(a, b) for a, b in zip(mel, mel[1:])):
            continue
        back = mel[::-1]
        if all(K._vert_ok(a, b) for a, b in zip(mel, back)) and not any(K._parallel(mel[k - 1], back[k - 1], mel[k], back[k]) for k in range(1, n)):
            tot += 1
    return tot


def test_counts_match_brute_force():
    notes = K.scale_notes(60, 72)
    for delay, steps in ((1, 0), (2, 4), (2, -4), (1, 2)):
        assert K.count_canons(6, delay, steps, notes=notes) == brute_canons(6, delay, steps, notes)
    for n in (4, 5, 6):
        assert K.count_crabs(n, notes=notes) == brute_crabs(n, notes)


def test_samples_are_canons():
    import numpy as np
    for steps in (0, 1, -4, 7):
        mel = K.sample_canon(10, 2, steps, rng=np.random.default_rng(1))
        lead, fol = K.line(mel), K.shift(K.line([K.diatonic(p, steps) for p in mel]), 2)
        f = K.faults([lead, fol], start=2, stop=10, allow_upper_fourths=False)
        assert f["dissonant"] == 0 and f["parallels"] == 0
    crab = K.sample_crab(10, rng=np.random.default_rng(2))
    assert K.crab_ok(crab)["dissonant"] == 0 and K.crab_ok(crab)["parallels"] == 0


def test_forms_make_klein_four():
    t = K.group_table()
    assert all(t[(f, f)] == "P" for f in K.FORMS)
    assert t[("I", "R")] == "RI" and t[("R", "I")] == "RI" and t[("I", "RI")] == "R"
    assert K.check_table_on([60, 64, 67, 65, 62, 71])
    ln = K.line([60, 62, 64], [1, 2, 1])
    assert K.retrograde(K.retrograde(ln)) == ln
    assert [p for p, _, _ in K.diatonic_invert(K.line([72, 79, 81]), K.degree_of(72)[0])] == [72, 65, 64]


def test_invertible_maps():
    octave = K.invertible(7)
    assert octave[4]["becomes"] == 3 and not octave[4]["consonant_after"]       # fifth -> fourth
    assert octave[2]["becomes"] == 5 and octave[2]["consonant_after"]           # third -> sixth
    tenth = K.invertible(9)
    assert all(tenth[s]["consonant_after"] for s in (0, 2, 4, 5, 7)) and tenth[2]["perfect_after"]
    twelfth = K.invertible(11)
    assert not twelfth[5]["consonant_after"]                                    # sixth -> seventh


def test_answers():
    subj = K.line([67, 72, 71, 72, 74])                                          # G C B C D in C
    assert [p for p, _, _ in K.tonal_answer(subj)] == [72, 79, 78, 79, 81]       # C G F# G A
    assert [p for p, _, _ in K.real_answer(subj)] == [74, 79, 78, 79, 81]
    tune = K.line([72, 72, 79, 79, 81, 81, 79])
    assert [p for p, _, _ in K.tonal_answer(tune)] == [79, 79, 84, 84, 88, 88, 86]


def test_faults_and_strettos():
    a = K.line([60, 64, 67, 64])
    assert K.faults([a, K.transpose(a, -12)])["parallels"] == 3                  # octaves all the way
    assert K.faults([K.line([60, 62]), K.line([48, 48])])["dissonant"] == 1      # a ninth over the bass
    st = K.strettos(K.line([72, 72, 79, 79, 81, 81, 79], [1, 1, 1, 1, 1, 1, 2]))
    assert {"delay": 2.0, "interval": -5, "overlap": 6, "dissonant": 0} in st
