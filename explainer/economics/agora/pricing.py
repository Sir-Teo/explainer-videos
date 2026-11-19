"""The price maker (Agora, Part 10): a seller who sets the price, and every way of setting it.

**One price.**  :class:`Linear` and :class:`ConstantElasticity` demand; :func:`monopoly` (the profit-maximizing
price, quantity, profit, consumer surplus and deadweight loss, with the Lerner index and the inverse-elasticity rule
checked); :func:`pass_through` (how much of a cost change reaches the price: a half for linear demand, more than one
for constant elasticity, numerically for any demand); :func:`ferry` (Bo's ferry: a toll on a crossing that costs
nothing at the margin, against islanders' values).

**Discrimination.**  :func:`first_degree` (every buyer pays her value), :func:`third_degree` (two groups with linear
demands, one price or two; Varian's output test), :func:`screening` (Mussa and Rosen with two types: the menu, the
low type's quality distorted down, the high type's information rent), :func:`two_part` (Oi's Disneyland: an entry fee
and a price per ride, for identical and for different buyers), :func:`bundling` (Adams and Yellen: separate prices,
a bundle, or both, for buyers with correlated values).

**Time.**  :func:`coase` (a durable good sold to buyers who can wait: the skimming equilibrium by backward induction,
and the first price falling toward cost as the seller can cut prices more often).

**Practice.**  :func:`littlewood` (two fare classes on a fixed number of seats: protect seats for the high fare
while the high fare times the chance of selling one more exceeds the low fare).

**The frontier.**  :func:`personalized` (Dube and Misra: randomize prices, fit a logit of purchase on features and
price, then price each buyer; profit, consumer and total surplus against the best single price).

**Natural monopoly and regulation.**  :func:`ramsey` (Ramsey-Boiteux prices for two products that must cover a fixed
cost, against a uniform markup), :func:`averch_johnson` (a rate-of-return constraint and too much capital),
:func:`monopsony` (one employer facing a rising supply of labour, and a minimum wage).

Plain numpy and scipy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar


# ---------------------------------------------------------------------------------------------------------------
# demand


@dataclass(frozen=True)
class Linear:
    """Q = a - b P (so P = a / b - Q / b)."""
    a: float
    b: float

    def q(self, p):
        return np.maximum(self.a - self.b * np.asarray(p, float), 0.0)

    def p(self, q):
        return (self.a - np.asarray(q, float)) / self.b

    def elasticity(self, p):
        p = np.asarray(p, float)
        return -self.b * p / np.maximum(self.q(p), 1e-300)

    def cs(self, p):
        """Consumer surplus at price p."""
        return 0.5 * self.q(p) * (self.a / self.b - np.asarray(p, float))


@dataclass(frozen=True)
class ConstantElasticity:
    """Q = A P^(-eps), eps > 1."""
    A: float
    eps: float

    def q(self, p):
        return self.A * np.asarray(p, float) ** (-self.eps)

    def p(self, q):
        return (np.asarray(q, float) / self.A) ** (-1 / self.eps)

    def elasticity(self, p):
        return -self.eps * np.ones_like(np.asarray(p, float))


def monopoly(d, c: float) -> dict:
    """The monopoly price for demand ``d`` and constant marginal cost ``c``, by maximizing profit numerically, with
    the Lerner index (p - c)/p and the inverse elasticity -1/eps at that price (equal at the optimum)."""
    if isinstance(d, ConstantElasticity):
        p = c * d.eps / (d.eps - 1)
    else:
        res = minimize_scalar(lambda p: -(p - c) * float(d.q(p)), bounds=(c, d.a / d.b), method="bounded",
                              options={"xatol": 1e-12})
        p = float(res.x)
    q = float(d.q(p))
    out = {"p": p, "q": q, "profit": (p - c) * q, "lerner": (p - c) / p, "inv_elasticity": -1 / float(d.elasticity(p))}
    if isinstance(d, Linear):
        qc = float(d.q(c))
        out.update({"cs": float(d.cs(p)), "q_competitive": qc, "cs_competitive": float(d.cs(c)),
                    "dwl": 0.5 * (p - c) * (qc - q)})
    return out


def pass_through(d, c: float, h: float = 1e-5) -> float:
    """dp/dc at the monopoly optimum, by a central difference."""
    return (monopoly(d, c + h)["p"] - monopoly(d, c - h)["p"]) / (2 * h)


def ferry(values, fares) -> dict:
    """Bo's ferry: crossing costs him nothing at the margin; each islander crosses if her value is at least the fare.
    For each fare: crossings, revenue, the surplus of those who cross, and the value lost by those who don't."""
    v = np.sort(np.asarray(values, float))[::-1]
    out = []
    for f in fares:
        cross = v >= f
        out.append({"fare": float(f), "cross": int(cross.sum()), "revenue": float(f * cross.sum()),
                    "surplus": float((v[cross] - f).sum()), "lost": float(v[~cross].sum())})
    grid = np.linspace(0, v.max(), 2001)
    rev = np.array([g * np.sum(v >= g) for g in grid])
    best = float(grid[int(np.argmax(rev))])
    return {"rows": out, "best_fare": best, "best_revenue": float(rev.max()), "total_value": float(v.sum())}


