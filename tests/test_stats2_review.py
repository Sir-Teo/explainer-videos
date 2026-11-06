"""Reference checks for the probability examples in Statistics, Built Part 2."""

from fractions import Fraction
from functools import lru_cache

import numpy as np
import pytest

from videos.stats.stats2.compute import cantor_cdf, monty, p_first_to


def test_cantor_distribution_has_exact_tails_and_flat_middle_third():
    assert [cantor_cdf(x) for x in [-10, -1, 0]] == [0, 0, 0]
    assert [cantor_cdf(x) for x in [1, 2, 10]] == [1, 1, 1]
    assert all(cantor_cdf(x) == .5 for x in np.linspace(1 / 3, 2 / 3, 101))
    assert np.all(np.diff([cantor_cdf(x) for x in np.linspace(0, 1, 1001)]) >= 0)
    assert cantor_cdf(1 / 9) == .25
    assert cantor_cdf(8 / 9) == .75


def test_fermat_completed_rounds_agree_with_pascals_stopping_recursion():
    @lru_cache(None)
    def stopping_game(a, b):
        if a == 0:
            return Fraction(1)
        if b == 0:
            return Fraction(0)
        return (stopping_game(a - 1, b) + stopping_game(a, b - 1)) / 2

    for a in range(1, 9):
        for b in range(1, 9):
            assert p_first_to(a, b) == stopping_game(a, b)
            assert p_first_to(a, b) + p_first_to(b, a) == 1
    assert p_first_to(2, 3) == Fraction(11, 16)


@pytest.mark.parametrize('q', [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)])
def test_biased_monty_distinguishes_a_fixed_reveal_from_the_switching_strategy(q):
    # Enumerate two independent fair bits representing the host's randomizer.
    # Car placements have equal prior mass. Host always reveals an unpicked goat.
    outcomes = []
    for car in [1, 2, 3]:
        for randomizer in range(4):
            opened = (3 if Fraction(randomizer, 4) < q else 2) if car == 1 else 5 - car
            remaining = next(door for door in [2, 3] if door != opened)
            outcomes.append((opened, remaining == car))
    conditional = [won for opened, won in outcomes if opened == 3]
    expected = Fraction(sum(conditional), len(conditional))
    actual = monty('biased', q)
    assert Fraction(*actual['switch']) == expected
    assert Fraction(*actual['stay']) == 1 - expected
    assert Fraction(sum(won for _, won in outcomes), len(outcomes)) == Fraction(2, 3)
