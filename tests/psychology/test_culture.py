import numpy as np

from explainer.psychology.psyche import culture as C


def test_conformist_transmission_amplifies_the_majority():
    assert C.conformist_path(0.4)[-1] < 0.01
    assert C.conformist_path(0.6)[-1] > 0.99
    assert abs(C.conformist_step(0.5) - 0.5) < 1e-12
    # the finite simulation follows the expected step on average
    sims = np.array([C.conformist_sim(n=400, p0=0.4, generations=1, seed=s)[1] for s in range(200)])
    assert abs(sims.mean() - C.conformist_step(0.4)) < 0.01


def test_henrich_critical_population():
    n_star = C.critical_size()
    assert abs(C.skill_change(n_star)) < 1e-9
    assert C.tasmania(20)[-1] < C.tasmania(20)[0] < C.tasmania(200)[-1]


def test_reference_group_hides_a_real_difference():
    r = C.reference_group()
    assert abs(r["gap_report"]) < 0.1 and r["gap_behaviour"] > 0.4


def test_trolley_order_is_shared_and_levels_vary():
    t = C.trolley()
    f = C.fit_trolley(t["share"])
    assert f["order_same"] == 1.0
    assert np.all(np.diff(f["case"]) < 0)
    assert np.ptp(t["share"][:, 2]) > 0.2


def test_prestige_bias_spreads_a_useless_marker():
    p = C.prestige_sim()
    assert p["share"][0] < 0.15 and p["share"][-1] > 0.6
