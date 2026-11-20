"""Agora's real business cycle (Part 29): the stochastic growth model with Brock and Mirman's closed form and on a
grid by value function iteration, and the real business cycle model with labour (Hansen's indivisible labour)
log-linearized and solved by the generalized Schur decomposition, with the Blanchard-Kahn count, impulse responses
and simulated moments.  numpy and scipy only."""

from __future__ import annotations

import numpy as np
from scipy.linalg import ordqz

from . import dp


# --- Brock and Mirman (1972) -----------------------------------------------------------------------------------------
def brock_mirman(alpha: float = 0.36, beta: float = 0.96, rho: float = 0.9, sigma: float = 0.02, T: int = 200,
                 seed: int = 0) -> dict:
    """Log utility, Cobb-Douglas output ``z k^alpha``, full depreciation: the policy is exactly
    ``k' = alpha beta z k^alpha`` and consumption ``(1 - alpha beta) z k^alpha``.  Simulates a path of log TFP and
    capital."""
    rng = np.random.default_rng(seed)
    lz = np.zeros(T)
    for t in range(1, T):
        lz[t] = rho * lz[t - 1] + sigma * rng.standard_normal()
    kss = (alpha * beta) ** (1 / (1 - alpha))
    k = np.empty(T + 1)
    k[0] = kss
    y = np.empty(T)
    for t in range(T):
        y[t] = np.exp(lz[t]) * k[t] ** alpha
        k[t + 1] = alpha * beta * y[t]
    return {"z": lz.tolist(), "k": k[:-1].tolist(), "y": y.tolist(), "c": ((1 - alpha * beta) * y).tolist(),
            "kss": float(kss), "saving_rate": alpha * beta}


def growth_vfi(alpha: float = 0.36, beta: float = 0.96, delta: float = 0.1, rho: float = 0.9, sigma: float = 0.02,
               nk: int = 151, nz: int = 5, iters: int = 1000, tol: float = 1e-8) -> dict:
    """The stochastic growth model with log utility and depreciation ``delta``, solved on a capital grid with a
    Rouwenhorst chain for log TFP.  Returns the grid, policy for next capital by state, and the number of iterations."""
    ch = dp.rouwenhorst(nz, rho, sigma)
    z, P = np.exp(np.array(ch["z"])), np.array(ch["P"])
    kss = (alpha / (1 / beta - 1 + delta)) ** (1 / (1 - alpha))
    k = np.linspace(0.5 * kss, 1.5 * kss, nk)
    V = np.zeros((nz, nk))
    res = z[:, None] * k[None, :] ** alpha + (1 - delta) * k[None, :]          # resources by (z, k)
    C = res[:, :, None] - k[None, None, :]                                     # (z, k, k')
    U = np.where(C > 0, np.log(np.maximum(C, 1e-300)), -1e10)
    for it in range(iters):
        EV = P @ V                                                             # (z, k')
        cand = U + beta * EV[:, None, :]
        Vn = cand.max(axis=2)
        gap = float(np.max(np.abs(Vn - V)))
        V = Vn
        if gap < tol:
            break
    pol = cand.argmax(axis=2)
    return {"k": k.tolist(), "z": z.tolist(), "kprime": k[pol].tolist(), "kss": float(kss), "iterations": it + 1,
            "V": V.tolist()}


