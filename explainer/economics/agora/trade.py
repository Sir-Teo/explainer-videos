"""Agora's trade, part I (Part 35): Ricardo with two goods, a chain of goods and a continuum (Dornbusch, Fischer and
Samuelson 1977); Heckscher-Ohlin's two-by-two-by-two world with its four theorems; specific factors; tariffs and
quotas in partial equilibrium, small and large; protection for sale (Grossman and Helpman 1994); a two-country tariff
war; and the tests and measures the part shows: Bernhofen and Brown's inner product, Leontief's ratio, Trefler's
factor-content statistics, and the gains-from-trade formula of Arkolakis, Costinot and Rodriguez-Clare.

numpy and scipy only.  Goods are indexed 1 and 2; a relative price ``p`` is the price of good 2 in units of good 1.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar


# --- Ricardo, two goods ----------------------------------------------------------------------------------------------
def ricardo_autarky(a1: float, a2: float, L: float, beta: float = 0.5) -> dict:
    """One country alone: ``a1``, ``a2`` hours per unit of goods 1 and 2, ``L`` hours, Cobb-Douglas spending share
    ``beta`` on good 1.  The relative price of good 2 is a2/a1; consumption equals production."""
    q1, q2 = beta * L / a1, (1 - beta) * L / a2
    return {"p": a2 / a1, "q1": q1, "q2": q2, "c1": q1, "c2": q2, "w1": 1 / a1, "w2": 1 / a2,
            "utility": q1 ** beta * q2 ** (1 - beta)}


def ricardo_trade(aH: tuple, aF: tuple, LH: float, LF: float, beta: float = 0.5) -> dict:
    """Two countries trade freely.  ``aH`` = (a1, a2) hours per unit at home, ``aF`` abroad.  World relative supply
    of good 2 is a step function of p; Cobb-Douglas demand gives relative demand (1 - beta)/beta / p.  Returns the
    world price, each country's output, consumption, real wage in each good, and the gain in utility over autarky."""
    pH, pF = aH[1] / aH[0], aF[1] / aF[0]               # autarky prices of good 2
    if pH > pF:                                          # foreign has the comparative advantage in good 2
        flip = ricardo_trade(aF, aH, LF, LH, beta)
        return {**flip, "H": flip["F"], "F": flip["H"], "exporter2": "F"}
    # home is cheaper in good 2: home exports good 2, foreign good 1
    Q2_full, Q1_full = LH / aH[1], LF / aF[0]            # both fully specialized
    p_full = (1 - beta) / beta * Q1_full / Q2_full      # the price that clears relative demand with full specialization
    p = min(max(p_full, pH), pF)
    out = {}

    def clear(Q1, Q2):                                  # spending on good 2 equals its value: p Q2 = (1-b)/b Q1
        return p * Q2 - (1 - beta) / beta * Q1

    if pH < p < pF:
        qH, qF = (0.0, Q2_full), (Q1_full, 0.0)
    elif p == pH:                                        # home's full output of good 2 is too much: it makes both
        h = brentq(lambda h: clear(Q1_full + (LH - h) / aH[0], h / aH[1]), 0.0, LH)
        qH, qF = ((LH - h) / aH[0], h / aH[1]), (Q1_full, 0.0)
    else:                                                # p == pF: foreign makes both
        h = brentq(lambda h: clear((LF - h) / aF[0], Q2_full + h / aF[1]), 0.0, LF)
        qH, qF = (0.0, Q2_full), ((LF - h) / aF[0], h / aF[1])
    for name, q, a, L in (("H", qH, aH, LH), ("F", qF, aF, LF)):
        income = q[0] + p * q[1]                         # in units of good 1
        c1, c2 = beta * income, (1 - beta) * income / p
        aut = ricardo_autarky(a[0], a[1], L, beta)
        out[name] = {"q1": q[0], "q2": q[1], "c1": c1, "c2": c2, "income": income,
                     "w1": income / L, "w2": income / L / p, "utility": c1 ** beta * c2 ** (1 - beta),
                     "gain": c1 ** beta * c2 ** (1 - beta) / aut["utility"] - 1, "autarky": aut}
    return {"p": p, "pH": pH, "pF": pF, "H": out["H"], "F": out["F"], "exporter2": "H",
            "wage_ratio": out["H"]["income"] / LH / (out["F"]["income"] / LF)}


