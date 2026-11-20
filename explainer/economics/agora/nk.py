"""Agora's sticky prices (Part 30): Mankiw's menu-cost arithmetic, Calvo pricing and the New Keynesian Phillips curve,
the three-equation model solved by undetermined coefficients and, with habits and indexation, by the QZ decomposition,
determinacy and the Taylor principle, optimal policy under discretion and commitment, the zero lower bound by
backward recursion with forward guidance, and a population of price setters (Calvo, Caplin-Spulber, and menu costs with
idiosyncratic shocks) showing the selection effect.  numpy and scipy only."""

from __future__ import annotations

import numpy as np
from scipy.linalg import ordqz


# --- menu costs (Mankiw 1985; Akerlof and Yellen 1985) ---------------------------------------------------------------
def menu_cost(eps: float = 6.0, gaps=(0.01, 0.02, 0.05, 0.1)) -> dict:
    """A monopolist facing demand ``p^(-eps)`` with marginal cost 1 sets ``p* = eps/(eps - 1)``.  If its price stays
    ``g`` too high (log points) after a fall in demand it should have met, its profit falls by roughly
    ``(eps - 1) g^2 / 2`` of profit (second order), while output, and the surplus it carries, falls by about
    ``eps g`` (first order).  Returns both, exactly, for each gap."""
    ps = eps / (eps - 1)

    def profit(p):
        return (p - 1) * p ** (-eps)

    out = []
    for g in gaps:
        p = ps * np.exp(g)
        loss = 1 - profit(p) / profit(ps)
        q = 1 - (p / ps) ** (-eps)
        out.append({"gap": g, "profit_loss": float(loss), "output_loss": float(q), "ratio": float(q / loss)})
    return {"eps": eps, "markup": ps, "rows": out}


# --- Calvo pricing and the New Keynesian Phillips curve --------------------------------------------------------------
def kappa(theta: float, beta: float = 0.99, sigma: float = 1.0, phi: float = 1.0, alpha: float = 0.0,
          eps: float = 6.0) -> float:
    """Gali's slope of the New Keynesian Phillips curve ``pi = beta E pi' + kappa x``: Calvo's probability of keeping
    the price ``theta``, decreasing returns ``alpha`` (with the strategic complementarity they imply)."""
    lam = (1 - theta) * (1 - beta * theta) / theta * (1 - alpha) / (1 - alpha + alpha * eps)
    return float(lam * (sigma + (phi + alpha) / (1 - alpha)))


def calvo_durations(theta: float, months_per_period: int = 3) -> dict:
    """Under Calvo a price survives a period with probability ``theta``: the mean duration is ``1/(1 - theta)`` periods,
    the median ``log(0.5)/log(theta)``; also the share of prices changing per month."""
    per_month = 1 - theta ** (1 / months_per_period)
    return {"mean_months": months_per_period / (1 - theta), "median_months": months_per_period * np.log(0.5) /
            np.log(theta), "monthly_frequency": float(per_month)}


def theta_from_monthly(freq: float, months_per_period: int = 3) -> float:
    """Calvo's quarterly theta implied by a monthly frequency of price changes."""
    return float((1 - freq) ** months_per_period)


# --- the three-equation model ---------------------------------------------------------------------------------------
# Gali's (2015, ch. 3) baseline: prices last three quarters on average, decreasing returns, a Taylor rule
DEFAULT = {"beta": 0.99, "sigma": 1.0, "kappa": None, "theta": 2 / 3, "phi": 1.0, "eps": 6.0, "alpha": 1 / 3,
           "phi_pi": 1.5, "phi_x": 0.125}


def _params(**kw) -> dict:
    p = {**DEFAULT, **kw}
    if p["kappa"] is None:
        p["kappa"] = kappa(p["theta"], p["beta"], p["sigma"], p["phi"], p["alpha"], p["eps"])
    return p


def determinacy(phi_pi: float, phi_x: float, beta: float = 0.99, sigma: float = 1.0, kap: float = 0.1275) -> dict:
    """With ``E z' = M z`` for ``z = (x, pi)`` under the rule ``i = phi_pi pi + phi_x x``, the equilibrium is unique when
    both roots of ``M`` lie outside the unit circle (both variables jump).  Also the analytical condition
    ``kappa (phi_pi - 1) + (1 - beta) phi_x > 0``."""
    M = np.array([[1 + phi_x / sigma + kap / (sigma * beta), (phi_pi - 1 / beta) / sigma],
                  [-kap / beta, 1 / beta]])
    lam = np.linalg.eigvals(M)
    n_out = int(np.sum(np.abs(lam) > 1))
    return {"roots": [complex(v) for v in lam], "moduli": sorted(float(abs(v)) for v in lam), "unique": n_out == 2,
            "condition": kap * (phi_pi - 1) + (1 - beta) * phi_x > 0}