# --- the real business cycle model -----------------------------------------------------------------------------------
class RBC:
    """Hansen's (1985) indivisible-labour economy: utility ``log c - A n``, output ``z k^alpha n^(1-alpha)``, capital
    depreciating at ``delta``, log TFP an AR(1).  Steady state hours ``n_ss`` pin down ``A``.  The model is
    log-linearized around the steady state and solved by the QZ (generalized Schur) decomposition."""

    def __init__(self, alpha=0.36, beta=0.99, delta=0.025, rho=0.95, sigma=0.007, n_ss=1 / 3, frisch=None):
        """``frisch`` is the Frisch elasticity of hours: utility ``log c - A n^(1 + 1/frisch) / (1 + 1/frisch)``;
        ``None`` means infinite, Hansen's indivisible labour (``log c - A n``)."""
        self.alpha, self.beta, self.delta, self.rho, self.sigma = alpha, beta, delta, rho, sigma
        self.inv_frisch = 0.0 if frisch is None else 1.0 / frisch
        r = 1 / beta - 1 + delta
        self.k_n = (alpha / r) ** (1 / (1 - alpha))                            # k / n in steady state
        self.n_ss = n_ss
        self.k_ss = self.k_n * n_ss
        self.y_ss = self.k_ss ** alpha * n_ss ** (1 - alpha)
        self.i_ss = delta * self.k_ss
        self.c_ss = self.y_ss - self.i_ss
        # A n^(1/frisch) c = (1 - alpha) y / n in the steady state
        self.A = (1 - alpha) * self.y_ss / (n_ss ** (1 + self.inv_frisch) * self.c_ss)

    # levels from logs: x = (log k, log z, log c)
    def _n(self, lk, lz, lc):
        a = self.alpha
        return ((1 - a) * np.exp(lz) * np.exp(lk) ** a / (self.A * np.exp(lc))) ** (1 / (a + self.inv_frisch))

    def _y(self, lk, lz, lc):
        return np.exp(lz) * np.exp(lk) ** self.alpha * self._n(lk, lz, lc) ** (1 - self.alpha)

    def _f(self, xn, x):
        """The equilibrium conditions f(x_{t+1}, x_t) = 0 (deterministic part)."""
        lk, lz, lc = x
        lkn, lzn, lcn = xn
        y = self._y(lk, lz, lc)
        yn = self._y(lkn, lzn, lcn)
        f1 = lkn - np.log((1 - self.delta) * np.exp(lk) + y - np.exp(lc))
        f2 = lzn - self.rho * lz
        f3 = -lc - (np.log(self.beta) - lcn + np.log(self.alpha * yn / np.exp(lkn) + 1 - self.delta))
        return np.array([f1, f2, f3])

    def linear_system(self):
        """The log-linearized system ``A E[x_{t+1}] = B x_t`` for ``x = (log k, log z, log c)`` in deviations, by
        central differences of the equilibrium conditions."""
        xs = np.array([np.log(self.k_ss), 0.0, np.log(self.c_ss)])
        h = 1e-6
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            A[:, j] = (self._f(xs + e, xs) - self._f(xs - e, xs)) / (2 * h)
            B[:, j] = -(self._f(xs, xs + e) - self._f(xs, xs - e)) / (2 * h)
        return A, B

    def phase(self, k0: float = -0.2, offsets=(-0.06, -0.03, 0.0, 0.03, 0.06), periods: int = 80,
              bound: float = 0.45) -> list:
        """Deterministic paths (technology at its mean) of log deviations of capital and consumption from capital
        ``k0`` and consumption on the saddle path plus each offset; unstable paths stop once they leave ``bound``."""
        A, B = self.linear_system()
        M = np.linalg.solve(A, B)
        out = []
        for d in offsets:
            x = np.array([k0, 0.0, self.F[0, 0] * k0 + d])
            ks, cs = [x[0]], [x[2]]
            for _ in range(periods):
                x = M @ x
                if max(abs(x[0]), abs(x[2])) > bound:
                    break
                ks.append(float(x[0]))
                cs.append(float(x[2]))
            out.append({"offset": d, "k": ks, "c": cs})
        return out

    def solve(self) -> dict:
        """Linearize and solve: ``A E[x_{t+1}] = B x_t`` with ``A = df/dx_{t+1}``, ``B = -df/dx_t``.  The generalized
        eigenvalues of (B, A) are sorted, stable first; Blanchard and Kahn: as many stable roots as predetermined
        variables (two: capital and technology).  Returns the policy ``c = F s`` and transition ``s' = P s`` for the
        state ``s = (k, z)``, all in log deviations."""
        A, B = self.linear_system()
        S, T, alpha_, beta_, Q, Z = ordqz(B, A, sort="iuc", output="complex")
        lam = alpha_ / beta_
        n_stable = int(np.sum(np.abs(lam) < 1))
        ns = 2
        Z11, Z21 = Z[:ns, :ns], Z[ns:, :ns]
        F = np.real(Z21 @ np.linalg.inv(Z11))
        Pm = np.real(Z11 @ np.linalg.solve(T[:ns, :ns], S[:ns, :ns]) @ np.linalg.inv(Z11))
        self.F, self.P = F, Pm
        return {"F": F.tolist(), "P": Pm.tolist(), "eigenvalues": [complex(v) for v in lam],
                "moduli": sorted(float(abs(v)) for v in lam), "n_stable": n_stable, "bk_ok": n_stable == ns}

    def _others(self, s, c):
        """Log deviations of hours, output and investment, given the state (k, z) and consumption c."""
        a = self.alpha
        k, z = s
        n = (z + a * k - c) / (a + self.inv_frisch)                             # from the labour condition
        y = z + a * k + (1 - a) * n
        i = (self.y_ss * y - self.c_ss * c) / self.i_ss
        return n, y, i

    def irf(self, periods: int = 40, shock: float = 0.01) -> dict:
        """Responses, in percent, to a technology shock of ``shock`` in log z."""
        s = np.array([0.0, shock])
        out = {k: [] for k in ("k", "z", "c", "n", "y", "i", "w")}
        for t in range(periods):
            c = float((self.F @ s)[0])
            n, y, i = self._others(s, c)
            for key, v in (("k", s[0]), ("z", s[1]), ("c", c), ("n", n), ("y", y), ("i", i), ("w", y - n)):
                out[key].append(100 * float(v))
            s = self.P @ s
        return out

    def simulate(self, T: int = 20000, seed: int = 0) -> dict:
        """A long simulation of log deviations: output, consumption, investment, hours, productivity (y - n)."""
        rng = np.random.default_rng(seed)
        s = np.zeros(2)
        rec = {k: np.empty(T) for k in ("y", "c", "i", "n", "w")}
        for t in range(T):
            c = float((self.F @ s)[0])
            n, y, i = self._others(s, c)
            rec["y"][t], rec["c"][t], rec["i"][t], rec["n"][t], rec["w"][t] = y, c, i, n, y - n
            s = self.P @ s
            s[1] += self.sigma * rng.standard_normal()
        return {k: v.tolist() for k, v in rec.items()}


