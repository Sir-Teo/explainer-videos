"""Agora's economics of AI (Part 65): tasks done by people or machines, new tasks, general-purpose technologies that
need complementary investment, growth when research itself can be automated, and the arithmetic that turns task-level
gains into aggregate ones.

* **The task model** (:func:`tasks`, :func:`task_paths`): Acemoglu and Restrepo's economy on tasks [N - 1, N], those
  below I done by capital; output, the wage and the labour share in the short run (capital fixed) and the long run
  (capital supplied at a fixed rental); displacement, productivity and reinstatement by new tasks.
* **The J-curve** (:func:`j_curve`): a general-purpose technology that needs years of unmeasured intangible investment
  before it pays (after Brynjolfsson, Rock and Syverson).
* **Growth with automated research** (:func:`ideas_growth`): a semi-endogenous growth model whose research tasks can be
  done by capital as well as people (after Aghion, Jones and Jones): with complements, the tasks left to people set
  the pace; with every task automated, growth explodes.
* **From tasks to aggregates** (:func:`hulten_ai`): the share of GDP in tasks that AI makes cheaper, times the saving
  (Hulten's theorem, after Acemoglu 2024).
* **Keynes's two forecasts** (:func:`keynes`): living standards since 1930 and hours worked since 1950, from the Data
  Room.

numpy only.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# the task model


def tasks(I: float, N: float = 1.0, sigma: float = 0.8, K: float = 1.0, L: float = 1.0, AK: float = 1.0,
          AL: float = 1.0, R: float | None = None, g_new: float = 1.0) -> dict:
    """Output from tasks on [N - 1, N] combined with elasticity sigma; tasks below I are done by capital (productivity
    AK), the rest by labour (AL, times ``g_new`` in new tasks, those above 1: people's comparative advantage in new
    work).  Short run (R None): capital K fixed.  Long run: capital supplied at rental R, output set by the unit-cost
    condition with the final good as numeraire.  Labour spread optimally over its tasks acts like b = J =
    integral of g^(sigma - 1) over them.  Returns output, wage, rental and labour share."""
    a = I - (N - 1)                                  # capital's share of tasks
    b = max(0.0, min(N, 1.0) - I) + max(0.0, N - max(I, 1.0)) * g_new ** (sigma - 1)
    r = (sigma - 1) / sigma
    if R is None:
        Y = (a ** (1 / sigma) * (AK * K) ** r + b ** (1 / sigma) * (AL * L) ** r) ** (1 / r)
        w = Y ** (1 / sigma) * b ** (1 / sigma) * AL ** r * L ** (-1 / sigma)
        rk = Y ** (1 / sigma) * a ** (1 / sigma) * AK ** r * K ** (-1 / sigma) if a > 0 else np.nan
    else:
        x = a * (R / AK) ** (1 - sigma)
        y = (1 - x) / b                               # (w/AL)^(1 - sigma)
        w = AL * y ** (1 / (1 - sigma))
        # labour demand: L = b Y (w/AL)^(-sigma) / AL
        Y = L * AL / (b * (w / AL) ** (-sigma))
        rk = R
    return {"Y": float(Y), "w": float(w), "r": float(rk), "labour_share": float(w * L / Y)}


def task_paths(sigma: float = 0.8, K: float = 2.0, R: float = 0.8, steps: int = 41, g_new: float = 4.0) -> dict:
    """Automation (the frontier I rising from 0.2 to 0.8 with N = 1) in the short run (capital K fixed; a task is
    automated only while capital is cheaper than labour there, so the threshold used stops at cost parity) and the
    long run (capital supplied at rental R), then new tasks (N rising from 1 to 1.4 with I = 0.8, long run; people
    are ``g_new`` times as productive in the new tasks as in the old), and the
    decomposition of the short-run wage change up to parity into displacement and productivity:
    d ln w = (1/sigma) d ln(N - I) + (1/sigma) d ln Y."""
    Is = np.linspace(0.2, 0.8, steps)
    sr = [_short_run(i, K, 1.0, sigma, 1.0, 1.0) for i in Is]
    lr = [tasks(i, sigma=sigma, R=R) for i in Is]
    Ns = np.linspace(1.0, 1.4, steps)
    nt = [tasks(0.8, N=n, sigma=sigma, R=R, g_new=g_new) for n in Ns]
    parity = sr[-1][3]
    Y0, Y1 = sr[0][0], sr[-1][0]
    displacement = (1 / sigma) * np.log((1 - parity) / (1 - Is[0]))
    productivity = (1 / sigma) * np.log(Y1 / Y0)
    short = {"Y": [d[0] for d in sr], "w": [d[1] for d in sr], "labour_share": [d[1] / d[0] for d in sr],
             "I_used": [d[3] for d in sr]}
    return {"I": Is.tolist(), "N": Ns.tolist(), "sigma": sigma, "R": R, "K": K, "parity": float(parity),
            "short": short,
            "long": {k: [d[k] for d in lr] for k in ("Y", "w", "labour_share")},
            "new_tasks": {k: [d[k] for d in nt] for k in ("Y", "w", "labour_share")},
            "displacement": float(displacement), "productivity": float(productivity),
            "dlnw": float(np.log(sr[-1][1] / sr[0][1])), "w_peak": float(max(d[1] for d in sr)),
            "I_peak": float(Is[int(np.argmax([d[1] for d in sr]))])}


def so_so(sigma: float = 0.8, R_grid=None) -> dict:
    """So-so automation: automate the tasks from I = 0.5 to 0.6 in the long run, for capital that is barely cheaper
    than labour or much cheaper; the wage gain and the fall in the labour share."""
    R_grid = np.linspace(0.3, 0.95, 14) if R_grid is None else np.asarray(R_grid)
    base_w = None
    rows = []
    for R in R_grid:
        a = tasks(0.5, sigma=sigma, R=R)
        b = tasks(0.6, sigma=sigma, R=R)
        rows.append({"R": float(R), "wage_gain": b["w"] / a["w"] - 1,
                     "share_fall": a["labour_share"] - b["labour_share"], "w_over_R": a["w"] / R})
        base_w = base_w or a["w"]
    return {"rows": rows}


# ---------------------------------------------------------------------------------------------------------------
# the J-curve


def j_curve(years: int = 31, start: int = 3, invest: float = 0.05, build: int = 10, lag: int = 4,
            gamma: float = 0.5, delta: float = 0.1, kappa: float = 0.25) -> dict:
    """A general-purpose technology arrives in year ``start`` (after Brynjolfsson, Rock and Syverson).  Over
    ``build`` years firms build a stock H of intangible capital (reorganization, training, their own software) with a
    hump-shaped flow, peaking at ``invest`` of output, plus upkeep ``delta`` H; the stock raises output by ``gamma``
    H, but only ``lag`` years after it is built.  Everything is relative to the path without the technology.
    Measured productivity counts neither the investment as output nor the stock as an input: Y - I.  True
    productivity counts both: Y / (1 + kappa H).  Measured productivity first falls below the old path, then rises
    above the true one: the J-curve."""
    t = np.arange(years)
    H = np.zeros(years + 1)
    meas, true, inv_ = [], [], []
    for k in t:
        x = (k - start + 0.5) / build
        new = invest * np.sin(np.pi * x) if 0 <= x <= 1 else 0.0
        inv = new + delta * H[k]
        Y = 1 + gamma * (H[k - lag] if k >= lag else 0.0)
        meas.append(Y - inv)
        true.append(Y / (1 + kappa * H[k]))
        inv_.append(inv)
        H[k + 1] = H[k] + new
    meas, true = np.array(meas), np.array(true)
    above = np.nonzero(meas > true + 1e-9)[0]
    return {"t": t.tolist(), "measured": meas.tolist(), "true": true.tolist(), "investment": inv_,
            "start": start, "build": build, "lag": lag, "low": float(meas.min()), "low_year": int(meas.argmin()),
            "end": float(meas[-1]), "end_true": float(true[-1]), "cross": int(above[0]) if len(above) else None}


# ---------------------------------------------------------------------------------------------------------------
# growth with automated research


def ideas_growth(beta: float, sigma: float = 0.3, years: int = 200, n: float = 0.01, phi: float = 0.5,
                 alpha: float = 0.35, save: float = 0.25, dep: float = 0.05, research_k: float = 0.05,
                 theta: float = 0.02, cap: float = 0.5, machine: float = 6.67) -> dict:
    """Semi-endogenous growth with automatable research.  Goods Y = A K^alpha L^(1 - alpha); capital saved at rate
    ``save``; a share ``research_k`` of capital and the researchers S (growing at n with the population) produce
    research input R = [beta^(1/sigma) (k_R)^((sigma-1)/sigma) + (1 - beta)^(1/sigma) S^((sigma-1)/sigma)]^(sigma/
    (sigma-1)); ideas grow by theta R A^phi.  With beta < 1 and complements (sigma < 1) the people's tasks bind and
    growth settles near n/(1 - phi) adjusted for capital deepening; with beta = 1 research grows with capital, which
    grows with ideas, and growth accelerates without bound (stopped at ``cap`` a year)."""
    A, K, L, S = 1.0, 3.0, 1.0, 1.0
    out = {"year": [], "growth": [], "ideas_growth": [], "people_share": []}
    y_prev = A * K ** alpha * L ** (1 - alpha)
    r = (sigma - 1) / sigma
    for t in range(years):
        kR = machine * research_k * K               # research machines, in researcher-equivalents (1 at the start)
        if beta >= 1.0:
            R, people = kR, 0.0
        elif beta <= 0.0:
            R, people = S, 1.0
        else:
            hm = (1 - beta) ** (1 / sigma) * S ** r
            R = (beta ** (1 / sigma) * kR ** r + hm) ** (1 / r)
            people = hm / (beta ** (1 / sigma) * kR ** r + hm)      # people's share of research costs
        dA = theta * R * A ** phi
        gA = dA / A
        A += dA
        Y = A * K ** alpha * L ** (1 - alpha)
        K = (1 - dep) * K + save * Y * (1 - research_k)
        L *= 1 + n
        S *= 1 + n
        gy = (Y / L) / (y_prev / (L / (1 + n))) - 1
        y_prev = Y
        out["year"].append(t)
        out["growth"].append(float(gy))
        out["ideas_growth"].append(float(gA))
        out["people_share"].append(float(people))
        if gy > cap:
            break
    out["beta"] = beta
    out["final_growth"] = out["growth"][-1]
    out["exploded"] = out["growth"][-1] > cap
    return out


# ---------------------------------------------------------------------------------------------------------------
# from tasks to aggregates


def hulten_ai(exposed=0.20, adopted=0.23, saving=0.27, labour_cost=0.535) -> dict:
    """Hulten's arithmetic for AI (after Acemoglu 2024): the share of tasks (by value) exposed, the share of those
    where using AI pays within the horizon, the saving in labour costs on those tasks and labour's share of their
    costs give the share of GDP made cheaper and the rise in TFP: TFP gain = share affected x cost saving.  The
    defaults are Acemoglu's inputs, rounded: about a fifth of tasks exposed, 23% of those worth doing with AI within
    ten years, a 27% labour-cost saving, labour 53.5% of those tasks' costs; they give about 0.66%.  Arrays work."""
    share = np.asarray(exposed, float) * np.asarray(adopted, float)
    cost_saving = np.asarray(saving, float) * np.asarray(labour_cost, float)
    tfp = share * cost_saving
    return {"share_affected": share, "cost_saving": cost_saving, "tfp": tfp}


