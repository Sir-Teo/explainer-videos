"""The Works' building (Part 26): value as income over a rate, refinancing and the development margin."""

import math

from explainer.industry.works import building as B


def test_value_is_income_over_rate():
    b = B.Building()
    assert math.isclose(b.rent_roll(), 400_000 * 50 * 0.95 / 1e6)
    assert math.isclose(b.noi(), 19.0 - 9.0)
    assert math.isclose(b.value(), 10.0 / 0.05)
    # a one-point rise in the rate costs a sixth of the value at 5%, a fifth at 4%
    assert math.isclose(B.rate_move(0.05), -1 / 6)
    assert math.isclose(B.rate_move(0.04), -0.2)


def test_fixed_costs_make_vacancy_hit_income_harder():
    b = B.Building()
    emptier = b.but(occupancy=0.95 * 2 / 3)
    assert emptier.rent_roll() / b.rent_roll() > 0.66
    assert emptier.noi() / b.noi() < 0.4


def test_refinance_takes_the_tightest_test_and_the_office_cannot_refinance():
    r = B.run_it()
    off, shed = r["office"], r["warehouse"]
    t = off["at"]["tests"]
    assert off["at"]["new_loan"] == min(t.values())
    assert off["at"]["gap"] > off["loan"] / 2
    assert off["at"]["keys"]["lender_loss"] > 0
    assert off["at"]["extend"]["interest_cover"] < 1
    assert shed["at"]["gap"] == 0 and shed["at"]["cash_out"] > 0
    assert shed["now"]["value"] > shed["then"]["value"]


def test_development_margin_and_implied_cap():
    cap = B.implied_cap(0.067, 0.254)
    assert math.isclose(B.dev_margin(0.067, cap), 0.254)
    assert 0.05 < cap < 0.06