def irf_ar1(shock: str, rho_s: float = 0.5, size: float = 1.0, periods: int = 16, **kw) -> dict:
    """Responses of the output gap (percent), inflation, the nominal rate and the real rate (annualized percentage
    points) to an AR(1) shock in the three-equation model, by undetermined coefficients (Gali, ch. 3).  ``shock`` is
    "monetary" (a shock ``v`` to the rule), "demand" (to the natural rate) or "cost" (a cost-push shock ``u``);
    ``size`` is in annualized percentage points (1.0 is Gali's 25 basis points a quarter)."""
    p = _params(**kw)
    b, s, k, fp, fx = p["beta"], p["sigma"], p["kappa"], p["phi_pi"], p["phi_x"]
    r = rho_s
    # x = E x' - (1/s)(fp pi + fx x + v - E pi' - rn);  pi = b E pi' + k x + u;  E y' = r y (y = Psi * shock)
    A = np.array([[1 - r + fx / s, (fp - r) / s], [-k, 1 - b * r]])
    unit = {"monetary": np.array([-1 / s, 0.0]), "demand": np.array([1 / s, 0.0]), "cost": np.array([0.0, 1.0])}[shock]
    psi = np.linalg.solve(A, unit)
    path = (size / 4) * r ** np.arange(periods)                       # quarterly units
    x = psi[0] * path
    pi = psi[1] * path
    v = path if shock == "monetary" else 0 * path
    i = fp * pi + fx * x + v
    real = i - r * pi                                                   # i - E pi'
    return {"q": list(range(periods)), "x": x.tolist(), "pi": (4 * pi).tolist(), "i": (4 * i).tolist(),
            "real": (4 * real).tolist(), "psi": psi.tolist(), "kappa": k}


# --- a general linear rational-expectations solver --------------------------------------------------------------
def klein(A, B, n_pre: int) -> dict:
    """Solve ``A E[z_{t+1}] = B z_t`` with the first ``n_pre`` variables predetermined (Klein 2000): returns
    ``y = F s`` for the jump variables and ``s' = P s``, plus the generalized eigenvalues and the Blanchard-Kahn
    verdict."""
    S, T, a, b, Q, Z = ordqz(B, A, sort="iuc", output="complex")
    with np.errstate(divide="ignore", invalid="ignore"):
        lam = a / b
    n_stable = int(np.sum(np.abs(lam) < 1))
    Z11, Z21 = Z[:n_pre, :n_pre], Z[n_pre:, :n_pre]
    F = np.real(Z21 @ np.linalg.inv(Z11))
    P = np.real(Z11 @ np.linalg.solve(T[:n_pre, :n_pre], S[:n_pre, :n_pre]) @ np.linalg.inv(Z11))
    return {"F": F, "P": P, "moduli": sorted(float(abs(v)) for v in lam if np.isfinite(v)), "n_stable": n_stable,
            "bk_ok": n_stable == n_pre}


