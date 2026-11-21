"""Agora's macro-econometrics (Part 54's harness, turned on one economy's history; Part 55).

* **Vector autoregressions** (:func:`chol_irf`, :func:`bootstrap_irf`): reduced-form VARs by least squares (reusing
  ``rbc.var_ols``), recursive identification, and residual-bootstrap bands.
* **The Island's structural VAR** (:func:`island_svar`, :func:`svar_simulate`, :func:`svar_true_irf`): output growth,
  inflation and the policy rate driven by supply, demand and monetary shocks through a VAR(2), with an impact matrix
  that is not recursive, only supply moving output in the long run, a monetary shock whose variance is larger in
  meeting quarters, and an external proxy for it. The truth is known, so every scheme can be graded.
* **Five identification schemes** on one fitted VAR: timing (:func:`recursive`), long-run restrictions
  (:func:`long_run`, Blanchard and Quah 1989), sign restrictions (:func:`sign_set`, Uhlig 2005), an external
  instrument (:func:`proxy`, Stock and Watson 2012; Mertens and Ravn 2013), heteroskedasticity (:func:`hetero`,
  Rigobon 2003); :func:`schemes_mc` runs them on many histories.
* **Local projections against VARs** (:func:`lp_iv`, :func:`lp_var_mc`): Jorda (2005), with the bias and variance
  trade-off of Plagborg-Moller and Wolf (2021) and Li, Plagborg-Moller and Wolf (2024) seen in simulation.
* **A small New Keynesian DSGE model estimated** (:func:`nk_solve`, :func:`nk_simulate`, :func:`nk_loglik`,
  :func:`nk_mh`): the three-equation model with AR(1) shocks solved by undetermined coefficients, its state-space
  likelihood by the Kalman filter (statkit's ``ts.kalman``), Bayesian estimation by random-walk Metropolis-Hastings
  (An and Schorfheide 2007), and a likelihood profile that shows weak identification (Canova and Sala 2009).
* **Impulse-response matching** (:func:`irf_match`): Christiano, Eichenbaum and Evans's estimator.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from . import rbc
from explainer.stats.kit import ts

# ---------------------------------------------------------------------------------------------------------------
# reduced-form VARs


def var_fit(X, p: int = 4) -> dict:
    return rbc.var_ols(X, p)


def ma(A, h: int) -> list:
    return rbc._ma(A, h)


def irf_from_impact(fit: dict, b, h: int) -> np.ndarray:
    """Responses (h+1 x k) of every variable to a structural shock with impact vector ``b``."""
    return np.array([P @ np.asarray(b, float) for P in ma(fit["A"], h)])


def chol_irf(fit: dict, k: int, h: int, unit: int | None = None) -> np.ndarray:
    """Recursive identification: the k-th Cholesky shock, scaled so variable ``unit`` (default k) moves by one on
    impact."""
    L = np.linalg.cholesky(fit["Sigma"])
    unit = k if unit is None else unit
    return irf_from_impact(fit, L[:, k] / L[unit, k], h)


def bootstrap_irf(X, p: int, k: int, h: int, reps: int = 300, seed: int = 0, unit: int | None = None) -> dict:
    """A residual bootstrap of :func:`chol_irf`: 16th, 50th and 84th percentiles across resampled histories."""
    X = np.asarray(X, float)
    fit = var_fit(X, p)
    rng = np.random.default_rng(seed)
    T, kk = X.shape
    U = fit["U"]
    out = []
    for _ in range(reps):
        Xb = np.zeros_like(X)
        Xb[:p] = X[:p]
        draw = U[rng.integers(0, len(U), T - p)]
        for t in range(p, T):
            Xb[t] = fit["c"] + sum(fit["A"][j] @ Xb[t - 1 - j] for j in range(p)) + draw[t - p]
        out.append(chol_irf(var_fit(Xb, p), k, h, unit))
    out = np.array(out)
    return {"point": chol_irf(fit, k, h, unit), "lo": np.percentile(out, 16, 0), "mid": np.percentile(out, 50, 0),
            "hi": np.percentile(out, 84, 0)}


# ---------------------------------------------------------------------------------------------------------------
# the Island's structural VAR

SHOCKS = ("supply", "demand", "monetary")
VARS = ("output growth", "inflation", "the policy rate")


def island_svar() -> dict:
    """The truth: x_t = A1 x_{t-1} + A2 x_{t-2} + B e_t with x = (output growth, inflation, the rate) and
    e = (supply, demand, monetary), each of unit variance. The impact matrix B is not lower triangular: a monetary
    tightening lowers output and inflation within the quarter. Its demand and monetary columns are set so that only
    supply shocks move the level of output in the long run (the row of C(1) B for output growth is (s, 0, 0))."""
    A1 = np.array([[0.35, -0.15, -0.04],
                   [0.10, 0.55, -0.04],
                   [0.15, 0.35, 0.65]])
    A2 = np.array([[0.05, 0.0, 0.0],
                   [0.0, 0.15, 0.0],
                   [0.0, 0.05, 0.10]])
    C1 = np.linalg.inv(np.eye(3) - A1 - A2)
    c = C1[0]
    b_s = np.array([0.60, -0.40, -0.05])
    b_d = np.array([np.nan, 0.30, 0.25])
    b_d[0] = -(c[1] * b_d[1] + c[2] * b_d[2]) / c[0]
    b_m = np.array([-0.12, np.nan, 0.90])
    b_m[1] = -(c[0] * b_m[0] + c[2] * b_m[2]) / c[1]
    B = np.column_stack([b_s, b_d, b_m])
    return {"A": [A1, A2], "B": B, "C1": C1}


def svar_simulate(T: int = 240, seed: int = 0, burn: int = 100, meeting_sd: float = 2.0, meeting_share: float = 0.5,
                  proxy_noise: float = 0.8) -> dict:
    """A history of ``T`` quarters. In 'meeting' quarters (a random ``meeting_share`` of them) the monetary shock's
    standard deviation is multiplied by ``meeting_sd``; nothing else changes. A proxy for the monetary shock (a
    market surprise, say) is the shock plus independent noise of s.d. ``proxy_noise``."""
    M = island_svar()
    rng = np.random.default_rng(seed)
    n = T + burn
    meet = rng.random(n) < meeting_share
    e = rng.standard_normal((n, 3))
    e[:, 2] *= np.where(meet, meeting_sd, 1.0)
    x = np.zeros((n, 3))
    for t in range(2, n):
        x[t] = M["A"][0] @ x[t - 1] + M["A"][1] @ x[t - 2] + M["B"] @ e[t]
    z = e[:, 2] + proxy_noise * rng.standard_normal(n)
    s = slice(burn, n)
    return {"X": x[s], "e": e[s], "meet": meet[s], "z": z[s]}


def svar_true_irf(h: int = 20) -> dict:
    """True responses to each unit shock (the monetary one per point of the rate on impact): output growth, its
    level (cumulated), inflation and the rate."""
    M = island_svar()
    psi = ma(M["A"], h)
    out = {}
    for j, name in enumerate(SHOCKS):
        b = M["B"][:, j] / (M["B"][2, j] if name == "monetary" else 1.0)
        r = np.array([P @ b for P in psi])
        out[name] = {"dy": r[:, 0].tolist(), "y": np.cumsum(r[:, 0]).tolist(), "pi": r[:, 1].tolist(),
                     "i": r[:, 2].tolist()}
    return out


def _pack(r: np.ndarray, scale: float = 1.0) -> dict:
    r = np.asarray(r) * scale
    return {"dy": r[:, 0].tolist(), "y": np.cumsum(r[:, 0]).tolist(), "pi": r[:, 1].tolist(), "i": r[:, 2].tolist()}


def _rate_unit(r: np.ndarray) -> np.ndarray:
    """Scale responses to a one-point rise in the rate on impact."""
    return r / r[0, 2]


# ---------------------------------------------------------------------------------------------------------------
# five identification schemes


def recursive(fit: dict, h: int) -> np.ndarray:
    """Timing: the rate ordered last, so the monetary shock cannot move output or inflation within the quarter."""
    return _rate_unit(chol_irf(fit, 2, h))


def long_run(fit: dict, h: int) -> dict:
    """Blanchard and Quah: the shock that moves the level of output in the long run is supply; the other two are
    not separately identified (both leave output unchanged in the long run)."""
    B0 = rbc.long_run_impact(fit["A"], fit["Sigma"])
    b = B0[:, 0] * np.sign(B0[0, 0])
    return {"supply": irf_from_impact(fit, b, h)}


def sign_set(fit: dict, h: int, draws: int = 4000, seed: int = 0, horizon: int = 2) -> dict:
    """Uhlig's sign restrictions: every impact matrix B = chol(Sigma) Q for an orthonormal Q is consistent with the
    data. Keep the columns under which the rate rises and inflation and output growth fall for ``horizon`` quarters.
    Returns the accepted responses' pointwise 16-84% band, median, min and max, per point of the rate on
    impact."""
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(fit["Sigma"])
    psi = ma(fit["A"], h)
    keep = []
    for _ in range(draws):
        Q, R = np.linalg.qr(rng.standard_normal((3, 3)))
        Q = Q @ np.diag(np.sign(np.diag(R)))
        for j in range(3):
            b = L @ Q[:, j]
            for sgn in (1.0, -1.0):
                bb = sgn * b
                r = np.array([P @ bb for P in psi])
                if r[0, 2] > 0 and np.all(r[:horizon + 1, 1] <= 0) and np.all(r[:horizon + 1, 0] <= 0):
                    keep.append(_rate_unit(r))
    keep = np.array(keep)
    y = np.cumsum(keep[:, :, 0], axis=1)
    pack = {}
    for name, arr in (("y", y), ("pi", keep[:, :, 1]), ("i", keep[:, :, 2])):
        pack[name] = {"lo": np.percentile(arr, 16, 0).tolist(), "mid": np.percentile(arr, 50, 0).tolist(),
                      "hi": np.percentile(arr, 84, 0).tolist(), "min": arr.min(0).tolist(),
                      "max": arr.max(0).tolist()}
    return {**pack, "accepted": int(len(keep)), "tried": int(draws * 6)}


def proxy(fit: dict, z, h: int) -> np.ndarray:
    """An external instrument: the monetary column of B is proportional to Cov(u_t, z_t)."""
    z = np.asarray(z, float)[fit["p"]:]
    U = fit["U"]
    b = (U - U.mean(0)).T @ (z - z.mean()) / len(z)
    return _rate_unit(irf_from_impact(fit, b, h))


def hetero(fit: dict, regime, h: int) -> np.ndarray:
    """Rigobon: if only the monetary shock's variance differs between regimes, Sigma_1 - Sigma_0 = (s1^2 - s0^2) b b',
    a matrix of rank one whose leading eigenvector is the monetary column."""
    reg = np.asarray(regime, bool)[fit["p"]:]
    U = fit["U"]
    S1 = np.cov(U[reg], rowvar=False)
    S0 = np.cov(U[~reg], rowvar=False)
    w, V = np.linalg.eigh(S1 - S0)
    b = V[:, np.argmax(np.abs(w))] * np.sqrt(abs(w).max())
    b = b * np.sign(b[2])
    return _rate_unit(irf_from_impact(fit, b, h))


def schemes_one(T: int = 240, seed: int = 0, p: int = 4, h: int = 16) -> dict:
    """Every scheme on one history, with the truth."""
    H = svar_simulate(T, seed)
    fit = var_fit(H["X"], p)
    tr = svar_true_irf(h)
    return {"truth": tr, "recursive": _pack(recursive(fit, h)), "proxy": _pack(proxy(fit, H["z"], h)),
            "hetero": _pack(hetero(fit, H["meet"], h)), "sign": sign_set(fit, h, seed=seed),
            "long_run": _pack(long_run(fit, h)["supply"]), "T": T, "p": p,
            "proxy_corr": float(np.corrcoef(H["z"], H["e"][:, 2])[0, 1])}


def schemes_mc(reps: int = 200, T: int = 240, p: int = 4, h: int = 16, seed: int = 0) -> dict:
    """The recursive, proxy and heteroskedasticity schemes for the monetary shock, and the long-run scheme for the
    supply shock, on ``reps`` histories: the mean response and a 5-95% band across histories."""
    out = {m: {"y": [], "pi": []} for m in ("recursive", "proxy", "hetero", "long_run")}
    for r in range(reps):
        H = svar_simulate(T, seed + r)
        fit = var_fit(H["X"], p)
        res = {"recursive": recursive(fit, h), "proxy": proxy(fit, H["z"], h), "hetero": hetero(fit, H["meet"], h),
               "long_run": long_run(fit, h)["supply"]}
        for m, rr in res.items():
            out[m]["y"].append(np.cumsum(rr[:, 0]))
            out[m]["pi"].append(rr[:, 1])
    summ = {}
    for m, d in out.items():
        summ[m] = {}
        for k, a in d.items():
            a = np.array(a)
            summ[m][k] = {"mean": a.mean(0).tolist(), "lo": np.percentile(a, 5, 0).tolist(),
                          "hi": np.percentile(a, 95, 0).tolist()}
    return {"methods": summ, "truth": svar_true_irf(h), "reps": reps, "T": T, "h": h}


# ---------------------------------------------------------------------------------------------------------------
# local projections against VARs


def lp_iv(X, z, k: int, h: int, lags: int = 4, unit: int = 2) -> np.ndarray:
    """Local projections of variable ``k`` on the instrument ``z`` with ``lags`` lags of every variable as
    controls, divided by the impact response of variable ``unit`` (the first stage)."""
    X = np.asarray(X, float)
    z = np.asarray(z, float)
    T = len(z)

    def proj(y, hh):
        rows = np.arange(lags, T - hh)
        Z = np.column_stack([np.ones(len(rows)), z[rows]] + [X[rows - j] for j in range(1, lags + 1)])
        b, *_ = np.linalg.lstsq(Z, y[rows + hh], rcond=None)
        return b[1]

    first = proj(X[:, unit], 0)
    return np.array([proj(X[:, k], hh) for hh in range(h + 1)]) / first


def lp_var_mc(reps: int = 300, T: int = 200, h: int = 16, seed: int = 1) -> dict:
    """The monetary shock's effect on the level of output, by a VAR(1) (too few lags for the VAR(2) truth), a VAR(4)
    and local projections with four lags, each using the proxy (inside the VAR as an external instrument, or as the
    projection's regressor): mean and 5-95% band across histories."""
    tr = np.array(svar_true_irf(h)["monetary"]["y"])
    out = {"var1": [], "var4": [], "lp": []}
    for r in range(reps):
        H = svar_simulate(T, seed + r)
        for name, p in (("var1", 1), ("var4", 4)):
            fit = var_fit(H["X"], p)
            out[name].append(np.cumsum(proxy(fit, H["z"], h)[:, 0]))
        dy = lp_iv(H["X"], H["z"], 0, h)
        out["lp"].append(np.cumsum(dy))
    summ = {}
    for m, a in out.items():
        a = np.array(a)
        summ[m] = {"mean": a.mean(0).tolist(), "lo": np.percentile(a, 5, 0).tolist(),
                   "hi": np.percentile(a, 95, 0).tolist(), "bias": (a.mean(0) - tr).tolist(),
                   "sd": a.std(0).tolist(), "rmse": np.sqrt(((a - tr) ** 2).mean(0)).tolist()}
    return {"methods": summ, "truth": tr.tolist(), "reps": reps, "T": T, "h": h}


# ---------------------------------------------------------------------------------------------------------------
# a small New Keynesian model, solved and estimated

NK_DEFAULT = {"kappa": 0.1, "sigma": 1.5, "phi_pi": 1.5, "phi_x": 0.25, "beta": 0.99,
              "rho_d": 0.8, "rho_u": 0.6, "rho_v": 0.4, "sd_d": 0.5, "sd_u": 0.2, "sd_v": 0.25}
NK_NAMES = ("output gap", "inflation", "the rate")


def nk_solve(par: dict) -> np.ndarray:
    """The three-equation model with AR(1) demand (d), cost (u) and monetary (v) shocks:

        x_t = E x_{t+1} - (1/sigma)(i_t - E pi_{t+1}) + d_t
        pi_t = beta E pi_{t+1} + kappa x_t + u_t
        i_t = phi_pi pi_t + phi_x x_t + v_t

    Guess x = a s and pi = b s for each shock s with persistence rho; returns Gamma (3 x 3), whose column j gives the
    output gap, inflation and the rate per unit of shock j."""
    k, sg, fp, fx, be = (par[n] for n in ("kappa", "sigma", "phi_pi", "phi_x", "beta"))
    G = np.zeros((3, 3))
    for j, (rho, unit) in enumerate(((par["rho_d"], (1.0, 0.0, 0.0)), (par["rho_u"], (0.0, 1.0, 0.0)),
                                     (par["rho_v"], (0.0, 0.0, 1.0)))):
        d_, u_, v_ = unit
        # a = rho a - (1/sg)(fp b + fx a + v_ - rho b) + d_ ;  b = be rho b + k a + u_
        M = np.array([[1 - rho + fx / sg, (fp - rho) / sg],
                      [-k, 1 - be * rho]])
        rhs = np.array([d_ - v_ / sg, u_])
        a, b = np.linalg.solve(M, rhs)
        G[:, j] = [a, b, fp * b + fx * a + v_]
    return G


def nk_simulate(par: dict | None = None, T: int = 200, seed: int = 0, me: float = 0.05, burn: int = 100) -> dict:
    par = {**NK_DEFAULT, **(par or {})}
    rng = np.random.default_rng(seed)
    G = nk_solve(par)
    rho = np.array([par["rho_d"], par["rho_u"], par["rho_v"]])
    sd = np.array([par["sd_d"], par["sd_u"], par["sd_v"]])
    s = np.zeros(3)
    S, Y = [], []
    for t in range(T + burn):
        s = rho * s + sd * rng.standard_normal(3)
        if t >= burn:
            S.append(s.copy())
            Y.append(G @ s + me * rng.standard_normal(3))
    return {"Y": np.array(Y), "S": np.array(S), "par": par, "me": me}


def nk_loglik(par: dict, Y, me: float = 0.05, obs=(0, 1, 2)) -> float:
    """The Gaussian likelihood of the observed series (``obs`` picks among the output gap, inflation and the rate),
    by the Kalman filter on the state s_t = diag(rho) s_{t-1} + w_t, y_t = Gamma s_t + measurement error."""
    try:
        G = nk_solve(par)
    except np.linalg.LinAlgError:
        return -np.inf
    rho = np.array([par["rho_d"], par["rho_u"], par["rho_v"]])
    sd = np.array([par["sd_d"], par["sd_u"], par["sd_v"]])
    if np.any(np.abs(rho) >= 1) or np.any(sd <= 0):
        return -np.inf
    F = np.diag(rho)
    Q = np.diag(sd ** 2)
    P0 = np.diag(sd ** 2 / (1 - rho ** 2))
    obs = list(obs)
    Yo = np.asarray(Y, float)[:, obs]
    out = ts.kalman(Yo, F, G[obs], Q, me ** 2 * np.eye(len(obs)), np.zeros(3), P0)
    return float(out["loglik"])


NK_EST = ("kappa", "sigma", "phi_pi", "phi_x", "rho_v")
NK_PRIOR = {"kappa": ("gamma", 0.15, 0.10), "sigma": ("gamma", 1.5, 0.5), "phi_pi": ("gamma", 1.5, 0.3),
            "phi_x": ("gamma", 0.25, 0.15), "rho_v": ("beta", 0.5, 0.2)}


def _logprior(name: str, x: float) -> float:
    from scipy import stats

    kind, m, s = NK_PRIOR[name]
    if kind == "gamma":
        if x <= 0:
            return -np.inf
        a = (m / s) ** 2
        return float(stats.gamma.logpdf(x, a, scale=m / a))
    if not 0 < x < 1:
        return -np.inf
    v = s * s
    c = m * (1 - m) / v - 1
    return float(stats.beta.logpdf(x, m * c, (1 - m) * c))


def prior_draws(name: str, n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    kind, m, s = NK_PRIOR[name]
    if kind == "gamma":
        a = (m / s) ** 2
        return rng.gamma(a, m / a, n)
    v = s * s
    c = m * (1 - m) / v - 1
    return rng.beta(m * c, (1 - m) * c, n)


def nk_mh(Y, draws: int = 6000, burn: int = 1500, seed: int = 0, me: float = 0.05, scale: float = 0.8,
          obs=(0, 1, 2)) -> dict:
    """Bayesian estimation of kappa, sigma, phi_pi, phi_x and rho_v (the rest fixed at the truth) by random-walk
    Metropolis-Hastings in logs (logit for rho_v), with a proposal scaled from the inverse Hessian at the mode."""
    names = NK_EST

    def to_par(u):
        p = dict(NK_DEFAULT)
        for n, x in zip(names, u):
            p[n] = 1 / (1 + np.exp(-x)) if n == "rho_v" else float(np.exp(x))
        return p

    def jac(u):  # log |d par / d u|
        out = 0.0
        for n, x in zip(names, u):
            if n == "rho_v":
                q = 1 / (1 + np.exp(-x))
                out += np.log(q * (1 - q))
            else:
                out += x
        return out

    def post(u):
        p = to_par(u)
        lp = sum(_logprior(n, p[n]) for n in names)
        if not np.isfinite(lp):
            return -np.inf
        return nk_loglik(p, Y, me, obs) + lp + jac(u)

    u0 = np.array([np.log(0.15), np.log(1.5), np.log(1.5), np.log(0.25), 0.0])
    res = minimize(lambda u: -post(u), u0, method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-6,
                                                                          "fatol": 1e-8})
    mode = res.x
    k = len(mode)
    Hs = np.zeros((k, k))
    eps = 1e-3
    f0 = post(mode)
    for a in range(k):
        for b in range(a, k):
            ea, eb = np.eye(k)[a] * eps, np.eye(k)[b] * eps
            v = (post(mode + ea + eb) - post(mode + ea - eb) - post(mode - ea + eb) + post(mode - ea - eb)) / (
                4 * eps * eps)
            Hs[a, b] = Hs[b, a] = v
    try:
        cov = np.linalg.inv(-Hs)
        np.linalg.cholesky(cov)
    except np.linalg.LinAlgError:
        cov = np.eye(k) * 0.01
    Lc = np.linalg.cholesky(cov) * scale
    rng = np.random.default_rng(seed)
    u, fu = mode.copy(), f0
    chain, acc = [], 0
    for it in range(draws + burn):
        prop = u + Lc @ rng.standard_normal(k)
        fp = post(prop)
        if np.log(rng.random()) < fp - fu:
            u, fu = prop, fp
            if it >= burn:
                acc += 1
        if it >= burn:
            p = to_par(u)
            chain.append([p[n] for n in names])
    chain = np.array(chain)
    return {"names": list(names), "chain": chain, "mode": [to_par(mode)[n] for n in names],
            "accept": acc / draws, "truth": [NK_DEFAULT[n] for n in names]}


def nk_profile(Y, name: str, grid, me: float = 0.05, obs=(0, 1, 2)) -> list:
    """The log likelihood with one parameter fixed at each grid value and the other estimated ones re-optimized."""
    others = [n for n in NK_EST if n != name]
    out = []
    u = np.array([np.log(NK_DEFAULT[n]) if n != "rho_v" else 0.4 for n in others])
    for g in grid:
        def f(v):
            p = dict(NK_DEFAULT)
            p[name] = g
            for n, x in zip(others, v):
                p[n] = 1 / (1 + np.exp(-x)) if n == "rho_v" else float(np.exp(x))
            return -nk_loglik(p, Y, me, obs)

        r = minimize(f, u, method="Nelder-Mead", options={"maxiter": 2000, "xatol": 1e-5, "fatol": 1e-6})
        u = r.x
        out.append(-float(r.fun))
    return out


# ---------------------------------------------------------------------------------------------------------------
# matching impulse responses


def nk_irf(par: dict, h: int = 12) -> np.ndarray:
    """Responses of the output gap, inflation and the rate to a monetary shock of one unit."""
    G = nk_solve(par)
    return np.array([G[:, 2] * par["rho_v"] ** t for t in range(h + 1)])


def irf_match(target, se, h: int = 12, free=("kappa", "sigma"), start=(0.3, 1.0)) -> dict:
    """Christiano, Eichenbaum and Evans: choose the free parameters (others at the truth) so the model's responses to
    a monetary shock come closest to the estimated ones, each weighted by its inverse sampling variance."""
    target, se = np.asarray(target, float), np.asarray(se, float)
    w = 1 / np.maximum(se, 1e-6) ** 2

    def obj(v):
        p = dict(NK_DEFAULT)
        for n, x in zip(free, v):
            p[n] = float(np.exp(x))
        r = nk_irf(p, h)
        # the shock's size is unknown: scale the model so the rate's impact matches
        r = r * target[0, 2] / r[0, 2]
        return float((w * (r - target) ** 2).sum())

    res = minimize(obj, np.log(start), method="Nelder-Mead", options={"xatol": 1e-7, "fatol": 1e-9})
    est = {n: float(np.exp(x)) for n, x in zip(free, res.x)}
    p = {**NK_DEFAULT, **est}
    r = nk_irf(p, h)
    p0 = {**NK_DEFAULT, **{n: s for n, s in zip(free, start)}}
    r0 = nk_irf(p0, h)
    return {"estimate": est, "fitted": (r * target[0, 2] / r[0, 2]).tolist(),
            "start_irf": (r0 * target[0, 2] / r0[0, 2]).tolist(), "objective": float(res.fun)}


__all__ = ["var_fit", "ma", "irf_from_impact", "chol_irf", "bootstrap_irf", "island_svar", "svar_simulate",
           "svar_true_irf", "recursive", "long_run", "sign_set", "proxy", "hetero", "schemes_one", "schemes_mc",
           "lp_iv", "lp_var_mc", "nk_solve", "nk_simulate", "nk_loglik", "nk_mh", "nk_profile", "prior_draws",
           "nk_irf", "irf_match", "NK_DEFAULT", "NK_EST", "NK_PRIOR", "SHOCKS"]