def ppf(a1: float, a2: float, L: float, n: int = 50) -> tuple:
    """The production possibility frontier: (good 1, good 2) along the straight line."""
    q1 = np.linspace(0, L / a1, n)
    return q1, (L - a1 * q1) / a2


def ricardo_world_supply(aH: tuple, aF: tuple, LH: float, LF: float) -> dict:
    """The world relative supply of good 2 (Q2/Q1) as a step function of p, for drawing: flat at each autarky price,
    vertical at full specialization."""
    pH, pF = sorted((aH[1] / aH[0], aF[1] / aF[0]))
    lo = aH if aH[1] / aH[0] <= aF[1] / aF[0] else aF
    hi = aF if lo is aH else aH
    Llo, Lhi = (LH, LF) if lo is aH else (LF, LH)
    full = (Llo / lo[1]) / (Lhi / hi[0])
    return {"p_low": pH, "p_high": pF, "full": full}


# --- many goods: the chain, and the continuum ------------------------------------------------------------------------
def chain(aH, aF, omega: float) -> dict:
    """Ricardo's chain of comparative advantage: goods ranked by aF/aH (home's relative productivity).  With relative
    wage ``omega`` = w/w*, home makes good i when omega * aH_i < aF_i."""
    aH, aF = np.asarray(aH, float), np.asarray(aF, float)
    A = aF / aH
    order = np.argsort(-A)
    return {"A": A, "order": order, "home": omega < A, "omega": omega}


def dfs(A, b=None, L: float = 1.0, Lf: float = 1.0, g: float = 1.0) -> dict:
    """Dornbusch, Fischer and Samuelson (1977) on a grid of goods z in [0, 1].  ``A`` = a*(z)/a(z), decreasing in z;
    ``b`` spending shares (uniform if None); ``g`` the share of a good that survives shipping (1: free trade).  Home
    exports z with omega <= g A(z), foreign exports z with omega >= A(z)/g, and goods in between are not traded.  The
    relative wage omega balances trade: home's spending on foreign goods equals foreign spending on home goods."""
    A = np.asarray(A, float)
    n = len(A)
    z = (np.arange(n) + 0.5) / n
    b = np.full(n, 1.0 / n) if b is None else np.asarray(b, float) / np.sum(b)

    def gap(lw):
        w = np.exp(lw)
        hx, fx = w <= g * A, w >= A / g
        # home imports: home income w L times the share it spends on foreign exports; and the reverse
        return w * L * b[fx].sum() - Lf * b[hx].sum()

    lo, hi = np.log(A.min() * g) - 1, np.log(A.max() / g) + 1
    lw = brentq(gap, lo, hi, xtol=1e-12)
    w = float(np.exp(lw))
    hx, fx = w <= g * A, w >= A / g
    zH = float(z[hx].max()) if hx.any() else 0.0
    zF = float(z[fx].min()) if fx.any() else 1.0
    return {"omega": w, "z": z, "home_exports": hx, "foreign_exports": fx, "nontraded": ~(hx | fx),
            "zH": zH, "zF": zF, "share_home": float(b[w <= A].sum())}


def dfs_demand(z, L: float, Lf: float) -> np.ndarray:
    """The B(z) curve with uniform shares and free trade: omega = z/(1 - z) * Lf/L."""
    z = np.asarray(z, float)
    return z / (1 - z) * Lf / L


# --- Heckscher-Ohlin, two by two by two ------------------------------------------------------------------------------
def _cd_const(alpha: float) -> float:
    return alpha ** alpha * (1 - alpha) ** (1 - alpha)


def unit_cost(alpha: float, w, r):
    """Cobb-Douglas unit cost with labour share ``alpha``:
    c = w^alpha r^(1-alpha) / (alpha^alpha (1-alpha)^(1-alpha))."""
    return np.asarray(w, float) ** alpha * np.asarray(r, float) ** (1 - alpha) / _cd_const(alpha)


def ho_factor_prices(alphas: tuple, prices: tuple) -> dict:
    """Zero profits in both goods pin the wage and the rent (both goods produced): ln p_i = alpha_i ln w +
    (1 - alpha_i) ln r - ln k_i, a linear system in (ln w, ln r).  Goods 1 and 2 have labour shares alphas."""
    a1, a2 = alphas
    M = np.array([[a1, 1 - a1], [a2, 1 - a2]])
    rhs = np.log(prices) + np.log([_cd_const(a1), _cd_const(a2)])
    lw, lr = np.linalg.solve(M, rhs)
    return {"w": float(np.exp(lw)), "r": float(np.exp(lr))}


