"""Agora's geoeconomics and industrial policy (Part 66): tariffs set by formula, tariffs with their revenue in the
quantitative trade model, trade wars as repeated games, the power that dependence gives, resilience against
efficiency, learning by doing and the infant-industry tests, and subsidy races.

* **The reciprocal formula** (:func:`reciprocal_rate`): the United States' April 2025 rate for a partner, the
  bilateral deficit over imports divided by an import-demand elasticity times a pass-through, halved, with a floor.
* **Tariffs in general equilibrium** (:func:`tariff_hat`): exact hat algebra with tariff revenue rebated
  (after Dekle, Eaton and Kortum; Costinot and Rodriguez-Clare), on observed flows; uniform tariffs with and without
  retaliation, the optimal tariff, and who pays (:func:`tariff_scenarios`, :func:`two_bloc`).
* **Trade wars as games** (:func:`stage_payoffs`, :func:`repeated`): payoffs of a two-bloc tariff game from the model
  and a ten-round game against partners who retaliate in kind, never, or for ever.
* **Dependence as power** (:func:`cutoff_loss`): the welfare loss from losing a supplier with import share s, by the
  ACR formula 1 - (1 - s)^(1/theta), which bounds what a hegemon can demand (after Clayton, Maggiori and Schreger).
* **Resilience** (:func:`resilience`): how much to buy from a cheap supplier that can be cut off, privately and for
  society when a disruption costs more than the firm bears.
* **Infant industries** (:func:`infant_industry`): learning by doing behind a temporary tariff, with the Mill and
  Bastable tests.
* **Subsidy races** (:func:`brander_spencer`): two exporters in a third market, their governments' subsidies, the Nash
  subsidies and the prisoners' dilemma.

numpy only.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# the formula


def reciprocal_rate(us_imports: float, us_exports: float, eps: float = 4.0, phi: float = 0.25, halve: bool = True,
                    floor: float = 0.10) -> float:
    """The rate the United States set on 2 April 2025 for a partner: the tariff that would 'balance' bilateral trade,
    (imports - exports) / (eps phi imports), with eps = 4 and phi = 0.25 so that eps phi = 1; halved; at least the
    floor.  With phi near one (pass-through to import prices close to complete), the same formula gives a quarter of
    the rate."""
    raw = (us_imports - us_exports) / (eps * phi * us_imports)
    r = 0.5 * raw if halve else raw
    return float(max(floor, r))


# ---------------------------------------------------------------------------------------------------------------
# tariffs in the quantitative model


def tariff_hat(X, t_new, theta: float = 4.0, iters: int = 40000, tol: float = 1e-12, step: float = 0.3,
               zero_deficits: bool = False) -> dict:
    """Counterfactual equilibrium after tariffs t_new[n, i] (imposed by n on goods from i), starting from free trade
    with observed spending X[n, i] (domestic spending on the diagonal), in the Armington / Eaton-Kortum model with
    trade elasticity theta.  Tariff revenue is rebated to the importing country; each country's deficit is held fixed
    in units of world income.

    Given wage changes w: shares pi'[n, i] ~ pi[n, i] (w_i (1 + t_ni))^(-theta); spending E'_n = (w_n Y_n + D_n) /
    (1 - sum_i pi'_ni t_ni / (1 + t_ni)); sales w_i Y_i = sum_n pi'_ni E'_n / (1 + t_ni).  Welfare: real spending,
    E'_n / E_n over the price index P-hat_n = (sum_i pi_ni (w_i (1 + t_ni))^(-theta))^(-1/theta)."""
    X = np.asarray(X, float)
    T = np.asarray(t_new, float)
    E = X.sum(axis=1)
    Y = X.sum(axis=0)
    D = np.zeros_like(E) if zero_deficits else E - Y
    pi = X / E[:, None]
    tau = 1.0 + T
    w = np.ones(len(E))
    for _ in range(iters):
        num = pi * (w[None, :] * tau) ** (-theta)
        pin = num / num.sum(axis=1, keepdims=True)
        En = (w * Y + D) / (1 - (pin * T / tau).sum(axis=1))
        sales = (pin * En[:, None] / tau).sum(axis=0)
        exc = (sales - w * Y) / Y
        w_new = w * (1 + step * exc)
        w_new /= (w_new * Y).sum() / Y.sum()
        if np.max(np.abs(w_new - w)) < tol:
            w = w_new
            break
        w = w_new
    num = pi * (w[None, :] * tau) ** (-theta)
    pin = num / num.sum(axis=1, keepdims=True)
    En = (w * Y + D) / (1 - (pin * T / tau).sum(axis=1))
    Phat = num.sum(axis=1) ** (-1 / theta)
    welfare = (En / E) / Phat - 1
    revenue = (pin * En[:, None] * T / tau).sum(axis=1)
    imp_after = (pin * En[:, None] / tau).sum(axis=1) - np.diag(pin) * En      # at world prices
    return {"w": w, "pi": pi, "pi_new": pin, "E_new": En, "Phat": Phat, "welfare": welfare, "revenue": revenue,
            "imports_before": E - np.diag(X), "imports_after": imp_after}


def tariff_scenarios(X, us: int, t: float = 0.15, thetas=(2.0, 4.0, 8.0)) -> dict:
    """A uniform US tariff t on every partner, without and with retaliation in kind, for several trade elasticities:
    US welfare, the average partner's (weighted by GDP), the fall in US imports, and how much of the tariff partners
    absorb in their prices (their wages relative to the world's, against the tariff)."""
    X = np.asarray(X, float)
    N = len(X)
    E = X.sum(axis=1)
    rows = []
    for th in thetas:
        for retal in (False, True):
            T = np.zeros((N, N))
            T[us, :] = t
            T[us, us] = 0.0
            if retal:
                T[:, us] = t
                T[us, us] = 0.0
            R = tariff_hat(X, T, th)
            others = [k for k in range(N) if k != us]
            wp = float(np.average(R["welfare"][others], weights=E[others]))
            imp_fall = 1 - R["imports_after"][us] / R["imports_before"][us]
            wus = R["w"][us]
            absorbed = float(1 - np.average(R["w"][others], weights=E[others]) / wus)
            rows.append({"theta": th, "retaliation": retal, "us": float(R["welfare"][us]), "partners": wp,
                         "imports_fall": float(imp_fall), "absorbed": absorbed / t,
                         "revenue_share": float(R["revenue"][us] / R["E_new"][us])})
    return {"t": t, "rows": rows}


def two_bloc(X, us: int, theta: float = 4.0, grid=None) -> dict:
    """The United States against the rest of the world as one bloc: welfare for every pair of uniform tariffs on a
    grid, each side's best response, the Nash tariffs (where the best responses cross) and the optimal tariff
    without retaliation."""
    grid = np.round(np.linspace(0.0, 0.6, 25), 4) if grid is None else np.asarray(grid)
    X = np.asarray(X, float)
    N = len(X)
    others = [k for k in range(N) if k != us]
    E = X.sum(axis=1)
    W_us = np.zeros((len(grid), len(grid)))
    W_ro = np.zeros_like(W_us)
    for a, tu in enumerate(grid):
        for b, tr in enumerate(grid):
            T = np.zeros((N, N))
            T[us, others] = tu
            T[others, us] = tr
            R = tariff_hat(X, T, theta, iters=8000, tol=1e-10)
            W_us[a, b] = R["welfare"][us]
            W_ro[a, b] = np.average(R["welfare"][others], weights=E[others])
    br_us = grid[np.argmax(W_us, axis=0)]           # US best response to each rest-of-world tariff
    br_ro = grid[np.argmax(W_ro, axis=1)]           # rest of world's best response to each US tariff
    # Nash: iterate best responses from free trade
    a, b = 0, 0
    for _ in range(50):
        a_new = int(np.argmax(W_us[:, b]))
        b_new = int(np.argmax(W_ro[a_new, :]))
        if (a_new, b_new) == (a, b):
            break
        a, b = a_new, b_new
    opt = int(np.argmax(W_us[:, 0]))
    return {"grid": grid, "W_us": W_us, "W_ro": W_ro, "br_us": br_us, "br_ro": br_ro,
            "nash": (float(grid[a]), float(grid[b])), "nash_us": float(W_us[a, b]), "nash_ro": float(W_ro[a, b]),
            "optimal": float(grid[opt]), "optimal_us": float(W_us[opt, 0]), "optimal_ro": float(W_ro[opt, 0]),
            "theta": theta}


def purge_deficits(X, theta: float = 4.0) -> np.ndarray:
    """The flows of a world in which every country's trade is balanced, from the observed ones: the counterfactual
    with deficits set to zero and no tariffs (Dekle, Eaton and Kortum's first step).  Tariff wars are computed on this
    world, as is usual, so that a country's optimal tariff does not depend on a deficit held fixed by assumption."""
    R = tariff_hat(X, np.zeros_like(np.asarray(X, float)), theta, zero_deficits=True)
    return R["pi_new"] * R["E_new"][:, None]


# ---------------------------------------------------------------------------------------------------------------
# trade wars as repeated games


def stage_payoffs(B: dict, t: float) -> dict:
    """The stage game from a two-bloc table: each side either keeps free trade or imposes the tariff t (the grid
    value nearest t).  Payoffs are welfare changes in percent: (US, rest of the world)."""
    g = np.asarray(B["grid"])
    k = int(np.argmin(np.abs(g - t)))
    W_us, W_ro = np.asarray(B["W_us"]), np.asarray(B["W_ro"])
    pay = {("free", "free"): (0.0, 0.0),
           ("tariff", "free"): (100 * W_us[k, 0], 100 * W_ro[k, 0]),
           ("free", "tariff"): (100 * W_us[0, k], 100 * W_ro[0, k]),
           ("tariff", "tariff"): (100 * W_us[k, k], 100 * W_ro[k, k])}
    return {"t": float(g[k]), "pay": {f"{a}|{b}": v for (a, b), v in pay.items()}}


PARTNERS = ("tit for tat", "never retaliates", "retaliates for ever")
PLANS = ("free trade throughout", "a tariff, kept", "a tariff for two rounds, then free trade")


def repeated(stage: dict, rounds: int = 10, delta: float = 0.9) -> dict:
    """Ten rounds against three kinds of partner: tit for tat (copies your last move), never retaliates, and
    retaliates for ever once you impose a tariff.  Three plans: free trade throughout, a tariff kept for ever, and a
    tariff for two rounds then free trade.  The discounted sum of your payoffs (percent of income per round)."""
    pay = {tuple(k.split("|")): v for k, v in stage["pay"].items()}

    def mine(plan, r):
        if plan == PLANS[0]:
            return "free"
        if plan == PLANS[1]:
            return "tariff"
        return "tariff" if r < 2 else "free"

    out = {}
    for partner in PARTNERS:
        for plan in PLANS:
            total, last, angry, path = 0.0, "free", False, []
            for r in range(rounds):
                me = mine(plan, r)
                if partner == PARTNERS[0]:
                    them = last
                elif partner == PARTNERS[1]:
                    them = "free"
                else:
                    them = "tariff" if angry else "free"
                u = pay[(me, them)][0]
                total += delta ** r * u
                path.append((me, them, u))
                last = me
                if me == "tariff":
                    angry = True
            out[f"{partner}|{plan}"] = {"total": total, "path": path}
    best = {p: max(PLANS, key=lambda q: out[f"{p}|{q}"]["total"]) for p in PARTNERS}
    return {"results": out, "best": best, "delta": delta, "rounds": rounds}


# ---------------------------------------------------------------------------------------------------------------
# dependence as power


def cutoff_loss(share, theta: float = 4.0):
    """The welfare loss from losing every import from a supplier with expenditure share s, when the rest of the
    world can replace it at the same prices otherwise: by the ACR formula the domestic-and-other share rises from
    1 - s to 1, so welfare falls by 1 - (1 - s)^(1/theta).  This bounds the concession a supplier can extract by
    threatening a cutoff."""
    s = np.asarray(share, float)
    return 1 - (1 - s) ** (1 / theta)


# ---------------------------------------------------------------------------------------------------------------
# resilience


def resilience(cost_gap: float = 0.10, p: float = 0.05, loss: float = 4.0, spill: float = 1.0,
               grid=None) -> dict:
    """A firm buys a share x of an input from a cheap supplier (cheaper by cost_gap) that is cut off with probability
    p; a cutoff costs it loss x^2 / 2 (scrambling for replacements is convex in how much is missing), and costs the
    rest of the economy spill times that again (its customers, its workers).  Expected cost per unit of the input:
    (1 - x) cost_gap + p (1 + s) loss x^2 / 2 with s = 0 for the firm and spill for society.  The private and social
    optima, x* = min(1, cost_gap / (p (1 + s) loss)), and the expected cost of each."""
    grid = np.linspace(0, 1, 101) if grid is None else np.asarray(grid)

    def cost(x, s):
        return (1 - x) * cost_gap + p * (1 + s) * loss * x ** 2 / 2

    xp = min(1.0, cost_gap / (p * loss))
    xs = min(1.0, cost_gap / (p * (1 + spill) * loss))
    return {"grid": grid, "private": cost(grid, 0.0), "social": cost(grid, spill), "x_private": xp, "x_social": xs,
            "social_at_private": float(cost(xp, spill)), "social_at_social": float(cost(xs, spill)),
            "cost_gap": cost_gap, "p": p, "spill": spill}


# ---------------------------------------------------------------------------------------------------------------
# infant industries


def infant_industry(b: float, years: int = 40, p_world: float = 1.0, c0: float = 1.6, Q0: float = 1.0,
                    tariff: float = 0.6, protect: int = 10, demand: float = 1.0, r: float = 0.05) -> dict:
    """Learning by doing: the domestic industry's unit cost is c0 (Q / Q0)^(-b), with Q its cumulative output.  Behind
    a tariff (the home price rises to p_world (1 + tariff)) it supplies the home market of size ``demand`` while its
    cost is below the protected price; after ``protect`` years the tariff goes, and it survives only if its cost is
    below the world price, when it also exports as much again.  With demand fixed, the social value of a year is
    (p_world - c) times what it produces: negative while it learns (the consumers' extra payments above its margin),
    positive once it beats the world price.  Mill's test: it survives without protection.  Bastable's test: the
    discounted social value is positive."""
    Q, rows = Q0, []
    pv_cost = pv_gain = 0.0
    for t in range(years):
        c = c0 * (Q / Q0) ** (-b)
        protected = t < protect
        price = p_world * (1 + tariff) if protected else p_world
        q = (demand if c <= price else 0.0) if protected else (2 * demand if c <= p_world else 0.0)
        v = (p_world - c) * q
        if v < 0:
            pv_cost -= v / (1 + r) ** t
        else:
            pv_gain += v / (1 + r) ** t
        rows.append({"t": t, "cost": float(c), "price": float(price), "q": float(q), "value": float(v)})
        Q += q
    c_end = rows[min(protect, years - 1)]["cost"]
    return {"b": b, "rows": rows, "mill": bool(c_end <= p_world), "bastable": bool(pv_gain > pv_cost),
            "pv_cost": float(pv_cost), "pv_gain": float(pv_gain), "cost_after": float(c_end), "protect": protect,
            "p_world": p_world, "tariff": tariff}


# ---------------------------------------------------------------------------------------------------------------
# subsidy races


def brander_spencer(a: float = 10.0, c: float = 1.0) -> dict:
    """Two exporters, one from each country, sell only to a third market with inverse demand p = a - q1 - q2 and
    unit cost c.  A subsidy s_i per unit lowers firm i's cost.  Cournot quantities q_i = (a - c + 2 s_i - s_j) / 3;
    country i's welfare is firm i's profit minus the subsidy bill.  One government alone: s* = (a - c)/4.  Both
    (Nash): s = (a - c)/5 each.  Returns the four outcomes."""
    def outcome(s1, s2):
        q1 = (a - c + 2 * s1 - s2) / 3
        q2 = (a - c + 2 * s2 - s1) / 3
        p = a - q1 - q2
        w1 = (p - c + s1) * q1 - s1 * q1
        w2 = (p - c + s2) * q2 - s2 * q2
        cs = (q1 + q2) ** 2 / 2
        return {"s1": s1, "s2": s2, "q1": q1, "q2": q2, "p": p, "w1": w1, "w2": w2, "consumers": cs}

    one = (a - c) / 4
    nash = (a - c) / 5
    return {"none": outcome(0, 0), "one": outcome(one, 0), "both": outcome(nash, nash), "s_one": one,
            "s_nash": nash, "a": a, "c": c}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "annotations")]
