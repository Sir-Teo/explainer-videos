"""Agora's tax (Part 41): who pays, what it costs, and how high the rates should be.

* **Laffer** (:func:`laffer`, :func:`mcpf`): revenue t (1 - t)^e from a base with constant elasticity e; its top at
  1 / (1 + e); the marginal cost of public funds along it.
* **Incidence** (:func:`harberger`): a tax on capital in a one-good economy with Cobb-Douglas production, in which
  capital's supply responds to its net return with elasticity ``eta``; eta = 0 is a closed economy with a fixed
  stock (capital bears it all), a large eta a small open economy (workers bear it, and more).
* **Deadweight loss** (:func:`triangle`): a unit tax in a market with constant-elasticity demand and supply; the
  revenue, the exact loss and Harberger's approximation 1/2 t^2 (elasticity) p q.
* **Ramsey** (:func:`ramsey`): taxes on independent goods that raise a given revenue at the least loss: t/(1 + t)
  proportional to one over the demand elasticity, against a uniform rate raising the same.
* **Mirrlees** (:func:`diamond_schedule`): the optimal marginal rates of a nonlinear income tax with quasi-linear
  preferences (Diamond 1998): T'/(1 - T') = (1 + 1/e) (1 - F)/(w f) (1 - mean of g above w), for skills that are
  lognormal with a Pareto tail and welfare weights that fall with skill.
* **The top rate** (:func:`top_rate`, :func:`top_revenue`): (1 - g) / (1 - g + a e), and the top bracket's revenue
  against its rate.
* **Bunching** (:func:`bunching`): taxpayers facing a kink, with optimization frictions; Saez's estimator with a
  polynomial counterfactual.
* **Evasion** (:func:`allingham_sandmo`): the declared share of income when audits find evaders with probability p
  and fine them theta times the evaded tax.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

# ---------------------------------------------------------------------------------------------------------------
# Laffer


def laffer(t, e: float):
    """Revenue per unit of untaxed base when the base shrinks like (1 - t)^e."""
    t = np.asarray(t, float)
    return t * (1.0 - t) ** e


def laffer_peak(e: float) -> float:
    return 1.0 / (1.0 + e)


def mcpf(t, e: float):
    """The marginal cost of public funds on the Laffer curve's base: raising t by dt costs taxpayers the base times
    dt (the envelope theorem) and raises the base times (1 - t e/(1 - t)) dt, so each extra dollar of revenue costs
    (1 - t)/(1 - t - t e); infinite at the curve's top, 1/(1 + e), and beyond it."""
    t = np.asarray(t, float)
    den = 1.0 - t - t * e
    return np.where(den > 0, (1.0 - t) / np.where(den > 0, den, 1.0), np.inf)


# ---------------------------------------------------------------------------------------------------------------
# incidence


def harberger(tau: float, eta: float, alpha: float = 0.3, A: float = 1.0, K0: float = 1.0, L: float = 1.0) -> dict:
    """A tax ``tau`` on the return to capital.  Output A K^alpha L^(1 - alpha); firms pay capital its marginal
    product; capital's supply is K0 (r_net / r0)^eta, where r0 is the untaxed return.  Returns the capital stock,
    the gross and net returns, the wage, the revenue, and the losses of workers and of capital's owners (in output)
    with the share of the total burden borne by workers."""
    def mpk(K):
        return alpha * A * (K / L) ** (alpha - 1)

    def mpl(K):
        return (1 - alpha) * A * (K / L) ** alpha
    r0, w0 = mpk(K0), mpl(K0)
    # log K - log K0 = eta [log(1 - tau) + (alpha - 1)(log K - log K0)], solved in closed form; eta = inf is a small
    # open economy whose net return is pinned at r0
    if np.isinf(eta):
        K = K0 * (1 - tau) ** (1 / (1 - alpha))
    else:
        K = K0 * np.exp(eta * np.log(1 - tau) / (1 + eta * (1 - alpha)))
    r = mpk(K)
    rn = (1 - tau) * r
    w = mpl(K)
    revenue = tau * r * K
    worker_loss = (w0 - w) * L
    # the owners' loss: the fall in the net return on the original stock, as a first-order measure (for supply that
    # responds, the surplus of the capital that leaves is the integral under the supply curve)
    if eta == 0:
        owner_loss = (r0 - rn) * K0
    elif np.isinf(eta):
        owner_loss = 0.0
    else:
        rs = np.linspace(rn, r0, 400)
        owner_loss = float(np.trapezoid(K0 * (rs / r0) ** eta, rs))
    total = worker_loss + owner_loss
    return {"K": K, "r": r, "r_net": rn, "w": w, "r0": r0, "w0": w0, "revenue": revenue, "worker_loss": worker_loss,
            "owner_loss": owner_loss, "worker_share": worker_loss / total, "dwl": total - revenue,
            "worker_per_revenue": worker_loss / revenue}


