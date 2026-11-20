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

    def solve(self) -> dict:
        """Linearize and solve: ``A E[x_{t+1}] = B x_t`` with ``A = df/dx_{t+1}``, ``B = -df/dx_t``.  The generalized
        eigenvalues of (B, A) are sorted, stable first; Blanchard and Kahn: as many stable roots as predetermined
        variables (two: capital and technology).  Returns the policy ``c = F s`` and transition ``s' = P s`` for the
        state ``s = (k, z)``, all in log deviations."""
        xs = np.array([np.log(self.k_ss), 0.0, np.log(self.c_ss)])
        h = 1e-6
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            A[:, j] = (self._f(xs + e, xs) - self._f(xs - e, xs)) / (2 * h)
            B[:, j] = -(self._f(xs, xs + e) - self._f(xs, xs - e)) / (2 * h)
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