def ho_inputs(alphas: tuple, w: float, r: float) -> np.ndarray:
    """Unit input requirements [[aL1, aL2], [aK1, aK2]] at factor prices (w, r) (Shephard's lemma)."""
    out = np.zeros((2, 2))
    for i, a in enumerate(alphas):
        c = unit_cost(a, w, r)
        out[0, i], out[1, i] = a * c / w, (1 - a) * c / r
    return out


def ho_outputs(alphas: tuple, prices: tuple, L: float, K: float) -> dict:
    """Outputs with both goods produced: the factor markets clear, aL Q = L, aK Q = K.  Outside the cone of
    diversification one output is negative and the country specializes (reported as ``diversified``: False)."""
    fp = ho_factor_prices(alphas, prices)
    A = ho_inputs(alphas, fp["w"], fp["r"])
    Q = np.linalg.solve(A, [L, K])
    return {**fp, "Q": Q, "A": A, "diversified": bool(np.all(Q >= 0)), "kL": A[1] / A[0]}


def ho_autarky(alphas: tuple, L: float, K: float, beta: float = 0.5) -> dict:
    """Autarky in the 2x2x2 economy with Cobb-Douglas spending share ``beta`` on good 1: the relative price of good 2
    (good 1 the numeraire) at which the country's own outputs match its demand."""
    def gap(lp):
        o = ho_outputs(alphas, (1.0, np.exp(lp)), L, K)
        Q = o["Q"]
        return np.log(max(Q[1], 1e-300) * np.exp(lp) / max(Q[0], 1e-300)) - np.log((1 - beta) / beta)

    lp = brentq(gap, -6, 6)
    return {"p": float(np.exp(lp)), **ho_outputs(alphas, (1.0, np.exp(lp)), L, K)}


def ho_world(alphas: tuple, endow: dict, beta: float = 0.5) -> dict:
    """Free trade between countries with endowments ``endow`` = {name: (L, K)} and the same technologies: one world
    price at which world outputs match world demand.  Factor prices are equalized while both countries are
    diversified."""
    def world(lp):
        Q = sum(ho_outputs(alphas, (1.0, np.exp(lp)), L, K)["Q"] for L, K in endow.values())
        return Q

    def gap(lp):
        Q = world(lp)
        return np.log(max(Q[1], 1e-300) * np.exp(lp) / max(Q[0], 1e-300)) - np.log((1 - beta) / beta)

    lp = brentq(gap, -6, 6)
    p = float(np.exp(lp))
    out = {"p": p}
    for name, (L, K) in endow.items():
        o = ho_outputs(alphas, (1.0, p), L, K)
        income = o["Q"][0] + p * o["Q"][1]
        c = np.array([beta * income, (1 - beta) * income / p])
        out[name] = {**o, "C": c, "X": o["Q"] - c, "income": income}
    return out


def stolper_samuelson(alphas: tuple, prices: tuple, dp: float = 0.10, good: int = 0) -> dict:
    """Percent changes in the wage and the rent when the price of ``good`` rises by ``dp`` (the other fixed): the
    magnification effect, one factor's real return up more than any price, the other's down."""
    base = ho_factor_prices(alphas, prices)
    new_p = list(prices)
    new_p[good] *= 1 + dp
    new = ho_factor_prices(alphas, tuple(new_p))
    return {"dw": new["w"] / base["w"] - 1, "dr": new["r"] / base["r"] - 1, "dp": dp, "base": base, "new": new}


def rybczynski(alphas: tuple, prices: tuple, L: float, K: float, dK: float = 0.10) -> dict:
    """Percent changes in the two outputs when capital rises by ``dK`` at fixed prices."""
    a = ho_outputs(alphas, prices, L, K)["Q"]
    b = ho_outputs(alphas, prices, L, K * (1 + dK))["Q"]
    return {"dQ": b / a - 1, "dK": dK, "before": a, "after": b}


def unit_value_isoquant(alpha: float, price: float, w: float, r: float, n: int = 120) -> tuple:
    """The Lerner diagram: the (labour, capital) combinations that make one dollar's worth (1/price units) of a
    Cobb-Douglas good, centred on the cost-minimizing point at (w, r)."""
    c = unit_cost(alpha, w, r)
    q = 1.0 / price
    Lstar, Kstar = alpha * c / w * q, (1 - alpha) * c / r * q
    t = np.linspace(-2.2, 2.2, n)
    Ls = Lstar * np.exp(t * (1 - alpha))
    Ks = Kstar * np.exp(-t * alpha)
    return Ls, Ks, (Lstar, Kstar)


