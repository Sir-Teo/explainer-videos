import numpy as np
import pytest

from explainer.psychology.psyche import conditioning as C


def test_rescorla_wagner_is_gradient_descent_and_learns_the_classics():
    rng = np.random.default_rng(0)
    v, x = rng.normal(size=3), np.array([1.0, 0.0, 1.0])
    eps = 1e-6
    num = np.array([((0.7 - x @ (v + eps * e)) ** 2 - (0.7 - x @ (v - eps * e)) ** 2) / (4 * eps)
                    for e in np.eye(3)])
    assert np.allclose(C.rw_gradient(v, x, 0.7), num, atol=1e-6)
    # acquisition approaches λ, extinction returns to 0
    _, V = C.rescorla_wagner(C.sequence([("A+", 60), ("A-", 60)]))
    assert V[60, 0] == pytest.approx(1.0, abs=1e-3) and V[-1, 0] == pytest.approx(0.0, abs=1e-3)
    # blocking: X learns almost nothing after A already predicts the outcome
    _, Vb = C.rescorla_wagner(C.sequence([("A+", 30), ("AX+", 20)]))
    _, Vc = C.rescorla_wagner(C.sequence([("AX+", 20)]))
    assert Vb[-1, 1] < 0.02 < 0.45 < Vc[-1, 1]
    # conditioned inhibition and overexpectation
    _, Vi = C.rescorla_wagner(C.sequence([("A+ AX-", 300)]))
    assert Vi[-1, 1] == pytest.approx(-1.0, abs=0.02)
    _, Vo = C.rescorla_wagner(C.sequence([("A+ B+", 80), ("AB+", 60)]))
    assert Vo[80, 0] > 0.99 and Vo[-1, 0] == pytest.approx(0.5, abs=0.01)


@pytest.mark.parametrize("p1,p0", [(0.6, 0.2), (0.8, 0.8), (0.3, 0.7), (0.4, 0.0)])
def test_the_asymptote_is_the_contingency(p1, p0):
    cues, V = C.rw_asymptote([("CX", 0.25, p1), ("C", 0.75, p0)])
    assert cues == "CX"
    assert V[1] == pytest.approx(C.delta_p(p1, p0)) and V[0] == pytest.approx(p0)
    # simulation agrees with the solved asymptote on average
    sims = [C.contingency_learning(p1, p0, n=1500, rng=np.random.default_rng(s), alpha=0.05)[-300:].mean()
            for s in range(6)]
    assert np.mean(sims) == pytest.approx(p1 - p0, abs=0.05)


def test_outcome_density_biases_ratings_before_the_asymptote():
    hi = np.mean([C.contingency_learning(0.75, 0.75, n=20, rng=np.random.default_rng(s))[-1] for s in range(400)])
    lo = np.mean([C.contingency_learning(0.25, 0.25, n=20, rng=np.random.default_rng(s))[-1] for s in range(400)])
    assert hi > lo + 0.05 and lo > -0.02


def test_rescorla_1968_orders_like_the_paper():
    med = {g: np.median([C.rescorla_1968(*g, rng=np.random.default_rng(s)) for s in range(8)])
           for g in C.RESCORLA_1968_GROUPS}
    for p in (0.4, 0.2, 0.1):  # equal probabilities: little or no conditioning
        assert abs(med[(p, p)]) < 0.1
    assert med[(0.4, 0.0)] > med[(0.4, 0.1)] > med[(0.4, 0.2)] > med[(0.4, 0.4)]
    assert C.suppression_ratio(0.0) == pytest.approx(0.5)


def test_attention_rules_disagree_about_what_deserves_it():
    seq = C.sequence([("A+ B+ A+ B-", 200)])
    _, _, Am = C.mackintosh(seq)
    _, _, Ap = C.pearce_hall(seq)
    assert Am[-1, 0] > 0.9 > 0.2 > Am[-1, 1]  # Mackintosh: the reliable predictor
    assert Ap[-1, 1] > 0.3 > 0.05 > Ap[-1, 0]  # Pearce-Hall: the uncertain one
    # latent inhibition: preexposure slows Pearce-Hall but not Rescorla-Wagner
    _, Vp, _ = C.pearce_hall(C.sequence([("X-", 40), ("X+", 4)]))
    _, Vn, _ = C.pearce_hall(C.sequence([("X+", 4)]))
    assert Vp[-1, 0] < 0.5 * Vn[-1, 0]


def test_extinction_is_new_learning_bound_to_its_context():
    assert C.renewal("AAA") == pytest.approx(0.0, abs=0.01)
    assert C.renewal("ABA") > 0.7 and C.renewal("ABC") > 0.7
    probes, curve = C.extinction_in_context([("A", 1.0, 20), ("A", 0.0, 40), ("test", "A", 0.0),
                                             ("test", "A", 24.0)], tau=40.0)
    assert probes[0] < 0.01 < 0.3 < probes[1] < 0.6  # partial spontaneous recovery
    assert curve[19] > 0.99


def test_operant_signatures_and_shaping():
    rng = np.random.default_rng(2)
    fr, _ = C.schedule("FR", 20, rng=rng)
    vr, _ = C.schedule("VR", 20, rng=rng)
    fi, rfi = C.schedule("FI", 60, rng=rng)
    vi, _ = C.schedule("VI", 60, rng=rng)
    assert len(vr) > len(fr) and len(fr) > len(vi)
    # the FI scallop: more responses late in the interval than early
    since = np.array([t - rfi[rfi < t].max() for t in fi if (rfi < t).any()])
    assert (since > 40).sum() > 3 * (since < 20).sum()
    mu, hit = C.shaping(rng=np.random.default_rng(1))
    mu0, hit0 = C.shaping(rng=np.random.default_rng(1), successive=False)
    assert mu[-1] > 2.5 > 1.0 > mu0[-1] and hit > 0.3 > 0.01 > hit0
    lat = np.median([C.puzzle_box(rng=np.random.default_rng(s)) for s in range(200)], axis=0)
    assert lat[:3].mean() > 3 * lat[-3:].mean()


def test_melioration_matches_on_vi_and_goes_exclusive_on_vr():
    B, R = C.concurrent(means=(30.0, 90.0), rng=np.random.default_rng(1))
    assert B[0] / B.sum() == pytest.approx(R[0] / R.sum(), abs=0.06)
    Bv, _ = C.concurrent(kind=("VR", "VR"), means=(20.0, 40.0), rng=np.random.default_rng(1))
    assert Bv[0] / Bv.sum() > 0.9
    assert C.melioration_trap().mean() < 1.5 < 2.9 < C.melioration_trap(policy="maximize").mean()


def test_timing_is_scalar_and_rw_misses_the_spacing_law():
    t = np.linspace(0, 120, 1201)
    a, b = C.peak_curve(t, 20), C.peak_curve(t, 40)
    u = np.linspace(0, 2, 50)
    assert np.interp(u, t / 20, a) == pytest.approx(np.interp(u, t / 40, b), abs=1e-3)
    r = np.array([1, 4, 16])
    assert C.reinforcements_to_acquisition(r)[0] / C.reinforcements_to_acquisition(r)[-1] == pytest.approx(16)
    rw = C.rw_trials_to_criterion(r)
    assert rw[0] / rw[-1] < 3
