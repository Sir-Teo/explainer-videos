"""Agora's political economy (Part 47): groups that lobby, contests for rents, voters, politicians as agents, elites
who extend the franchise, audits, cycles timed to elections, rain and conflict, persuasion, and the regression
discontinuity of close elections.

* **Collective action** (:func:`olson_effort`, :func:`group_contest`): members of a group each choose how much to
  spend lobbying for a policy worth B to the group, shared equally; each weighs only their own share, so the group's
  total effort falls with its size; a small group with a large stake per head beats a large group with a larger
  total stake.
* **Rent seeking** (:func:`tullock`, :func:`tokens_game`): Tullock's contest, where n players spend to win a prize
  and the total spent approaches the prize; the Play-it game, where tokens can build a public good or lobby for a
  share of a fixed prize.
* **Voters** (:func:`probabilistic_voting`): two parties compete for groups with different shares of swing voters;
  the policy they converge on maximizes a weighted welfare in which swing and organized groups count for more.
* **Politicians as agents** (:func:`agency`, :func:`mayors`): voters re-elect an incumbent who takes no more than a
  threshold in rents; the lowest threshold that keeps office worth more than one big grab; a lame duck grabs all;
  mayors who can and cannot run again.
* **Why bad institutions persist** (:func:`franchise`): Acemoglu and Robinson's elite, who face a revolutionary
  threat now and then; promises of redistribution are credible only if threats recur often; otherwise the elite
  extends the vote, which commits it.
* **Corruption measured** (:func:`road_projects`): road projects with money missing; audits from above and meetings
  from below, randomized; what villagers perceive.
* **Cycles and delegation** (:func:`election_cycle`): an incumbent facing myopic voters lowers unemployment before
  each election and pays with inflation after it; a delegated central bank does not.
* **Conflict** (:func:`rain_conflict`): rainfall shocks move growth; growth moves the risk of civil conflict; growth is
  measured with error, which biases least squares toward zero; rainfall as the instrument.
* **Persuasion** (:func:`persuasion_rate`): DellaVigna and Kaplan's rate of persuasion.
* **Close elections** (:func:`rd_local_linear`, :func:`rd_bins`): a local linear regression discontinuity with a
  triangular kernel and robust standard errors, and binned means for plotting.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


# ---------------------------------------------------------------------------------------------------------------
# collective action and rent seeking


def olson_effort(B: float, n, K: float = 1.0):
    """Total lobbying effort of a group of n members against fixed resistance K, when the policy worth B to the
    group (B/n to each) is won with probability E/(E + K): each member's first-order condition (B/n) K/(E+K)^2 = 1
    gives E = sqrt(B K / n) - K, or nothing if that is negative."""
    n = np.asarray(n, float)
    return np.maximum(np.sqrt(B * K / n) - K, 0.0)


def group_contest(n_small: float, B_small: float, n_large: float, B_large: float) -> dict:
    """Two groups contest a policy: the small group gains B_small if it passes, the large group loses B_large.
    Each member spends to sway the outcome, weighing only their own share (free riding), so each group acts as if
    its stake were its stake per head, v = B/n.  The Tullock contest between the groups gives efforts
    E_s = v_s^2 v_l / (v_s + v_l)^2, E_l = v_s v_l^2 / (v_s + v_l)^2 and the probability the policy passes,
    v_s / (v_s + v_l)."""
    vs, vl = B_small / n_small, B_large / n_large
    p = vs / (vs + vl)
    Es = vs ** 2 * vl / (vs + vl) ** 2
    El = vs * vl ** 2 / (vs + vl) ** 2
    return {"v_small": vs, "v_large": vl, "p_pass": float(p), "E_small": float(Es), "E_large": float(El),
            "expected_loss": float(p * B_large - p * B_small)}


def tullock(prize: float, n: int, r: float = 1.0) -> dict:
    """Tullock's contest: n players spend x_i to win a prize with probability x_i^r / sum x_j^r.  The symmetric
    equilibrium spends x* = prize r (n - 1) / n^2 each (for r <= n/(n - 1)), so the total is prize r (n - 1)/n."""
    x = prize * r * (n - 1) / n ** 2
    return {"each": float(x), "total": float(n * x), "dissipated": float(n * x / prize)}


def tokens_game(N: int = 10, endowment: float = 100.0, mpcr: float = 0.3, prize: float = 400.0,
                build=None, lobby=None) -> dict:
    """The Play-it game: each of N players splits ``endowment`` tokens between keeping them, building (each token
    returns ``mpcr`` to every player) and lobbying (a prize of ``prize`` tokens is shared in proportion to
    lobbying).  Returns each player's payoff for given choices, and the Nash and the best outcomes."""
    def payoff(b, lob):
        b, lob = np.asarray(b, float), np.asarray(lob, float)
        share = lob / lob.sum() if lob.sum() > 0 else np.full(N, 1.0 / N)
        return endowment - b - lob + mpcr * b.sum() + prize * share
    nash_each = tullock(prize, N)["each"]
    nash = payoff(np.zeros(N), np.full(N, nash_each))
    best = payoff(np.full(N, endowment), np.zeros(N))
    out = {"nash_lobby": nash_each, "nash_payoff": float(nash[0]), "best_payoff": float(best[0]),
           "nash_total_lobbying": float(N * nash_each)}
    if build is not None:
        out["payoffs"] = payoff(build, lobby).tolist()
    return out