def hulten_scenarios() -> dict:
    """Three readings of the same arithmetic: Acemoglu's inputs; wider adoption and larger savings (the middle of the
    experiments); and everything exposed adopted at the experiments' larger savings.  Each over ten years, with the
    implied addition to annual growth."""
    rows = []
    for name, ex, ad, sv in (("Acemoglu's inputs", 0.20, 0.23, 0.27),
                             ("wider adoption", 0.20, 0.60, 0.40),
                             ("everything exposed, adopted", 0.50, 1.00, 0.40)):
        h = hulten_ai(ex, ad, sv)
        tfp = float(h["tfp"])
        rows.append({"name": name, "exposed": ex, "adopted": ad, "saving": sv, "share": float(h["share_affected"]),
                     "cost_saving": float(h["cost_saving"]), "tfp": tfp,
                     "per_year": float((1 + tfp) ** 0.1 - 1)})
    return {"rows": rows}


# ---------------------------------------------------------------------------------------------------------------
# the experiments: an assistant at a support desk


def support_desk(n: int = 2000, seed: int = 65, mean_effect: float = 0.14, slope: float = 0.11) -> dict:
    """An Island support desk after Brynjolfsson, Li and Raymond: agents differ in skill; half, drawn at random, get
    an AI assistant.  Output is resolutions per hour; the assistant's planted effect on log output falls with skill
    (``mean_effect`` on average, ``slope`` less per standard deviation of skill, never below -2%).  Returns the
    estimated average effect with its standard error, effects by fifth of skill against the truth, and the gap between
    the top and bottom fifths with and without the assistant."""
    rng = np.random.default_rng(seed)
    skill = rng.normal(0.0, 1.0, n)
    treat = rng.permutation(np.r_[np.ones(n // 2), np.zeros(n - n // 2)]).astype(bool)
    effect = np.maximum(mean_effect - slope * skill, -0.02)
    base = 0.9 + 0.22 * skill + rng.normal(0.0, 0.18, n)            # log resolutions per hour
    y = base + treat * effect
    d = y[treat].mean() - y[~treat].mean()
    se = np.sqrt(y[treat].var(ddof=1) / treat.sum() + y[~treat].var(ddof=1) / (~treat).sum())
    q = np.quantile(skill, [0.2, 0.4, 0.6, 0.8])
    fifth = np.searchsorted(q, skill)
    rows = []
    for f in range(5):
        m = fifth == f
        t, c = y[m & treat], y[m & ~treat]
        est = t.mean() - c.mean()
        se_f = np.sqrt(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c))
        rows.append({"fifth": f + 1, "est": float(np.expm1(est)), "lo": float(np.expm1(est - 1.96 * se_f)),
                     "hi": float(np.expm1(est + 1.96 * se_f)), "truth": float(np.expm1(effect[m].mean())),
                     "control": float(np.exp(c.mean())), "treated": float(np.exp(t.mean()))})
    gap_c = rows[4]["control"] / rows[0]["control"]
    gap_t = rows[4]["treated"] / rows[0]["treated"]
    return {"n": n, "est": float(np.expm1(d)), "lo": float(np.expm1(d - 1.96 * se)),
            "hi": float(np.expm1(d + 1.96 * se)), "truth": float(np.expm1(effect.mean())), "fifths": rows,
            "gap_control": float(gap_c), "gap_treated": float(gap_t)}


# ---------------------------------------------------------------------------------------------------------------
# Baumol: the sector that is not automated takes over


def baumol(years: int = 101, g_fast: float = 0.06, g_slow: float = 0.005, eps: float = 0.5,
           start_share: float = 0.5) -> dict:
    """Two sectors with productivity growing at ``g_fast`` (automated) and ``g_slow``; consumers combine their goods
    with elasticity ``eps`` < 1 (complements).  With a common wage, prices are inverse productivities, and the
    automated sector's share of spending falls as its good gets cheap; aggregate growth (a Divisia index: the
    spending-share-weighted average) slides from the average towards the slow sector's rate."""
    t = np.arange(years)
    a_fast, a_slow = (1 + g_fast) ** t, (1 + g_slow) ** t
    w0 = start_share / (1 - start_share)
    # spending shares with CES weights set so that the fast sector's share starts at start_share
    rel = w0 * (a_slow / a_fast) ** (1 - eps)              # p_fast^(1-eps) / p_slow^(1-eps), times the weight ratio
    share_fast = rel / (1 + rel)
    growth = share_fast * g_fast + (1 - share_fast) * g_slow
    return {"t": t.tolist(), "share_fast": share_fast.tolist(), "growth": growth.tolist(), "g_fast": g_fast,
            "g_slow": g_slow, "eps": eps}


# ---------------------------------------------------------------------------------------------------------------
# the race between automation and capital


def _short_run(I: float, K: float, L: float, sigma: float, AK: float, AL: float) -> tuple[float, float, float, float]:
    """Output, wage, rental and the automation actually used when tasks below ``I`` *can* be done by capital: a task
    is automated only if capital is cheaper per unit of work (r/AK < w/AL); otherwise the threshold stops where the
    two costs are equal."""
    def at(i):
        d = tasks(i, sigma=sigma, K=K, L=L, AK=AK, AL=AL)
        return d["Y"], d["w"], d["r"]

    Y, w, r = at(I)
    if r / AK <= w / AL:
        return Y, w, r, I
    lo, hi = 1e-6, I
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        _, wm, rm = at(mid)
        if rm / AK <= wm / AL:
            lo = mid
        else:
            hi = mid
    Y, w, r = at(lo)
    return Y, w, r, lo


def race(frontier, years: int = 60, sigma: float = 0.8, AK: float = 0.4, AL: float = 1.0, K0: float = 2.0,
         save: float = 0.2, dep: float = 0.05) -> dict:
    """Wages when the automation frontier I(t) (a function of the year, at most 0.999) advances and capital
    accumulates (K' = (1 - dep) K + save Y).  Labour is never paid less than a machine doing its work would cost:
    tasks are automated only where that is cheaper.  When the frontier reaches every task, the wage falls to that
    machine-equivalent level (AL r / AK) while output keeps growing (after Korinek and Suh's bounded-complexity
    scenario); when the frontier recedes as it advances, capital and wages grow together."""
    K, L = K0, 1.0
    out = {"year": [], "I": [], "I_used": [], "Y": [], "w": [], "labour_share": [], "K": []}
    for t in range(years):
        I = min(float(frontier(t)), 0.999)
        Y, w, r, used = _short_run(I, K, L, sigma, AK, AL)
        for k_, v in (("year", t), ("I", I), ("I_used", used), ("Y", Y), ("w", w), ("labour_share", w * L / Y),
                      ("K", K)):
            out[k_].append(float(v))
        K = (1 - dep) * K + save * Y
    w = np.array(out["w"])
    out["peak_year"] = int(w.argmax())
    out["peak_w"] = float(w.max())
    out["end_w"] = float(w[-1])
    out["machine_wage"] = AL * AK / AK            # with r = AK once every task is done by capital, w = AL
    return out


def race_scenarios(years: int = 60) -> dict:
    """Three frontiers, as in Korinek and Suh's scenarios: business as usual (the frontier creeps forward and the
    hardest tasks keep receding), every task automatable in twenty years, and in five."""
    fr = {"business as usual": lambda t: 0.30 + 0.25 * (1 - np.exp(-t / 40.0)),
          "every task in 20 years": lambda t: 0.30 + 0.70 * min(t / 20.0, 1.0),
          "every task in 5 years": lambda t: 0.30 + 0.70 * min(t / 5.0, 1.0)}
    return {k: race(f, years=years) for k, f in fr.items()}


# ---------------------------------------------------------------------------------------------------------------
# agents that transact: when software shops


def shoppers(mu_grid=None, n_sellers: int = 4, v: float = 1.0, c: float = 0.4, points: int = 4000) -> dict:
    """Varian's (1980) model of sales: a share mu of buyers compares every price (their agents shop for them), the
    rest buy from the first seller they meet.  Sellers mix over prices on [p0, v] with
    F(p) = 1 - [((1 - mu)/(n mu)) (v - p)/(p - c)]^(1/(n - 1)).  The average price paid falls from the monopoly price
    towards cost as mu rises: a world where every buyer has an agent is close to Bertrand."""
    mu_grid = np.linspace(0.02, 0.98, 49) if mu_grid is None else np.asarray(mu_grid, float)
    rows = []
    for mu in mu_grid:
        n = n_sellers
        p0 = c + (v - c) * (1 - mu) / (1 - mu + n * mu)
        p = np.linspace(p0, v, points)
        F = 1 - (((1 - mu) / (n * mu)) * (v - p) / np.maximum(p - c, 1e-12)) ** (1 / (n - 1))
        F = np.clip(F, 0, 1)
        Fmin = 1 - (1 - F) ** n
        e_p = p0 + np.trapezoid(1 - F, p)                     # E[p] = p0 + integral of (1 - F)
        e_min = p0 + np.trapezoid(1 - Fmin, p)
        paid = mu * e_min + (1 - mu) * e_p
        rows.append({"mu": float(mu), "p0": float(p0), "mean_price": float(e_p), "shoppers_pay": float(e_min),
                     "average_paid": float(paid), "markup": float((paid - c) / (v - c))})
    return {"rows": rows, "n": n_sellers, "v": v, "c": c}


# ---------------------------------------------------------------------------------------------------------------
# market structure: fixed costs that grow


def frontier_entry(years: int = 9, market0: float = 40.0, market_growth: float = 1.0, cost0: float = 0.4,
                   cost_growth: float = 2.0) -> dict:
    """A toy of a frontier-model market: each frontier model costs a fixed ``cost`` to train, rising by
    ``cost_growth`` (times one) a year; the market for frontier services, ``market``, grows by ``market_growth``.
    With Cournot competition on linear demand, profits per firm are market/(N + 1)^2, so free entry supports
    N = sqrt(market/cost) - 1 firms (rounded down).  When costs grow faster than the market, the number of frontier
    firms falls; a layer of open models priced near cost remains below the frontier."""
    t = np.arange(years)
    market = market0 * (1 + market_growth) ** t
    cost = cost0 * (1 + cost_growth) ** t
    n = np.floor(np.sqrt(market / cost) - 1).clip(min=1)
    return {"t": t.tolist(), "market": market.tolist(), "cost": cost.tolist(), "n": n.astype(int).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# Keynes's forecasts


def keynes(countries=("USA", "GBR", "DEU", "FRA", "JPN", "KOR")) -> dict:
    """Living standards since 1930 (Maddison Project, GDP per head, 1930 against 2022) and average annual hours worked
    per person employed since 1950 (Penn World Table 11.0), with Keynes's fifteen-hour week as 780 hours a year."""
    from explainer.economics import data

    ratio = {}
    for c in ("GBR", "USA", "FRA", "DEU", "SWE", "NLD"):
        m = data.maddison_country(c)
        d = dict(zip(m["year"], m["gdppc"]))
        if 1930 in d and 2022 in d:
            ratio[c] = d[2022] / d[1930]
    hours = {}
    for c in countries:
        rows = [r for r in data.pwt(c) if np.isfinite(r["avh"])]
        hours[c] = {"year": [r["year"] for r in rows], "hours": [r["avh"] for r in rows],
                    "name": rows[0]["country"] if rows else c}
    return {"ratio": ratio, "hours": hours, "keynes_hours": 15 * 52}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "annotations")]