# --- specific factors ------------------------------------------------------------------------------------------------
def specific_factors(pM: float, pA: float, L: float = 100.0, K: float = 100.0, T: float = 100.0,
                     theta: float = 0.5) -> dict:
    """Labour moves between manufacturing (with capital K) and agriculture (with land T); both Cobb-Douglas with
    labour share ``theta``.  The wage equalizes the values of the marginal products; capital and land earn the rest."""
    def gap(LM):
        return pM * theta * (K / LM) ** (1 - theta) - pA * theta * (T / (L - LM)) ** (1 - theta)

    LM = brentq(gap, 1e-9 * L, L * (1 - 1e-9))
    LA = L - LM
    w = pM * theta * (K / LM) ** (1 - theta)
    QM, QA = K ** (1 - theta) * LM ** theta, T ** (1 - theta) * LA ** theta
    rK = pM * (1 - theta) * QM / K
    rT = pA * (1 - theta) * QA / T
    return {"LM": LM, "LA": LA, "w": w, "rK": rK, "rT": rT, "QM": QM, "QA": QA, "income": pM * QM + pA * QA}


def specific_change(pM: float, pA: float, dpA: float = 0.10, **kw) -> dict:
    """Percent changes in the wage and the two rents when the price of food rises by ``dpA``."""
    a = specific_factors(pM, pA, **kw)
    b = specific_factors(pM, pA * (1 + dpA), **kw)
    return {"dw": b["w"] / a["w"] - 1, "drK": b["rK"] / a["rK"] - 1, "drT": b["rT"] / a["rT"] - 1, "dpA": dpA,
            "dLM": b["LM"] - a["LM"], "before": a, "after": b}


def vmpl_curves(pM: float, pA: float, L: float = 100.0, K: float = 100.0, T: float = 100.0, theta: float = 0.5,
                n: int = 120) -> dict:
    """The specific-factors diagram: the value of labour's marginal product in manufacturing against labour used there
    (from the left), and in agriculture against labour used there (from the right)."""
    LM = np.linspace(L * 0.04, L * 0.96, n)
    return {"LM": LM, "vM": pM * theta * (K / LM) ** (1 - theta), "vA": pA * theta * (T / (L - LM)) ** (1 - theta)}


# --- tariffs in partial equilibrium ----------------------------------------------------------------------------------
def tariff_small(a: float, b: float, c: float, d: float, pw: float, t: float) -> dict:
    """A small country: demand D = a - b p, supply S = c + d p, world price ``pw``, specific tariff ``t``.  Returns
    quantities and the areas: consumer loss, producer gain, revenue, and the two deadweight triangles."""
    p = pw + t
    D0, S0, D1, S1 = a - b * pw, c + d * pw, a - b * p, c + d * p
    M0, M1 = D0 - S0, D1 - S1
    cs_loss = t * (D1 + D0) / 2
    ps_gain = t * (S0 + S1) / 2
    revenue = t * M1
    prod_dwl = t * (S1 - S0) / 2
    cons_dwl = t * (D0 - D1) / 2
    return {"p": p, "D0": D0, "S0": S0, "D1": D1, "S1": S1, "M0": M0, "M1": M1, "cs_loss": cs_loss,
            "ps_gain": ps_gain, "revenue": revenue, "dwl_production": prod_dwl, "dwl_consumption": cons_dwl,
            "net": ps_gain + revenue - cs_loss}


def quota_equivalent(a: float, b: float, c: float, d: float, pw: float, quota: float) -> dict:
    """An import quota ``quota``: the home price at which imports equal the quota, and the quota rent (the revenue a
    tariff would have raised, now kept by whoever holds the licences)."""
    p = (a - c - quota) / (b + d)
    t = max(p - pw, 0.0)
    return {"p": p, "tariff_equivalent": t, "rent": t * quota}


