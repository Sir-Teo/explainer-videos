"""Agora's credit (Part 33): why financial systems amplify shocks and why their crises can be partly foreseen.
Minsky's three kinds of borrower; Fisher's debt deflation; Bernanke, Gertler and Gilchrist's costly-state-verification
contract and the financial accelerator; Kiyotaki and Moore's collateral cycle solved exactly under perfect foresight;
Geanakoplos's leverage cycle with natural buyers; households' balance sheets on the Island's counties (Mian and Sufi's
design); and the crisis predictor fitted to the Jorda-Schularick-Taylor database (a logit with country effects,
in-sample and out-of-sample areas under the ROC curve, and the paths of normal and financial recessions).  numpy and
scipy only."""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats


# --- Minsky's taxonomy -----------------------------------------------------------------------------------------------
def minsky_shares(cash, debt, rate: float, maturity: float = 20.0) -> dict:
    """Classify borrowers as Minsky did: *hedge* if cash flow covers interest and the principal due this year,
    *speculative* if it covers interest only, *Ponzi* if it does not cover even the interest.  ``cash`` and ``debt``
    are arrays (one entry per borrower); principal falls due evenly over ``maturity`` years."""
    cash, debt = np.asarray(cash, float), np.asarray(debt, float)
    interest = rate * debt
    due = interest + debt / maturity
    hedge = cash >= due
    ponzi = cash < interest
    spec = ~hedge & ~ponzi
    n = len(cash)
    return {"hedge": float(hedge.sum() / n), "speculative": float(spec.sum() / n), "ponzi": float(ponzi.sum() / n),
            "rate": rate}


def minsky_boom(n: int = 4000, years: int = 12, seed: int = 0, rate0: float = 0.03, rate_end: float = 0.06,
                growth: float = 0.10) -> dict:
    """A credit boom on the Island: borrowers' debt grows faster than their cash flow while credit is cheap, then the
    rate rises.  Each year's shares of hedge, speculative and Ponzi borrowers."""
    rng = np.random.default_rng(seed)
    cash = np.exp(rng.normal(0.0, 0.35, n))
    debt = cash * np.exp(rng.normal(np.log(4.0), 0.55, n))
    rates = np.concatenate([np.full(years - 3, rate0), np.linspace(rate0, rate_end, 4)[1:]])
    out = {"year": [], "rate": [], "hedge": [], "speculative": [], "ponzi": [], "debt_to_cash": []}
    for t in range(years):
        sh = minsky_shares(cash, debt, rates[t])
        for k in ("hedge", "speculative", "ponzi"):
            out[k].append(sh[k])
        out["year"].append(t)
        out["rate"].append(float(rates[t]))
        out["debt_to_cash"].append(float(np.median(debt / cash)))
        debt = debt * (1 + growth + 0.04 * rng.standard_normal(n))
        cash = cash * (1 + 0.02 + 0.03 * rng.standard_normal(n))
    return out


# --- Fisher's debt deflation ----------------------------------------------------------------------------------------
def debt_deflation(debt_to_income: float, deflation, real_growth, repay: float = 0.0) -> list:
    """The ratio of nominal debt to nominal income when prices fall at ``deflation`` (a fraction a year, a number or a
    path), real income grows at ``real_growth`` and a share ``repay`` of the debt is paid down each year.  The more
    debtors pay, the more they owe: with prices falling fast enough the ratio rises despite the repayments."""
    deflation = np.atleast_1d(np.asarray(deflation, float))
    real_growth = np.broadcast_to(np.asarray(real_growth, float), deflation.shape)
    b = [float(debt_to_income)]
    for d, g in zip(deflation, real_growth):
        b.append(b[-1] * (1 - repay) / ((1 - d) * (1 + g)))
    return b


# --- the costly-state-verification contract (Bernanke, Gertler and Gilchrist 1999) ---------------------------------
def _lognormal(omega, sigma):
    """F, f, Gamma, G and their derivatives for log(omega) ~ N(-sigma^2/2, sigma^2) (mean one)."""
    z = (np.log(omega) + 0.5 * sigma ** 2) / sigma
    F = stats.norm.cdf(z)
    f = stats.norm.pdf(z) / (omega * sigma)
    G = stats.norm.cdf(z - sigma)                      # E[omega; omega < omega_bar]
    Gamma = G + omega * (1 - F)
    return F, f, G, Gamma