# ---------------------------------------------------------------------------------------------------------------
# deadweight loss


def triangle(t: float, eps_d: float = 0.5, eps_s: float = 1.0, p0: float = 1.0, q0: float = 1.0) -> dict:
    """A tax of ``t`` per unit (as a share of the untaxed price) in a market with demand q0 (p/p0)^-eps_d and supply
    q0 (p/p0)^eps_s.  Returns the price buyers pay and sellers keep, the quantity, the revenue, the exact deadweight
    loss and Harberger's approximation."""
    T = t * p0

    def excess(ps):
        return q0 * ((ps + T) / p0) ** (-eps_d) - q0 * (ps / p0) ** eps_s
    ps = brentq(excess, 1e-9, p0 * 1.000001) if t > 0 else p0
    pb = ps + T
    q = q0 * (ps / p0) ** eps_s
    # consumer and producer surplus lost, by integrating the curves
    pbs = np.linspace(p0, pb, 400)
    cs = float(np.trapezoid(q0 * (pbs / p0) ** (-eps_d), pbs))
    pss = np.linspace(ps, p0, 400)
    prs = float(np.trapezoid(q0 * (pss / p0) ** eps_s, pss))
    revenue = T * q
    approx = 0.5 * t * t * (eps_d * eps_s / (eps_d + eps_s)) * p0 * q0
    return {"t": t, "p_buy": pb, "p_sell": ps, "q": q, "revenue": revenue, "dwl": cs + prs - revenue,
            "approx": approx, "buyer_share": (pb - p0) / T if T else eps_s / (eps_d + eps_s)}


# ---------------------------------------------------------------------------------------------------------------
# Ramsey


def _good(t, eps, A=1.0):
    """Revenue and deadweight loss of a tax t on a good with demand A p^-eps, produced at constant cost 1."""
    q = A * (1 + t) ** (-eps)
    rev = t * q
    if abs(eps - 1.0) < 1e-12:
        cs = A * np.log1p(t)
    else:
        cs = A * ((1 + t) ** (1 - eps) - 1) / (1 - eps)
    return rev, cs - rev


def ramsey(eps, revenue: float, A=None) -> dict:
    """Taxes on independent goods (demand A_i p^-eps_i, cost 1) that raise ``revenue`` at the least total deadweight
    loss: t_i / (1 + t_i) = k / eps_i, with k set by the revenue; against one uniform rate raising the same."""
    eps = np.asarray(eps, float)
    A = np.ones_like(eps) if A is None else np.asarray(A, float)

    def taxes(k):
        m = np.minimum(k / eps, 0.95)
        return m / (1 - m)

    def rev(ts):
        return float(sum(_good(t, e, a)[0] for t, e, a in zip(ts, eps, A)))
    k = brentq(lambda k: rev(taxes(k)) - revenue, 1e-9, 0.9 * eps.min())
    tr = taxes(k)
    u = brentq(lambda t: rev(np.full_like(eps, t)) - revenue, 1e-9, 5.0)
    tu = np.full_like(eps, u)

    def parts(ts):
        out = [_good(t, e, a) for t, e, a in zip(ts, eps, A)]
        return [o[0] for o in out], [o[1] for o in out]
    rr, dr = parts(tr)
    ru, du = parts(tu)
    return {"eps": eps.tolist(), "k": k, "ramsey": tr.tolist(), "uniform": u, "rev_ramsey": rr, "dwl_ramsey": dr,
            "rev_uniform": ru, "dwl_uniform": du, "total_ramsey": float(sum(dr)), "total_uniform": float(sum(du))}


