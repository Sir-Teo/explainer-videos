from explainer.philosophy.reasoner import theism as T


def test_plantinga_needs_s5():
    r = T.plantinga(3)
    assert r["S5"]["argument"]["valid_on"] == r["S5"]["argument"]["frames"]
    assert r["S5"]["mirror"]["valid_on"] == r["S5"]["mirror"]["frames"]
    assert r["S4"]["argument"]["valid_on"] < r["S4"]["argument"]["frames"]
    assert r["B"]["conclusion"]["valid_on"] == r["B"]["conclusion"]["frames"]


def test_godel_inconsistent_scott_collapses():
    g = T.godel()
    assert all(row["models"] == 0 for row in g["godel"])
    scott = g["scott"]
    assert sum(row["models"] for row in scott) > 0
    for row in scott:
        assert row["collapse"] == row["models"] == row["god_everywhere"] == row["one_god"]
        if row["worlds"] > 1:
            assert row["models"] == 0


def test_psr_collapse_and_fine_tuning():
    assert all(r["explainers_of_bccf"] == 0 for r in T.psr_collapse()["rows"])
    f = T.fine_tuning()
    assert f["posterior_this"]["multiverse"] == f["posterior_this"]["single chance"]
    assert f["posterior_some"]["multiverse"] > f["posterior_some"]["single chance"]


def test_wager_rowe_hume_branching():
    p = T.pascal()
    assert [r["eu"] for r in p["rows"]].count(float("inf")) == 4
    r = T.rowe()["rows"]
    assert r[0]["posterior"] < r[-1]["posterior"]
    h = T.hume()
    assert h["rows"][1]["posterior"] < 0.001 and h["first_over_half"] == 4
    s = T.sea_battle()
    assert not s["peircean"]["F battle or F no battle"] and s["peircean"]["F (battle or no battle)"]
    assert s["settled"]["F battle or F no battle"] and not s["settled"]["F battle"]