# ---------------------------------------------------------------------------------------------------------------
# price discrimination


def first_degree(d: Linear, c: float) -> dict:
    """Perfect discrimination: every buyer with value above cost buys at her value; the seller takes the whole
    surplus and there is no deadweight loss."""
    q = float(d.q(c))
    return {"q": q, "profit": float(d.cs(c)), "cs": 0.0, "dwl": 0.0}


def third_degree(d1: Linear, d2: Linear, c: float) -> dict:
    """Two groups the seller can tell apart (with no resale): a separate monopoly price for each, against one price
    for both.  Welfare (consumer surplus plus profit) and output in each case; Varian (1985): discrimination can
    raise welfare only if it raises output."""
    sep = [monopoly(d, c) for d in (d1, d2)]

    def total_q(p):
        return float(d1.q(p) + d2.q(p))

    hi = max(d1.a / d1.b, d2.a / d2.b)
    res = minimize_scalar(lambda p: -(p - c) * total_q(p), bounds=(c, hi), method="bounded", options={"xatol": 1e-12})
    pu = float(res.x)
    uni = {"p": pu, "q": total_q(pu), "profit": (pu - c) * total_q(pu),
           "cs": float(d1.cs(pu) + d2.cs(pu))}
    disc = {"p": [s["p"] for s in sep], "q": sum(s["q"] for s in sep), "profit": sum(s["profit"] for s in sep),
            "cs": sum(s["cs"] for s in sep)}
    for x in (uni, disc):
        x["welfare"] = x["cs"] + x["profit"]
    return {"uniform": uni, "discriminate": disc}


def screening(theta_lo: float, theta_hi: float, share_hi: float) -> dict:
    """Mussa-Rosen with two types: a buyer of type theta values quality q at theta * q, and quality costs q^2 / 2.
    The seller, who can't tell the types apart, offers a menu (q_L, p_L), (q_H, p_H).  The high type gets the
    efficient quality theta_H ("no distortion at the top"); the low type's quality is cut to theta_L - (share /
    (1 - share)) (theta_H - theta_L) (or to zero), which shrinks the rent the seller must leave the high type."""
    s = share_hi
    qH = theta_hi
    qL = max(theta_lo - s / (1 - s) * (theta_hi - theta_lo), 0.0)
    pL = theta_lo * qL
    rent = (theta_hi - theta_lo) * qL
    pH = theta_hi * qH - rent
    profit = (1 - s) * (pL - qL ** 2 / 2) + s * (pH - qH ** 2 / 2)
    # full information: each type gets its efficient quality and pays its full value
    full = (1 - s) * theta_lo ** 2 / 2 + s * theta_hi ** 2 / 2
    return {"qL": qL, "pL": pL, "qH": qH, "pH": pH, "rent": rent, "profit": profit, "profit_full_info": full,
            "q_efficient": [theta_lo, theta_hi]}


def two_part(demands, c: float) -> dict:
    """Oi's two-part tariff: an entry fee plus a price per unit.  With identical buyers the best tariff sets the price
    at marginal cost and the fee at a buyer's whole surplus.  With different buyers (all must enter), the price is
    raised above cost so that the fee, set at the smallest buyer's surplus, gives away less; ``profit_without_smallest``
    is the best tariff for the others alone, the alternative of shutting the smallest buyers out."""
    def profit(p):
        fee = min(float(d.cs(p)) for d in demands)
        return len(demands) * fee + (p - c) * sum(float(d.q(p)) for d in demands), fee

    hi = min(d.a / d.b for d in demands)
    res = minimize_scalar(lambda p: -profit(p)[0], bounds=(c, hi), method="bounded", options={"xatol": 1e-12})
    p = float(res.x)
    pr, fee = profit(p)
    single = [monopoly(d, c) for d in demands]
    out = {"p": p, "fee": fee, "profit": pr, "profit_at_cost": profit(c)[0], "fee_at_cost": profit(c)[1],
           "profit_one_price": sum(m["profit"] for m in single) if len(demands) == 1 else None}
    if len(demands) > 1:
        low = min(float(d.cs(c)) for d in demands)
        rest = [d for d in demands if float(d.cs(c)) > low + 1e-12]
        out["profit_without_smallest"] = two_part(rest, c)["profit"]
    return out


