"""The cycle machines (Part 6): the cobweb's stability rule, lead times that widen the swings, the bullwhip,
operating leverage."""

import numpy as np

from explainer.industry.works.cycle import bullwhip, cobweb, cobweb_eq, fleet, leverage, swing


def test_cobweb_converges_cycles_or_explodes_by_slopes():
    a, b, c = 10.0, 1.0, 0.0
    pe, _ = cobweb_eq(a, b, c, 0.8)
    for d, kind in ((0.8, "in"), (1.0, "cycle"), (1.25, "out")):
        p, q = cobweb(a, b, c, d, pe + 2.0, n=20)
        pe_d, qe_d = cobweb_eq(a, b, c, d)
        gap = np.abs(p - pe_d)
        if kind == "in":
            assert gap[-1] < 0.05 * gap[0]
        elif kind == "cycle":
            assert np.allclose(gap, gap[0])
        else:
            assert gap[-1] > 10 * gap[0]
        assert np.allclose(p[1:], a - b * q)  # every crop sells where the demand curve says
        assert np.all(np.sign(p[1:] - pe_d) == -np.sign(p[:-1] - pe_d))  # a high price is followed by a low one


def test_longer_lead_times_make_bigger_swings():
    swings = [swing(fleet(years=60, lead=L)["rate"], 15) for L in (1, 2, 3, 4)]
    assert all(s2 > s1 for s1, s2 in zip(swings, swings[1:]))
    f = fleet(years=60, lead=3)
    assert np.all(np.diff(f["demand"]) > 0)  # demand never falls: the swings are the fleet's own doing


def test_bullwhip_amplifies_up_the_chain():
    rng = np.random.default_rng(0)
    sales = 100 + rng.normal(0, 5, 300)
    orders = bullwhip(sales, tiers=3)  # a fourth tier swings so hard its orders hit zero (it cannot send goods back)
    sd = [np.std(orders[i, 30:]) for i in range(4)]
    assert all(b > a for a, b in zip(sd, sd[1:]))
    assert abs(orders[:, 30:].mean(axis=1) - sales[30:].mean()).max() < 5  # on average each tier orders what it sells


def test_leverage_turns_a_fall_in_sales_into_a_larger_fall_in_profit():
    r = leverage(100.0, 80.0, fixed=30.0, variable_share=0.5)
    assert np.isclose(r["profit0"], 20.0) and np.isclose(r["profit1"], 10.0)
    assert np.isclose(r["degree"], 2.5)  # (50 / 20): contribution over profit
