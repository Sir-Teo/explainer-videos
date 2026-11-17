"""Psyche's working memory (Part 19): each model against a closed form, a recovery check or its signature."""

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import ks_2samp

from explainer.psychology.psyche import wm


def test_von_mises_helpers_are_consistent():
    k = np.array([0.5, 2.0, 8.0, 40.0])
    assert np.allclose(wm.kappa_of_J(wm.fisher_J(k)), k, rtol=1e-4)
    assert np.allclose(wm.kappa_of_sd(wm.circ_sd(k)), k, rtol=1e-3)
    assert np.isclose(quad(lambda x: wm.vm_pdf(x, 3.0), -np.pi, np.pi)[0], 1.0)
    rng = np.random.default_rng(1)
    x = rng.vonmises(0, 5.0, 200_000)
    assert abs(np.sqrt(-2 * np.log(abs(np.mean(np.exp(1j * x))))) - wm.circ_sd(5.0)) < 0.005
    # Fisher information of a von Mises: the variance of the score sin(x) kappa
    assert abs(np.var(5.0 * np.sin(x)) - wm.fisher_J(5.0)) < 0.05 * wm.fisher_J(5.0)


def test_phonological_loop_word_length_and_suppression():
    short, long = wm.loop_span(0.3), wm.loop_span(0.9)
    assert short["span"] > long["span"] + 2
    s_short, s_long = wm.loop_span(0.3, suppress=True), wm.loop_span(0.9, suppress=True)
    assert abs(s_short["span"] - s_long["span"]) < 1e-9  # suppression abolishes the word-length effect
    assert s_short["span"] < short["span"]
    assert np.all(np.diff(short["p"]) <= 1e-9)


def test_partial_report_beats_whole_report_and_fades():
    r = wm.partial_report([0, 150, 300, 1000, 5000])
    assert r["available"][0] > 2 * r["whole"]
    assert np.all(np.diff(r["available"]) < 0)
    assert abs(r["available"][-1] - r["whole"]) < 0.01


def test_simple_first_trial_shows_no_forgetting_and_later_trials_do():
    d = np.array([3, 6, 9, 12, 15, 18.0])
    first = wm.brown_peterson(d, 1)
    assert np.all(first > 0.95)
    late = np.mean([wm.brown_peterson(d, t) for t in range(5, 21)], 0)
    assert np.all(np.diff(late) < 0) and late[0] > 0.7 and late[-1] < 0.2
    # forgetting at 18 s grows over the first few trials (Keppel and Underwood)
    p18 = [wm.brown_peterson([18.0], t)[0] for t in (1, 2, 3, 6)]
    assert p18[0] > p18[1] > p18[2] > p18[3]


def test_sternberg_models():
    rng = np.random.default_rng(3)
    sizes = np.array([1, 2, 4, 6])
    mean = {(m, pos): np.array([wm.sternberg_rts(k, pos, m, n=20000, rng=rng).mean() for k in sizes])
            for m in ("serial", "self", "parallel", "limited") for pos in (True, False)}

    def slope(y):
        return np.polyfit(sizes, y, 1)[0]

    assert abs(slope(mean["serial", True]) - 38) < 2 and abs(slope(mean["serial", False]) - 38) < 2
    assert abs(slope(mean["self", True]) - 19) < 2  # self-terminating: half the slope on positive trials
    assert abs(slope(mean["limited", True]) - 38) < 2
    # unlimited-capacity parallel: the slowest of k grows like the harmonic number, not linearly
    h = np.array([sum(1 / j for j in range(1, k + 1)) for k in sizes])
    assert np.allclose(mean["parallel", True] - 397, 38 * h, atol=3)
    # limited-capacity parallel with reallocation has the serial distribution
    a = wm.sternberg_rts(4, True, "serial", n=20000, base_sd=0, rng=rng)
    b = wm.sternberg_rts(4, True, "limited", n=20000, base_sd=0, rng=rng)
    assert ks_2samp(a, b).pvalue > 0.001


def test_change_detection_k():
    rng = np.random.default_rng(4)
    for N in (4, 6, 8):
        r = wm.change_detection(N, K=3.0, guess=0.4, n=100_000, rng=rng)
        assert abs(wm.k_cowan(r["H"], r["FA"], N) - 3.0) < 0.1
    r = wm.change_detection(2, K=3.0, n=10_000, rng=rng)
    assert r["H"] == 1.0 and r["FA"] == 0.0
    assert np.isclose(wm.k_pashler(0.8, 0.2, 6), 6 * 0.6 / 0.8)