def moments(series: dict, filter_: str = "hp", lam: float = 1600.0) -> dict:
    """Standard deviations (percent) of the filtered series, relative to output's, and their correlation with
    output.  ``series`` holds log levels (or log deviations), keyed with "y" for output."""
    cyc = {}
    for k, v in series.items():
        v = np.asarray(v, float)
        cyc[k] = np.asarray(dp.hp_filter(v, lam)["cycle"]) if filter_ == "hp" else v - v.mean()
    sy = cyc["y"].std()
    return {k: {"sd": float(100 * c.std()), "rel": float(c.std() / sy), "corr": float(np.corrcoef(c, cyc["y"])[0, 1])}
            for k, c in cyc.items()}


# --- what a technology shock does to hours, in the data (Gali 1999) ---------------------------------------------------
def var_ols(X, p: int = 4) -> dict:
    """A VAR(p) with a constant by least squares: ``x_t = c + A_1 x_{t-1} + ... + A_p x_{t-p} + u_t``."""
    X = np.asarray(X, float)
    T, k = X.shape
    Y = X[p:]
    Z = np.column_stack([np.ones(T - p)] + [X[p - j:T - j] for j in range(1, p + 1)])
    B, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    U = Y - Z @ B
    A = [B[1 + (j - 1) * k:1 + j * k].T for j in range(1, p + 1)]
    S = U.T @ U / (T - p - Z.shape[1])
    return {"c": B[0], "A": A, "Sigma": S, "U": U, "p": p}


