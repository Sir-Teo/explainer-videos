"""Tests for the Reasoner's mind module (Part 30)."""

from explainer.philosophy.reasoner import mind as M


def test_realizers_and_rulebook():
    r = M.realizers(steps=300)
    assert r["agree"] == 300
    rb = M.rulebook()
    assert rb["narrow_right"] == len(rb["narrow"]) and rb["wide_unmatched"] >= 1


def test_blockhead_and_supervenience():
    b = M.blockhead()
    assert b["rows"][-1]["log10_entries"] > 10 * b["log10_atoms"]
    s = M.supervenience()
    assert (s["A"]["weak"], s["A"]["strong"], s["A"]["global"]) == (True, False, False)
    assert (s["B"]["weak"], s["B"]["global"]) == (False, True)
    assert all(s["C"][k] for k in ("weak", "strong", "global"))


def test_life_gauge_systematicity_probe():
    lf = M.life(gens=120)
    assert lf["glider_c4"] and lf["gliders_out"] >= 3
    g = M.gauge()
    assert g["rows"][0]["bits"] == 2.0 and g["rows"][1]["bits"] < 2.0 and g["rows"][1]["readings_certain"] == 0
    sy = M.systematicity()
    assert sy["comp_right"] == sy["test"] and sy["table_right"] == 0
    p = M.probe_vs_use()["rows"]
    assert p[0]["probe_x"] > 0.95 and p[-1]["probe_x"] < 0.55 and p[-1]["task_y"] > 0.95


def test_ramsey_proportional_patterns():
    r = M.ramsey()
    assert (r["brain"]["candidates"], r["brain"]["realizations"]) == (1806, 1)
    assert r["brain"]["found"][0]["hurt"] == ["h1", "h2", "h3"]
    assert r["tank"]["realizations"] == 1 and r["thermostat"]["realizations"] == 0
    assert r["weak"]["without aspirin"]["realizations"] == 1 and r["weak"]["bumps only"]["realizations"] == 2
    q = {row["cause"]: row for row in M.proportional()["rows"]}
    assert q["red"]["info"] == q["the exact shade"]["info"] > q["scarlet"]["info"] > q["coloured"]["info"] == 0
    assert q["red"]["cause_bits"] < q["the exact shade"]["cause_bits"]
    f = M.real_patterns()["frames"]
    assert f[0]["ratio_two_part"] < 0.05 and f[-1]["ratio_two_part"] > 1.0
    assert all(a["ratio_two_part"] < b["ratio_two_part"] for a, b in zip(f, f[1:]))


def test_glider_law():
    g = M.glider_law(gens=300)
    assert g["holds"] == g["points"] == 11
