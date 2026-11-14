"""Monochord's counterpoint: the rules, the exact count of first-species lines, and the five species."""

import numpy as np
import pytest

from explainer.music.monochord import counterpoint as K

CF = K.FUX_DORIAN


def test_motion_and_intervals():
    assert K.motion(60, 62, 48, 50) == "parallel" and K.motion(60, 64, 48, 50) == "similar"
    assert K.motion(60, 62, 48, 47) == "contrary" and K.motion(60, 62, 48, 48) == "oblique" and K.motion(60, 60, 48, 48) == "static"
    assert K.vertical(60, 67) == 7 and K.vertical(60, 53, below=True) == 7
    c = K.candidates(CF)
    assert all(len(x) == 14 for i, x in enumerate(c) if i != 9) and 73 in c[-2]          # the raised leading note, C sharp, at the cadence


def test_counting_is_exact():
    n = K.count(CF)
    assert n == 152
    rng = np.random.default_rng(0)
    seen = set()
    for _ in range(400):
        line = K.sample(CF, rng=rng)
        assert K.check(CF, line) == []
        seen.add(tuple(line))
    assert len(seen) > 100                                       # uniform sampling visits most of the 152
    # brute force on a short cantus agrees with the dynamic programme
    short = [62, 65, 64, 62]
    cands = K.candidates(short)
    import itertools
    brute = sum(1 for line in itertools.product(*cands) if not K.check(short, list(line)))
    assert brute == K.count(short)
    f = K.funnel(CF)
    assert f[0][1] == np.prod([len(x) for x in K.candidates(CF)]) and f[-1][1] == 152
    assert all(b[1] <= a[1] for a, b in zip(f, f[1:]))


def test_rules_and_their_redundancy():
    full = K.count(CF)
    without = {r: K.count(CF, tuple(x for x in K.RULES if x != r)) for r in K.RULES}
    assert without["parallel"] == full                           # implied by the rule against similar motion into perfect intervals
    assert without["consonance"] > 100 * full and without["direct"] > full and without["recovery"] > 10 * full
    bad = [69, 76, 74, 72, 71, 69, 72, 71, 74, 73, 74]           # contains a direct fifth and other faults
    assert K.check(CF, bad)
    good = K.best(CF, tries=400)
    assert K.check(CF, good) == [] and K.score(CF, good) > 10


def test_species():
    rng = np.random.default_rng(2)
    for n in (2, 3, 4, 5):
        line = K.species(CF, n, rng, tries=60)
        assert line is not None
        assert line[-1][0] % 12 == 2 and line[-2][0] == 73                                # ends on D through C sharp
        cf_ev = [(c, 4.0 * k, 4.0) for k, c in enumerate(CF)]
        ind = K.independence(line, cf_ev)
        assert ind["fused"] == 0
        for p, a, d in line:                                     # every downbeat is consonant unless it is a prepared suspension
            if a % 4 == 0 and a < 40:
                c = CF[int(a // 4)]
                assert (p - c) % 12 in K.CONSONANT or n in (4, 5)
    four = K.species(CF, 4, np.random.default_rng(4), tries=60)
    sus = [(p, a) for p, a, d in four if a % 4 == 2 and d > 2 and (p - CF[int((a + 2) // 4)]) % 12 in (10, 11, 1, 2, 5)]
    assert sus                                                   # some held notes become dissonant, and resolve
    one = [(p, 4.0 * k, 4.0) for k, p in enumerate(K.best(CF, tries=300))]
    cf_ev = [(c, 4.0 * k, 4.0) for k, c in enumerate(CF)]
    assert K.independence(one, cf_ev)["together"] == 1.0 > K.independence(four, cf_ev)["together"]
    org = K.organum([60, 60, 67, 67, 69, 69, 67])
    ind = K.independence([(p, k, 1) for k, p in enumerate([60, 60, 67, 67, 69, 69, 67])], [(p, k, 1) for k, p in enumerate(org)])
    assert ind["fused"] == 1.0 and ind["parallel"] == 1.0


def test_below_the_cantus_and_other_cadences():
    # below: the first note an octave or unison under the cantus, the leading note a third below it at the cadence
    assert K.count(CF, below=True) == 42
    line = K.best(CF, below=True, tries=600)
    assert K.check(CF, line, below=True) == [] and K.vertical(CF[0], line[0], True) % 12 == 0 and line[-2] % 12 == 1
    short = [62, 65, 64, 62]
    import itertools
    cands = K.candidates(short, below=True)
    assert sum(1 for l in itertools.product(*cands) if not K.check(short, list(l), below=True)) == K.count(short, below=True)
    # a cantus that rises to its final: the counterpoint falls to it from the step above
    up = [60, 62, 65, 64, 62, 59, 60]
    assert K.count(up) > 0 and all(l[-2] % 12 == 2 for l in (K.sample(up, rng=np.random.default_rng(s)) for s in range(20)))


def test_fourth_species_breaks_a_tie_only_when_it_must():
    cf = [60, 62, 65, 64, 62, 67, 65, 64, 62, 60]                 # a leap of a fifth up: no unbroken chain of ties fits
    assert K._search(cf, [4] * len(cf), cf[-1], np.random.default_rng(0), budget=30000) is None
    line = K.species(cf, 4, np.random.default_rng(1), tries=20)
    assert line is not None and line[-1][0] % 12 == 0
    assert K.independence(line, [(c, 4.0 * k, 4.0) for k, c in enumerate(cf)])["fused"] == 0
