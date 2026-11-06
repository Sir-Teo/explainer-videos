"""statkit.amp: classical statistics when p and n grow together (Part 59 of *Statistics, Built*).

    the logistic MLE's bias, variance and LRT in the proportional regime              (Sur & Candes 2019)
    the logistic MLE by Newton's method, and the LRT for one coefficient
    exact ridge and ridgeless risk for isotropic features                    (Dobriban & Wager 2018; Hastie et al. 2022)
    the lasso by AMP, its state evolution, and the Donoho-Tanner curve from it   (Donoho, Maleki & Montanari 2009;
                                                                                  Bayati & Montanari 2011)
    random-features ridge regression, simulated                                   (Mei & Montanari 2022)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special, stats

# ---------------------------------------------------------------------------------------------- Gaussian quadrature

_GH_X, _GH_W = np.polynomial.hermite_e.hermegauss(81)
_GH_W = _GH_W / _GH_W.sum()


def _sigmoid(t):
    return special.expit(t)


def prox_logistic(z, lam, iters: int = 60):
    """prox_{lam rho}(z) for rho(t) = log(1 + e^t): the root of t + lam sigmoid(t) = z, by safeguarded Newton."""
    z = np.asarray(z, float)
    t = z - lam * _sigmoid(z)
    for _ in range(iters):
        s = _sigmoid(t)
        g = t + lam * s - z
        h = 1 + lam * s * (1 - s)
        step = g / h
        t = t - step
        if np.max(np.abs(step)) < 1e-12:
            break
    return t


# ----------------------------------------------------------------------------------------------- Sur and Candes


def _sc_expectations(alpha, sigma, lam, kappa, gamma):
    z1, z2 = np.meshgrid(_GH_X, _GH_X, indexing="ij")
    w = np.outer(_GH_W, _GH_W)
    q1 = gamma * z1
    q2 = -alpha * gamma * z1 + math.sqrt(kappa) * sigma * z2
    p = prox_logistic(q2, lam)
    r1 = _sigmoid(q1)  # rho'(Q1)
    rp = _sigmoid(p)  # rho'(prox)
    rpp = rp * (1 - rp)
    e1 = np.sum(w * 2 * r1 * (lam * rp) ** 2) / kappa ** 2
    e2 = np.sum(w * r1 * q1 * lam * rp)
    e3 = np.sum(w * 2 * r1 / (1 + lam * rpp))
    return e1, e2, e3


def sur_candes(kappa: float, gamma: float, x0=None) -> dict:
    """The Sur-Candes system (5) of PNAS 116 (2019) in (alpha, sigma, lambda), for dimensionality kappa = p/n and signal
    strength gamma^2 = Var(x'beta):
        sigma^2 = kappa^-2 E[2 rho'(Q1) (lambda rho'(prox_{lambda rho}(Q2)))^2]
        0       = E[rho'(Q1) Q1 lambda rho'(prox_{lambda rho}(Q2))]
        1 - kappa = E[2 rho'(Q1) / (1 + lambda rho''(prox_{lambda rho}(Q2)))]
    with (Q1, Q2) centred normal, Var Q1 = gamma^2, Cov = -alpha gamma^2, Var Q2 = alpha^2 gamma^2 + kappa sigma^2.
    Then beta_hat_j ~ alpha beta_j + sigma Z / sqrt(p)-scale noise (in the paper's normalization), and the LRT for a null
    coefficient is (kappa sigma^2 / lambda) chi^2_1 in the limit."""
    if gamma == 0:
        def f0(v):
            s, l = math.exp(v[0]), math.exp(v[1])
            e1, _, e3 = _sc_expectations(0.0, s, l, kappa, 0.0)
            return [e1 - s * s, e3 - (1 - kappa)]
        starts = [(x0[1], x0[2])] if x0 is not None else [(1.5, 1.0), (2.0, 0.3), (1.2, 0.1), (2.5, 0.05), (3.0, 2.0), (5.0, 5.0)]
        best = None
        for s0, l0 in starts:
            sol = optimize.root(f0, [math.log(s0), math.log(l0)], method="hybr", tol=1e-12)
            res = float(np.max(np.abs(f0(sol.x))))
            if best is None or res < best[1]:
                best = (sol, res)
        sol, res = best
        s, l = math.exp(sol.x[0]), math.exp(sol.x[1])
        return {"alpha": 1.0, "sigma": s, "lam": l, "factor": kappa * s * s / l, "ok": res < 1e-7, "residual": res}

    def f(v):
        a, s, l = v[0], math.exp(v[1]), math.exp(v[2])
        e1, e2, e3 = _sc_expectations(a, s, l, kappa, gamma)
        return [e1 - s * s, e2, e3 - (1 - kappa)]

    starts = [x0] if x0 is not None else [(1.2, 3.0, 1.0), (1.5, 4.7, 1.5), (1.05, 1.5, 0.5), (2.0, 8.0, 3.0)]
    best = None
    for a, s, l in starts:
        sol = optimize.root(f, [a, math.log(s), math.log(l)], method="hybr", tol=1e-12)
        res = float(np.max(np.abs(f(sol.x))))
        if best is None or res < best[1]:
            best = (sol, res)
        if res < 1e-9:
            break
    sol, res = best
    a, s, l = float(sol.x[0]), math.exp(sol.x[1]), math.exp(sol.x[2])
    return {"alpha": a, "sigma": s, "lam": l, "factor": kappa * s * s / l, "ok": res < 1e-7, "residual": res}


def mle_exists_boundary(gamma: float, n_mc: int = 400_000, seed: int = 0) -> float:
    """Candes & Sur's phase transition: the MLE exists iff kappa < h(gamma) = min_t E (Z - t V)_+^2, Z ~ N(0, 1)
    independent of V with density 2 rho'(gamma v) phi(v) (Monte Carlo over V by rejection-free importance weights)."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(n_mc)
    wv = 2 * _sigmoid(gamma * v)  # importance weights: density of V relative to phi
    z = rng.standard_normal(n_mc)

    def g(t):
        return float(np.mean(wv * np.maximum(z - t * v, 0.0) ** 2))
    r = optimize.minimize_scalar(g, bounds=(-20, 20), method="bounded")
    return float(r.fun)


# --------------------------------------------------------------------------------------------- logistic MLE


def logistic_mle(X, y, iters: int = 50, tol: float = 1e-10):
    """The logistic MLE by Newton's method (no intercept); returns (beta, log-likelihood, converged)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1])
    ll_old = -np.inf
    for _ in range(iters):
        eta = X @ b
        p = _sigmoid(eta)
        W = p * (1 - p)
        g = X.T @ (y - p)
        H = (X * W[:, None]).T @ X
        step = np.linalg.solve(H + 1e-12 * np.eye(len(b)), g)
        # backtracking on the log-likelihood
        t = 1.0
        while True:
            bn = b + t * step
            etan = X @ bn
            ll = float(np.sum(y * etan - np.logaddexp(0, etan)))
            if ll >= ll_old - 1e-12 or t < 1e-6:
                break
            t /= 2
        b = bn
        if abs(ll - ll_old) < tol:
            return b, ll, True
        ll_old = ll
    return b, ll_old, False


def lrt_one(X, y, j: int = 0) -> dict:
    """Twice the log-likelihood ratio for H0: beta_j = 0, by fitting with and without column j."""
    b, ll1, ok1 = logistic_mle(X, y)
    keep = np.ones(X.shape[1], bool)
    keep[j] = False
    _, ll0, ok0 = logistic_mle(X[:, keep], y)
    return {"llr2": 2 * (ll1 - ll0), "beta": b, "ok": ok1 and ok0}


# ---------------------------------------------------------------------------------------------- ridge risk


def mp_stieltjes(z, gamma: float):
    """The Stieltjes transform m(z) = E 1/(lambda - z) of the Marchenko-Pastur law with ratio gamma = p/n and unit
    variance (z off the support; for z < 0 real, the positive root)."""
    z = np.asarray(z, complex)
    a = 1 - gamma - z
    disc = np.sqrt(a * a - 4 * gamma * z)
    m1 = (a + disc) / (2 * gamma * z)
    m2 = (a - disc) / (2 * gamma * z)
    # choose the root with Im m > 0 when Im z > 0, and m > 0 for z < 0
    pick = np.where((np.imag(z) > 0) & (np.imag(m1) > 0) | (np.imag(z) == 0) & (np.real(m1) > 0), m1, m2)
    return pick


def ridge_risk(lam, gamma: float, snr: float, sigma2: float = 1.0):
    """Limiting out-of-sample excess risk E(x'(beta_hat - beta))^2 of ridge regression with isotropic Gaussian features,
    ||beta||^2 = snr * sigma2, and penalty lam (Dobriban & Wager 2018):
        bias = r^2 lam^2 m'(-lam),  variance = sigma2 gamma (m(-lam) - lam m'(-lam)),
    with m the Marchenko-Pastur Stieltjes transform at ratio gamma."""
    lam = np.asarray(lam, float)
    r2 = snr * sigma2
    h = 1e-6 * np.maximum(lam, 1e-3)
    m = np.real(mp_stieltjes(-lam, gamma))
    mp = (np.real(mp_stieltjes(-lam + h, gamma)) - np.real(mp_stieltjes(-lam - h, gamma))) / (2 * h)  # dm/dz at z = -lam
    bias = r2 * lam ** 2 * mp
    var = sigma2 * gamma * (m - lam * mp)
    return {"bias": bias, "var": var, "risk": bias + var}


def ridgeless_risk(gamma, snr: float, sigma2: float = 1.0):
    """Minimum-norm least squares with isotropic features (Hastie, Montanari, Rosset & Tibshirani 2022): excess risk
    sigma2 gamma/(1 - gamma) for gamma < 1, and r^2 (1 - 1/gamma) + sigma2/(gamma - 1) for gamma > 1."""
    g = np.asarray(gamma, float)
    r2 = snr * sigma2
    return np.where(g < 1, sigma2 * g / (1 - g), r2 * (1 - 1 / g) + sigma2 / (g - 1))


def optimal_ridge_risk(gamma: float, snr: float, sigma2: float = 1.0):
    """Ridge at the optimal penalty lam* = gamma/snr (Dobriban & Wager): the risk is sigma2 gamma m(-lam*)."""
    lam = gamma / snr
    return float(sigma2 * gamma * np.real(mp_stieltjes(-lam, gamma)) * lam / lam)


def ridge_sim(n: int, gamma: float, snr: float, lams, reps: int, rng: np.random.Generator, sigma2: float = 1.0) -> np.ndarray:
    """Simulated excess risk of ridge (lam > 0) or min-norm (lam = 0) regression, averaged over reps."""
    p = max(1, int(round(gamma * n)))
    out = np.zeros(len(lams))
    for _ in range(reps):
        X = rng.standard_normal((n, p))
        beta = rng.standard_normal(p)
        beta *= math.sqrt(snr * sigma2) / np.linalg.norm(beta)
        y = X @ beta + math.sqrt(sigma2) * rng.standard_normal(n)
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
        uy = U.T @ y
        for k, lam in enumerate(lams):
            # penalty normalized as in the theory: minimize ||y - Xb||^2/n + lam ||b||^2
            if lam == 0:
                d = np.where(s > 1e-10 * s.max(), 1 / s, 0.0)
            else:
                d = s / (s * s + n * lam)
            b = Vt.T @ (d * uy)
            out[k] += float(np.sum((b - beta) ** 2))
    return out / reps


# -------------------------------------------------------------------------------------------- AMP for the lasso


def soft(x, t):
    return np.sign(x) * np.maximum(np.abs(x) - t, 0.0)


def amp_lasso(A, y, theta: float, iters: int = 30) -> dict:
    """Approximate message passing for the lasso with the threshold policy theta_t = theta * tau_t, tau_t^2 estimated
    by ||z_t||^2/n (Donoho, Maleki & Montanari 2009).  A is n x p with i.i.d. N(0, 1/n) entries:
        x_{t+1} = eta(x_t + A' z_t; theta tau_t),  z_t = y - A x_t + (1/delta) z_{t-1} <eta'(...)>."""
    A, y = np.asarray(A, float), np.asarray(y, float)
    n, p = A.shape
    delta = n / p
    x = np.zeros(p)
    z = y.copy()
    hist = []
    for _ in range(iters):
        tau = math.sqrt(np.mean(z * z))
        r = x + A.T @ z
        xn = soft(r, theta * tau)
        onsager = z * np.mean(np.abs(r) > theta * tau) / delta
        z = y - A @ xn + onsager
        x = xn
        hist.append({"tau": tau, "x": x.copy()})
    return {"x": x, "tau": [h["tau"] for h in hist], "path": [h["x"] for h in hist]}


def _bg_mse(tau: float, thr: float, eps: float, n_mc: int = 0, mu: float = 1.0) -> float:
    """E[(eta(X + tau Z; thr) - X)^2] for X ~ (1 - eps) delta_0 + eps delta_{+-mu} ... computed by quadrature over Z
    (two-point signal +-mu with probability eps/2 each, and zero otherwise)."""
    z, w = _GH_X, _GH_W
    zero = np.sum(w * soft(tau * z, thr) ** 2)
    one = np.sum(w * (soft(mu + tau * z, thr) - mu) ** 2)
    return float((1 - eps) * zero + eps * one)


def state_evolution(delta: float, eps: float, sigma2: float, theta: float, iters: int = 30, mu: float = 1.0) -> np.ndarray:
    """tau_{t+1}^2 = sigma2 + (1/delta) E[(eta(X + tau_t Z; theta tau_t) - X)^2], tau_0^2 = sigma2 + E X^2 / delta."""
    tau2 = sigma2 + eps * mu * mu / delta
    out = [tau2]
    for _ in range(iters):
        tau = math.sqrt(tau2)
        tau2 = sigma2 + _bg_mse(tau, theta * tau, eps, mu=mu) / delta
        out.append(tau2)
    return np.asarray(out)


def minimax_threshold_curve(deltas) -> np.ndarray:
    """The Donoho-Tanner curve as AMP's state evolution gives it (Donoho, Maleki & Montanari 2009):
        rho(delta) = max_z [1 - (2/delta)((1 + z^2) Phi(-z) - z phi(z))] / [1 + z^2 - 2((1 + z^2) Phi(-z) - z phi(z))]."""
    out = []
    for d in np.atleast_1d(deltas):
        def neg(z):
            m = (1 + z * z) * stats.norm.cdf(-z) - z * stats.norm.pdf(z)
            return -(1 - 2 * m / d) / (1 + z * z - 2 * m)
        r = optimize.minimize_scalar(neg, bounds=(0, 10), method="bounded")
        out.append(-r.fun)
    return np.asarray(out)


# ------------------------------------------------------------------------------------------- random features


def random_features_sim(n: int, d: int, Ns, lam: float, reps: int, rng: np.random.Generator, sigma2: float = 0.25) -> np.ndarray:
    """Random-features ridge regression with ReLU features of Gaussian inputs and a linear target y = <x, beta> +
    noise, ||beta|| = 1: test error against the number of features N (Mei & Montanari's double descent, simulated)."""
    out = np.zeros(len(Ns))
    nt = 2000
    for _ in range(reps):
        beta = rng.standard_normal(d)
        beta /= np.linalg.norm(beta)
        X = rng.standard_normal((n, d)) / math.sqrt(d)
        Xt = rng.standard_normal((nt, d)) / math.sqrt(d)
        y = X @ beta * math.sqrt(d) / math.sqrt(d) + math.sqrt(sigma2) * rng.standard_normal(n)
        yt = Xt @ beta
        for k, N in enumerate(Ns):
            W = rng.standard_normal((N, d))
            F = np.maximum(X @ W.T, 0)
            Ft = np.maximum(Xt @ W.T, 0)
            if lam == 0:
                a = np.linalg.pinv(F) @ y
            else:
                a = np.linalg.solve(F.T @ F + n * lam * np.eye(N), F.T @ y) if N <= n else F.T @ np.linalg.solve(F @ F.T + n * lam * np.eye(n), y)
            out[k] += float(np.mean((Ft @ a - yt) ** 2))
    return out / reps


# ------------------------------------------------------------------------------------- Bayes-optimal AMP (replica)


def bayes_denoiser(r, tau: float, eps: float, mu: float = 1.0):
    """Posterior mean of X ~ (1 - eps) delta_0 + (eps/2)(delta_mu + delta_-mu) given X + tau Z = r."""
    r = np.asarray(r, float)
    a = (1 - eps) * stats.norm.pdf(r / tau)
    b = 0.5 * eps * stats.norm.pdf((r - mu) / tau)
    c = 0.5 * eps * stats.norm.pdf((r + mu) / tau)
    return mu * (b - c) / (a + b + c)


def bayes_mmse(tau: float, eps: float, mu: float = 1.0) -> float:
    """The scalar MMSE E[(E[X | X + tau Z] - X)^2] for the three-point prior, by quadrature over Z."""
    z, w = _GH_X, _GH_W
    zero = np.sum(w * bayes_denoiser(tau * z, tau, eps, mu) ** 2)
    one = np.sum(w * (bayes_denoiser(mu + tau * z, tau, eps, mu) - mu) ** 2)
    return float((1 - eps) * zero + eps * one)


def bayes_state_evolution(delta: float, eps: float, sigma2: float, iters: int = 200, mu: float = 1.0, start=None) -> np.ndarray:
    """State evolution of Bayes-optimal AMP: tau^2 <- sigma2 + mmse(tau)/delta, from an uninformative start; its fixed
    point gives AMP's MSE, which equals the replica (Bayes-optimal) MMSE outside the hard phase (Barbier et al. 2019)."""
    tau2 = sigma2 + eps * mu * mu / delta if start is None else start
    out = [tau2]
    for _ in range(iters):
        tau2 = sigma2 + bayes_mmse(math.sqrt(tau2), eps, mu) / delta
        out.append(tau2)
    return np.asarray(out)


def lasso_se_mse(delta: float, eps: float, sigma2: float, thetas=None, mu: float = 1.0) -> dict:
    """The lasso's MSE by state evolution at the best threshold multiple theta (a grid)."""
    thetas = np.linspace(0.5, 3.0, 26) if thetas is None else thetas
    best = None
    for th in thetas:
        t2 = state_evolution(delta, eps, sigma2, th, 200, mu)[-1]
        mse = _bg_mse(math.sqrt(t2), th * math.sqrt(t2), eps, mu=mu)
        if best is None or mse < best[1]:
            best = (th, mse)
    return {"theta": float(best[0]), "mse": float(best[1])}


# ------------------------------------------------------------------------------------------- free convolution


def free_semicircle_plus_pm1(xs, s2: float, eta: float = 1e-3, iters: int = 4000) -> np.ndarray:
    """The density of the free additive convolution of a semicircle of variance s2 with the law (delta_-1 + delta_1)/2,
    from Pastur's equation m(z) = E_D[1/(D - z - s2 m(z))], solved by damped iteration at z = x + i eta."""
    out = []
    m = 1j
    for x in np.atleast_1d(xs):
        z = x + 1j * eta
        for _ in range(iters):
            mn = 0.5 * (1 / (1 - z - s2 * m) + 1 / (-1 - z - s2 * m))
            if abs(mn - m) < 1e-12:
                m = mn
                break
            m = 0.5 * m + 0.5 * mn
        out.append(max(0.0, m.imag / math.pi))
    return np.asarray(out)


def mp_density(x, gamma: float):
    """The Marchenko-Pastur density (unit variance, ratio gamma <= 1)."""
    x = np.asarray(x, float)
    a, b = (1 - math.sqrt(gamma)) ** 2, (1 + math.sqrt(gamma)) ** 2
    d = np.zeros_like(x)
    k = (x > a) & (x < b)
    d[k] = np.sqrt((b - x[k]) * (x[k] - a)) / (2 * math.pi * gamma * x[k])
    return d


# ------------------------------------------------------------------------------------------- robust regression


def lad_fit(X, y):
    """Least absolute deviations by linear programming."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    c = np.r_[np.zeros(p), np.ones(n), np.ones(n)]
    A = np.hstack([X, np.eye(n), -np.eye(n)])
    r = optimize.linprog(c, A_eq=A, b_eq=y, bounds=[(None, None)] * p + [(0, None)] * (2 * n), method="highs")
    return r.x[:p]
