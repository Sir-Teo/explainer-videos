"""The Works' machinery business (Part 19): the tender, its attach threshold, and the installed base that steadies a
maker through the capital-goods cycle."""

from explainer.industry.works import machine as M


def test_tender_is_a_dilemma_when_servicing_is_worth_enough():
    t = M.Tender()
    tab = t.table()
    assert tab[("cut", "hold")][0] > tab[("hold", "hold")][0]       # cutting beats holding against a holder
    assert tab[("cut", "cut")][0] > tab[("hold", "cut")][0]         # and against a cutter
    assert t.equilibria() == [("cut", "cut")]
    assert tab[("hold", "hold")][0] > tab[("cut", "cut")][0]        # yet both would rather hold


def test_attach_threshold_matches_the_payoffs():
    a = M.attach_threshold()
    lo, hi = M.Tender(attach=a - 0.01), M.Tender(attach=a + 0.01)
    assert lo.payoff("cut", "hold") < lo.payoff("hold", "hold")
    assert hi.payoff("cut", "hold") > hi.payoff("hold", "hold")
    assert ("hold", "hold") in M.Tender(attach=0.3).equilibria()


def test_installed_base_steadies_revenue():
    rows = M.Maker().run(M.cycle_demand())
    new, svc = M.swings(rows, "new_rev"), M.swings(rows, "svc_rev")
    assert svc["cv"] < new["cv"] / 2
    assert svc["worst_fall"] > -0.1 > new["worst_fall"]
    r = rows[-1]
    assert r["base"] == sum(x["units"] for x in rows[-15:])
