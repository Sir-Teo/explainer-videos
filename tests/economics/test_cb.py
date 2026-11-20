"""Agora's central bank (Part 31): the market for reserves, the Island's monetary history and four ways to identify
a policy shock against the truth, the natural rate by the Kalman filter, self-fulfilling sovereign yields, and the
event-study arithmetic."""

import numpy as np
import pytest

from explainer.economics.agora import cb


def test_corridor_and_floor():
    c = cb.corridor_and_floor(1.0, 3.0, 50.0, 15.0)
    assert c["corridor_R"] == pytest.approx(50.0)
    assert c["corridor_i"] == pytest.approx(2.0)
    assert c["slope_per_unit"] == pytest.approx(-2 * 0.398942 / 15, rel=1e-3)
    assert c["floor_i"] == pytest.approx(1.0, abs=1e-6)
    i = cb.reserve_demand(np.array([280.0, 300.0, 320.0]), 1.0, 3.0, 50.0, 15.0)
    assert np.ptp(i) < 1e-6                                                       # flat on the floor


def test_true_response_is_a_delayed_fall():
    t = cb.true_irf(16)
    assert t["i"][0] == pytest.approx(1.0)
    assert t["y"][0] == 0 and min(t["y"]) < -0.3
    assert cb.peak(t["y"])["h"] == 3
    assert t["pi"][1] == 0 and t["pi"][-1] < -0.1


def test_methods_against_the_truth():
    R = cb.identification_mc(reps=40, T=240, h=12, seed=5)
    tr = R["truth"]
    m = R["methods"]
    assert m["naive"]["y"]["mean"][1] > 0.5                                        # rate rises "cause" booms
    assert m["var"]["pi"]["mean"][4] > 0.2                                         # the price puzzle
    assert m["var_news"]["pi"]["mean"][4] < m["var"]["pi"]["mean"][4]              # a proxy shrinks it
    for k in ("narrative", "hf_clean"):
        assert np.allclose(m[k]["y"]["mean"][:8], tr["y"][:8], atol=0.08)
    assert m["hf_info"]["y"]["mean"][1] > m["hf_clean"]["y"]["mean"][1] + 0.2     # the information effect
    assert R["narrative_corr"] > 0.95


def test_rstar_filter_tracks_with_honest_bands():
    r = cb.rstar_island(T=400, seed=1)
    truth, est = np.array(r["truth"]), np.array(r["estimate"])
    assert np.corrcoef(truth[40:], est[40:])[0, 1] > 0.8
    assert 0.7 < r["coverage90"] <= 1.0
    assert 0.2 < r["steady_se"] < 1.5


def test_debt_game_and_backstop():
    pr = cb.debt_params(1.2, 0.02, 0.025, 0.06)
    free = cb.debt_game(1.2, 0.02, cap=None, **pr)
    assert free["equilibria"] == pytest.approx([0.025, 0.06], abs=2e-4)
    assert free["stable"] == pytest.approx([0.025], abs=2e-4)
    capped = cb.debt_game(1.2, 0.02, cap=0.035, **pr)
    assert capped["equilibria"] == pytest.approx([0.025], abs=2e-4)
    up = cb.debt_path(0.064, periods=8, debt=1.2, rf=0.02, **pr)
    assert not np.isfinite(up[-1])                                                 # a spiral: no one lends
    down = cb.debt_path(0.064, periods=30, debt=1.2, rf=0.02, cap=0.035, **pr)
    assert down[-1] == pytest.approx(0.025, abs=1e-3)


def test_event_changes():
    s = {"2009-03-17": 3.0, "2009-03-18": 2.5, "2009-03-19": 2.6}
    ev = cb.event_changes(["2009-03-18", "2009-03-20"], s)
    assert len(ev) == 1 and ev[0]["change"] == pytest.approx(-0.5)
    qe = cb.qe_t_accounts(100)
    assert qe["central_bank"]["assets"]["bonds"] == qe["central_bank"]["liabilities"]["reserves"] == 100
