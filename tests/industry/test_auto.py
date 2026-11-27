"""The Works' car business (Part 17): the plant's break-even, the capped upside of a launch, the platform's scale curve,
the battery's parity price, the loan's payment, and Run it's showroom duel, a prisoner's dilemma."""

from explainer.industry.works import auto as A


def test_plant_break_even_and_capped_upside():
    p = A.Plant()
    be = p.break_even(2)
    assert abs(p.year(be, 2)["profit"]) < 1e-3
    assert 0.6 < be / p.capacity(2) < 0.7
    assert p.year(1e9, 2)["cars"] == p.capacity(2)          # demand beyond the shifts' capacity is lost
    assert 25 < p.hours_per_car() < 32
    L = A.launch()
    weak, plan, strong = (L["by_state"][k] for k in ("weak", "as planned", "strong"))
    assert weak["locked"] < 0 < plan["locked"] < strong["locked"]
    # the upside is capped by the line, the downside is not
    assert strong["locked"] - plan["locked"] < plan["locked"] - weak["locked"]
    assert weak["shifts"] == 1 and L["respond"] >= L["locked"]


def test_platform_battery_and_loan():
    pl = A.Platform()
    assert pl.per_car(200_000) == 5 * pl.per_car(1_000_000)
    assert A.battery(75, 139) == 75 * 139
    assert A.parity_per_kwh(75, 6000) == 80
    m = A.payment(45_000, 0.07, 60)
    assert 880 < m < 900 and abs(A.payment(1200, 0.0, 12) - 100) < 1e-9
    assert A.lease(48_000, 28_000, 0.06, 36) < A.payment(48_000, 0.06, 36)


def test_duel_is_a_prisoners_dilemma():
    t = A.run_it()["table"]
    hh, hd, dh, dd = t[("hold", "hold")], t[("hold", "discount")], t[("discount", "hold")], t[("discount", "discount")]
    assert dh[0] > hh[0] and dd[0] > hd[0]                   # discounting is the better reply to either move
    assert hh[0] > dd[0]                                     # and both are worse off when both discount
    assert A.run_it()["equilibria"] == [("discount", "discount")]
    assert A.run_it()["both_cut"] > hh[0]                    # cutting a shift each beats holding with idle crews