# ---------------------------------------------------------------------------------------------------------------
# Mirrlees and Diamond


def skills(n: int = 4000, mu: float = 0.0, sigma: float = 0.5, alpha: float = 2.0, tail: float = 0.97,
           w_max_q: float = 0.99995):
    """A grid of skills for a density that is lognormal(mu, sigma) below the ``tail`` quantile w1 and Pareto with
    exponent ``alpha`` above it, the body rescaled so that the density is continuous at w1 and the whole normalized
    to one.  Returns the grid w (up to the ``w_max_q`` quantile), the density f, the exact distribution function F
    (the Pareto tail runs on past the grid), the grid's weights dw, and the tail beyond the grid's end:
    ``(c, w_hi)``, with density c w^-(alpha + 1) above w_hi."""
    from scipy.stats import lognorm
    ln = lognorm(s=sigma, scale=np.exp(mu))
    w1 = ln.ppf(tail)
    c_tail = (1 - tail) * alpha * w1 ** alpha
    scale_body = c_tail * w1 ** (-alpha - 1) / ln.pdf(w1)
    w_lo = ln.ppf(0.0005)
    total = scale_body * (tail - 0.0005) + (1 - tail)
    w_hi = w1 * ((1 - w_max_q) / (1 - tail)) ** (-1 / alpha)
    w = np.exp(np.linspace(np.log(w_lo), np.log(w_hi), n))
    f = np.where(w <= w1, ln.pdf(w) * scale_body, c_tail * w ** (-alpha - 1)) / total
    F = np.where(w <= w1, scale_body * (ln.cdf(w) - 0.0005),
                 scale_body * (tail - 0.0005) + (1 - tail) * (1 - (w1 / w) ** alpha)) / total
    dw = np.gradient(w)
    return w, f, F, dw, (c_tail / total, w_hi)


def diamond_schedule(e: float = 0.25, nu: float = 1.0, mu: float = 0.0, sigma: float = 0.5, alpha: float = 2.0,
                     tail: float = 0.97, n: int = 4000) -> dict:
    """Optimal marginal tax rates by Diamond's (1998) formula for quasi-linear utility c - l^(1 + 1/e)/(1 + 1/e):
    T'/(1 - T') = (1 + 1/e) * (1 - F(w)) / (w f(w)) * (1 - G(w)), where G(w) is the average welfare weight above w,
    with weights proportional to w^-nu normalized to average one.  Income z = w l, with l = (w (1 - T'))^e.  The
    integrals above w include the Pareto tail beyond the grid exactly, so the rates approach Saez's limit
    1 / (1 + alpha e) at the top instead of falling to zero at an artificial maximum skill."""
    w, f, F, dw, (c, w_hi) = skills(n, mu, sigma, alpha, tail)
    g = w ** (-nu)
    beyond_f = c * w_hi ** (-alpha) / alpha                  # mass above the grid
    beyond_gf = c * w_hi ** (-alpha - nu) / (alpha + nu)      # integral of w^-nu f above the grid
    mean_g = np.sum(g * f * dw) + beyond_gf
    g = g / mean_g
    beyond_gf = beyond_gf / mean_g
    tailmass = 1 - F
    above_gf = np.cumsum((g * f * dw)[::-1])[::-1] + beyond_gf
    above_f = np.cumsum((f * dw)[::-1])[::-1] + beyond_f
    G = above_gf / above_f
    A = 1 + 1 / e
    B = tailmass / (w * f)
    C = 1 - G
    x = np.maximum(A * B * C, 0.0)
    tp = x / (1 + x)
    z = w * (w * (1 - tp)) ** e
    # the limit: B -> 1/alpha and G -> 0, so T'/(1 - T') -> (1 + e)/(alpha e); incomes z ~ w^(1 + e) have a Pareto
    # tail with exponent a = alpha/(1 + e), which is Saez's 1/(1 + a e)
    a_income = alpha / (1 + e)
    top = 1 / (1 + a_income * e)
    return {"w": w, "F": F, "z": z, "Tprime": tp, "A": A, "B": B, "C": C, "top": top, "e": e, "alpha": alpha,
            "a_income": a_income}


# ---------------------------------------------------------------------------------------------------------------
# the top rate


