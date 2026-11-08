"""Part 16's Reasoner: p-values, base rates, PPV, the garden of forking paths, optional stopping, Birnbaum's toy,
Lindley's paradox, severity, Simpson's paradox, betting and Ville's inequality, A/B peeking, AIC and BIC."""

import math

from explainer.philosophy.reasoner import stats as S


def test_distributions_and_t():
    assert abs(S.t_two_sided(2.024, 38) - 0.05) < 1e-3
    assert abs(S.p_two_sided(1.959964) - 0.05) < 1e-5
    assert abs(S.z_of_p(0.05) - 1.959964) < 1e-4
    d = S.p_distribution(sims=4000)
    assert abs(d["null_below_05"] - 0.05) < 0.015 and d["power"] > 0.5


def test_base_rate_and_ppv():
    b = S.base_rate()
    assert (b["sick"], b["tp"], b["fp"]) == (10, 9, 89) and abs(b["ppv_exact"] - 0.0917) < 1e-3
    vals = [round(r["ppv"], 2) for r in S.ioannidis_table()]
    assert vals[:7] == [0.85, 0.85, 0.41, 0.23, 0.17, 0.20, 0.12]


def test_garden_and_stopping():
    g = {r["freedom"]: r["rate"] for r in S.garden(studies=600)["rows"]}
    assert g["none"] < 0.08 and g["all four"] > 0.2
    o = S.optional_stopping(runs=300)
    assert o["final"] > 0.2 and o["lr_ever_10"] <= 0.12


def test_birnbaum_lindley_severity():
    b = S.birnbaum()
    assert b["proportional"] and b["p_binomial"] > 0.05 > b["p_negative_binomial"]
    rows = S.lindley()["rows"]
    assert all(abs(r["p"] - 0.0455) < 1e-3 for r in rows) and rows[0]["bf01"] < 1 < rows[-1]["bf01"]
    assert abs(S.prior_sensitivity()["max_bf10"] - math.e ** 2) < 1e-9
    s = S.severity()
    assert s["significant"]["sev_greater"][0] > 0.99


def test_simpson_and_betting():
    s = S.simpson()
    assert s["men_rate"] > s["women_rate"] and s["depts_women_higher"] == 4
    b = S.betting(runs=1500)
    assert all(b["ville"][str(a)] <= a + 0.015 for a in (0.2, 0.1, 0.05, 0.01))
    ab = S.ab_peeking(runs=150)
    assert ab["peeking_fp"] > 0.15 and ab["e_process_fp"] <= 0.08


def test_aic_bic():
    a = S.aic_bic(reps=60)
    assert a["best_predictive"] == 3 and a["bic_picks"][3] >= a["aic_picks"][3]