def csv_contract(sigma: float = 0.35, mu: float = 0.15, n: int = 600) -> dict:
    """The optimal debt contract when lenders must pay a share ``mu`` of a failed project's value to see its return.
    An entrepreneur with net worth N buys capital K (price one) whose return is omega R^k with omega lognormal of
    mean one and log standard deviation ``sigma``, repays omega_bar R^k K unless omega < omega_bar, and lenders, whose
    funds cost R, break even.  Traced over the default threshold: the premium s = R^k / R that makes a contract with
    that threshold optimal, the leverage K / N it supports, and the default probability.  The premium rises with
    leverage: the external finance premium."""
    ob = np.linspace(0.05, 1.2, n)
    F, f, G, Gamma = _lognormal(ob, sigma)
    dGamma, dG = 1 - F, ob * f
    lam = dGamma / (dGamma - mu * dG)
    s = lam / ((1 - Gamma) + lam * (Gamma - mu * G))
    lev = 1 / (1 - s * (Gamma - mu * G))
    ok = (dGamma - mu * dG > 0) & (lev > 1) & np.isfinite(lev) & (s > 1)
    ok &= np.concatenate([[True], np.diff(s) > 0])
    ok &= np.concatenate([[True], np.diff(lev) > 0])
    return {"omega_bar": ob[ok].tolist(), "premium": s[ok].tolist(), "leverage": lev[ok].tolist(),
            "default": F[ok].tolist(), "sigma": sigma, "mu": mu}


def premium_at(leverage: float, C: dict) -> float:
    """The external finance premium at a given leverage, interpolated on a traced contract ``C``."""
    return float(np.interp(leverage, C["leverage"], C["premium"]))


def accelerator(N: float, C: dict, K_star: float = 2.0, s_star: float | None = None, theta: float = 0.3) -> dict:
    """Investment when the expected return on capital falls with the capital stock, R^k / R = s* (K / K*)^-theta,
    and the premium a firm pays depends on its leverage K / N.  The firm invests until its return equals the
    premium: K solves s* (K / K*)^-theta = s(K / N).  Calibrated so that N = 1 gives K = K*."""
    s_star = premium_at(K_star, C) if s_star is None else s_star

    def gap(K):
        return s_star * (K / K_star) ** -theta - premium_at(K / N, C)

    lo = max(N * min(C["leverage"]) * 1.0001, 1e-6)
    hi = N * max(C["leverage"]) * 0.9999
    K = optimize.brentq(gap, lo, hi)
    return {"K": float(K), "premium": premium_at(K / N, C), "leverage": float(K / N), "N": N}


# --- the collateral cycle (Kiyotaki and Moore 1997) ----------------------------------------------------------------
KM = {"R": 1.1, "a": 1.0, "c": 0.5, "eta": 2.0, "k_star": 1.0}


def km_steady(**kw) -> dict:
    """The steady state: farmers' land k*, the user cost u* = a and the land price q* = R a / (R - 1); farmers borrow
    up to next period's value of their land, b* = q* k* / R."""
    p = {**KM, **kw}
    u = p["a"]
    q = p["R"] * u / (p["R"] - 1)
    return {"k": p["k_star"], "u": u, "q": q, "b": q * p["k_star"] / p["R"], **p}


def _km_u(k, p):
    """The user cost of land, set by the gatherers' marginal product: u = a (k / k*)^(1/eta)."""
    return p["a"] * (k / p["k_star"]) ** (1 / p["eta"])


