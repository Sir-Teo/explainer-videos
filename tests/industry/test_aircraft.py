"""The Works' aerospace business (Part 18): the programme's valley of cash and its learning curve, the engine paid back by
its service, and Run it's duel between a new airliner and a re-engine."""

from explainer.industry.works import aircraft as A


def test_programme_valley_and_learning():
    p = A.Programme()
    assert p.unit_cost(2) / p.unit_cost(1) == p.learning ** 1 or abs(p.unit_cost(2) / p.unit_cost(1) - p.learning) < 1e-12
    assert abs(p.unit_cost(400) / p.unit_cost(200) - p.learning) < 1e-12
    assert p.trough() < -p.dev                      # the valley is deeper than the development bill
    be = p.break_even()
    assert 500 < be["units"] < 1500 and be["year"] > p.dev_years + 5
    assert p.npv() > 0
    # the n-th aircraft first costs less than its price around the computed crossing
    n = p.unit_crosses_price()
    assert p.unit_cost(n * 1.01) < p.price < p.unit_cost(n * 0.99)
    # a learning curve of 0.9 instead of 0.82 sinks the programme
    assert A.Programme(learning=0.9).npv() < 0


def test_engine_paid_by_service():
    e = A.Engine().lifetime()
    assert e["sale"] < 0 < e["value"]
    assert 10 <= e["payback_years"] <= 20
    assert e["service_share"] > 0.6


def test_duel():
    r = A.run_it()
    assert r["equilibria"] == [("reengine", "reengine")]
    t = r["alt_table"]
    assert r["alt_equilibria"] == [("new", "new")]
    assert t[("reengine", "reengine")][0] > t[("new", "new")][0]     # the bigger leap makes it a prisoner's dilemma


def test_launch_aid_moves_a_flops_loss_to_governments():
    hit, flop = A.Programme(), A.Programme(rate=30, years=12)
    a_hit, a_flop = A.launch_aid(hit), A.launch_aid(flop)
    assert abs(a_hit["repaid"] - a_hit["loan"]) < 1          # a hit repays the loan in full
    assert a_hit["trough"] > hit.trough()                   # and the maker's hole is shallower
    unpaid = a_flop["loan"] - a_flop["repaid"]
    assert unpaid > 1e9                                     # a flop leaves governments holding the rest
    end = flop.flows()[-1]["cum"]
    assert abs((a_flop["cum"][max(a_flop["cum"])] - end) - unpaid) < 1e3   # the maker's loss shrinks by exactly that