def test_mixture_and_swap_fits_recover_their_parameters():
    rng = np.random.default_rng(5)
    n = 6000
    g, k = 0.3, 8.0
    e = np.where(rng.random(n) < g, rng.uniform(-np.pi, np.pi, n), rng.vonmises(0, k, n))
    f = wm.fit_mixture(e)
    assert abs(f["g"] - g) < 0.03 and abs(f["kappa"] - k) < 1.0
    # swaps: a quarter of responses go to one of three non-targets
    nt = rng.uniform(-np.pi, np.pi, (n, 3))
    which = rng.integers(0, 3, n)
    u = rng.random(n)
    centre = np.where(u < 0.25, nt[np.arange(n), which], 0.0)
    resp = np.where(u > 0.9, rng.uniform(-np.pi, np.pi, n), centre + rng.vonmises(0, k, n))
    s = wm.fit_swap(resp, resp[:, None] - nt)
    assert abs(s["pN"] - 0.25) < 0.03 and abs(s["pU"] - 0.10) < 0.03 and abs(s["kappa"] - k) < 1.0


@pytest.mark.parametrize("model", ["slots", "averaging", "equal", "variable"])
def test_process_model_densities_integrate_to_one(model):
    params = {"slots": (3.0, 10.0), "averaging": (3, 10.0), "equal": (20.0, 1.2), "variable": (20.0, 1.0, 8.0)}[model]
    x = np.linspace(-np.pi, np.pi, 4001)
    for N in (1, 2, 4, 6):
        f = wm.model_pdf(model, params, x, np.full(len(x), N))
        assert abs(np.trapezoid(f, x) - 1) < 1e-3


def test_model_comparison_picks_the_generating_model():
    rng = np.random.default_rng(6)
    N = np.repeat([1, 2, 4, 6], 400)
    e_vp = wm.simulate_report("variable", (25.0, 1.0, 15.0), N, rng)
    e_sl = wm.simulate_report("slots", (2.5, 12.0), N, rng)
    aic_vp = {m: wm.fit_model(m, e_vp, N)["aic"] for m in ("slots", "variable")}
    aic_sl = {m: wm.fit_model(m, e_sl, N)["aic"] for m in ("slots", "variable")}
    assert aic_vp["variable"] < aic_vp["slots"]
    assert aic_sl["slots"] < aic_sl["variable"] + 4  # VP nests slots-like tails only approximately
    f = wm.fit_model("slots", e_sl, N)
    assert abs(f["params"][0] - 2.5) < 0.4


def test_ring_attractor_holds_and_diffuses():
    r = wm.ring_attractor(delay=2000, trials=120, rng=np.random.default_rng(7))
    t, var = r["t"], np.var(r["angle"], 0)
    assert np.degrees(np.sqrt(var[-1])) < 30  # the bump survives two seconds without input
    i1, i2 = np.searchsorted(t, 500), np.searchsorted(t, 2000) - 1
    ratio = var[i2] / var[i1]
    assert 2.0 < ratio < 7.0  # about linear growth: four times the time, about four times the variance
    quiet = wm.ring_attractor(delay=1000, trials=4, noise=0.0)
    assert np.allclose(quiet["angle"], 0.0, atol=1e-6)


def test_training_far_transfer_vanishes_against_an_active_control():
    rng = np.random.default_rng(8)
    passive = [wm.training_trial(200, control="passive", rng=rng) for _ in range(60)]
    active = [wm.training_trial(200, control="active", rng=rng) for _ in range(60)]
    assert np.mean([r["near"] for r in active]) > 0.3
    assert abs(np.mean([r["far"] for r in active])) < 0.06
    assert np.mean([r["far"] for r in passive]) > 0.1  # expectation looks like transfer


def test_battery_task_five():
    from explainer.psychology import battery

    t = battery.run("change", {}, 400, seed=1)
    assert len(t) == 400 and set(np.unique(t.extra["set_size"])) == {2, 4, 6, 8}
    m = t.extra["set_size"] == 8
    H = t.correct[m & t.extra["changed"]].mean()
    FA = 1 - t.correct[m & ~t.extra["changed"]].mean()
    assert 2.0 < wm.k_cowan(H, FA, 8) < 5.0


def test_open_data_bays_2009():
    from explainer.psychology import opendata

    if not opendata.available("bays_2009"):
        pytest.skip("Bays et al. (2009) is not cached and cannot be fetched here")
    d = opendata.bays_2009()
    assert len(d["error"]) == 7271 and set(np.unique(d["set_size"])) == {1, 2, 4, 6}
    assert np.allclose(wm.wrap(d["response"] - d["target"]), d["error"], atol=1e-9)
    one = d["set_size"] == 1
    assert np.all(np.isnan(d["nontarget"][one]))