def bundling(v1, v2, c1: float = 0.0, c2: float = 0.0, grid: int = 121) -> dict:
    """Buyers with values (v1, v2) for two goods (one unit each).  Best separate prices, the best bundle price, and the
    best mixed menu (each good alone or both together), by grid search over prices (each buyer takes the option with
    the largest non-negative surplus)."""
    v1, v2 = np.asarray(v1, float), np.asarray(v2, float)
    top = max(v1.max(), v2.max())
    ps = np.linspace(0, top, grid)
    pb = np.linspace(0, v1.max() + v2.max(), 2 * grid)

    def sep(p1, p2):
        return np.sum((v1 >= p1) * (p1 - c1)) + np.sum((v2 >= p2) * (p2 - c2))

    best_sep = max(((sep(a, b), a, b) for a in ps for b in ps), key=lambda t: t[0])
    bund = [(np.sum((v1 + v2 >= p) * (p - c1 - c2)), p) for p in pb]
    best_b = max(bund, key=lambda t: t[0])

    def mixed(p1, p2, p):
        s0 = np.zeros_like(v1)
        s1, s2, s3 = v1 - p1, v2 - p2, v1 + v2 - p
        S = np.stack([s0, s1, s2, s3])
        k = np.argmax(S, axis=0)
        rev = np.array([0.0, p1 - c1, p2 - c2, p - c1 - c2])
        return float(np.sum(rev[k]))

    coarse = np.linspace(0, top, 31)
    coarse_b = np.linspace(0, v1.max() + v2.max(), 41)
    best_m = max(((mixed(a, b, p), a, b, p) for a in coarse for b in coarse for p in coarse_b if p <= a + b),
                 key=lambda t: t[0])
    # a mixed menu can always mimic the pure bundle (single goods priced out of reach) or separate prices
    big = 10 * (v1.max() + v2.max())
    for cand in ((mixed(big, big, best_b[1]), big, big, best_b[1]),
                 (mixed(best_sep[1], best_sep[2], best_sep[1] + best_sep[2]), best_sep[1], best_sep[2],
                  best_sep[1] + best_sep[2])):
        if cand[0] > best_m[0]:
            best_m = cand
    return {"separate": {"profit": float(best_sep[0]), "p1": float(best_sep[1]), "p2": float(best_sep[2])},
            "bundle": {"profit": float(best_b[0]), "p": float(best_b[1])},
            "mixed": {"profit": best_m[0], "p1": float(best_m[1]), "p2": float(best_m[2]), "p": float(best_m[3])},
            "corr": float(np.corrcoef(v1, v2)[0, 1])}


# ---------------------------------------------------------------------------------------------------------------
# durable goods: the Coase conjecture


def coase(delta: float, periods: int = 400) -> dict:
    """A seller of a durable good (cost zero) to buyers with values uniform on [0, 1], who can wait; the seller sets a
    price each period and cannot commit.  The skimming equilibrium by backward induction from a last period: with
    remaining buyers [0, x], the seller sells to the top, (s x, x], at price a x, and earns v x^2.  Returns the first
    price (as the number of periods grows, the stationary value) and the price path from x = 1."""
    a, v = 0.5, 0.25                      # one period left: price x / 2, profit x^2 / 4
    for _ in range(periods - 1):
        m = 1 - delta + delta * a           # price per unit of the marginal buyer's value, given tomorrow's a
        s = m / (2 * m - 2 * delta * v)     # the cutoff, as a share of today's top value
        s = min(max(s, 0.0), 1.0)
        a, v = s * m, m * s * (1 - s) + delta * v * s * s
    # the price path, using the stationary rule
    m = 1 - delta + delta * a
    s = m / (2 * m - 2 * delta * v)
    x, path, sold = 1.0, [], []
    for _ in range(12):
        path.append(a * x)
        sold.append(x - s * x)
        x *= s
    return {"first_price": a, "profit": v, "cutoff_share": s, "path": path, "sold": sold}


# ---------------------------------------------------------------------------------------------------------------
# natural monopoly and regulation