def hybrid_irf(habit: float = 0.0, index: float = 0.0, smooth: float = 0.0, rho_v: float = 0.5, size: float = 0.25,
               periods: int = 20, **kw) -> dict:
    """The three-equation model with external habits ``h`` (output depends on its own past), price indexation
    ``gamma`` (inflation on its own past) and interest-rate smoothing; the response to a monetary shock of ``size``
    annualized points, solved by QZ.  With ``h = gamma = 0`` it is the basic model."""
    p = _params(**kw)
    b, s, k, fp, fx = p["beta"], p["sigma"], p["kappa"], p["phi_pi"], p["phi_x"]
    h, g, rs = habit, index, smooth
    # state s = (x_{t-1}, pi_{t-1}, i_{t-1}, v_t); jumps y = (x_t, pi_t, i_t).  z = (s, y), 7 variables.
    n = 7
    A = np.zeros((n, n))
    B = np.zeros((n, n))
    X1, P1, I1, V, X, PI, I = range(7)
    # predetermined laws: x_{t} -> X1', pi_t -> P1', i_t -> I1', v' = rho v
    A[0, X1], B[0, X] = 1, 1
    A[1, P1], B[1, PI] = 1, 1
    A[2, I1], B[2, I] = 1, 1
    A[3, V], B[3, V] = 1, rho_v
    # IS with habit: x = (1/(1+h)) E x' + (h/(1+h)) x_{-1} - ((1-h)/((1+h) s)) (i - E pi')
    c = (1 - h) / ((1 + h) * s)
    A[4, X], A[4, PI] = 1 / (1 + h), c
    B[4, X], B[4, X1], B[4, I] = 1, -h / (1 + h), c
    # hybrid NKPC: pi = (b/(1+b g)) E pi' + (g/(1+b g)) pi_{-1} + k x
    A[5, PI] = b / (1 + b * g)
    B[5, PI], B[5, P1], B[5, X] = 1, -g / (1 + b * g), -k
    # rule: i = rs i_{-1} + (1 - rs)(fp pi + fx x) + v
    B[6, I], B[6, I1], B[6, PI], B[6, X], B[6, V] = 1, -rs, -(1 - rs) * fp, -(1 - rs) * fx, -1
    sol = klein(A, B, 4)
    s_ = np.array([0, 0, 0, size / 4])
    xs, ps, is_ = [], [], []
    for _ in range(periods):
        y = sol["F"] @ s_
        xs.append(float(y[0]))
        ps.append(4 * float(y[1]))
        is_.append(4 * float(y[2]))
        s_ = sol["P"] @ s_
    return {"q": list(range(periods)), "x": xs, "pi": ps, "i": is_, "bk_ok": sol["bk_ok"],
            "peak_x": int(np.argmin(xs)), "peak_pi": int(np.argmin(ps))}


# --- optimal policy (Clarida, Gali and Gertler 1999) --------------------------------------------------------------
def optimal_policy(rho_u: float = 0.5, size: float = 1.0, periods: int = 12, **kw) -> dict:
    """A cost-push shock ``u`` of ``size`` annualized points with persistence ``rho_u``; the loss is
    ``pi^2 + (kappa/eps) x^2``.  Discretion: ``x = -(eps) pi`` with ``pi`` proportional to ``u``.  Commitment (timeless):
    ``x_t - x_{t-1} = -eps pi_t``, so the price level returns to where it started.  Returns paths and the two losses."""
    p = _params(**kw)
    b, k, eps = p["beta"], p["kappa"], p["eps"]
    w = k / eps                                     # weight on the output gap in the loss
    u = (size / 4) * rho_u ** np.arange(periods)
    # discretion: pi = w/(k^2 + w(1 - b rho)) u, x = -(k/w) pi
    pi_d = w / (k ** 2 + w * (1 - b * rho_u)) * u
    x_d = -(k / w) * pi_d
    # commitment: p_hat_t = delta p_hat_{t-1} + delta/(1 - delta b rho) u_t  with delta the stable root of
    # b d^2 - (1 + b + k^2/w) d + 1 = 0  (Gali, ch. 5); pi = p_hat - p_hat_{-1}; x = -(eps) p_hat ... in gap units
    a = 1 + b + k ** 2 / w
    delta = (a - np.sqrt(a ** 2 - 4 * b)) / (2 * b)
    ph = np.zeros(periods)
    prev = 0.0
    for t in range(periods):
        ph[t] = delta * prev + delta / (1 - delta * b * rho_u) * u[t]
        prev = ph[t]
    pi_c = np.diff(np.concatenate([[0.0], ph]))
    x_c = -(k / w) * ph
    disc = b ** np.arange(periods)

    def loss(pi, x):
        return float(np.sum(disc * (pi ** 2 + w * x ** 2)))

    return {"q": list(range(periods)), "pi_d": (4 * pi_d).tolist(), "x_d": x_d.tolist(),
            "pi_c": (4 * pi_c).tolist(), "x_c": x_c.tolist(), "price_d": np.cumsum(pi_d).tolist(),
            "price_c": ph.tolist(), "loss_d": loss(pi_d, x_d), "loss_c": loss(pi_c, x_c), "delta": float(delta),
            "weight": w}


