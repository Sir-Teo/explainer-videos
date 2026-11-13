"""statkit.ot (Part 61): one-dimensional and discrete transport, Gaussians, Sinkhorn, maps, barycenters, ranks,
gradient flows and flow matching."""

import math

import numpy as np

from explainer.stats.kit import ot as O


def test_one_dimension_and_lp_duality():
    rng = np.random.default_rng(1)
    x, y = rng.standard_normal(300), rng.standard_normal(500) * 2 + 1
    # W1 as quantile distance equals the area between CDFs
    assert abs(O.wasserstein_1d(x, y, 1) - O.w1_cdf_area(x, y)) < 1e-10
    # equal sizes: W_p is the sorted pairing, and the LP agrees
    a, b = rng.standard_normal(40), rng.standard_normal(40) + 0.5
    w2 = math.sqrt(np.mean((np.sort(a) - np.sort(b)) ** 2))
    assert abs(O.wasserstein_1d(a, b, 2) - w2) < 1e-10
    assert abs(O.assignment(a[:, None], b[:, None], 2)["W"] - w2) < 1e-10
    # Kantorovich LP: primal = dual, feasible potentials, complementary slackness, sparse vertex
    X, Y = rng.standard_normal((6, 2)), rng.standard_normal((7, 2)) + 1
    p, q = rng.dirichlet(np.ones(6)), rng.dirichlet(np.ones(7))
    C = O.cost_matrix(X, Y, 2)
    lp = O.kantorovich_lp(p, q, C)
    assert np.allclose(lp["P"].sum(1), p, atol=1e-9) and np.allclose(lp["P"].sum(0), q, atol=1e-9)
    assert abs(p @ lp["f"] + q @ lp["g"] - lp["cost"]) < 1e-9
    slack = C - lp["f"][:, None] - lp["g"][None, :]
    assert slack.min() > -1e-9 and np.all(slack[lp["P"] > 1e-9] < 1e-8)
    assert np.sum(lp["P"] > 1e-9) <= 6 + 7 - 1


def test_gaussians_and_barycenters():
    # W2 between 1D normals is |m1 - m2|^2 + |s1 - s2|^2; commuting covariances axis by axis
    assert abs(O.gaussian_w2([0], [[1]], [3], [[4]]) - math.sqrt(9 + 1)) < 1e-12
    assert abs(O.gaussian_w2([0, 0], np.diag([1, 9]), [0, 0], np.diag([4, 1])) - math.sqrt(1 + 4)) < 1e-12
    S1 = np.array([[2.0, 0.5], [0.5, 1.0]])
    S2 = np.array([[1.0, -0.3], [-0.3, 3.0]])
    A = O.gaussian_map(S1, S2)
    assert np.allclose(A, A.T) and np.all(np.linalg.eigvalsh(A) > 0) and np.allclose(A @ S1 @ A, S2)
    # the Gaussian barycenter of diag(1, 4) and diag(4, 1) is 2.25 I; fixed point holds in general
    assert np.allclose(O.gaussian_barycenter([np.diag([1.0, 4.0]), np.diag([4.0, 1.0])]), 2.25 * np.eye(2))
    Sb = O.gaussian_barycenter([S1, S2])
    r = O.sqrtm_psd(Sb)
    assert np.allclose(Sb, 0.5 * O.sqrtm_psd(r @ S1 @ r) + 0.5 * O.sqrtm_psd(r @ S2 @ r), atol=1e-8)
    # the 1D barycenter averages quantiles: for a location-scale family, mean and sd average
    rng = np.random.default_rng(2)
    z = rng.standard_normal(20000)
    q = O.barycenter_1d([1 + 2 * z, 5 + 4 * z], [0.5, 0.5], 4000)
    u = (np.arange(4000) + 0.5) / 4000
    assert np.allclose(q, 3 + 3 * np.quantile(z, u))  # location 3, scale 3: the averages of (1, 5) and (2, 4)


def test_sinkhorn():
    rng = np.random.default_rng(3)
    X, Y = rng.standard_normal((40, 2)), rng.standard_normal((40, 2)) + [1.5, 0]
    a = np.full(40, 1 / 40)
    C = O.cost_matrix(X, Y, 2)
    exact = O.assignment(X, Y, 2)["cost"]
    costs = []
    for eps in (1.0, 0.3, 0.1):
        s = O.sinkhorn(a, a, C, eps, 50000, 1e-10)
        # the flag reports the stop honestly: eps = 0.1 is still at ~2e-6 after 50,000 sweeps
        assert s["converged"] == (s["errs"][-1] < 1e-10) == (eps > 0.2) and s["iters"] == len(s["errs"])
        assert not O.sinkhorn(a, a, C, eps, 2, 1e-10)["converged"]
        assert np.allclose(s["P"].sum(1), a, atol=1e-5) and np.allclose(s["P"].sum(0), a, atol=1e-12)
        # the dual objective equals the primal entropic objective <P, C> + eps sum P log(P / ab')
        ent = float(np.sum(s["P"] * np.log(s["P"] / (a[:, None] * a[None, :]) + 1e-300)))
        assert abs(s["obj"] - (s["cost"] + eps * ent)) < 1e-4
        costs.append(s["cost"])
    assert costs[0] > costs[1] > costs[2] > exact - 1e-9 and costs[2] - exact < 0.15
    # the Sinkhorn divergence is ~0 for a law against itself and positive for different laws
    assert abs(O.sinkhorn_divergence(X, X, 0.5)) < 1e-6 and O.sinkhorn_divergence(X, Y, 0.5) > 0.5


