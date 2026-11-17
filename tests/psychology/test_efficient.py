"""Psyche's efficient codes (Part 58)."""

import numpy as np

from explainer.psychology.psyche import efficient as E


def _patches(n=4000):
    imgs = [E.dead_leaves(size=64, seed=s) for s in range(3)]
    return E.patches(imgs, n=n, seed=1)


def test_dead_leaves_fills_the_image():
    im = E.dead_leaves(size=48, seed=2)
    assert im.shape == (48, 48) and np.isfinite(im).all() and 0 <= im.min() and im.max() <= 1


def test_whitening_flattens_the_spectrum():
    X = _patches()
    Xw, W, ev = E.zca(X, eps=1e-3)
    w = np.linalg.eigvalsh(np.cov(Xw, rowvar=False))[::-1]
    assert ev[0] / ev[-2] > 20  # images: power falls steeply
    assert w[0] / w[-2] < 3  # whitened: nearly flat (the last direction is the removed mean)


def test_ista_solves_the_lasso():
    rng = np.random.default_rng(0)
    D = rng.standard_normal((16, 8))
    D /= np.linalg.norm(D, axis=0)
    a_true = np.zeros(8)
    a_true[[1, 5]] = [2.0, -1.5]
    x = D @ a_true
    a = E.sparse_code(x[None], D, lam=0.01, iters=2000)[0]
    assert np.allclose(a, a_true, atol=0.05)
    # optimality: the subgradient condition |D^T (x - D a)| <= lam
    g = D.T @ (x - D @ a)
    assert np.all(np.abs(g) <= 0.01 + 1e-3)


def test_sparse_code_is_localized_and_beats_pca():
    X = _patches(6000)
    Xw, _, _ = E.zca(X, eps=1.0)
    Xw = Xw / Xw.std()
    d = E.learn_dictionary(Xw, atoms=32, lam=0.4, epochs=80, seed=3, snapshots=(0, 80))
    assert set(d["snapshots"]) == {0, 80}
    assert d["err"][-1] < d["err"][0]
    loc = np.median(E.localization(d["D"])["localization"])
    pcs = np.linalg.eigh(np.cov(X, rowvar=False))[1][:, ::-1][:, :32]
    assert loc > np.median(E.localization(pcs)["localization"]) + 0.2


def test_laughlin_response_is_the_cdf():
    rng = np.random.default_rng(1)
    c = rng.normal(0, 0.3, 5000)
    r = E.laughlin(c)
    assert np.all(np.diff(r["response"]) >= 0)
    mid = np.argmin(abs(r["grid"]))
    assert abs(r["response"][mid] - 0.5) < 0.03


def test_efficient_bias_is_repulsive():
    b = E.efficient_bias(n_grid=180)
    th, bias = b["theta"], b["bias"]
    near = (th > 5) & (th < 30)
    assert np.all(bias[near] > 0)  # just clockwise of vertical: pushed further away
    assert abs(bias[0]) < 0.5


def test_rate_distortion_trades_rate_for_width():
    g = E.generalization(betas=(0.02, 0.5), n=31)
    assert g["rates"][0] < g["rates"][1]
    assert g["gradients"][0][3] > g["gradients"][1][3]  # the cheap code generalizes more broadly
    assert np.all(np.diff(g["gradients"][1]) <= 1e-12)


def test_normalization_saturates_and_masks():
    c = np.array([0.15, 1.0, 10.0])
    r = E.normalization(c)
    assert abs(r[0] - 0.5) < 1e-12 and r[2] < 1
    assert abs(E.normalization(0.15, mask=0.15) - 1 / 3) < 1e-12


def test_predictive_coding_reduces_error():
    rng = np.random.default_rng(2)
    D = rng.standard_normal((12, 3)) / 2
    prior = np.zeros(3)
    x = D @ np.array([1.0, -1.0, 0.5])
    r = E.predictive_coding(D, x, prior, steps=200, lr=0.1)
    assert r["e0"][-1] < r["e0"][0]
    # the fixed point is the MAP estimate (ridge with precision 1)
    assert np.allclose(r["r"], np.linalg.solve(D.T @ D + np.eye(3), D.T @ x), atol=1e-3)


def test_free_energy_bounds_surprise():
    f = E.free_energy_gaussian(x=2.0, prior_sd=1.0, noise_sd=0.5)
    assert abs(f["post_mu"] - 1.6) < 1e-12
    assert np.all(f["F"] >= f["surprise"] - 1e-12)
    assert abs(f["F"].min() - f["surprise"]) < 1e-3
    assert abs(f["surprise"] - (0.5 * np.log(2 * np.pi * 1.25) + 4 / 2.5)) < 1e-9


def test_tilt_aftereffect_is_repulsive_and_peaks_away_from_adapter():
    t = E.tilt_aftereffect()
    pos = t["tests"] > 0
    assert np.all(t["shift"][pos] > 0) and np.all(t["shift"][t["tests"] < 0] < 0)
    i = np.argmax(t["shift"])
    assert 10 <= t["tests"][i] <= 35


def test_one_and_done():
    s = E.samples_value()
    assert s["best_k"] == 1
    assert abs(s["accuracy"][2] - (0.65 ** 3 + 3 * 0.65 ** 2 * 0.35)) < 1e-9
