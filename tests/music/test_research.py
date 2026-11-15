"""Monochord's research methods (Part 67): the manuscript tradition, neighbour joining and the Robinson-Foulds distance,
reconstruction, ABX power and the series' star problems.

    python -m pytest -q tests/music/test_research.py
"""

import numpy as np
import pytest

from explainer.music.monochord import research as R
from explainer.tts import REPO_ROOT


def test_neighbor_joining_recovers_a_clear_tree():
    # four witnesses in two clear pairs: ((a, b), (c, d))
    D = np.array([[0, 2, 9, 9], [2, 0, 9, 9], [9, 9, 0, 2], [9, 9, 2, 0]], float)
    nj = R.neighbor_joining(D, ["a", "b", "c", "d"])
    s = R.splits(nj, ["a", "b", "c", "d"])
    assert frozenset({"c", "d"}) in s or frozenset({"a", "b"}) in s


def test_tradition_reconstruction_beats_the_witnesses():
    tune = list(range(60, 80)) * 2
    rng = np.random.default_rng(5)
    t = R.copy_tradition(tune, rng, generations=4, error_rate=0.05)
    W = [t["mss"][i]["notes"] for i in t["survive"]]
    rec = R.reconstruct(W)
    assert R.hamming(rec, tune) <= np.median([R.hamming(w, tune) for w in W])
    true = R.true_adjacency(t["mss"], t["survive"])
    D = np.array([[R.hamming(a, b) for b in W] for a in W])
    rf = R.rf_distance(true, R.neighbor_joining(D, [str(i) for i in t["survive"]]), t["survive"])
    assert rf["share"] > 0.5


def test_abx_power_is_exact():
    p = R.abx_power(0.5, 20)
    assert p["critical"] == 15 and p["size"] == pytest.approx(p["power"]) and p["size"] < 0.05
    assert R.abx_power(0.9, 20)["power"] > 0.95
    n = R.abx_trials_needed(0.75)
    assert R.abx_power(0.75, n)["power"] >= 0.8 > R.abx_power(0.75, n - 1)["power"] or n < 30


def test_star_problems_are_read():
    ps = R.star_problems(REPO_ROOT)
    assert len(ps) > 40 and all(isinstance(n, int) and q for n, q in ps)