def km_path(shock: float = 0.01, T: int = 40, static: bool = False, **kw) -> dict:
    """Kiyotaki and Moore's response to an unexpected fall of ``shock`` in the farmers' tradable output at date 0,
    under perfect foresight afterwards, solved exactly.

    Farmers hold land k_t, borrow up to the discounted value of their land next period (b_t = q_{t+1} k_t / R) and
    invest all their net worth: k_t (q_t - q_{t+1} / R) = (a + q_t) k_{t-1} - R b_{t-1}.  The user cost u_t =
    q_t - q_{t+1} / R is the gatherers' marginal product, u = a (k / k*)^(1/eta).  From date 1 net worth is a k_{t-1},
    so k_t / k* = (k_{t-1} / k*)^(eta / (1 + eta)): the fall persists.  At date 0 the farmers also lose the fall in
    the land price on the land they hold: k_0 u_0 = [a (1 - shock) - (q* - q_0)] k*, with q_0 the discounted sum of
    future user costs, which depends on the whole path.  ``static=True`` holds the land price at q* (no capital
    loss): the static multiplier alone."""
    p = km_steady(**kw)
    R, a, ks, eta = p["R"], p["a"], p["k_star"], p["eta"]
    rho = eta / (1 + eta)

    def path_from(k0):
        k = [k0]
        for _ in range(T):
            k.append(ks * (k[-1] / ks) ** rho)
        k = np.array(k)
        u = _km_u(k, p)
        disc = R ** -np.arange(T + 1)
        q = np.array([np.sum(u[t:] * disc[: T + 1 - t]) + R ** -(T + 1 - t) * p["q"] for t in range(T + 1)])
        return k, u, q

    if static:
        k0 = ks * (1 - shock) ** rho
    else:
        def gap(k0):
            k, u, q = path_from(k0)
            return k0 * u[0] - (a * (1 - shock) - (p["q"] - q[0])) * ks

        grid = ks * (1 - np.linspace(0, 0.95, 381))
        vals = np.array([gap(x) for x in grid])
        neg = np.nonzero(vals < 0)[0]
        if len(neg) == 0:
            raise ValueError("no equilibrium: the shock is too large for this calibration")
        j = neg[0]
        k0 = optimize.brentq(gap, grid[j], grid[j - 1])
    k, u, q = path_from(k0)
    if static:
        q = np.full_like(q, p["q"])
    # output next period: farmers (a + c) k_t, gatherers G(K - k_t), with G' = R u
    dY = (a + p["c"]) * (k - ks) + R * a * ks * (1 - (k / ks) ** (1 / rho)) * rho
    Y_star = 2 * (a + p["c"]) * ks
    return {"t": list(range(T + 1)), "k": (100 * (k / ks - 1)).tolist(), "q": (100 * (q / p["q"] - 1)).tolist(),
            "Y": (100 * dY / Y_star).tolist(), "k0": float(100 * (k0 / ks - 1)), "q0": float(100 * (q[0] / p["q"] - 1)),
            "shock": shock, "static": static, "params": p}


def km_amplification(shock: float = 0.01, **kw) -> dict:
    """The fall in farmers' land at date 0 per unit of the shock: without the credit constraint (none), with the
    constraint but the land price held fixed (static), and with the land price's feedback (dynamic)."""
    st = km_path(shock, static=True, **kw)
    dy = km_path(shock, **kw)
    return {"none": 0.0, "static": -st["k0"] / (100 * shock), "dynamic": -dy["k0"] / (100 * shock),
            "q0": dy["q0"], "static_path": st, "dynamic_path": dy}


# --- the leverage cycle (Geanakoplos 2010) -------------------------------------------------------------------------
def leverage_static(d: float = 0.2, leverage: bool = True) -> dict:
    """One period.  A continuum of agents h in [0, 1], each with one unit of cash and one unit of an asset that pays 1
    with probability h (in agent h's opinion) and d otherwise.  The most optimistic buy: the marginal buyer h1 values
    the asset at p = h1 + (1 - h1) d; buyers spend their cash and, with leverage, borrow d per unit (all a lender will
    lend without risk).  Market clearing: p h1 = (1 - h1) + d with leverage, (1 - h1) without."""
    extra = d if leverage else 0.0

    def gap(h):
        return (h + (1 - h) * d) * h - (1 - h) - extra

    h1 = optimize.brentq(gap, 1e-9, 1 - 1e-9)
    p = h1 + (1 - h1) * d
    return {"h1": float(h1), "p": float(p), "margin": float((p - d) / p) if leverage else 1.0, "d": d,
            "average": float(0.5 + 0.5 * d)}