def tariff_large(a: float, b: float, c: float, d: float, e: float, f: float, t: float) -> dict:
    """A large country: home import demand M = (a - c) - (b + d) p; foreign export supply X* = e + f p*.  A specific
    tariff drives p = p* + t.  Home welfare change against free trade: consumer and producer surplus, revenue (part of
    it paid by foreigners through a lower p*)."""
    def eq(tt):
        ps = ((a - c) - (b + d) * tt - e) / (b + d + f)
        return ps, ps + tt

    pf0, _ = eq(0.0)
    ps, p = eq(t)
    D0, S0 = a - b * pf0, c + d * pf0
    D1, S1 = a - b * p, c + d * p
    dcs = -(p - pf0) * (D0 + D1) / 2
    dps = (p - pf0) * (S0 + S1) / 2
    M1 = D1 - S1
    rev = t * M1
    return {"p_world": ps, "p_home": p, "p_free": pf0, "M": M1, "dcs": dcs, "dps": dps, "revenue": rev,
            "tot_gain": (pf0 - ps) * M1, "welfare": dcs + dps + rev}


def optimal_tariff(a, b, c, d, e, f) -> dict:
    """The tariff that maximizes the large country's welfare; with linear curves, compare 1/(elasticity of foreign
    export supply) evaluated at the optimum (as an ad valorem rate)."""
    r = minimize_scalar(lambda t: -tariff_large(a, b, c, d, e, f, t)["welfare"], bounds=(0.0, 20.0), method="bounded",
                        options={"xatol": 1e-10})
    t = float(r.x)
    o = tariff_large(a, b, c, d, e, f, t)
    X = e + f * o["p_world"]
    elas = f * o["p_world"] / X
    return {"t": t, "ad_valorem": t / o["p_world"], "inverse_elasticity": 1 / elas, **o}


# --- protection for sale ----------------------------------------------------------------------------------------------
def protection_for_sale(z, e, organized, a: float, alpha_L: float) -> np.ndarray:
    """Grossman and Helpman (1994): the equilibrium ad valorem tariff in each industry,
    t/(1 + t) = (I - alpha_L)/(a + alpha_L) * z/e, with I = 1 for an organized industry, z = output/imports, e the
    import demand elasticity, a the weight on welfare relative to contributions, alpha_L the organized share of the
    population.  Unorganized industries get import subsidies (negative t)."""
    z, e, I = np.asarray(z, float), np.asarray(e, float), np.asarray(organized, float)
    x = (I - alpha_L) / (a + alpha_L) * z / e
    return x / (1 - x)


# --- a tariff war -----------------------------------------------------------------------------------------------------
def _market(A: float, bH: float, bF: float, t: float) -> dict:
    """One good, imported by H from F: demand A - p in both, supply bH p at home and bF p abroad (bF > bH).  A tariff
    at or above the prohibitive level shuts trade, and each side is at its autarky price."""
    ps = (2 * A - (1 + bH) * t) / (2 + bH + bF)
    p = ps + t
    imp = A - (1 + bH) * p
    if imp <= 0:
        p, ps, imp = A / (1 + bH), A / (1 + bF), 0.0
    return {"p": p, "ps": ps, "M": imp,
            "W_imp": (A - p) ** 2 / 2 + bH * p ** 2 / 2 + t * imp,
            "W_exp": (A - ps) ** 2 / 2 + bF * ps ** 2 / 2}


def prohibitive(A: float, bH: float, bF: float) -> float:
    """The tariff that shuts the market: the gap between the two autarky prices."""
    return A / (1 + bH) - A / (1 + bF)


def war_welfare(tH: float, tF: float, A: float = 10.0, b_lo: float = 0.5, b_hi: float = 2.0) -> tuple:
    """Two mirror-image countries: H imports good 1 from F, F imports good 2 from H.  Each country's welfare sums its
    surplus as importer of one good (where its own tariff applies) and as exporter of the other (where the other's
    applies)."""
    m1, m2 = _market(A, b_lo, b_hi, tH), _market(A, b_lo, b_hi, tF)
    return m1["W_imp"] + m2["W_exp"], m2["W_imp"] + m1["W_exp"]


