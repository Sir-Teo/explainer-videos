"""Tests for the Reasoner's free will module (Part 32)."""

from explainer.philosophy.reasoner import freewill as F


def test_rules_on_the_coin():
    r = F.rule_check()
    assert r["pairs"] == 64 and r["alpha_fail"] == 0 and r["beta_box_fail"] == 0
    assert r["beta_fail"] >= 1 and r["agg_fail"] >= 1
    assert r["N_no_heads"] and r["N_no_tails"] and not r["N_both"]


def test_frankfurt_rollback_prediction():
    f = F.frankfurt()
    assert f["N_shoots"] and not f["N_on_his_own"] and not f["can_avoid_shooting"] and f["can_avoid_own"]
    r = F.rollback()
    assert abs(r["running"][-1] - r["p"]) < 0.05
    s = F.self_prediction()
    assert s["public_right"] == 0 and all(s["differs"])


def test_accumulator():
    a = F.accumulator(trials=200)
    assert a["crossed"] > 150 and a["rp_end"] > a["rp_start"] + 0.1
    assert -1.0 < a["half_rise"] < 0


def test_miracles_interruptus_responsibility():
    m = F.miracles()
    assert m["miracle_changes_act"] and m["lawful_diff_at_0"] > 1
    assert all(d > 0 for t, d in enumerate(m["lawful_diff_per_t"]) if t not in (m["steps"] - 1,))
    i = F.interruptus(trials=800)
    rts = [b["mean_rt_ms"] for b in i["bins"]]
    assert rts == sorted(rts, reverse=True) and i["corr"] < -0.5
    r = F.responsibility()
    assert r["votes"][0]["degree"] == 1.0 and abs(r["votes"][-1]["degree"] - 1 / 6) < 1e-3
    assert r["hands"] == {"designer": 1.0, "deployer": 0.5, "overseer": 0.5}


def test_responsive_and_chsh():
    a = F.reasons_responsive()["agents"]
    assert a["a responsive agent"]["moderate"] and not a["an erratic agent"]["moderate"]
    assert not a["a compulsive agent"]["weak"]
    c = F.chsh_local()
    assert c["strategies"] == 16 and c["max"] == 2 and c["tsirelson"] > 2.8


def test_levels_and_torn():
    lv = F.levels()
    assert lv["fine_deterministic"] and lv["deterministic_rows"] == []
    assert all(abs(sum(r.values()) - 1) < 1e-3 for r in lv["probs"].values())
    t = F.torn_decision(exponents=(3, 6))
    assert t["rows"][0]["side"] == "right" and t["rows"][0]["mirror"] == "left"
    assert abs(t["slope"] - t["ln10_over_lambda"]) < 0.01


def test_blame_ledgers():
    b = F.blame_ledgers()
    assert b["risk_total"] == 5.0 and b["outcome_total"] == 6.0 and b["p_some_victim"] == 0.9933


def test_avoider_is_deterministic_and_avoids():
    a = F.avoider()
    assert a["deterministic"] and a["sighted_hits"] == 0 and a["blind_hits"] > 0 and a["dodges"] > 0