def leverage_cycle(d: float = 0.2) -> dict:
    """Two periods (Geanakoplos's tree): the asset pays 1 unless news is bad twice, when it pays d.  Agent h thinks
    each period's news is good with probability h.  At date 0 buyers h >= h0 borrow the most a lender will lend
    without risk, the price after bad news p_D; after bad news they are wiped out, and the next most optimistic
    (h in [h_D, h0), who sold at date 0 and hold cash 1 + p0) buy, borrowing d.  Four equations: two market
    clearings and two marginal buyers (h_D indifferent at D; h0 indifferent between buying levered now and keeping
    cash to buy levered after bad news)."""

    def eqs(x):
        p0, h0, pD, hD = x
        e1 = p0 * h0 - (1 - h0) - pD
        e2 = pD - (h0 - hD) * (1 + p0) - d
        e3 = pD - (hD + (1 - hD) * d)
        lev0 = h0 * (1 - pD) / max(p0 - pD, 1e-9)
        cash = h0 + (1 - h0) * h0 * (1 - d) / max(pD - d, 1e-9)
        e4 = lev0 - cash
        return [e1, e2, e3, e4]

    sol = optimize.fsolve(eqs, [0.9, 0.85, 0.6, 0.5], full_output=True)
    p0, h0, pD, hD = sol[0]
    fund0 = h0 * 1 + (1 - h0) * (h0 + (1 - h0) * d)         # the marginal buyer's own value of the asset
    return {"p0": float(p0), "h0": float(h0), "pD": float(pD), "hD": float(hD), "d": d,
            "margin0": float((p0 - pD) / p0), "marginD": float((pD - d) / pD), "leverage0": float(p0 / (p0 - pD)),
            "leverageD": float(pD / (pD - d)), "ok": bool(sol[2] == 1),
            "h0_value_at_D": float(h0 + (1 - h0) * d), "fund0": float(fund0)}


# --- households' balance sheets: the Island's counties (Mian and Sufi's design) ------------------------------------
def counties(n: int = 400, seed: int = 0, mpc_base: float = 0.02, mpc_slope: float = 0.06,
             price_drop: float = 0.25) -> dict:
    """``n`` counties.  Leverage (households' debt over their housing wealth) varies across counties; house prices
    fall more where supply is inelastic (the instrument) and where leverage was high.  Spending falls by the MPC out of
    housing wealth times the loss, and the MPC rises with leverage (planted: mpc_base + mpc_slope * leverage).  The
    cross-county regression of spending growth on the housing-wealth loss, overall and by leverage quintile."""
    rng = np.random.default_rng(seed)
    lev = np.clip(rng.beta(2.5, 3.5, n), 0.02, 0.95)
    inelastic = rng.uniform(0, 1, n)
    dp = -price_drop * (0.4 + 0.9 * inelastic + 0.5 * lev) * (1 + 0.15 * rng.standard_normal(n))
    wealth_loss = dp * 3.0                               # housing wealth of three years' spending
    mpc = mpc_base + mpc_slope * lev
    ds = mpc * wealth_loss + 0.01 * rng.standard_normal(n)
    X = np.column_stack([np.ones(n), wealth_loss])
    b = np.linalg.lstsq(X, ds, rcond=None)[0]
    q = np.quantile(lev, [0.2, 0.4, 0.6, 0.8])
    bins = np.digitize(lev, q)
    by = []
    for k in range(5):
        m = bins == k
        Xm = np.column_stack([np.ones(m.sum()), wealth_loss[m]])
        bk = np.linalg.lstsq(Xm, ds[m], rcond=None)[0]
        by.append({"lev": float(lev[m].mean()), "mpc": float(bk[1]), "truth": float(mpc[m].mean())})
    return {"lev": lev.tolist(), "dp": (100 * dp).tolist(), "ds": (100 * ds).tolist(),
            "loss": (100 * wealth_loss).tolist(),
            "mpc": float(b[1]), "mpc_truth": float(mpc.mean()), "by_quintile": by}


# --- the macrohistory database: the crisis predictor and the shape of recessions -----------------------------------
WARS = ((1914, 1919), (1939, 1947))


def _lagged(x, iso, k):
    out = np.full(len(x), np.nan)
    out[k:] = np.where(iso[k:] == iso[:-k], x[:-k], np.nan) if k > 0 else x
    return out


def jst_panel(D: dict) -> dict:
    """Arrays from the JST database: year, country, crisis starts, real loans per head growth (log differences),
    loans to GDP, real house prices, real GDP per head, and the war years."""
    iso = np.array(D["iso"])
    yr = np.array(D["year"], int)
    f = {k: np.array(D[k], float) for k in ("tloans", "cpi", "gdp", "hpnom", "rgdpbarro", "crisisJST", "pop")}
    with np.errstate(divide="ignore", invalid="ignore"):
        rl = np.log(f["tloans"] / f["cpi"])
        cg = 100 * f["tloans"] / f["gdp"]
        rh = np.log(f["hpnom"] / f["cpi"])
        y = np.log(f["rgdpbarro"])
    with np.errstate(invalid="ignore"):
        drl = rl - _lagged(rl, iso, 1)
    war = np.zeros(len(yr), bool)
    for a, b in WARS:
        war |= (yr >= a) & (yr <= b)
    return {"iso": iso, "year": yr, "country": np.array(D["country"]), "crisis": np.nan_to_num(f["crisisJST"]),
            "drl": drl, "cg": cg, "rh": rh, "y": y, "war": war}