def ramsey(d1: ConstantElasticity, d2: ConstantElasticity, c1: float, c2: float, F: float) -> dict:
    """Ramsey-Boiteux: the prices that cover marginal and fixed costs with the least loss of surplus.  Markups follow
    the inverse-elasticity rule (p_i - c_i) / p_i = k / eps_i, with k set so that profit just covers F.  Compared with
    a uniform markup that also covers F, and with marginal-cost prices that leave the fixed cost unpaid."""
    def profit_at(k):
        p1 = c1 / (1 - k / d1.eps)
        p2 = c2 / (1 - k / d2.eps)
        return (p1 - c1) * float(d1.q(p1)) + (p2 - c2) * float(d2.q(p2)) - F, p1, p2

    assert profit_at(1.0)[0] > 0, "the fixed cost exceeds the most a monopolist could earn"
    k = brentq(lambda k: profit_at(k)[0], 1e-9, 1.0)
    _, p1, p2 = profit_at(k)

    def cs(d, p):
        # surplus above price p for constant elasticity: integral_p^inf A t^-eps dt
        return d.A * p ** (1 - d.eps) / (d.eps - 1)

    def uniform_profit(m):
        return (c1 * m - c1) * float(d1.q(c1 * m)) + (c2 * m - c2) * float(d2.q(c2 * m)) - F

    top = minimize_scalar(lambda m: -uniform_profit(m), bounds=(1.0, 50.0), method="bounded").x
    mu = brentq(uniform_profit, 1.0 + 1e-9, top)
    loss = lambda q1, q2: cs(d1, c1) + cs(d2, c2) - cs(d1, q1) - cs(d2, q2) - F  # noqa: E731
    return {"k": k, "p": [p1, p2], "markups": [(p1 - c1) / p1, (p2 - c2) / p2], "uniform_markup": mu,
            "uniform_p": [c1 * mu, c2 * mu], "loss_ramsey": loss(p1, p2), "loss_uniform": loss(c1 * mu, c2 * mu),
            "mc_deficit": F}


