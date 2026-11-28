"""The Works' telecoms: the clock auction, the subscriber and the tower."""

from explainer.industry.works.telco import Auction, Subscriber, Tower


def test_auction_demand_reduction():
    A = Auction()
    s4, s2 = A.run(cap=4), A.run(cap=2)
    assert sum(s4["won"]) <= A.supply and sum(s2["won"]) <= A.supply
    # bidding for fewer blocks ends the auction lower and leaves the bidder better off
    assert s2["price"] < s4["price"] and s2["won"][0] < s4["won"][0] and s2["surplus"][0] > s4["surplus"][0]
    assert s2["revenue"] < s4["revenue"]
    # every winner pays the same price per block
    assert abs(s4["revenue"] - s4["price"] * sum(s4["won"])) < 1e-9


def test_subscriber_and_tower():
    S = Subscriber()
    assert abs(S.months() - 1 / 0.0092) < 1e-9
    assert S.lifetime() > S.but(churn=0.015).lifetime() > 0
    T = Tower()
    assert T.yield_(1) < T.yield_(2) < T.yield_(3)
    assert T.margin(3) > T.margin(1)