def logit_fe(X, y, groups, ridge: float = 1e-4) -> np.ndarray:
    """A logit with a fixed effect per group (a light ridge keeps groups with no events finite).  Returns the
    coefficients: one per group, then one per column of X."""
    g = sorted(set(groups))
    Z = np.column_stack([(np.asarray(groups) == c).astype(float) for c in g] + [X])
    y = np.asarray(y, float)

    def nll(b):
        z = Z @ b
        return np.sum(np.logaddexp(0, z) - y * z) + ridge * b @ b

    def grad(b):
        pr = 1 / (1 + np.exp(-(Z @ b)))
        return Z.T @ (pr - y) + 2 * ridge * b

    b0 = np.zeros(Z.shape[1])
    b0[: len(g)] = np.log(max(y.mean(), 1e-3) / (1 - max(y.mean(), 1e-3)))
    r = optimize.minimize(nll, b0, jac=grad, method="BFGS", options={"maxiter": 2000})
    return r.x


def logit_predict(b, X, groups, levels) -> np.ndarray:
    """Probabilities from :func:`logit_fe`'s coefficients; a group not seen in fitting gets the mean effect."""
    ng = len(levels)
    fe = {c: b[i] for i, c in enumerate(levels)}
    mean_fe = float(np.mean(b[:ng]))
    z = np.array([fe.get(c, mean_fe) for c in groups]) + np.asarray(X) @ b[ng:]
    return 1 / (1 + np.exp(-z))


