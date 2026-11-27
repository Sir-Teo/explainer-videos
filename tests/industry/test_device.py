"""The Works' electronics business (Part 16): the split adds up, turnkey revenue makes the margin thin without changing
the profit, and Run it's renewal probability decides the order."""

from explainer.industry.works import device as D


def test_split_adds_to_price_and_turnkey_only_changes_the_margin():
    d = D.Device()
    assert abs(sum(d.split().values()) - d.price) < 1e-9
    t, c = D.Assembler(turnkey=True).year(20e6, d), D.Assembler(turnkey=False).year(20e6, d)
    assert abs(t["profit"] - c["profit"]) < 1e-3
    assert t["margin"] < 0.05 < c["margin"]
    assert t["revenue"] / c["revenue"] == (d.bom + d.fee) / d.fee


def test_run_it_depends_on_renewal():
    b0, b1 = D.play("build", 0.0), D.play("build", 1.0)
    assert b0["expected"] < 0 < b1["expected"]
    p = b0["break_even_p"]
    assert 0.2 < p < 0.5
    assert abs(D.play("build", p)["expected"]) < 1.0
    # building abroad pays only when renewal is likely
    assert D.play("abroad", 0.2)["expected"] < D.play("build", 0.2)["expected"]
    assert D.play("abroad", 0.9)["expected"] > D.play("build", 0.9)["expected"]
    assert D.play("decline", 0.5)["expected"] == 0.0