def _ma(A, h: int) -> list:
    """Moving-average coefficients Psi_0 ... Psi_h of a VAR."""
    k = A[0].shape[0]
    psi = [np.eye(k)]
    for s in range(1, h + 1):
        psi.append(sum(A[j] @ psi[s - 1 - j] for j in range(min(s, len(A)))))
    return psi


def long_run_impact(A, S):
    """Blanchard and Quah (1989): the impact matrix B0 (with ``B0 B0' = S``) under which only the first shock moves the
    first variable's level in the long run.  With ``C(1) = (I - sum A_j)^-1``, the long-run responses ``C(1) B0`` are
    the lower-triangular Cholesky factor of ``C(1) S C(1)'``."""
    k = S.shape[0]
    C1 = np.linalg.inv(np.eye(k) - sum(A))
    L = np.linalg.cholesky(C1 @ S @ C1.T)
    return np.linalg.solve(C1, L)


def gali(prod_growth, hours, p: int = 4, h: int = 12, differenced: bool = True, reps: int = 300,
         seed: int = 0) -> dict:
    """Gali (1999): a VAR in productivity growth and hours (their growth if ``differenced``, else their level),
    identified by assuming only technology moves productivity in the long run.  Returns the responses, in percent, of
    the levels of productivity, hours and output (their sum) to a one-standard-deviation technology shock, with
    16th-84th percentile bands from a residual bootstrap."""
    X = np.column_stack([prod_growth, hours]).astype(float)

    def responses(Xs):
        fit = var_ols(Xs, p)
        B0 = long_run_impact(fit["A"], fit["Sigma"])
        r = np.array([P @ B0[:, 0] for P in _ma(fit["A"], h)])
        prod = np.cumsum(r[:, 0])
        hrs = np.cumsum(r[:, 1]) if differenced else r[:, 1]
        return fit, np.vstack([prod, hrs, prod + hrs]) * 100

    fit, base = responses(X)
    # the technology shock's share of the forecast-error variance of output's and hours' levels, by horizon
    B0 = long_run_impact(fit["A"], fit["Sigma"])
    R = np.array([P @ B0 for P in _ma(fit["A"], h)])                           # (h+1, variable, shock)
    lev = np.cumsum(R, axis=0) if differenced else np.concatenate(
        [np.cumsum(R[:, :1], axis=0), R[:, 1:]], axis=1)
    out_resp = lev[:, 0, :] + lev[:, 1, :]
    share_y = np.cumsum(out_resp ** 2, axis=0)
    share_n = np.cumsum(lev[:, 1, :] ** 2, axis=0)
    tech_y = (share_y[:, 0] / share_y.sum(axis=1)).tolist()
    tech_n = (share_n[:, 0] / share_n.sum(axis=1)).tolist()
    rng = np.random.default_rng(seed)
    T = len(X)
    draws = []
    for _ in range(reps):
        U = fit["U"][rng.integers(0, len(fit["U"]), len(fit["U"]))]
        Xb = np.empty_like(X)
        Xb[:p] = X[:p]
        for t in range(p, T):
            Xb[t] = fit["c"] + sum(fit["A"][j] @ Xb[t - 1 - j] for j in range(p)) + U[t - p]
        try:
            draws.append(responses(Xb)[1])
        except np.linalg.LinAlgError:
            continue
    D = np.array(draws)
    lo, hi = np.percentile(D, 16, axis=0), np.percentile(D, 84, axis=0)
    names = ("productivity", "hours", "output")
    return {"h": list(range(h + 1)), **{n: base[i].tolist() for i, n in enumerate(names)},
            **{f"{n}_lo": lo[i].tolist() for i, n in enumerate(names)},
            **{f"{n}_hi": hi[i].tolist() for i, n in enumerate(names)},
            "share_negative_impact": float(np.mean(D[:, 1, 0] < 0)), "reps": len(D),
            "tech_share_output": tech_y, "tech_share_hours": tech_n}
