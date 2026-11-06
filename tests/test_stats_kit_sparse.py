import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import sparse as SP


def _diab():
    X, y, names = museum.diabetes()
    Xs, ys, *_ = SP.standardize(X, y)
    return Xs, ys, names


def test_diabetes_shape_and_lars_matches_cd_at_knots():
    X, y, names = museum.diabetes()
    assert X.shape == (442, 10) and len(names) == 10 and abs(y.mean() - 152.13) < 0.01
    Xs, ys, _ = _diab()
    Xn = Xs / np.sqrt(len(ys))  # unit-norm columns
    L = SP.lars(Xn, ys, lasso=True)
    # the lasso path joins in the published order (Efron et al. 2004, Fig. 1): bmi, ltg, bp, hdl, sex, glu, tc, tch, ldl, age
    joins = [int(a[1:]) for a in L["actions"] if a.startswith("+")]
    assert joins[:4] == [2, 8, 3, 6]
    # LARS-lasso's knots solve the lasso: compare with coordinate descent at an interior knot
    k = 5
    lam = L["lams"][k] / len(ys)
    b = SP.lasso_cd(Xn, ys, lam)
    assert np.max(np.abs(b - L["coefs"][k])) < 1e-6
    # the end of the path is least squares
    ols = np.linalg.lstsq(Xn, ys, rcond=None)[0]
    assert np.max(np.abs(L["coefs"][-1] - ols)) < 1e-6


def test_lasso_kkt_and_ridge_svd():
    Xs, ys, _ = _diab()
    lam = 0.1 * SP.lam_max(Xs, ys)
    b = SP.lasso_cd(Xs, ys, lam)
    k = SP.kkt(Xs, ys, b, lam)
    assert k["on_err"] < 1e-7 and k["off_max"] <= lam + 1e-9
    r = SP.ridge_svd(Xs, ys, [0.0, 10.0])
    direct = np.linalg.solve(Xs.T @ Xs + 10.0 * np.eye(10), Xs.T @ ys)
    assert np.allclose(r["coefs"][1], direct) and abs(r["df"][0] - 10) < 1e-9


def test_thresholds_and_ncv_orthonormal():
    z = np.linspace(-5, 5, 101)
    assert np.allclose(SP.soft(z, 1), np.sign(z) * np.maximum(np.abs(z) - 1, 0))
    assert np.allclose(SP.mcp_threshold(z[np.abs(z) > 3], 1, 3), z[np.abs(z) > 3])
    assert np.allclose(SP.scad_threshold(z[np.abs(z) > 3.7], 1), z[np.abs(z) > 3.7])
    rng = np.random.default_rng(1)
    Q, _ = np.linalg.qr(rng.standard_normal((200, 5)))
    X = Q * np.sqrt(200)
    y = X @ np.array([3, -2, 0.5, 0, 0]) + rng.standard_normal(200)
    zz = X.T @ y / 200
    assert np.allclose(SP.ncv_cd(X, y, 0.8, "mcp"), SP.mcp_threshold(zz, 0.8, 3.0), atol=1e-8)
    assert np.allclose(SP.ncv_cd(X, y, 0.8, "scad"), SP.scad_threshold(zz, 0.8), atol=1e-8)
    assert np.allclose(SP.lasso_cd(X, y, 0.8), SP.soft(zz, 0.8), atol=1e-8)


def test_group_lasso_kkt():
    rng = np.random.default_rng(2)
    X = rng.standard_normal((150, 9))
    X -= X.mean(0)
    groups = np.repeat([0, 1, 2], 3)
    y = X[:, :3] @ np.array([1.0, -1, 0.5]) + rng.standard_normal(150)
    y -= y.mean()
    lam = 0.15
    b = SP.group_lasso(X, y, groups, lam)
    g = X.T @ (y - X @ b) / 150
    for k in range(3):
        idx = groups == k
        # KKT in the orthonormalized parametrization reduces, for a zero group, to a bound on the projected gradient
        if np.all(b[idx] == 0):
            q, r = np.linalg.qr(X[:, idx])
            assert np.linalg.norm(q.T @ (y - X @ b) * np.sqrt(150) / 150) <= lam * np.sqrt(3) + 1e-8
        else:
            assert np.linalg.norm(b[idx]) > 0
    assert np.all(b[:3] != 0)