def averch_johnson(A: float, a: float, b: float, p: float, w: float, r: float, s: float) -> dict:
    """A regulated firm with q = A K^a L^b sold at price p, paying wage w and cost of capital r, may earn at most the
    allowed return s > r on its capital: p q - w L <= s K.  Compared with the unregulated choice's capital-labour
    ratio at the same output, the regulated firm uses too much capital (Averch and Johnson 1962)."""
    def neg(x, regulated):
        K, L = np.exp(x)
        q = A * K ** a * L ** b
        prof = p * q - w * L - r * K
        if regulated:
            excess = p * q - w * L - s * K
            prof -= 1e4 * max(excess, 0.0) ** 2
        return -prof

    free = minimize(lambda x: neg(x, False), x0=np.log([1.0, 1.0]), method="Nelder-Mead",
                    options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
    Kf, Lf = np.exp(free.x)
    reg = minimize(lambda x: neg(x, True), x0=free.x, method="Nelder-Mead",
                   options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
    Kr, Lr = np.exp(reg.x)
    qr = A * Kr ** a * Lr ** b
    # the least-cost ratio for any output: K / L = (a / b) (w / r)
    return {"free": {"K": Kf, "L": Lf, "ratio": Kf / Lf}, "regulated": {"K": Kr, "L": Lr, "ratio": Kr / Lr, "q": qr},
            "efficient_ratio": a / b * w / r}


def monopsony(w0: float, slope: float, mrp: float, min_wage: float | None = None) -> dict:
    """One employer, a labour supply w = w0 + slope L, and a constant marginal revenue product.  The monopsonist hires
    where the marginal cost of labour (w0 + 2 slope L) equals mrp, and pays the supply wage there; competition would
    hire where w = mrp.  A minimum wage between the two raises both pay and employment."""
    Lm = (mrp - w0) / (2 * slope)
    wm = w0 + slope * Lm
    Lc = (mrp - w0) / slope
    out = {"monopsony": {"L": Lm, "w": wm}, "competitive": {"L": Lc, "w": mrp},
           "markdown": (mrp - wm) / wm}
    if min_wage is not None:
        Lmw = min((min_wage - w0) / slope, Lc) if min_wage <= mrp else 0.0
        out["minimum"] = {"w": min_wage, "L": Lmw}
    return out


def littlewood(seats: int, p_lo: float, p_hi: float, mean_hi: float, sd_hi: float, mean_lo: float = 1e9,
               draws: int = 200_000, seed: int = 1972) -> dict:
    """Littlewood's rule (1972): low fares are booked first; keep y seats back for late high-fare passengers, where
    y is the largest number with p_hi * P(high demand >= y) >= p_lo.  Expected revenue by simulation for every
    protection level, with high-fare demand normal (rounded, floored at zero) and low-fare demand plentiful."""
    from scipy.stats import norm  # noqa: PLC0415

    y_rule = int(np.floor(norm.ppf(1 - p_lo / p_hi, loc=mean_hi, scale=sd_hi)))
    rng = np.random.default_rng(seed)
    hi = np.maximum(np.round(rng.normal(mean_hi, sd_hi, draws)), 0)
    rev = []
    for y in range(seats + 1):
        lo_sold = min(seats - y, mean_lo)
        hi_sold = np.minimum(hi, seats - lo_sold)
        rev.append(float(np.mean(lo_sold * p_lo + hi_sold * p_hi)))
    best = int(np.argmax(rev))
    return {"protect_rule": y_rule, "protect_best": best, "revenue": rev, "revenue_rule": rev[max(min(y_rule, seats), 0)],
            "revenue_none": rev[0], "revenue_best": rev[best]}



# ---------------------------------------------------------------------------------------------------------------
# the frontier: prices learned from an experiment


def _logit_fit(Z: np.ndarray, y: np.ndarray, iters: int = 50) -> np.ndarray:
    """Logistic regression by Newton's method (IRLS)."""
    b = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ b))
        W = p * (1 - p)
        step = np.linalg.solve(Z.T @ (Z * W[:, None]) + 1e-9 * np.eye(Z.shape[1]), Z.T @ (y - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def personalized(n_train: int = 8000, n_test: int = 200_000, beta=(0.45, 0.3, 0.2, 0.0, 0.0, 0.0),
                 mu: float = 1.0, scale: float = 0.35, grid=None, seed: int = 2023) -> dict:
    """Personalized pricing learned from a price experiment, after Dube and Misra (2023).  Buyers have features X
    (standard normal) and a log-logistic willingness to pay, log v = mu + X beta + scale * e.  The seller shows
    randomly drawn prices from ``grid`` to ``n_train`` buyers, fits a logit of purchase on the features and log
    price (the true model's form), then prices every test buyer at the fitted model's best price, and compares that
    with the best single price (also chosen from the fitted model).  Profit, consumer surplus and total surplus are
    realized on fresh test buyers, with zero marginal cost."""
    rng = np.random.default_rng(seed)
    beta = np.asarray(beta, float)
    k = beta.size
    grid = np.linspace(0.5, 12.0, 116) if grid is None else np.asarray(grid, float)

    def draw(n):
        X = rng.normal(size=(n, k))
        logv = mu + X @ beta + scale * rng.logistic(size=n)
        return X, np.exp(logv)

    X, v = draw(n_train)
    shown = rng.choice(grid, n_train)
    bought = (v >= shown).astype(float)
    Z = np.column_stack([np.ones(n_train), X, np.log(shown)])
    b = _logit_fit(Z, bought)

    Xt, vt = draw(n_test)
    idx = np.column_stack([np.ones(n_test), Xt]) @ b[:-1]
    lg = np.log(grid)
    # the fitted model's expected revenue for every buyer at every grid price
    P = 1 / (1 + np.exp(-(idx[:, None] + b[-1] * lg[None, :])))
    R = P * grid[None, :]
    best = np.argmax(R, axis=1)
    p_pers = grid[best]
    p_unif = float(grid[np.argmax(R.mean(axis=0))])

    def outcome(p):
        buy = vt >= p
        prof = float(np.mean(np.where(buy, p, 0.0)))
        cs = float(np.mean(np.where(buy, vt - p, 0.0)))
        return {"profit": prof, "cs": cs, "total": prof + cs, "share_buying": float(np.mean(buy))}

    pers, unif = outcome(p_pers), outcome(np.full(n_test, p_unif))
    first = {"profit": float(np.mean(vt)), "cs": 0.0, "total": float(np.mean(vt)), "share_buying": 1.0}
    hist = np.bincount(best, minlength=grid.size)
    return {"coef": b, "true": {"beta": beta, "price": -1 / scale}, "p_uniform": p_unif, "uniform": unif,
            "personal": pers, "first_degree": first, "share_pay_less": float(np.mean(p_pers < p_unif)),
            "profit_gain": pers["profit"] / unif["profit"] - 1, "cs_change": pers["cs"] / unif["cs"] - 1,
            "hist": hist, "grid": grid, "p_personal_quantiles": np.quantile(p_pers, [0.1, 0.5, 0.9])}