# --- the zero lower bound ---------------------------------------------------------------------------------------
def zlb(T: int = 8, rn_low: float = -2.0, extra: int = 0, periods: int = 16, **kw) -> dict:
    """The natural rate (annualized, percent) falls to ``rn_low`` for ``T`` quarters and then returns to normal for
    good; the policy rate is held at zero through ``T + extra`` quarters, then follows the rule, under which the
    economy is back at its steady state.  Solved backwards (perfect foresight, as in Eggertsson and Woodford 2003).
    ``extra > 0`` is forward guidance: a promise to stay at zero after the shock has passed."""
    p = _params(**kw)
    b, s, k = p["beta"], p["sigma"], p["kappa"]
    rstar = 400 * (1 / b - 1)                      # the normal natural rate, annualized percent
    end = T + extra
    x = np.zeros(max(periods, end + 1))
    pi = np.zeros_like(x)
    i_gap = np.zeros_like(x)
    # deviations from the steady state: the policy rate's deviation is -rstar while at zero
    for t in range(end - 1, -1, -1):
        rn = (rn_low if t < T else rstar) / 4
        xn, pn = (x[t + 1], pi[t + 1])
        idev = -rstar / 4                          # i = 0 means a deviation of -r* (with zero target inflation)
        x[t] = xn - (1 / s) * (idev - pn - (rn - rstar / 4))
        pi[t] = b * pn + k * x[t]
        i_gap[t] = idev
    n = periods
    return {"q": list(range(n)), "x": x[:n].tolist(), "pi": (4 * pi[:n]).tolist(),
            "i": (4 * (i_gap[:n] + rstar / 4)).tolist(), "T": T, "extra": extra}


def forward_guidance_puzzle(horizons=(1, 4, 8, 12, 16, 20), cut: float = 0.25, **kw) -> dict:
    """The effect on today's output gap and inflation of a promise to lower the policy rate by ``cut`` annualized
    points for one quarter, ``h`` quarters ahead, all else at steady state: in the basic model it does not fade with
    the horizon (Del Negro, Giannoni and Patterson)."""
    p = _params(**kw)
    b, s, k = p["beta"], p["sigma"], p["kappa"]
    rows = []
    for h in horizons:
        x = np.zeros(h + 2)
        pi = np.zeros(h + 2)
        for t in range(h, -1, -1):
            idev = -cut / 4 if t == h else 0.0
            x[t] = x[t + 1] - (1 / s) * (idev - pi[t + 1])
            pi[t] = b * pi[t + 1] + k * x[t]
        rows.append({"h": h, "x0": float(x[0]), "pi0": float(4 * pi[0])})
    return {"rows": rows, "cut": cut}


# --- a population of price setters --------------------------------------------------------------------------------
def price_setters(kind: str = "calvo", n: int = 20000, months: int = 24, freq: float = 0.1, shock: float = 0.05,
                  sigma_a: float = 0.04, band: float | None = None, burn: int = 120, seed: int = 0) -> dict:
    """Firms' log prices chase targets ``m + a_i`` (money plus an idiosyncratic random walk with monthly s.d.
    ``sigma_a``).  "calvo": a random ``freq`` of firms reset each month; "menu": a firm resets when its gap exceeds
    ``band`` (set so that ``freq`` reset each month in the steady state).  After ``burn`` months money jumps by
    ``shock``; returns the aggregate price level's response (share of the shock passed through) and the share of
    firms resetting each month."""
    rng = np.random.default_rng(seed)
    a = np.zeros(n)
    p = rng.normal(0, sigma_a, n)
    m = 0.0
    if kind == "menu" and band is None:
        band = calibrate_band(freq, sigma_a, n=min(n, 20000), seed=seed)
    level, resets = [], []
    for t in range(burn + months):
        if t == burn:
            m += shock
        a += sigma_a * rng.standard_normal(n)
        target = m + a
        if kind == "calvo":
            reset = rng.random(n) < freq
        else:
            reset = np.abs(p - target) > band
        p = np.where(reset, target, p)
        level.append(float(p.mean() - a.mean()))      # the price level net of the idiosyncratic drift
        resets.append(float(reset.mean()))
    base = level[burn - 1]
    pass_through = [(v - base) / shock for v in level[burn:]]
    resets = resets[burn:]
    return {"kind": kind, "pass_through": pass_through, "resets": resets, "band": band, "freq": freq}


def calibrate_band(freq: float, sigma_a: float, n: int = 20000, months: int = 240, seed: int = 0) -> float:
    """The band at which a menu-cost (S,s) firm with random-walk targets resets a share ``freq`` of the time."""
    lo, hi = 0.2 * sigma_a, 20 * sigma_a
    for _ in range(30):
        mid = (lo + hi) / 2
        rng = np.random.default_rng(seed)
        gap = np.zeros(n)
        count = 0
        for t in range(months):
            gap += sigma_a * rng.standard_normal(n)
            r = np.abs(gap) > mid
            if t >= months // 2:
                count += r.sum()
            gap[r] = 0.0
        f = count / (n * (months - months // 2))
        if f > freq:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