def test_bayes_shrinkage_profiles():
    y = np.array([0.0, 0.5, 1.0, 3.0, 8.0])
    lm = SP.laplace_posterior_mean(y, 1.0)
    assert lm[0] == pytest.approx(0.0, abs=1e-12) and np.all(lm[1:] > 0) and np.all(lm[1:] < y[1:])
    # check the closed form against quadrature
    th = np.linspace(-20, 20, 400001)
    for yi, mi in zip(y, lm):
        w = np.exp(-(yi - th) ** 2 / 2 - np.abs(th))
        assert mi == pytest.approx(np.sum(th * w) / np.sum(w), abs=1e-5)
    hs = SP.horseshoe_posterior_mean(y, 0.1)
    assert hs[1] < 0.2 * y[1] and hs[4] > 0.9 * y[4]
    rng = np.random.default_rng(3)
    theta = np.r_[np.full(10, 6.0), np.zeros(190)]
    yy = theta + rng.standard_normal(200)
    g = SP.horseshoe_gibbs(yy, iters=3000, burn=500, rng=rng)
    assert np.mean(np.abs(g["mean"][10:])) < 0.25 and np.mean(g["mean"][:10]) > 5.0
    bl = SP.bayes_lasso_gibbs(yy, 1.0, iters=3000, burn=500, rng=rng)
    assert np.all(bl["mean"] != 0)


def test_basis_pursuit_and_phantom():
    rng = np.random.default_rng(4)
    A = rng.standard_normal((40, 100)) / np.sqrt(40)
    x = np.zeros(100)
    x[[3, 50, 77]] = [1.0, -2.0, 0.5]
    assert np.max(np.abs(SP.basis_pursuit(A, A @ x) - x)) < 1e-6
    assert 0.37 < SP.phase_curve([0.5])[0] < 0.40  # Donoho-Tanner rho(0.5) ~ 0.385 for sign-symmetric signals
    img = SP.shepp_logan(64)
    assert img.shape == (64, 64) and img.max() == pytest.approx(1.0) and img.min() >= -1e-12
    mask = SP.radial_mask(64, 22)
    F = np.fft.fft2(img, norm="ortho")
    y = np.where(mask, F, 0)
    me = SP.min_energy(y, mask)
    rec = SP.tv_recover(y, mask, iters=1500)["x"]
    err_me = np.linalg.norm(me - img) / np.linalg.norm(img)
    err_tv = np.linalg.norm(rec - img) / np.linalg.norm(img)
    assert mask.mean() < 0.45 and err_tv < 0.1 * err_me


def test_debiased_and_double_selection_run():
    rng = np.random.default_rng(5)
    n, p = 100, 150
    X = rng.standard_normal((n, p))
    beta = np.zeros(p)
    beta[:3] = [2.0, 1.0, 0.5]
    y = X @ beta + rng.standard_normal(n)
    Xc, yc = X - X.mean(0), y - y.mean()
    lam = np.sqrt(2 * np.log(p) / n)
    r = SP.debiased_lasso(Xc, yc, 0, lam)
    assert r["lo"] < r["b"] < r["hi"] and abs(r["b"] - 2.0) < 4 * r["se"]
    d = X[:, :5] @ np.full(5, 0.5) + rng.standard_normal(n)
    yy = 1.0 * d + X[:, :5] @ np.full(5, 0.5) + rng.standard_normal(n)
    ds = SP.double_selection(yy, d, X, lam, lam)
    assert ds["lo"] < ds["hi"] and ds["n_selected"] >= 3


def test_soft_impute_recovers_low_rank():
    rng = np.random.default_rng(6)
    U, V = rng.standard_normal((60, 3)), rng.standard_normal((40, 3))
    M = U @ V.T
    obs = rng.random(M.shape) < 0.5
    Z = SP.soft_impute(M, obs, lam=0.5, iters=500)["Z"]
    err = np.linalg.norm((Z - M)[~obs]) / np.linalg.norm(M[~obs])
    assert err < 0.15


def test_phantom_panel():
    from explainer.stats.viz import PhantomPanel

    p = PhantomPanel(SP.shepp_logan(32), size=2.0, caption="truth", lo=0, hi=1)
    assert len(p) == 3 and abs(p.image.height - 2.0) < 1e-9
    q = p.panel_for(np.zeros((32, 32)))
    assert np.allclose(q.get_center(), p.image.get_center())
