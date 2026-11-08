from explainer.philosophy.reasoner import persist as P


def test_black_spheres_are_weakly_discernible():
    b = P.black_spheres()
    assert b["spheres"]["grade"] == "weak" and b["singlet"]["grade"] == "weak"
    assert b["one red"]["grade"] == "absolute" and b["no relation"]["grade"] == "indiscernible"
    assert b["arrow"]["relative"]


def test_reid_and_theseus():
    r = P.reid()
    assert r["verdicts"] == {"boy = officer": True, "officer = general": True, "boy = general": False}
    assert r["closure_boy_general"] and not r["direct_transitive"]
    t = P.theseus(20)
    assert t["share_repaired"][0] == 1.0 and t["share_repaired"][-1] == 0.0 and t["share_rebuilt"][-1] == 1.0


def test_evans_needs_rigidity():
    e = P.evans()
    assert e["rigid_vague"] == 0 and e["nonrigid_vague"] > 0


def test_fission():
    f = P.fission()
    assert f["t0_L4"] and f["t0_R4"] and f["shared"] == ["t0", "t1", "t2"]


def test_weight_drift_separates_connectedness_from_continuity():
    r = P.weight_drift()
    assert r["final"] < 0.35 and r["min_step"] > 0.95
    assert r["below_half_at"] is not None and 10 < r["below_half_at"] < r["steps"]