# ---------------------------------------------------------------------------------------------------------------
# voters


def probabilistic_voting(alpha, phi, income, organized=None, h: float = 0.0) -> dict:
    """Two parties choose consumption for each group g (population share alpha_g, income income_g) by lump-sum
    transfers that must balance; voters in group g vote for the party that offers them more, plus an ideological
    taste whose density at indifference is phi_g (the share of swing voters).  An organized group gives money
    that buys votes, adding h to its weight.  With log utility both parties choose c_g proportional to the weight
    phi_g (+ h if organized): the policy that maximizes sum alpha_g w_g log c_g subject to the budget."""
    alpha, phi, income = (np.asarray(v, float) for v in (alpha, phi, income))
    w = phi.copy()
    if organized is not None:
        w = w + h * np.asarray(organized, float)
    total = float(np.sum(alpha * income))
    c = w * total / float(np.sum(alpha * w))
    return {"c": c.tolist(), "transfer": (c - income).tolist(), "weights": w.tolist()}


def rd_local_linear(x, y, h: float, kernel: str = "triangular", cutoff: float = 0.0) -> dict:
    """A local linear regression discontinuity at ``cutoff``: weighted least squares on each side within bandwidth
    h (triangular or uniform kernel), the jump in the intercepts, and its heteroskedasticity-robust standard error
    (the conventional estimate of rdrobust)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok] - cutoff, y[ok]
    res = {}
    for side, s in (("right", (x >= 0) & (x < h)), ("left", (x < 0) & (x > -h))):
        w = (1 - np.abs(x[s]) / h) if kernel == "triangular" else np.ones(int(s.sum()))
        X = np.column_stack([np.ones(int(s.sum())), x[s]])
        XtW = X.T * w
        M = np.linalg.inv(XtW @ X)
        b = M @ (XtW @ y[s])
        e = y[s] - X @ b
        V = M @ ((X.T * (w ** 2 * e ** 2)) @ X) @ M
        res[side] = (b, V, int(s.sum()))
    jump = float(res["right"][0][0] - res["left"][0][0])
    se = float(np.sqrt(res["right"][1][0, 0] + res["left"][1][0, 0]))
    return {"jump": jump, "se": se, "h": h, "n_left": res["left"][2], "n_right": res["right"][2],
            "fit_left": res["left"][0].tolist(), "fit_right": res["right"][0].tolist()}


def rd_bins(x, y, lo: float, hi: float, width: float) -> dict:
    """Means of y in bins of x of the given width (for a discontinuity plot)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    edges = np.arange(lo, hi + 1e-9, width)
    mids, means, ns = [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = (x >= a) & (x < b)
        if s.sum() >= 3:
            mids.append(float((a + b) / 2))
            means.append(float(y[s].mean()))
            ns.append(int(s.sum()))
    return {"mids": mids, "means": means, "n": ns}


# ---------------------------------------------------------------------------------------------------------------
# politicians as agents


def agency(W: float, R: float, delta: float) -> dict:
    """Barro and Ferejohn: an incumbent earns W a term in office and can take up to R in rents.  Voters re-elect
    if rents are at most r*.  Complying forever is worth (W + r*)/(1 - delta); grabbing everything is worth W + R
    once.  The voters' best threshold is the lowest that keeps compliance worth it:
    r* = max(0, (1 - delta)(W + R) - W).  A lame duck, who cannot run again, takes R."""
    r_star = max(0.0, (1 - delta) * (W + R) - W)
    return {"r_star": float(r_star), "lame_duck": float(R), "share_taken": float(r_star / R) if R else 0.0}


def mayors(n: int = 2000, R: float = 1.0, W_mean: float = 0.1, W_sd: float = 0.3, delta: float = 0.43,
           honesty_lo: float = 0.3, scale: float = 0.06, noise: float = 0.02, seed: int = 0) -> dict:
    """Municipalities whose mayors differ in what office is worth to them (W, normal, at least 0) and in honesty
    (each would take at most a share h of the rents R, h uniform on [honesty_lo, 1]).  First-term mayors, who can
    run again, take the smaller of h R and the agency model's threshold r*; second-term mayors, barred from running,
    take h R.  Audits measure the share of resources misappropriated, ``scale`` times the share of R taken, with
    noise.  Returns the average shares and how much less first-term mayors take."""
    rng = np.random.default_rng(seed)
    W = np.maximum(rng.normal(W_mean, W_sd, n), 0.0)
    h = rng.uniform(honesty_lo, 1.0, n)
    first = rng.random(n) < 0.5
    r_star = np.maximum(0.0, (1 - delta) * (W + R) - W)
    taken = np.where(first, np.minimum(h * R, r_star), h * R)
    measured = np.clip(scale * taken / R + noise * rng.standard_normal(n), 0, None)
    a, b = float(measured[first].mean()), float(measured[~first].mean())
    return {"first_term": a, "lame_duck": b, "fewer": float(1 - a / b), "share_first": float(first.mean())}


# ---------------------------------------------------------------------------------------------------------------
# why bad institutions persist


def franchise(q: float, mu: float, elite: float = 0.1, elite_income: float = 0.7, beta: float = 0.95) -> dict:
    """Acemoglu and Robinson's elite and poor.  Income per head is 1; the elite (share ``elite``) earn
    ``elite_income`` of it.  A tax tau, rebated lump sum, costs tau^2/2 of income, so the poor's income is
    y_p + tau (1 - y_p) - tau^2 / 2 and their ideal tax is tau* = 1 - y_p.  In each period a revolutionary
    threat arises with probability q; a revolution gives the poor (1 - mu)/(1 - elite) per head forever and the elite
    nothing.  Without the vote the elite can redistribute only while a threat lasts (they cannot commit to later
    periods); with the vote the poor set tau* forever.  Returns the poor's values of revolution, of promises, and of
    democracy, and what the elite does when a threat arises: promise, democratize, or face a revolution."""
    y_p = (1 - elite_income) / (1 - elite)
    tau = 1 - y_p

    def inc(t):
        return y_p + t * (1 - y_p) - t ** 2 / 2
    # values under non-democracy: V_T (threat now, promise tau*), V_0 (no threat, no tax)
    a = np.array([[1 - beta * q, -beta * (1 - q)], [-beta * q, 1 - beta * (1 - q)]])
    rhs = np.array([inc(tau), inc(0.0)])
    VT, V0 = np.linalg.solve(a, rhs)
    VD = inc(tau) / (1 - beta)
    VR = (1 - mu) / (1 - elite) / (1 - beta)
    if VT >= VR:
        outcome = "promise"
    elif VD >= VR:
        outcome = "democratize"
    else:
        outcome = "revolution"
    return {"V_revolution": float(VR), "V_promise": float(VT), "V_democracy": float(VD), "outcome": outcome,
            "tau": float(tau), "y_poor": float(y_p)}


def franchise_map(qs, mus, **kw) -> dict:
    """The elite's choice over a grid of threat frequencies q and revolution costs mu (0 promise, 1 democratize,
    2 revolution)."""
    code = {"promise": 0, "democratize": 1, "revolution": 2}
    grid = np.array([[code[franchise(q, m, **kw)["outcome"]] for q in qs] for m in mus])
    return {"q": list(map(float, qs)), "mu": list(map(float, mus)), "grid": grid.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# corruption measured


def road_projects(n: int = 600, base: float = 0.28, sd: float = 0.18, audit_effect: float = -0.08,
                  meeting_effect: float = -0.01, perception_slope: float = 0.08, seed: int = 0) -> dict:
    """Olken's design on the Island: n village road projects, a share of each project's spending missing (the gap
    between reported costs and an engineer's estimate, measured with error).  Projects are randomized to an audit
    (probability one instead of 0.04) and, independently, to village meetings.  Returns the mean missing share by
    arm, the estimated effects, and how weakly villagers' perceptions track the truth."""
    rng = np.random.default_rng(seed)
    audit = rng.random(n) < 0.5
    meet = rng.random(n) < 0.5
    true = np.clip(base + sd * rng.standard_normal(n) + audit_effect * audit + meeting_effect * meet, -0.2, 0.9)
    measured = true + 0.06 * rng.standard_normal(n)
    X = np.column_stack([np.ones(n), audit, meet])
    b, *_ = np.linalg.lstsq(X, measured, rcond=None)
    e = measured - X @ b
    V = np.linalg.inv(X.T @ X) @ ((X.T * e ** 2) @ X) @ np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(V))
    perceived = 0.4 + perception_slope * true + 0.2 * rng.standard_normal(n)
    return {"control": float(measured[~audit & ~meet].mean()), "audit": float(b[1]), "audit_se": float(se[1]),
            "meetings": float(b[2]), "meetings_se": float(se[2]), "mean": float(measured.mean()),
            "perception_corr": float(np.corrcoef(perceived, true)[0, 1]),
            "true": np.round(true[:300], 4).tolist(), "perceived": np.round(perceived[:300], 4).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# cycles and delegation


def election_cycle(years: int = 16, term: int = 4, a: float = 0.5, u_star: float = 5.0, myopia: float = 0.5,
                   b: float = 0.4) -> dict:
    """Nordhaus's political business cycle.  Inflation follows pi_t = pi_{t-1} + a (u* - u_t): pushing
    unemployment below its natural rate raises inflation, and it stays raised.  Voters judge the incumbent at each
    election by the term's record, weighting year k of the term by myopia^(years left before the election), and
    dislike unemployment above the natural rate in proportion and inflation in proportion to its square (times
    b/2).  The incumbent chooses the path of unemployment to do best at every election, with a small quadratic cost
    of moving it.  Returns the paths of unemployment and inflation, the election years, and the path under
    delegation to a central bank that keeps unemployment at its natural rate."""
    u = np.full(years, u_star)

    def loss(dev):
        uu = u_star + dev
        pi = np.zeros(years)
        prev = 0.0
        for t in range(years):
            prev = prev + a * (u_star - uu[t])
            pi[t] = prev
        L = 0.0
        for start in range(0, years, term):
            for k in range(term):
                t = start + k
                w = myopia ** (term - 1 - k)
                L += w * ((uu[t] - u_star) + b * pi[t] ** 2 / 2)
        return L + 0.5 * np.sum(dev ** 2)
    res = minimize(loss, np.zeros(years), method="BFGS")
    dev = res.x
    uu = u_star + dev
    pi = np.cumsum(a * (u_star - uu))
    return {"u": uu.tolist(), "pi": pi.tolist(), "u_delegated": u.tolist(), "pi_delegated": [0.0] * years,
            "elections": list(range(term - 1, years, term))}


# ---------------------------------------------------------------------------------------------------------------
# conflict, persuasion


def rain_conflict(countries: int = 41, years: int = 19, first: float = 1.0, effect: float = -2.0,
                  feedback: float = -0.01, error_sd: float = 0.04, base: float = 0.25, seed: int = 0) -> dict:
    """Miguel, Satyanath and Sergenti's design on the Island.  Rainfall growth (normal) raises economic growth by
    ``first`` per unit; the probability of conflict changes by ``effect`` per unit of growth (so a five-point fall in
    growth raises it by 10 points); conflict lowers growth a little (``feedback``); and growth is measured with
    error (``error_sd``), as national accounts in poor countries are.  The error biases least squares toward zero;
    rainfall, which is unrelated to both the error and conflict's own causes, recovers the effect.  Returns the first
    stage, the OLS and 2SLS estimates, and the 2SLS standard error."""
    rng = np.random.default_rng(seed)
    n = countries * years
    rain = rng.normal(0, 0.03, n)
    other = rng.normal(0, 0.03, n)
    growth0 = first * rain + other
    p0 = np.clip(base + effect * growth0, 0, 1)
    conflict = (rng.random(n) < p0).astype(float)
    growth = growth0 + feedback * conflict
    measured = growth + error_sd * rng.standard_normal(n)
    X = np.column_stack([np.ones(n), rain])
    fs, *_ = np.linalg.lstsq(X, measured, rcond=None)
    ols = float(np.polyfit(measured, conflict, 1)[0])
    ghat = X @ fs
    iv = float(np.cov(ghat, conflict)[0, 1] / np.cov(ghat, measured)[0, 1])
    e = conflict - (conflict.mean() - iv * measured.mean()) - iv * measured
    zc = ghat - ghat.mean()
    se_iv = float(np.sqrt(np.sum(zc ** 2 * e ** 2)) / np.sum(zc * (measured - measured.mean())))
    F = float(fs[1] ** 2 / (np.var(measured - X @ fs, ddof=2) / np.sum((rain - rain.mean()) ** 2)))
    return {"first_stage": float(fs[1]), "F": F, "ols": ols, "iv": iv, "iv_se": se_iv, "truth": effect,
            "conflict_rate": float(conflict.mean()), "n": n}


def persuasion_rate(y_treated: float, y_control: float, e_treated: float, e_control: float) -> float:
    """DellaVigna and Kaplan's persuasion rate: the share of those who received the message, and would not
    otherwise have acted, who were moved: ((y_T - y_C)/(e_T - e_C)) / (1 - y_0), with y_0 = y_C."""
    return float((y_treated - y_control) / (e_treated - e_control) / (1 - y_control))