def tariff_war(A: float = 10.0, b_lo: float = 0.5, b_hi: float = 2.0) -> dict:
    """Best responses, the Nash tariff, and the payoff matrix of free trade against the Nash tariff: a prisoner's
    dilemma, each better off taxing whatever the other does, both worse off when both do."""
    def best(tF):
        r = minimize_scalar(lambda t: -war_welfare(t, tF, A, b_lo, b_hi)[0], bounds=(0, prohibitive(A, b_lo, b_hi)),
                            method="bounded",
                            options={"xatol": 1e-10})
        return float(r.x)

    t = 0.0
    for _ in range(200):
        t_new = best(t)
        if abs(t_new - t) < 1e-10:
            break
        t = t_new
    tn = t
    W0 = war_welfare(0, 0, A, b_lo, b_hi)[0]
    pay = {}
    for i, th in (("free", 0.0), ("tariff", tn)):
        for j, tf in (("free", 0.0), ("tariff", tn)):
            wh, wf = war_welfare(th, tf, A, b_lo, b_hi)
            pay[(i, j)] = (wh - W0, wf - W0)
    grid = np.linspace(0, 2 * tn, 41)
    return {"nash": tn, "free_welfare": W0, "payoffs": pay, "grid": grid.tolist(),
            "best_response": [best(x) for x in grid]}


# --- tests and measures -----------------------------------------------------------------------------------------------
def inner_product(pa, T) -> float:
    """Bernhofen and Brown's test: autarky prices times net exports should be negative (a country exports what was
    cheap at home before trade)."""
    return float(np.dot(np.asarray(pa, float), np.asarray(T, float)))


def leontief_ratio(exports: dict, imports: dict) -> dict:
    """Capital per worker embodied in a million dollars of exports and of import replacements; HO predicts the
    capital-abundant United States exports the more capital-intensive bundle (ratio below one)."""
    kx, km = exports["capital"] / exports["labour"], imports["capital"] / imports["labour"]
    return {"exports": kx, "imports": km, "ratio": km / kx}


def factor_content(D: dict) -> dict:
    """Trefler's comparison for Heckscher-Ohlin-Vanek: measured factor content of net exports F_fc against the
    prediction V_fc - s_c V_fw, with s_c the country's share of world spending (GDP less the trade balance).  Each
    factor is scaled by sigma_f sqrt(s_c), with sigma_f from the factor's residuals, as in Trefler.  Returns the sign
    test, the variance ratio ('missing trade'), the rank correlation, and the points."""
    from scipy.stats import spearmanr  # noqa: PLC0415

    cs = sorted(set(D["country"]))
    fs = sorted(set(D["factor"]))
    F = {(c, f): x for c, f, x in zip(D["country"], D["factor"], D["at"])}
    V = {(c, f): x for c, f, x in zip(D["country"], D["factor"], D["v"])}
    Y = {c: y for c, y in zip(D["country"], D["y"])}
    B = {c: x for c, x in zip(D["country"], D["b"])}
    s = {c: (Y[c] - B[c]) / (sum(Y.values()) - sum(B.values())) for c in cs}
    meas, pred, fac, cty = [], [], [], []
    by = {}
    for f in fs:
        Vw = sum(V[c, f] for c in cs)
        pr = np.array([V[c, f] - s[c] * Vw for c in cs])
        me = np.array([F[c, f] for c in cs])
        sc = np.sqrt([s[c] for c in cs])
        sig = np.sqrt(np.mean(((me - pr) / sc) ** 2)) or 1.0       # a perfect fit: no scaling needed
        meas += list(me / (sig * sc))
        pred += list(pr / (sig * sc))
        fac += [f] * len(cs)
        cty += cs
        by[f] = {"sign": float(np.mean(np.sign(me) == np.sign(pr))), "variance_ratio": float(np.var(me) / np.var(pr))}
    meas, pred = np.array(meas), np.array(pred)
    return {"sign_test": float(np.mean(np.sign(meas) == np.sign(pred))),
            "variance_ratio": float(np.var(meas) / np.var(pred)),
            "rank": float(spearmanr(meas, pred).correlation), "measured": meas, "predicted": pred,
            "factor": fac, "country": cty, "by_factor": by, "n_countries": len(cs), "n_factors": len(fs)}


def acr_gains(domestic_share: float, eps: float) -> float:
    """Arkolakis, Costinot and Rodriguez-Clare (2012): the loss from moving to autarky, as a share of real income,
    1 - lambda^(1/eps) with eps the (positive) trade elasticity."""
    return float(1 - domestic_share ** (1 / abs(eps)))


def grubel_lloyd(x, m) -> np.ndarray:
    """The Grubel-Lloyd index of two-way trade, 1 - |X - M|/(X + M): 1 when exports equal imports, 0 for one-way
    trade."""
    x, m = np.asarray(x, float), np.asarray(m, float)
    return 1 - np.abs(x - m) / (x + m)
