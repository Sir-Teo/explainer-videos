"""Tests for the Reasoner's consciousness module (Part 31)."""

from explainer.philosophy.reasoner import consciousness as C


def test_two_d_and_mary():
    d = C.two_d()["sentences"]
    assert d["water is H2O"]["necessary"] and not d["water is H2O"]["a_priori"]
    p = d["pain is C-fibre firing"]
    assert p["primary"] == p["secondary"] and not p["necessary"]
    m = C.mary()
    assert len(m["before"]) == 3 and len(m["after"]) == 1 and m["physical_agree"] == 1


def test_workspace_and_metacognition():
    w = C.workspace(trials=60)
    seen = [r["seen"] for r in w["rows"]]
    assert seen[0] == 0 and seen[-1] == 60 and all(a <= b + 6 for a, b in zip(seen, seen[1:]))
    assert w["late_low"] + w["late_high"] >= 0.95 * w["trials"]       # bimodal: ignition is all or none
    m = {r["observer"]: r for r in C.metacognition(trials=5000)["rows"]}
    assert abs(m["blindsight"]["correct"] - m["a normal observer"]["correct"]) < 1e-9
    assert m["a normal observer"]["auroc2"] > 0.65 and abs(m["blindsight"]["auroc2"] - 0.5) < 0.03


def test_phi_and_objections():
    ex = C.phi_examples()
    assert ex["two separate pairs"]["phi"] == 0 and ex["a feedforward chain"]["phi"] == 0
    assert ex["OR, AND, XOR loop"]["phi"] > 0
    a = {r["name"]: r["phi"] for r in C.aaronson()["rows"]}
    assert a["a 2-bit adder"] == 0 and min(v for k, v in a.items() if k != "a 2-bit adder") > 0
    u = C.unfolding()
    assert u["match"] == 8 and u["loop_phi"] > 0 and u["unrolled_phi"] == 0


def test_tmaze_introspection_indicators():
    t = C.tmaze()
    assert t["best"] == "look at the cue, then the cued arm" and t["F_exact"] < t["F_prior"] < t["F_wrong"]
    assert abs(t["F_exact"] - t["surprise"]) < 1e-9
    i = C.introspection()
    assert i["shades"] == 4096 and i["words"] == 11 and 0 < i["share_unsayable"] < 0.5
    ind = C.indicators()
    assert ind["total"] == 14 and ind["distinct"] == 6