def test_rates_maps_and_ranks():
    rng = np.random.default_rng(4)
    r3 = O.empirical_rate(3, [30, 60, 120, 240], 4, rng)
    assert -0.5 < r3["slope"] < -0.2
    # the entropic map recovers a linear Gaussian map better than the identity does
    Sig = np.array([[3.0, 1.0], [1.0, 1.0]])
    A = O.gaussian_map(np.eye(2), Sig)
    X = rng.standard_normal((400, 2))
    Y = rng.standard_normal((400, 2)) @ np.linalg.cholesky(Sig).T
    T = O.entropic_map(X, Y, 0.1)
    Z = rng.standard_normal((300, 2))
    err = np.mean(np.sum((T(Z) - Z @ A.T) ** 2, 1))
    assert err < 0.2 * np.mean(np.sum((Z - Z @ A.T) ** 2, 1))
    # center-outward ranks: a bijection onto the grid; a symmetric cloud's deepest points are near its centre
    Xr = rng.standard_normal((180, 2))
    co = O.center_outward(Xr, O.spherical_grid(180, n_rad=4))
    G = co["grid"]
    assert sorted(map(tuple, np.round(co["F"], 9))) == sorted(map(tuple, np.round(G, 9)))
    inner = co["rank"] == co["rank"].min()
    assert np.linalg.norm(Xr[inner], axis=1).mean() < np.linalg.norm(Xr[~inner], axis=1).mean()


def test_tests_flows_and_flow_matching():
    rng = np.random.default_rng(5)
    # the rank energy test: valid under H0 (Cauchy), powerful under a shift
    rej = sum(O.rank_energy_test(rng.standard_cauchy((30, 2)), rng.standard_cauchy((30, 2)), rng, 99)["p"] < 0.1 for _ in range(60))
    assert rej <= 14
    assert O.rank_energy_test(rng.standard_cauchy((40, 2)), rng.standard_cauchy((40, 2)) + 3, rng, 99)["p"] < 0.05
    assert O.hotelling_two_sample(rng.standard_normal((50, 2)), rng.standard_normal((50, 2)) + 1)["p"] < 1e-4
    # Langevin particles track the exact Gaussian Fokker-Planck flow
    Sig = np.array([[1.0, 0.5], [0.5, 1.0]])
    Si = np.linalg.inv(Sig)
    m0, S0 = np.array([2.0, -1.0]), 0.3 * np.eye(2)
    snaps = O.langevin(lambda X: -X @ Si.T, rng.multivariate_normal(m0, S0, 4000), 0.01, 100, rng, 100)
    m, S = O.fokker_planck_gaussian(m0, S0, np.zeros(2), Sig, [1.0])[0]
    assert np.allclose(snaps[-1].mean(0), m, atol=0.06) and np.allclose(np.cov(snaps[-1].T), S, atol=0.08)
    kl = [O.gaussian_kl(mm, SS, np.zeros(2), Sig) for mm, SS in O.fokker_planck_gaussian(m0, S0, np.zeros(2), Sig, [0, 0.5, 1, 2])]
    assert all(a > b for a, b in zip(kl, kl[1:]))
    assert kl[-1] <= math.exp(-2 * 2 / np.linalg.eigvalsh(Sig).max()) * kl[0] + 1e-12
    # flow matching: OT pairing gives straight paths, so one Euler step already lands near the data
    Y = np.vstack([rng.normal([-2, 0], 0.3, (100, 2)), rng.normal([2, 0], 0.3, (100, 2))])
    X0 = rng.standard_normal((200, 2))
    v_ot = O.flow_matching_fit(X0, Y, rng, 0.3, 20, "ot")
    v_in = O.flow_matching_fit(X0, Y[rng.permutation(200)], rng, 0.3, 20, "independent")
    Z = rng.standard_normal((200, 2))
    w_ot = O.assignment(O.integrate_flow(v_ot, Z, 1)[-1], Y, 2)["W"]
    w_in = O.assignment(O.integrate_flow(v_in, Z, 1)[-1], Y, 2)["W"]
    assert w_ot < 0.6 * w_in
