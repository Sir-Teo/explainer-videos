"""The permutation machine (Part 10): tokens land in the slots they are dealt, and groups follow the slots."""

import numpy as np

from explainer.stats import PermutationMachine, axes


def test_shuffle_reassigns_groups_and_reset_restores():
    vals = [1, 2, 3, 10, 20]
    m = PermutationMachine(vals, [True, True, True, False, False])
    a, b = m.groups()
    assert sorted(a) == [1, 2, 3] and sorted(b) == [10, 20]
    m.shuffle([3, 4, 0, 1, 2])  # tokens 0 and 1 move to B's slots
    a, b = m.groups()
    assert sorted(a) == [3, 10, 20] and sorted(b) == [1, 2]
    m.reset()
    assert sorted(m.groups()[0]) == [1, 2, 3]


def test_drops_stack_in_bins():
    m = PermutationMachine([1, 2], [True, False])
    A = axes([-2, 2], [0, 1])
    d1, d2, d3 = m.drop(A.ax, 0.1, 0.5), m.drop(A.ax, -0.1, 0.5), m.drop(A.ax, 1.0, 0.5)
    assert np.isclose(d1.get_x(), d2.get_x()) and d2.get_y() > d1.get_y()
    assert not np.isclose(d3.get_x(), d1.get_x())