def top_rate(a: float, e: float, g: float = 0.0) -> float:
    """Saez's (2001) optimal top rate: (1 - g) / (1 - g + a e)."""
    return (1 - g) / (1 - g + a * e)


def top_revenue(taus, a: float, e: float, tau0: float = 0.4) -> np.ndarray:
    """Revenue from the top bracket against its rate, per taxpayer in the bracket at the reference rate ``tau0`` and
    in units of the threshold.  Incomes in the tail are Pareto with exponent a (so the bracket's mean is a/(a - 1)
    times the threshold) and every one of them scales with ((1 - tau)/(1 - tau0))^e; the tail keeps its shape, more
    or fewer people cross the threshold, and the income above it scales with the power a e.  So the revenue is
    tau/(a - 1) ((1 - tau)/(1 - tau0))^(a e), whose peak is Saez's 1/(1 + a e) exactly."""
    taus = np.asarray(taus, float)
    return taus / (a - 1.0) * np.clip((1 - taus) / (1 - tau0), 0.0, None) ** (a * e)


# ---------------------------------------------------------------------------------------------------------------
# bunching


def bunching(n: int = 200000, e: float = 0.25, z_star: float = 50.0, t0: float = 0.2, t1: float = 0.4,
             mu: float = np.log(40.0), sigma: float = 0.5, friction: float = 0.01, bin_w: float = 0.5,
             window: float = 2.5, lo: float = 25.0, hi: float = 75.0, degree: int = 7, seed: int = 0) -> dict:
    """Taxpayers with quasi-linear utility choose income z = n (1 - t)^e; the marginal rate rises from t0 to t1 at
    z_star.  Those whose choice would straddle the kink bunch at it; each choice then has a small multiplicative
    error (optimization frictions).  Saez's estimator: fit a polynomial to the histogram outside a window around the
    kink, take the excess mass inside it in units of the counterfactual density at the kink, and divide by
    z_star * ln((1 - t0) / (1 - t1))."""
    rng = np.random.default_rng(seed)
    nn = np.exp(rng.normal(mu, sigma, n))
    z0 = nn * (1 - t0) ** e
    z1 = nn * (1 - t1) ** e
    z = np.where(z0 <= z_star, z0, np.where(z1 >= z_star, z1, z_star))
    bunched = float(np.mean((z0 > z_star) & (z1 < z_star)))
    z = z * np.exp(friction * rng.standard_normal(n))
    edges = np.arange(lo, hi + bin_w / 2, bin_w)
    h, _ = np.histogram(z, bins=edges)
    mid = (edges[:-1] + edges[1:]) / 2
    out = np.abs(mid - z_star) > window
    x = (mid - z_star) / (hi - lo)
    coef = np.polyfit(x[out], h[out], degree)
    cf = np.polyval(coef, x)
    inside = ~out
    B = float(np.sum(h[inside] - cf[inside]))
    h0 = float(np.polyval(coef, 0.0))
    b = B / h0 * bin_w                       # excess mass in units of income at the counterfactual density
    e_hat = b / (z_star * np.log((1 - t0) / (1 - t1)))
    return {"mid": mid.tolist(), "h": h.tolist(), "cf": cf.tolist(), "B": B, "b": b, "e_hat": float(e_hat), "e": e,
            "z_star": z_star, "t0": t0, "t1": t1, "window": window, "share_bunched": bunched, "n": n,
            "bin_w": bin_w}


# ---------------------------------------------------------------------------------------------------------------
# evasion


def allingham_sandmo(p: float, t: float = 0.3, theta: float = 1.0, rho: float = 2.0, W: float = 100.0) -> float:
    """The share of income declared by a taxpayer with CRRA utility (relative risk aversion ``rho``) who is audited
    with probability p and then pays the evaded tax plus a fine of theta times it: maximize
    (1 - p) U(W - t d) + p U(W - t d - (1 + theta) t (W - d)) over the declared income d in [0, W]."""
    def U(c):
        c = np.maximum(c, 1e-9)
        return np.log(c) if rho == 1 else c ** (1 - rho) / (1 - rho)
    d = np.linspace(0, W, 4001)
    eu = (1 - p) * U(W - t * d) + p * U(W - t * d - (1 + theta) * t * (W - d))
    return float(d[int(np.argmax(eu))] / W)