def auc(score, y) -> float:
    """The area under the ROC curve: the chance a random crisis year scores above a random calm year."""
    s, y = np.asarray(score, float), np.asarray(y, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = stats.rankdata(np.concatenate([pos, neg]))
    return float((r[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def roc(score, y, n: int = 101) -> dict:
    """The ROC curve: true- and false-positive rates over thresholds."""
    s, y = np.asarray(score, float), np.asarray(y, float)
    th = np.quantile(s, np.linspace(1, 0, n))
    tpr = [float(np.mean(s[y == 1] >= t)) for t in th]
    fpr = [float(np.mean(s[y == 0] >= t)) for t in th]
    return {"fpr": [0.0] + fpr + [1.0], "tpr": [0.0] + tpr + [1.0]}


def predictors(P: dict, measure: str = "real_loans", lags: int = 5) -> tuple:
    """The regressors and the rows that have them: ``"real_loans"``, growth of real bank loans in each of the
    ``lags`` years before (Schularick and Taylor's specification, with country effects); ``"credit_gdp"``, the rise in
    loans to GDP over the five years before (one regressor, pooled across countries)."""
    iso = P["iso"]
    if measure == "real_loans":
        X = np.column_stack([_lagged(P["drl"], iso, k) for k in range(1, lags + 1)])
        groups = iso
    else:
        X = (_lagged(P["cg"], iso, 1) - _lagged(P["cg"], iso, 6))[:, None] / 10.0     # per 10 points of GDP
        groups = np.zeros(len(iso), int)
    ok = np.all(np.isfinite(X), axis=1) & ~P["war"]
    return X, groups, ok


def crisis_predictor(P: dict, measure: str = "real_loans", lags: int = 5, oos_from: int = 1950) -> dict:
    """The probability of a crisis starting in year t from the credit measure of the years before (see
    :func:`predictors`), war years left out.  In-sample fit and area under the ROC curve; with country effects alone;
    and out of sample, refitting each year on the years before it and scoring only the years from ``oos_from``."""
    iso, yr, cr = P["iso"], P["year"], P["crisis"]
    X, groups, ok = predictors(P, measure, lags)
    levels = sorted(set(groups[ok]))
    b = logit_fe(X[ok], cr[ok], groups[ok])
    p_in = logit_predict(b, X[ok], groups[ok], levels)
    b0 = logit_fe(np.zeros((ok.sum(), 1)), cr[ok], iso[ok])
    p_fe = logit_predict(b0, np.zeros((ok.sum(), 1)), iso[ok], sorted(set(iso[ok])))
    late = yr[ok] >= oos_from
    oos_p, oos_y = [], []
    for Y in sorted(set(yr[ok & (yr >= oos_from)])):
        tr = ok & (yr < Y)
        te = ok & (yr == Y)
        if cr[tr].sum() < 5 or te.sum() == 0:
            continue
        bt = logit_fe(X[tr], cr[tr], groups[tr])
        oos_p.extend(logit_predict(bt, X[te], groups[te], sorted(set(groups[tr]))).tolist())
        oos_y.extend(cr[te].tolist())
    return {"measure": measure, "coef": b[len(levels):].tolist(), "sum_coef": float(b[len(levels):].sum()),
            "n": int(ok.sum()), "crises": int(cr[ok].sum()), "auc_in": auc(p_in, cr[ok]),
            "auc_in_late": auc(p_in[late], cr[ok][late]), "auc_fe": auc(p_fe, cr[ok]),
            "auc_oos": auc(oos_p, oos_y), "n_oos": len(oos_y), "crises_oos": int(np.sum(oos_y)),
            "roc_in": roc(p_in, cr[ok]), "roc_oos": roc(oos_p, oos_y), "b": b.tolist()}


def predict_before(P: dict, iso_code: str, year: int, measure: str = "credit_gdp", ahead: int = 3) -> float:
    """The chance of a crisis starting in the ``ahead`` years after ``year`` in one country, from a model fitted only
    on the years before ``year``: one minus the product of the yearly no-crisis chances, with the credit measure held
    at its value for the year after ``year``."""
    iso, yr, cr = P["iso"], P["year"], P["crisis"]
    X, groups, ok = predictors(P, measure)
    tr = ok & (yr <= year)
    b = logit_fe(X[tr], cr[tr], groups[tr])
    i = int(np.nonzero((iso == iso_code) & (yr == year + 1))[0][0])
    p1 = float(logit_predict(b, X[i:i + 1], groups[i:i + 1], sorted(set(groups[tr])))[0])
    return 1 - (1 - p1) ** ahead


def lead(x, iso, k):
    """x shifted ``k`` rows ahead within each country (NaN past a country's last year)."""
    out = np.full(len(x), np.nan)
    out[:-k] = np.where(iso[:-k] == iso[k:], x[k:], np.nan)
    return out


def big_booms(P: dict, n: int = 8, first: int = 1955, last: int = 2015, ahead: int = 3) -> list:
    """The ``n`` largest rises in loans to GDP over five years, one per country, from ``first`` to ``last``: booms
    with no crisis inside the five years, ending in a year when output per head still grew.  Each with whether a crisis
    started in the ``ahead`` years after."""
    iso, yr, cr, cg, y = P["iso"], P["year"], P["crisis"], P["cg"], P["y"]
    idx = {(a, b): i for i, (a, b) in enumerate(zip(iso, yr))}
    eps = []
    for i in range(len(yr)):
        t = int(yr[i])
        j, h = idx.get((iso[i], t - 5)), idx.get((iso[i], t - 1))
        if not (first <= t <= last) or j is None or h is None:
            continue
        if not (np.isfinite(cg[i]) and np.isfinite(cg[j]) and np.isfinite(y[i]) and np.isfinite(y[h]) and y[i] > y[h]):
            continue
        if any(cr[idx[(iso[i], t - k)]] == 1 for k in range(5) if (iso[i], t - k) in idx):
            continue
        out = any(cr[idx[(iso[i], t + k)]] == 1 for k in range(1, ahead + 1) if (iso[i], t + k) in idx)
        eps.append((float(cg[i] - cg[j]), str(iso[i]), t, float(cg[i]), bool(out)))
    eps.sort(reverse=True)
    chosen = []
    for e in eps:
        if all(e[1] != c[1] for c in chosen):
            chosen.append(e)
    return [{"rise": e[0], "iso": e[1], "year": e[2], "level": e[3], "crisis": e[4]} for e in chosen[:n]]


def boom_odds(P: dict, window: int = 3, ahead: int = 3, last: int = 2017) -> dict:
    """The chance of a crisis starting within ``ahead`` years, by quintile of the rise in loans to GDP over the past
    ``window`` years; and when house prices have also risen fast (both in the top quintile)."""
    iso, yr, cr = P["iso"], P["year"], P["crisis"]
    dcg = P["cg"] - _lagged(P["cg"], iso, window)
    drh = P["rh"] - _lagged(P["rh"], iso, window)
    nxt = np.zeros(len(yr))
    for k in range(1, ahead + 1):
        nxt = np.maximum(nxt, np.nan_to_num(lead(cr, iso, k)))
    ok = np.isfinite(dcg) & ~P["war"] & (yr <= last)
    q = np.quantile(dcg[ok], [0.2, 0.4, 0.6, 0.8])
    bins = np.digitize(dcg[ok], q)
    by = [float(nxt[ok][bins == k].mean()) for k in range(5)]
    ok2 = ok & np.isfinite(drh)
    top_c = dcg > np.quantile(dcg[ok2], 0.8)
    top_h = drh > np.quantile(drh[ok2], 0.8)
    both = ok2 & top_c & top_h
    neither = ok2 & ~top_c & ~top_h
    return {"by_quintile": by, "base": float(nxt[ok].mean()), "both": float(nxt[both].mean()),
            "n_both": int(both.sum()),
            "neither": float(nxt[neither].mean()), "cuts": q.tolist()}


def recession_paths(P: dict, H: int = 6, window: int = 2, first: int = 1870) -> dict:
    """Real GDP per head after each business-cycle peak (a year above both neighbours, war years left out), in
    percent of its level at the peak, for normal recessions and for financial ones (a crisis within ``window`` years
    of the peak); means and counts."""
    iso, yr, cr, y = P["iso"], P["year"], P["crisis"], P["y"]
    idx = {(a, b): i for i, (a, b) in enumerate(zip(iso, yr))}
    paths = {"normal": [], "financial": []}
    for i in range(1, len(yr) - 1):
        if not (iso[i - 1] == iso[i] == iso[i + 1]) or P["war"][i] or yr[i] < first:
            continue
        if not (np.isfinite(y[i - 1:i + 2]).all() and y[i] > y[i - 1] and y[i + 1] < y[i]):
            continue
        if not all((iso[i], yr[i] + h) in idx for h in range(H + 1)):
            continue
        p = [100 * (y[idx[(iso[i], yr[i] + h)]] - y[i]) for h in range(H + 1)]
        if not np.all(np.isfinite(p)):
            continue
        fin = any(cr[idx[(iso[i], yr[i] + k)]] == 1 for k in range(-window, window + 1) if (iso[i], yr[i] + k) in idx)
        paths["financial" if fin else "normal"].append(p)
    out = {"h": list(range(H + 1))}
    for k, v in paths.items():
        a = np.array(v)
        out[k] = a.mean(axis=0).tolist()
        out[f"n_{k}"] = len(v)
        out[f"se_{k}"] = (a.std(axis=0, ddof=1) / np.sqrt(len(v))).tolist()
    return out


# --- the countercyclical capital buffer (Basel III's guide) --------------------------------------------------------
def hp_trend(x, lam: float) -> np.ndarray:
    """The Hodrick-Prescott trend of ``x`` (two-sided)."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return x.copy()
    D = np.zeros((n - 2, n))
    for i in range(n - 2):
        D[i, i:i + 3] = (1.0, -2.0, 1.0)
    return np.linalg.solve(np.eye(n) + lam * D.T @ D, x)


def one_sided_gap(x, lam: float = 400000 / 4 ** 4, start: int = 10) -> np.ndarray:
    """The credit-to-GDP gap as the Basel Committee's guide defines it, with only the data known at each date: for
    each t, the HP trend of x up to t, and x_t minus its last value.  ``lam`` defaults to 400,000 on quarterly data
    rescaled to annual data (Ravn and Uhlig's fourth power); NaN for the first ``start`` years."""
    x = np.asarray(x, float)
    gap = np.full(len(x), np.nan)
    for t in range(start, len(x)):
        gap[t] = x[t] - hp_trend(x[: t + 1], lam)[-1]
    return gap


def ccyb_guide(gap, low: float = 2.0, high: float = 10.0, top: float = 2.5) -> np.ndarray:
    """The buffer the guide suggests: zero below a gap of ``low`` points, ``top`` percent of risk-weighted assets
    above ``high``, linear between."""
    g = np.asarray(gap, float)
    return np.clip((g - low) / (high - low), 0, 1) * top
