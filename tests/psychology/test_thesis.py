"""The dissertation's registered report (Part 62)."""

import numpy as np
import pytest

from explainer.psychology.psyche import thesis as Th

REGISTERED = "1ee2fa7b1189547d57863b673b825ff6d434d63461032bd0d718fd6919aee462"


def test_plan_is_unchanged_since_registration():
    assert Th.plan_hash() == REGISTERED
    assert Th.DEVIATION["registered_min_per_cell"] == 4 and Th.DEVIATION["used_min_per_cell"] == 2


def test_spearman_brown():
    assert Th.spearman_brown(0.5) == pytest.approx(2 / 3)
    assert Th.spearman_brown(0.58) == pytest.approx(1.16 / 1.58)


def test_simulated_reliability_is_recovered():
    rels = []
    for s in range(30):
        h = Th.simulate_halves(n_people=200, true_rel=0.6, seed=s)
        rels.append(Th.reliability(h["slope_odd"], h["slope_even"]))
    assert abs(np.mean(rels) - 0.6) < 0.05


def test_decision_rule():
    assert Th.verdict({"slope_ci": [0.3, 0.6], "diff_ci": [0.1, 0.2]}) == {"H1": "supported", "H2": "supported"}
    assert Th.verdict({"slope_ci": [0.75, 0.9], "diff_ci": [-0.1, 0.2]})["H1"] == "refuted"
    assert Th.verdict({"slope_ci": [0.5, 0.9], "diff_ci": [-0.1, 0.2]}) == {"H1": "inconclusive", "H2": "not supported"}


def test_person_halves_rules():
    rng = np.random.default_rng(0)
    rows = {"subject": [], "trial": [], "rt": [], "same": [], "angle": [], "correct": []}
    for s in range(5):
        for t in range(1, 97):
            a = [0, 50, 100, 150][(t // 2) % 4]  # every angle in both odd and even trials
            rows["subject"].append(s)
            rows["trial"].append(t)
            rows["angle"].append(float(a))
            rows["same"].append((t // 8) % 2 == 0)
            rows["correct"].append(True)
            rows["rt"].append(1000 + 10 * a + rng.normal(0, 100))
    d = {k: np.array(v) for k, v in rows.items()}
    h = Th.person_halves(d, min_per_cell=2)
    assert len(h["subject"]) == 5 and h["excluded"] == 0
    assert np.allclose(h["slope_odd"], 10, atol=3)


def test_ledger_by_act_counts_every_row():
    from explainer.psychology import ledger
    b = Th.ledger_by_act(ledger.rows())
    assert b["table"].sum() == len(ledger.rows())


def test_scorecard_runs():
    rows = Th.scorecard(seed=1)
    assert len(rows) == 13
    assert sum(1 for r in rows if r[4] is None) == 6


def test_ledger_by_decade_counts_every_row_once():
    from explainer.psychology import ledger
    rows = ledger.rows()
    b = Th.ledger_by_decade(rows)
    assert b["table"].sum() == len(rows)
    share = b["table"][:, 0] / b["table"].sum(1)
    assert share[0] > share[-1]

