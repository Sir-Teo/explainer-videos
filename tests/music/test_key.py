"""Monochord's keys against Krumhansl and Kessler's published numbers, and on the series' own tunes."""

import numpy as np
import pytest

from explainer.music.monochord import key as K
from explainer.music.monochord import melody as M

C = M.corpus()


def test_names_signatures_and_relations():
    assert K.key_name((0, "major")) == "C major" and K.key_name((6, "minor")) == "F♯ minor" and K.key_name((3, "major")) == "E♭ major"
    assert K.key_name((10, "minor")) == "B♭ minor" and K.key_name((1, "minor")) == "C♯ minor" and K.key_name((9, "minor"), short=True) == "a"
    assert K.relative((0, "major")) == (9, "minor") and K.relative((9, "minor")) == (0, "major") and K.parallel((0, "major")) == (0, "minor")
    assert [K.signature((t, "major")) for t in (0, 7, 2, 9, 5, 10, 3)] == [0, 1, 2, 3, -1, -2, -3] and K.signature((9, "minor")) == 0
    assert K.shared_notes((0, "major"), (7, "major")) == 6 and K.shared_notes((0, "major"), (6, "major")) == 2
    for a in range(12):
        for b in range(12):
            assert K.shared_notes((a, "major"), (b, "major")) == [7, 6, 5, 4, 3, 2, 2][K.fifths_apart((a, "major"), (b, "major"))]     # a fifth away, one note changes
    assert [K.key_name(k) for k in K.keys_containing([0, 2, 4])] == ["C major", "F major", "G major"]
    assert len(K.keys_containing([11, 5])) == 2 and K.keys_containing([11, 5, 0]) == [(0, "major")]                   # a tritone and one more note name the key


def test_the_map_of_keys_matches_the_published_one():
    near = dict(K.nearest_keys((0, "major"), top=5))
    assert near[(9, "minor")] == pytest.approx(0.651, abs=0.002) and near[(7, "major")] == pytest.approx(0.591, abs=0.002)
    assert near[(5, "major")] == pytest.approx(0.591, abs=0.002) and near[(4, "minor")] == pytest.approx(0.536, abs=0.002) and near[(0, "minor")] == pytest.approx(0.511, abs=0.002)
    Cm = K.key_correlations()
    assert Cm[0, 6] == pytest.approx(-0.683, abs=0.002)                                    # C major and F sharp major: as far apart as keys get
    t = K.torus()
    e = t["eigenvalues"]
    assert e[0] == pytest.approx(e[1], rel=1e-6) and e[2] == pytest.approx(e[3], rel=1e-6) and t["explained"] > 0.8        # two circles
    ang = t["angles"]
    step = lambda a, b: (b - a + 0.5) % 1.0 - 0.5                                          # noqa: E731
    for tonic in range(12):
        a, b = ang[(tonic, "major")], ang[((tonic + 7) % 12, "major")]
        assert abs(step(a[0], b[0])) == pytest.approx(1 / 12, abs=1e-6) and abs(step(a[1], b[1])) == pytest.approx(1 / 4, abs=1e-6)
        third = ang[((tonic + 4) % 12, "major")]
        assert abs(step(a[1], third[1])) < 1e-6 and abs(step(a[0], third[0])) == pytest.approx(1 / 3, abs=1e-6)


def test_finding_the_key_of_the_tunes():
    def accuracy(finder, n=None):
        right = total = 0
        for m in C:
            p, b = (m.pitches, m.beats) if n is None else (m.pitches[:n], m.beats[:n])
            for tr in range(12):
                right += finder([x + tr for x in p], b) == (tr, m.mode)
                total += 1
        return right / total

    kk = accuracy(lambda p, b: K.find_key(K.distribution(p, b)))
    tp = accuracy(lambda p, b: K.find_key(K.distribution(p, b), (K.TEMPERLEY_MAJOR, K.TEMPERLEY_MINOR)))
    by = accuracy(K.bayes_key)
    assert 0.78 < kk < 0.85 and tp > 0.95 and by > 0.93                                    # the listeners' ratings do worse than the corpus counts
    assert 0.88 < accuracy(lambda p, b: (p[-1] % 12, "major")) < 0.93                      # "the key is the last note" is right nine times in ten
    assert accuracy(K.bayes_key, 5) > 0.85 > accuracy(K.bayes_key, 3)                      # five notes are usually enough
    maj, _ = K.learn_profiles(C)
    assert np.corrcoef(maj, K.KK_MAJOR)[0, 1] > 0.9 and np.corrcoef(maj, K.TEMPERLEY_MAJOR)[0, 1] > 0.9      # ratings follow how often notes occur
    post = K.posterior([0, 0, 7, 7, 9, 9, 7])
    assert max(post, key=post.get) == (0, "major") and sum(post.values()) == pytest.approx(1.0)


def test_tracking_a_change_of_key():
    c_major = [0, 2, 4, 5, 7, 9, 11, 12, 11, 9, 7, 5, 4, 2, 0, 4, 7, 4, 0]
    piece = c_major + [p + 7 for p in c_major]                                             # the same music in C, then in G
    path = K.track(piece, [1.0] * len(piece), window=8, hop=4, profiles=(K.TEMPERLEY_MAJOR, K.TEMPERLEY_MINOR))
    assert path[0]["key"] == (0, "major") and path[-1]["key"] == (7, "major")
    assert K.distribution([0, 12, 24], [1, 2, 1])[0] == pytest.approx(1.0)
