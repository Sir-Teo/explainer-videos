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
          AL: float = 1.0, R: float | None = None) -> dict:
    """Output from tasks on [N - 1, N] combined with elasticity sigma; tasks below I are done by capital (productivity
    AK), the rest by labour (AL).  Short run (R None): capital K fixed.  Long run: capital supplied at rental R, output
    set by the unit-cost condition with the final good as numeraire.  Returns output, wage, rental and labour share."""
    a, b = I - (N - 1), N - I                        # task shares of capital and labour
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


def task_paths(sigma: float = 0.8, K: float = 2.0, R: float = 0.8, steps: int = 41) -> dict:
    """Automation (I rising from 0.2 to 0.8 with N = 1) in the short run and the long run, then new tasks (N rising
    from 1 to 1.4 with I = 0.8), and the decomposition of the short-run wage change into displacement and
    productivity: d ln w = (1/sigma) d ln(N - I) + (1/sigma) d ln Y."""
    Is = np.linspace(0.2, 0.8, steps)
    sr = [tasks(i, sigma=sigma, K=K) for i in Is]
    lr = [tasks(i, sigma=sigma, R=R) for i in Is]
    Ns = np.linspace(1.0, 1.4, steps)
    nt = [tasks(0.8, N=n, sigma=sigma, R=R) for n in Ns]
    dlnY = np.log(sr[-1]["Y"] / sr[0]["Y"])
    displacement = (1 / sigma) * np.log((1 - Is[-1]) / (1 - Is[0]))
    productivity = (1 / sigma) * dlnY
    return {"I": Is.tolist(), "N": Ns.tolist(), "sigma": sigma, "R": R,
            "short": {k: [d[k] for d in sr] for k in ("Y", "w", "labour_share")},
            "long": {k: [d[k] for d in lr] for k in ("Y", "w", "labour_share")},
            "new_tasks": {k: [d[k] for d in nt] for k in ("Y", "w", "labour_share")},
            "displacement": float(displacement), "productivity": float(productivity),
            "dlnw": float(np.log(sr[-1]["w"] / sr[0]["w"]))}


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


def j_curve(years: int = 31, start: int = 3, invest: float = 0.05, build: int = 10, payoff: float = 1.2,
            growth: float = 0.015) -> dict:
    """A general-purpose technology arrives in year ``start``.  Over ``build`` years firms divert a hump-shaped share
    of output, peaking at ``invest``, to intangible capital (reorganization, training, their own software) that the
    national accounts do not count as output; each unit of it later raises output by ``payoff`` units a year
    (capital that is used but never measured).  Productivity relative to the path without the technology: measured
    (intangible investment not counted as output, intangible capital not counted as input) against true (both
    counted).  Measured productivity first falls below the old path, then rises above it: the J-curve."""
    t = np.arange(years)
    base = (1 + growth) ** t
    H, meas, true = 0.0, [], []
    for k in t:
        x = (k - start + 0.5) / build
        inv = invest * np.sin(np.pi * x) if 0 <= x <= 1 else 0.0
        out = 1 + payoff * H * 0.1                     # gross output gain from the intangible stock
        meas.append(out * (1 - inv))                   # measured output: the investment is invisible
        true.append(out / (1 + 0.1 * H))               # true productivity: the stock counted as an input
        H = 0.9 * H + inv
    meas, true = np.array(meas), np.array(true)
    return {"t": t.tolist(), "measured": meas.tolist(), "true": true.tolist(), "start": start, "build": build,
            "low": float(meas.min()), "low_year": int(meas.argmin()), "end": float(meas[-1]),
            "base": base.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# growth with automated research


def ideas_growth(beta: float, sigma: float = 0.3, years: int = 200, n: float = 0.01, phi: float = 0.5,
                 alpha: float = 0.35, save: float = 0.25, dep: float = 0.05, research_k: float = 0.05,
                 theta: float = 0.02, cap: float = 0.5) -> dict:
    """Semi-endogenous growth with automatable research.  Goods Y = A K^alpha L^(1 - alpha); capital saved at rate
    ``save``; a share ``research_k`` of capital and the researchers S (growing at n with the population) produce
    research input R = [beta^(1/sigma) (k_R)^((sigma-1)/sigma) + (1 - beta)^(1/sigma) S^((sigma-1)/sigma)]^(sigma/
    (sigma-1)); ideas grow by theta R A^phi.  With beta < 1 and complements (sigma < 1) the people's tasks bind and
    growth settles near n/(1 - phi) adjusted for capital deepening; with beta = 1 research grows with capital, which
    grows with ideas, and growth accelerates without bound (stopped at ``cap`` a year)."""
    A, K, L, S = 1.0, 3.0, 1.0, 1.0
    out = {"year": [], "growth": [], "ideas_growth": []}
    y_prev = A * K ** alpha * L ** (1 - alpha)
    r = (sigma - 1) / sigma
    for t in range(years):
        kR = research_k * K
        if beta >= 1.0:
            R = kR
        elif beta <= 0.0:
            R = S
        else:
            R = (beta ** (1 / sigma) * kR ** r + (1 - beta) ** (1 / sigma) * S ** r) ** (1 / r)
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
        if gy > cap:
            break
    out["beta"] = beta
    out["final_growth"] = out["growth"][-1]
    out["exploded"] = out["growth"][-1] > cap
    return out


# ---------------------------------------------------------------------------------------------------------------
# from tasks to aggregates


def hulten_ai(exposed: float, adopted: float, saving: float, labour_cost: float = 0.57) -> dict:
    """Hulten's arithmetic for AI: the share of tasks (by value) exposed, the share of those where using AI pays,
    the saving in labour costs on those tasks, and labour's share of their costs give the share of GDP made cheaper
    and the rise in TFP.  ``exposed`` etc. may be arrays."""
    share = np.asarray(exposed) * np.asarray(adopted)
    tfp = share * np.asarray(saving) * labour_cost
    return {"share_affected": share, "tfp": tfp}


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
