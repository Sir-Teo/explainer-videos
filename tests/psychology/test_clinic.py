import numpy as np

from explainer.psychology.psyche import clinic as K


def test_kappa_by_hand():
    # p_o = 0.85; p_e = 0.25*0.30 + 0.75*0.70 = 0.60; kappa = 0.25/0.40
    assert abs(K.kappa([[20, 5], [10, 65]]) - 0.625) < 1e-12
    assert abs(K.kappa([[50, 0], [0, 50]]) - 1.0) < 1e-12


def test_unreliable_diagnosis_cannot_be_valid():
    rows = [K.two_clinicians(noise=nz) for nz in (0.2, 0.5, 1.0, 2.0)]
    kap = [r["kappa"] for r in rows]
    val = [r["validity"] for r in rows]
    assert all(np.diff(kap) < 0) and all(np.diff(val) < 0)


def test_strong_connections_give_hysteresis():
    strong = K.sweep(c=1.0, reps=8)
    weak = K.sweep(c=0.2, reps=8)
    gap_strong = np.max(strong["down"] - strong["up"])
    gap_weak = np.max(weak["down"] - weak["up"])
    assert gap_strong > 4 and gap_weak < 2.5


def test_comorbidity_positive_manifold():
    m = K.comorbidity()
    off = m["R"][~np.eye(len(m["R"]), dtype=bool)]
    assert off.min() > 0 and m["pc1"] > 0.2


def test_screen_natural_frequencies():
    s = K.screen()
    assert abs(s["tp"] - 90) < 1e-9 and abs(s["fp"] - 891) < 1e-6 and 0.09 < s["ppv"] < 0.093


def test_formula_beats_wandering_clinician():
    r = K.clinician_vs_formula()
    assert r["clinician"] < r["unit"] <= r["ceiling"] + 1e-9 and r["fitted"] <= r["ceiling"] + 0.02


def test_avoidance_preserves_fear_and_exposure_extinguishes_it():
    kept = np.median([K.avoidance(seed=s)["fear"][-1] for s in range(21)])
    gone = K.avoidance(prevent=True)["fear"][-1]
    assert kept > 0.5 and gone < 0.05


def test_extinction_is_context_bound():
    r = K.renewal()
    assert r["test"]["B"] < 0.05 and r["test"]["A"] > 0.9 and r["test"]["C"] > 0.9


def test_triadic_design():
    esc, ines, none = (K.helplessness(p) for p in ("escapable", "inescapable", "none"))
    assert esc.mean() > 0.9 and ines.mean() < 0.2 and ines.mean() < none.mean() < esc.mean()


def test_mood_model_recovers_weights():
    d = K.mood_task(n=300, seed=1)
    f = K.fit_mood(d)
    assert abs(f["w"][3] - d["true_w"][3]) < 0.15 and f["r2"] > 0.4


def test_hollow_mask_needs_a_strong_prior():
    strong, weak = K.hollow_mask(8.0), K.hollow_mask(1.0)
    assert strong["p_convex"] > 0.9 and weak["p_convex"] < 0.1 and strong["mean"] > 0 > weak["mean"]


def test_prior_tradeoff_has_an_interior_optimum():
    pp = np.linspace(0, 20, 401)
    mse = K.prior_tradeoff(pp, p_typical=0.95)
    k = int(np.argmin(mse))
    assert 0 < k < len(pp) - 1
    assert np.argmin(K.prior_tradeoff(pp, p_typical=0.5)) < k


def test_strong_priors_condition_hallucinations():
    lo, hi = K.conditioned_hallucinations(0.3, reps=100), K.conditioned_hallucinations(1.5, reps=100)
    assert hi["overall"] > lo["overall"] + 0.1


def test_aberrant_salience_grows_with_bursts():
    assert K.aberrant_salience(0.0)["salient"] == 0 and K.aberrant_salience(0.3)["salient"] > 5


def test_redish_drug_value_never_settles():
    nat, drug = K.redish(0.0), K.redish(0.2, reward=0.5, cost=1.0)
    assert abs(nat[-1] - 1.0) < 1e-3 and drug[-1] > 5 and np.all(np.diff(drug) >= 0.1 * 0.2 - 1e-12)


def test_discount_reversal():
    k = 0.05
    assert K.discount(50, 0, k) > K.discount(100, 30, k) and K.discount(50, 60, k) < K.discount(100, 90, k)


def test_extinction_in_more_contexts_generalizes():
    r = K.renewal_contexts()
    assert np.all(np.diff(r["fear"]) < 0) and r["fear"][0] > 0.6 and r["fear"][-1] < 0.25


def test_scheduled_activity_breaks_the_trap():
    stuck = np.median([K.activation(0, seed=s)["active"][-30:].mean() for s in range(21)])
    freed = np.median([K.activation(14, seed=s)["active"][-30:].mean() for s in range(21)])
    assert stuck < 0.2 and freed > 0.8


def test_every_arm_improves_and_the_control_sets_the_effect():
    changes = {a: K.therapy_trial(a)["change"] for a in K.ARMS}
    assert all(c < -3 for c in changes.values())
    assert K.trial_effect("active", "waitlist", n=1000) > K.trial_effect("active", "placebo", n=1000) + 0.3


def test_publication_filter_inflates_and_random_effects_recovers():
    p = K.publication_filter()
    allr = K.random_effects(p["d"], p["v"])
    pub = K.random_effects(p["d"][p["published"]], p["v"][p["published"]])
    assert abs(allr["mu"] - 0.3) < 0.06 and pub["mu"] > allr["mu"] + 0.08


def test_random_effects_matches_fixed_when_homogeneous():
    r = K.random_effects([0.5, 0.5, 0.5], [0.1, 0.2, 0.3])
    assert r["tau2"] == 0 and abs(r["mu"] - 0.5) < 1e-12


def test_reliable_change_and_cutoff():
    assert abs(K.reliable_change(28, 16, 7, 0.85) + 12 / (np.sqrt(2) * 7 * np.sqrt(0.15))) < 1e-12
    assert abs(K.jt_cutoff(28, 6, 7, 5) - (6 * 7 + 5 * 28) / 11) < 1e-12
    assert abs(K.dose_response(8) - 0.5) < 1e-12 and abs(K.dose_response(26) - 0.75) < 1e-9


def test_jt_categories_sum_to_one_and_regression_fools_them():
    r = K.therapy_trial("none", n=2000, seed=3)
    c = K.jt_categories(r["pre"], r["post"], float(np.sqrt(50)), 0.85, 20.8)
    assert abs(sum(c.values()) - 1) < 1e-12 and c["recovered"] > 0.2
